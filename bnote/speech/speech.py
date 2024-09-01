"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import queue
import threading
import time
import re
from pathlib import Path

"""
Audio card selection :
https://forum.videolan.org/viewtopic.php?t=116672
https://www.olivieraubert.net/vlc/python-ctypes/doc/
"""
import vlc

from bnote.debug.colored_log import ColoredLogger, SYNTHESIS_LOG
from bnote.speech.wave import ESpeakWave, PicoWave, MBrolaWave, CerenceWave
from bnote.tools.singleton_meta import SingletonMeta

# Set up the logger for this file
from bnote.tools.volume import Volume

log = ColoredLogger(__name__)
log.setLevel(SYNTHESIS_LOG)

# Il faut le chemin complet car il est aussi définit dans un fichier de config pour la tts cerence-nuance-codefactory
# (prompter/config/audioconfig.json)
WAVE_FILE_PATH = Path("/home/pi/bnote/text.wav")


# Installation de vlc sur Ubuntu de dev via
# fm@fm-VirtualBox:~$ sudo apt install vlc

class SpeechManager(metaclass=SingletonMeta):
    def __init__(self):

        # A dictionary with callback notifications.
        self.callbacks = dict()

        # The queue with message to speak (text to speak + some params)
        self.queued_messages_to_speak = queue.Queue()

        # Instanciate the thread that hold TTS
        self._speech_thread = None

    def enable(self):
        if self._speech_thread is None:
            self._speech_thread = SpeechThread(self.__voice_events_callback, self.queued_messages_to_speak)
            self._speech_thread.start()
            self._speech_thread.tts_init_done.wait(timeout=5)

    def disable(self):
        if self._speech_thread:
            self.stop()
            self._speech_thread.stop_thread()
            self._speech_thread = None

    def is_enable(self):
        return self._speech_thread is not None

    def register_voice_event_callback(self, event_name, callback):
        """Register a callback function to that will be called when the event_name will occur.

        The event_name are : "StartStream", "EndStream".

        The callback function can be my_callback_function(**kwargs) and the parameters will be in the kwargs dict.
        """
        self.callbacks[event_name] = callback

    def deregister_voice_event_callback(self, event_name):
        """Remove the callback notification for the event_name

        """
        if event_name in self.callbacks:
            del self.callbacks[event_name]

    @staticmethod
    def available_speech_languages():
        """
        Return : A list with all available language with at least one synthesis.
        """
        return list(set(PicoWave().supported_languages())
                    | set(MBrolaWave().supported_languages())
                    | set(ESpeakWave().supported_languages())
                    | set(CerenceWave().supported_languages()))

    @staticmethod
    def language_synthesis(speech_language):
        """
        Return : The synthesis dict for a given language.
        as {'picotts:"picotts", 'mbrola':"mbrola", 'espeak':"espeak"} if kanguage defined in each synthesis.
        """
        available_synthesis = dict()
        if speech_language in PicoWave().supported_languages():
            available_synthesis['picotts'] = "picotts"
        if speech_language in MBrolaWave().supported_languages():
            available_synthesis['mbrola'] = "mbrola"
        if speech_language in ESpeakWave().supported_languages():
            available_synthesis['espeak'] = "espeak"
        if speech_language in CerenceWave().supported_languages():
            available_synthesis['cerence'] = "cerence"
        return available_synthesis

    @staticmethod
    def language_voice(speech_language, speech_synthesis):
        voices = None
        if speech_synthesis == 'picotts':
            voices = PicoWave().voices_for_language(speech_language)
        elif speech_synthesis == 'mbrola':
            voices = MBrolaWave().voices_for_language(speech_language)
        elif speech_synthesis == 'espeak':
            voices = ESpeakWave().voices_for_language(speech_language)
        elif speech_synthesis == 'cerence':
            voices = CerenceWave().voices_for_language(speech_language)
        if voices:
            voices_dict = dict()
            for (gender, voice_id) in voices:
                voices_dict[voice_id] = "{} ({})".format(voice_id, gender)
            return voices_dict
        else:
            return {'default': "default"}

    @staticmethod
    def default_speech_synthesis(language):
        """
        For a given language, return the favorite synthesis
        """
        # Priorise Cerence pour les tests.
        if language in CerenceWave().supported_languages():
            return 'cerence'
        if language in PicoWave().supported_languages():
            return 'picotts'
        if language in MBrolaWave().supported_languages():
            return 'mbrola'
        if language in ESpeakWave().supported_languages():
            return 'espeak'
        return ""

    @staticmethod
    def default_voice(language, synthesis):
        voices = None
        if synthesis == 'picotts':
            voices = PicoWave().voices_for_language(language)
        elif synthesis == 'mbrola':
            voices = MBrolaWave().voices_for_language(language)
        elif synthesis == 'espeak':
            voices = ESpeakWave().voices_for_language(language)
        elif synthesis == 'cerence':
            voices = CerenceWave().voices_for_language(language)
        if voices and len(voices) > 0:
            # Return voide id.
            return voices[0][1]
        return ""

    def speak(self, text_to_speak, lang_id, synthesis, voice, headphone, volume, speed, purge_before_speak):
        log.info(f"{text_to_speak=} {lang_id=} {synthesis=} {voice=} {volume=} {speed=} {purge_before_speak=}")
        # text_to_speak = "un texte super long à lire pour tester"
        if self._speech_thread:
            if purge_before_speak:
                self.stop()
            self.queued_messages_to_speak.put(
                (text_to_speak, lang_id, synthesis, voice, headphone, volume, speed, purge_before_speak))

    def stop(self):
        if self._speech_thread:
            while True:
                try:
                    self.queued_messages_to_speak.get_nowait()
                except queue.Empty:
                    break
            # Do it one more time because
            try:
                self.queued_messages_to_speak.get_nowait()
            except queue.Empty:
                pass
            self._speech_thread.stop_speak()

    def __voice_events_callback(self, event_name, **kwargs):
        # log.debug(f"{event_name=} {kwargs=}")
        callback = self.callbacks.get(event_name, None)
        if callback:
            kwargs["event_name"] = event_name
            callback(**kwargs)


