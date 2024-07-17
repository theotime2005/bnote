"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.tools.speech_wrapper import speak
from bnote.tools.volume import Volume
import bnote.ui as ui


class VolumeDialogBox(ui.UiDialogBox):
    def __init__(self, dialog_box_name, edit_box_name, callback_save_the_new_volume, channel='speech'):
        self.__old_volume = Volume().get_volume(channel)
        self.__save_the_new_volume = callback_save_the_new_volume
        self.__channel = channel
        item_list = [
                ui.UiButton(name=_("volume &up"), action=self._exec_volume_up, is_auto_close=False),
                ui.UiButton(name=_("volume &down"), action=self._exec_volume_down, is_auto_close=False),
                ui.UiEditBox(name=edit_box_name, value=("volume", str(self.__old_volume))),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_set_volume_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_set_volume_dialog)
            ]

        kwargs = {
            'name': dialog_box_name,
            "item_list": item_list,
            "action_cancelable": self._exec_cancel_set_volume_dialog,
        }
        super(VolumeDialogBox, self).__init__(**kwargs)

    def _exec_valid_set_volume_dialog(self):
        kwargs = self.get_values()
        if 'volume' in kwargs:
            volume = kwargs['volume']
            try:
                volume = int(volume)
                Volume().set_volume(volume, self.__channel)
                self.__save_the_new_volume(volume)
            except ValueError:
                # How alert user ?
                pass

    def _exec_cancel_set_volume_dialog(self):
        # Restore the old_volume
        Volume().set_volume(self.__old_volume, self.__channel)
        self.__save_the_new_volume(self.__old_volume)

    def _exec_volume_up(self):
        new_volume = self.volume_up(self.__channel, with_voice_feedback=(self.__channel == 'speech'))
        self.__save_the_new_volume(new_volume)
        self.set_value('volume', str(new_volume))

    def _exec_volume_down(self):
        new_volume = self.volume_down(self.__channel, with_voice_feedback=(self.__channel == 'speech'))
        self.__save_the_new_volume(new_volume)
        self.set_value('volume', str(new_volume))

    @staticmethod
    def volume_down(channel, with_voice_feedback=True) -> int:
        echo = ""
        if with_voice_feedback:
            if channel == 'radio':
                echo = _("media volume 0%")
            else:
                echo = _("volume 0%")
        level = Volume().volume_down(channel)
        if with_voice_feedback and level != Volume().volume_preset_values()[0]:
            if channel == 'radio':
                echo = _("media volume down, {}%").format(level)
            else:
                echo = _("volume down, {}%").format(level)
        # Speak
        if with_voice_feedback:
            speak(text=echo, volume=level)
        return level

    @staticmethod
    def volume_up(channel, with_voice_feedback=True) -> int:
        echo = ""
        if with_voice_feedback:
            if channel == 'radio':
                echo = _("media volume 100%")
            else:
                echo = _("volume 100%")
        level = Volume().volume_up(channel)
        if with_voice_feedback and level < 100:
            if channel == 'radio':
                echo = _("media volume up, {}%").format(level)
            else:
                echo = _("volume up, {}%").format(level)
        # Speak
        if with_voice_feedback:
            speak(text=echo, volume=level)
        return level


class SpeedDialogBox(ui.UiDialogBox):
    def __init__(self, dialog_box_name, edit_box_name, callback_save_the_new_speed, current_speed, speed_range):
        self.__old_speed = current_speed
        self.__speed_range = speed_range
        self.__save_the_new_speed = callback_save_the_new_speed
        item_list = [
                ui.UiButton(name=_("speed &up"), action=self._speed_up, is_auto_close=False),
                ui.UiButton(name=_("speed &down"), action=self._speed_down, is_auto_close=False),
                ui.UiEditBox(name=edit_box_name, value=("speed", str(self.__old_speed))),
                ui.UiButton(name=_("&ok"), action=self._exec_valid_set_speed_dialog),
                ui.UiButton(name=_("&cancel"), action=self._exec_cancel_set_speed_dialog)
            ]

        kwargs = {
            'name': dialog_box_name,
            "item_list": item_list,
            "action_cancelable": self._exec_cancel_set_speed_dialog,
        }
        super(SpeedDialogBox, self).__init__(**kwargs)

    def _exec_valid_set_speed_dialog(self):
        kwargs = self.get_values()
        if 'speed' in kwargs:
            speed = kwargs['speed']
            self.__save_the_new_speed(speed)

    def _exec_cancel_set_speed_dialog(self):
        # Restore the old_speed
        self.__save_the_new_speed(self.__old_speed)

    def _speed_up(self):
        kwargs = self.get_values()
        if 'speed' in kwargs:
            speed = kwargs['speed']
            try:
                new_speed = self.speed_up(int(speed), self.__speed_range)
                self.__save_the_new_speed(new_speed)
                self.set_value('speed', str(new_speed))
            except ValueError:
                pass

    def _speed_down(self):
        kwargs = self.get_values()
        if 'speed' in kwargs:
            speed = kwargs['speed']
            try:
                new_speed = self.speed_down(int(speed), self.__speed_range)
                self.__save_the_new_speed(new_speed)
                self.set_value('speed', str(new_speed))
            except ValueError:
                pass

    @staticmethod
    def speed_down(current_speed, speed_range) -> int:
        echo = _("minimum speed")
        if current_speed - 10 in speed_range:
            current_speed = current_speed - 10
            echo = _("speed down {}").format(current_speed)
        else:
            current_speed = speed_range.start
        # Speak
        speak(echo)
        return current_speed

    @staticmethod
    def speed_up(current_speed, speed_range) -> int:
        echo = _("maximum speed")
        if current_speed + 10 in speed_range:
            current_speed = current_speed + 10
            echo = _("speed up {}").format(current_speed)
        else:
            current_speed = speed_range.stop
        # Speak
        speak(echo)
        return current_speed
