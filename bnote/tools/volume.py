"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time

from bnote.debug.colored_log import ColoredLogger, SYNTHESIS_LOG

# Set up the logger for this file
from bnote.tools.io_util import Gpio
from bnote.tools.settings import Settings

log = ColoredLogger(__name__)
log.setLevel(SYNTHESIS_LOG)

"""
Audio Volume control class
"""


class Volume:
    @staticmethod
    def get_volume(channel="speech"):
        if Gpio().is_head_phone():
            volume = Settings().data[channel]["volume_headphone"]
        else:
            volume = Settings().data[channel]["volume_hp"]
        return volume

    @staticmethod
    def set_volume(volume, channel="speech"):
        # log.error(f"Change volume {channel=}")
        if Gpio().is_head_phone():
            key = "volume_headphone"
        else:
            key = "volume_hp"
        Settings().data[channel][key] = volume

    @staticmethod
    def volume_up(channel="speech"):
        volume = Volume.get_volume(channel)
        for value in Volume.volume_preset_values():
            if value > volume:
                volume = value
                break
        return volume

    @staticmethod
    def volume_down(channel="speech"):
        volume = Volume.get_volume(channel)
        for value in reversed(Volume.volume_preset_values()):
            if value < volume:
                volume = value
                break
        if volume < 0:
            volume = 0
        return volume

    @staticmethod
    def volume_preset_values():
        # return [40, 55, 65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100]
        return [5, 10, 20, 30, 40, 55, 65, 70, 75, 80, 85, 90, 92, 94, 96, 98, 100]


import vlc


def main():
    print("--------------")
    print("Volume control class test:")
    print("--------------")

    # pcms = audio.pcms()
    # print(f"audio.pcms={pcms}")
    # cards = audio.cards()
    # print(f"audio.cards={cards}")
    # mixers = audio.mixers(cardindex=0)
    # print(f"audio.mixers={mixers}")
    # mixers = audio.mixers(cardindex=1)
    # print(f"audio.mixers={mixers}")
    #
    # i_hp = vlc.Instance('--aout=alsa', '--alsa-audio-device=hw:CARD=Headphones,DEV=0')
    # media = i_hp.media_new("")
    # media_player = media.player_new_from_media()
    # media_player.play()
    #
    # mixer = audio.Mixer(control='Headphone', cardindex=0)
    # print(f"{mixer.cardname()=}")
    # print(f"{mixer.getvolume()=}")
    # mixer.setvolume(30)
    # mixer = audio.Mixer(control='PCM', cardindex=1)
    # print(f"{mixer.cardname()=}")
    # print(f"{mixer.getvolume()=}")
    # mixer.setvolume(70)

    i_hp = vlc.Instance("--aout=alsa", "--alsa-audio-device=hw:1,0")
    media = i_hp.media_new("text_picotts.wav")
    media_player = media.player_new_from_media()
    media_player.audio_set_volume(80)
    media_player.play()
    while not media_player.is_playing():
        time.sleep(0.1)
        print("wait not speaking")
    while media_player.is_playing():
        time.sleep(0.1)
        print("wait speaking")
    media_player = media.player_new_from_media()
    media_player.audio_set_volume(80)
    media_player.play()
    while not media_player.is_playing():
        time.sleep(0.1)
        print("wait not speaking")
    while media_player.is_playing():
        time.sleep(0.1)
        print("wait speaking")


#     scanCards = audio.cards()
#     print("cards:", scanCards)
#
#     for card in scanCards:
#         scanMixers = audio.mixers(scanCards.index(card))
#         print("mixers:", scanMixers)
#
#     volume = Volume()
#     volume.volume_up()
#     volume.volume_up()
#     volume.volume_up()
#     volume.volume_up()
#     volume.volume_up()


if __name__ == "__main__":
    main()
