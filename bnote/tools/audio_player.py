"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from pathlib import Path
import time
import subprocess
import vlc
from bnote.tools.midi2audio import FluidSynth
from bnote.tools.io_util import Gpio
from bnote.tools.singleton_meta import SingletonMeta
from bnote.tools.settings import Settings
from bnote.apps.fman.file_manager import BNOTE_FOLDER

WAVE_FILE_PATH = BNOTE_FOLDER / Path("tmp/midi.wav")
# WAVE_FILE_PATH = Path("/var/log/tmp/midi.wav")


class AudioPlayer(metaclass=SingletonMeta):

    def __init__(self):
        self.__vlc_instance = None
        self.__media_player = None

        # playlist parameters
        # if media_list_index != -1 a play list is playing.
        self.__playlist_index = -1
        self.__playlist = None
        # Keep an instance of FluidSynth class to avoid lost time loading.
        # self.__fluidsynth = None
# PLAYLIST API
    # def playlist_is_playing(self):
    #     with self.lock:
    #         return self.media_list_index != -1

    def playlist_play(self, playlist):
        # Cleanup current playing.
        self.stop()
        self.__playlist = playlist
        if self.__playlist and len(self.__playlist) > 0:
            self.__playlist_index = 0
            self.__file_play(self.__playlist[0])

    def playlist_is_playing(self):
        return self.__playlist is not None

    def get_playlist_index(self):
        return self.__playlist_index

    def playlist_next(self) -> bool:
        if self.__playlist:
            self.__playlist_index += 1
            if len(self.__playlist) > self.__playlist_index:
                self.__stop()
                self.__file_play(self.__playlist[self.__playlist_index])
                return True
        return False

    def playlist_previous(self):
        if self.__playlist:
            if self.__playlist_index > 0:
                self.__playlist_index -= 1
            if len(self.__playlist) > self.__playlist_index:
                self.__stop()
                self.__file_play(self.__playlist[self.__playlist_index])

    @vlc.callbackmethod
    def cb_song_finished(self, event, data):
        self.__media_player = None
        # print(f"finished !!! {event=} {data=}")
        if not self.playlist_next():
            self.stop()

    def get_media_player_time(self):
        """
        return (time elapsed, total duration)
        """
        if self.__media_player:
            return self.__media_player.get_time(), self.__media_player.get_length()

    def get_media_player_position(self):
        """
        return the reading position in percent between 0.0 to 1.0
        """
        if self.__media_player:
            return self.__media_player.get_position()

    def set_media_player_position(self, value):
        """
        return the reading position in percent between 0.0 to 1.0
        """
        if self.__media_player:
            return self.__media_player.set_position(value)

    def stop(self):
        self.__stop()
        self.__playlist = None
        self.__playlist_index = -1

    def file_play(self, filename, index):
        # Cleanup current playing.
        self.stop()
        self.__file_play(filename)
        self.__playlist_index = index

    def __file_play(self, filename):
        self.__vlc_instance = AudioPlayer.__get_interface()
        media = self.__vlc_instance.media_new(filename)
        self.__media_player = media.player_new_from_media()
        manager = self.__media_player.event_manager()
        # manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.playlist_next_item)
        manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.cb_song_finished, 1)
        self.set_volume()
        self.__media_player.play()

    def radio_play(self, radio_url):
        # Cleanup current playing.
        # print(f"{radio_url=}")
        self.stop()
        self.__vlc_instance = AudioPlayer.__get_interface()
        self.__media_player = self.__vlc_instance.media_player_new()
        media = self.__vlc_instance.media_new(radio_url)
        media.get_mrl()
        self.__media_player.set_media(media)
        self.set_volume()
        self.__media_player.play()

    def midi_play(self, midi_file):
        # Cleanup current playing.
        self.stop()
        if Path(midi_file).exists():
            # A voir remplacement par :
            # timidity .bnote/bnote-documents/Bass_sample.mid -Ow -o test.wav
            subprocess.call(['timidity', midi_file, '-Ow', '-o', WAVE_FILE_PATH])
            # if self.__fluidsynth is None:
            #     self.__fluidsynth = FluidSynth(sound_font="/usr/share/sounds/sf2/FluidR3_GM.sf2")
            # self.__fluidsynth.midi_to_audio('new_song.mid', WAVE_FILE_PATH)

            self.__vlc_instance = AudioPlayer.__get_interface()
            media = self.__vlc_instance.media_new(WAVE_FILE_PATH)
            self.__media_player = media.player_new_from_media()
            self.set_volume()
            self.__media_player.play()
            # print(f"{self.__state()=}")
            # wait so the video can be played for 5 seconds
            # irrespective for length of video
            # time.sleep(5)

            # # pausing the player
            # self.media_player.set_pause(1)
            # print(f"{self.state()=}")
            #
            # # irrespective for length of video
            # time.sleep(5)
            #
            # self.media_player.play()
            # print(f"{self.state()=}")

    def __stop(self):
        # Lock this method freeze because self.__media_list_player.stop() call cb_playlist_stopped() ???
        # with self.__lock:
        if self.__media_player:
            if self.__media_player:
                self.__media_player.stop()
                self.__media_player.release()
                self.__media_player = None
            return True

    def pause(self):
        if self.__media_player:
            self.__media_player.set_pause(1)
            return True

    def resume(self):
        if self.__media_player:
            self.__media_player.set_pause(0)
            return True

    def forward(self, duration):
        if self.__media_player:
            position = self.__media_player.get_time()
            position = position + duration
            self.__media_player.set_time(position)

    def backward(self, duration):
        if self.__media_player:
            position = self.__media_player.get_time()
            position = position - duration
            self.__media_player.set_time(position)

    def __state(self):
        if self.__media_player:
            return self.__media_player.get_state()

    def is_paused(self):
        state = self.__state()
        if state:
            # print(f"{state=}-is paused ?{state == vlc.State.Paused}")
            return state == vlc.State.Paused

    def is_playing(self):
        return (self.__media_player is not None) and self.__media_player.is_playing()

    def get_volume(self):
        return self.__get_volume()

    def set_volume(self):
        media_player = self.__media_player
        if media_player:
            media_player.audio_set_volume(AudioPlayer.__get_volume())

    @staticmethod
    def __get_interface():
        headphone = Gpio().is_head_phone()
        if headphone:
            return vlc.Instance('--aout=alsa', '--alsa-audio-device=hw:0,0')
        else:
            return vlc.Instance()

    @staticmethod
    def __get_volume():
        headphone = Gpio().is_head_phone()
        if headphone:
            return Settings().data['radio']['volume_headphone']
        else:
            return Settings().data['radio']['volume_hp']