class SpeechThread(threading.Thread):
    # soundless_text_watchdog used to pass over the empty text spoken by cerence (to avoid an infinite loop).
    # Note : First value is 1 second (thus first message is not cut) and the next values will be 0.05 second (see below in run())
    soundless_text_watchdog = 1

    def __init__(self, voice_events_callback, queued_messages_to_speak):
        threading.Thread.__init__(self)
        self._voice_events_callback = voice_events_callback
        self._queued_messages_to_speak = queued_messages_to_speak
        self.wave_converters = {'pico': PicoWave(), 'espeak': ESpeakWave(), 'mbrola': MBrolaWave(),
                                'cerence': CerenceWave()}
        self.tts_init_done = threading.Event()
        self._stop_thread_event = threading.Event()
        self._stop_speak_event = threading.Event()

    def run(self):
        # Delete older wav file.
        WAVE_FILE_PATH.unlink(True)

        # Set self.tts_init_done Event, thus caller knows that voices() is available.
        self.tts_init_done.set()
        i_headphone = vlc.Instance('--aout=alsa', '--alsa-audio-device=hw:0,0')
        # i_hp = vlc.Instance('--aout=alsa', '--alsa-audio-device=hw:1,0')
        i_hp = vlc.Instance()

        while not self._stop_thread_event.is_set():
            try:
                # Get infos from queue without blocking.
                (text_to_speak, lang_id, synthesis, voice, headphone, volume, speed, purge_before_speak) = \
                    self._queued_messages_to_speak.get(block=False)
            except queue.Empty:
                pass
            else:
                # https://stackoverflow.com/a/25736082
                sentences = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text_to_speak)

                for sentence in sentences:
                    if not sentence or (len(sentence) == 0):
                        continue
                    # For pico tts it is necessary to change "'" by its unicode value U+2019.
                    sentence = sentence.replace("'", "\u2019")
                    log.debug(f"{sentence=} {volume=} {speed=} "
                              f"{purge_before_speak=} {self._queued_messages_to_speak.qsize()=}")
                    # if purge_before_speak:
                    # start_time_stop = time.time_ns()
                    # self._tts.stop()
                    # log.debug(f"call self._tts.stop() in {(time.time_ns() - start_time_stop) / 1000000} ms.")

                    # Ready to speak.
                    self._stop_speak_event.clear()
                    # self._voice_events_callback("StartStream")
                    start_time_speak = time.time_ns()
                    if text_to_speak:
                        # Delete older wav file.
                        WAVE_FILE_PATH.unlink(True)
                        # Set the wanted volume
                        Volume().set_volume(volume)
                        if (synthesis == 'picotts') and (lang_id in self.wave_converters['pico'].supported_languages()):
                            self.wave_converters['pico'].convert_to_wave(text_to_speak=sentence, language=lang_id,
                                                                         voice=voice,
                                                                         file_name=WAVE_FILE_PATH, speed=speed)
                        elif (synthesis == 'mbrola') and (
                                lang_id in self.wave_converters['mbrola'].supported_languages()):
                            self.wave_converters['mbrola'].convert_to_wave(text_to_speak=sentence, language=lang_id,
                                                                           voice=voice,
                                                                           file_name=WAVE_FILE_PATH, speed=speed)
                        elif (synthesis == 'espeak') and (
                                lang_id in self.wave_converters['espeak'].supported_languages()):
                            self.wave_converters['espeak'].convert_to_wave(text_to_speak=sentence, language=lang_id,
                                                                           voice=voice,
                                                                           file_name=WAVE_FILE_PATH, speed=speed)
                        elif (synthesis == 'cerence') and (
                                lang_id in self.wave_converters['cerence'].supported_languages()):
                            self.wave_converters['cerence'].convert_to_wave(text_to_speak=sentence, language=lang_id,
                                                                            voice=voice,
                                                                            file_name=WAVE_FILE_PATH, speed=speed)
                        if not WAVE_FILE_PATH.exists():
                            continue
                        # Play the wave with VLC player
                        if headphone:
                            instance = i_headphone
                        else:
                            instance = i_hp
                        media = instance.media_new(WAVE_FILE_PATH)
                        media_player = media.player_new_from_media()
                        media_player.audio_set_volume(volume)
                        media_player.play()
                        # player = vlc.MediaPlayer(WAVE_FILE_PATH)
                        # player.play()

                        log.warning(f"1. {media_player.is_playing()=}")
                        # Don't wait more than soundless_text_watchdog second if media_player.is_playing() remains False
                        while not self._stop_thread_event.is_set() and \
                                not media_player.is_playing() and \
                                (not media_player.is_playing() and SpeechThread.soundless_text_watchdog > 0):
                            time.sleep(0.01)
                            SpeechThread.soundless_text_watchdog -= 0.01
                            log.warning(f"2. {media_player.is_playing()=} {SpeechThread.soundless_text_watchdog=}")

                        # Set to a right value that is fast enough to pass over the wave with empty text.
                        SpeechThread.soundless_text_watchdog = 0.05

                        while not (self._stop_thread_event.is_set() or self._stop_speak_event.is_set()) \
                                and media_player.is_playing():
                            time.sleep(0.1)
                            log.warning(f"3. {media_player.is_playing()=}")
                        time.sleep(0.2)
                        log.warning(f"4. {media_player.is_playing()=}")

                        if media_player.is_playing():
                            # Stop current play.
                            media_player.stop()
                            while media_player.is_playing():
                                time.sleep(0.1)
                                log.warning(f"5. {media_player.is_playing()=}")
                self._voice_events_callback("EndStream")
                log.debug(f"call speak in {(time.time_ns() - start_time_speak) / 1000000} ms")
            self._stop_thread_event.wait(0.002)
        log.info(f"End of SpeechThread...")

    def _private_voice_events_callback(self, event_name, **kwargs):
        # log.error(f"{event_name=} {kwargs=}")
        self._voice_events_callback(event_name, **kwargs)

    def stop_thread(self):
        self._stop_thread_event.set()

    def stop_speak(self):
        self._stop_speak_event.set()
