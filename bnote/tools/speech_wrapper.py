"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from bnote.debug.colored_log import ColoredLogger, SYNTHESIS_LOG
from bnote.speech.speech import SpeechManager
from bnote.tools.io_util import Gpio
from bnote.tools.settings import Settings

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(SYNTHESIS_LOG)


def speak(text, lang_id=None, synthesis=None, voice=None, volume=None, speed=None, purge_before_speak=True):
    # log.error(f"{text=} {lang_id=} {volume=} {speed=} {purge_before_speak=}")
    headphone = (Gpio().is_head_phone())
    if volume is None:
        if headphone:
            volume = Settings().data['speech']['volume_headphone']
        else:
            volume = Settings().data['speech']['volume_hp']
    if speed is None:
        speed = Settings().data['speech']['speed']
    if lang_id is None:
        lang_id = Settings().data['speech']['language']
    if synthesis is None:
        synthesis = Settings().data['speech']['synthesis']
    if voice is None:
        voice = Settings().data['speech']['voice']
    log.warning(
        f"{SpeechManager().is_enable()} {text=} {lang_id=} {synthesis=} {voice=} {headphone=} {volume=} {speed=} {purge_before_speak=}")

    SpeechManager().speak(text_to_speak=text, lang_id=lang_id, synthesis=synthesis, voice=voice, headphone=headphone,
                          volume=volume, speed=speed,
                          purge_before_speak=purge_before_speak)


def stop():
    SpeechManager().stop()
