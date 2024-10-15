"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import queue
import threading
import time
from pathlib import Path

import fluidsynth
import mido

from tools.singleton_meta import SingletonMeta


# class MidiPlayer(metaclass=SingletonMeta):
#     FILE_ITEM = "file"
#     MIDO_ITEM = "mido"
#     MIDO_LIST = "list"
#     NOTE_ITEM = "note"
#     MIDO_TRACK = "track"
#
#     def __init__(self):
#         self.__midi_thread = None
#         self.__queued_items_to_play = queue.Queue()
#         self.__start_midi_tread()
#
#     def play(self, file, headphone=True):
#         if self.__midi_thread is None:
#             self.__start_midi_tread()
#         if self.__midi_thread:
#             self.__queued_items_to_play.put((MidiPlayer.FILE_ITEM, file, headphone))
#
#     def play_mido_message(self, msg, headphone=True):
#         if self.__midi_thread is None:
#             self.__start_midi_tread()
#         if self.__midi_thread:
#             self.__queued_items_to_play.put((MidiPlayer.MIDO_ITEM, msg, headphone))
#
#     def play_mido_track(self, track, headphone=True):
#         if self.__midi_thread is None:
#             self.__start_midi_tread()
#         if self.__midi_thread:
#             self.__queued_items_to_play.put((MidiPlayer.MIDO_TRACK, track, headphone))
#
#     def play_mido_message_list(self, msg_list, headphone=True):
#         if self.__midi_thread is None:
#             self.__start_midi_tread()
#         if self.__midi_thread:
#             self.__queued_items_to_play.put((MidiPlayer.MIDO_LIST, msg_list, headphone))
#
#     def play_note(self, note_value, duration, headphone=True):
#         if self.__midi_thread is None:
#             self.__start_midi_tread()
#         if self.__midi_thread:
#             self.__queued_items_to_play.put((MidiPlayer.NOTE_ITEM, (note_value, duration), headphone))
#         # self.__fs_headphone.noteon(0, note_value, 127)
#         # time.sleep(duration)
#         # self.__fs_headphone.noteoff(0, note_value)
#
#     def pause(self, value=True):
#         if self.__midi_thread:
#             self.__midi_thread.midi_pause(value)
#
#     def stop(self):
#         if self.__midi_thread:
#             while True:
#                 try:
#                     self.__queued_items_to_play.get_nowait()
#                 except queue.Empty:
#                     break
#             self.__midi_thread.midi_stop()
#
#     def is_playing(self):
#         if self.__midi_thread is not None:
#             return self.__midi_thread.is_playing.is_set()
#         return False
#
#     def is_paused(self):
#         if self.__midi_thread is not None:
#             return self.__midi_thread.is_paused.is_set()
#         return False
#
#     def stop_midi_thread(self):
#         if self.__midi_thread is not None:
#             self.__midi_thread.stop_thread()
#             self.__midi_thread = None
#
#     def __start_midi_tread(self):
#         self.__midi_thread = MidiThread(self.__queued_items_to_play)
#         self.__midi_thread.start()
#         self.__midi_thread.midi_init_done.wait(timeout=5)
#
#
# class MidiThread(threading.Thread):
#     def __init__(self, queued_items_to_play):
#         threading.Thread.__init__(self)
#         self.midi_init_done = threading.Event()
#         self.is_playing = threading.Event()
#         self.is_paused = threading.Event()
#         self.__stop_thread_event = threading.Event()
#         self.__midi_stop_event = threading.Event()
#         self.__midi_pause_event = threading.Event()
#         self.__queued_items_to_play = queued_items_to_play
#         mido.set_backend('mido.backends.rtmidi/LINUX_ALSA')
#         # Sortie casque
#         self.__headphone_index = len(mido.get_output_names())
#         self.__fs_headphone = fluidsynth.Synth()
#         self.__fs_headphone.start(driver="alsa", device="hw:0,0")
#         self.__sfid_headphone = self.__fs_headphone.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
#         self.__fs_headphone.program_select(0, self.__sfid_headphone, 0, 0)
#         self.__headphone_port = None
#         if self.__headphone_index < len(mido.get_output_names()):
#             self.__headphone_port = mido.open_output(mido.get_output_names()[self.__headphone_index])
#         # Sortie HP
#         self.__loud_speaker_index = len(mido.get_output_names())
#         self.__fs_loud_speaker = fluidsynth.Synth()
#         self.__fs_loud_speaker.start(driver="alsa")
#         self.__sfid_loud_speaker = self.__fs_loud_speaker.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
#         self.__fs_loud_speaker.program_select(0, self.__sfid_loud_speaker, 0, 0)
#         self.__loud_speaker_port = None
#         if self.__loud_speaker_index < len(mido.get_output_names()):
#             self.__loud_speaker_port = mido.open_output(mido.get_output_names()[self.__loud_speaker_index])
#
#         # pour le debug (à retirer)
#         # for i in range(0, len(mido.get_output_names())):
#         #     port = mido.open_output(mido.get_output_names()[i])
#         #     print(f"{i=} {port=}")
#
#
#     def run(self):
#         print(f"started...")
#         self.midi_init_done.set()
#         while not self.__stop_thread_event.is_set():
#             try:
#                 # Get infos from queue without blocking.
#                 (item_type, item, headphone) = self.__queued_items_to_play.get(block=False)
#                 self.is_playing.set()
#             except queue.Empty:
#                 time.sleep(0.01)
#                 self.is_playing.clear()
#                 if self.__midi_stop_event.is_set():
#                     self.__midi_stop_event.clear()
#                 pass
#             else:
#                 if item_type == MidiPlayer.FILE_ITEM:
#                     if Path(item).exists():
#                         mid = mido.MidiFile(item)
#                         print(f"{mid.length=}")
#                         for msg in mid.play():
#                             while self.is_paused.is_set():
#                                 time.sleep(1)
#                                 print("paused")
#                             self.__play_mido_msg(msg, headphone)
#                             if self.__midi_stop_event.is_set():
#                                 self.__midi_stop_event.clear()
#                                 self.__midi_pause_event.clear()
#                                 self.is_paused.clear()
#                                 break
#                 elif item_type == MidiPlayer.MIDO_ITEM:
#                     self.__play_mido_msg(item, headphone)
#                 elif item_type == MidiPlayer.MIDO_LIST:
#                     for sub_item in item:
#                         self.__play_mido_msg(sub_item, headphone)
#                 elif item_type == MidiPlayer.NOTE_ITEM:
#                     self.__play_note(item, headphone)
#                 elif item_type == MidiPlayer.MIDO_TRACK:
#                     self.__play_mido_track(item, headphone)
#
#         self.__fs_headphone.delete()
#         self.__fs_loud_speaker.delete()
#
#     def __play_mido_msg(self, msg, headphone=True):
#         while self.__midi_pause_event.is_set():
#             if self.__midi_stop_event.is_set():
#                 return
#             time.sleep(0.000001)
#
#         if headphone and not self.__headphone_port is None:
#             # print(msg, msg.bytes())
#             self.__headphone_port.send(msg)
#         elif not self.__loud_speaker_port is None:
#             self.__loud_speaker_port.send(msg)
#
#     def __play_mido_msg_list(self, msg_list, headphone=True):
#         while self.__midi_pause_event.is_set():
#             if self.__midi_stop_event.is_set():
#                 return
#             time.sleep(0.000001)
#
#         if headphone and not self.__headphone_port is None:
#             for msg in msg_list:
#                 self.__headphone_port.send(msg)
#         elif not self.__loud_speaker_port is None:
#             for msg in msg_list:
#                 self.__loud_speaker_port.send(msg)
#
#     def __play_note(self, item, headphone=True):
#         while self.__midi_pause_event.is_set():
#             if self.__midi_stop_event.is_set():
#                 return
#             time.sleep(0.000001)
#
#         if headphone and not self.__headphone_port is None:
#             self.__fs_headphone.noteon(0, item[0], 127)
#             time.sleep(item[1])
#             self.__fs_headphone.noteoff(0, item[0])
#         elif not self.__loud_speaker_port is None:
#             self.__loud_speaker.noteon(0, item[0], 127)
#             time.sleep(item[1])
#             self.__loud_speaker.noteoff(0, item[0])
#
#     def __play_mido_track(self, track, headphone=True):
#         while self.__midi_pause_event.is_set():
#             if self.__midi_stop_event.is_set():
#                 return
#             time.sleep(0.000001)
#
#         if headphone and not self.__headphone_port is None:
#             for msg in track:
#                 print(msg.time)
#                 self.__headphone_port.send(msg)
#         elif not self.__loud_speaker_port is None:
#             self.__loud_speaker_port.send(msg)
#
#     def midi_pause(self, value=True, headphone=True):
#         if value:
#             self.__midi_pause_event.set()
#             self.is_paused.set()
#             if headphone and not self.__headphone_port is None:
#                 self.__headphone_port.panic()
#             elif not self.__loud_speaker_port is None:
#                 self.__loud_speaker_port.panic()
#         else:
#             self.__midi_pause_event.clear()
#             self.is_paused.clear()
#
#     def midi_stop(self, headphone=True):
#         self.__midi_stop_event.set()
#         if headphone and not self.__headphone_port is None:
#             self.__headphone_port.panic()
#         elif not self.__loud_speaker_port is None:
#             self.__loud_speaker_port.PANIC()
#
#     def stop_thread(self):
#         self.midi_stop()
#         self.__stop_thread_event.set()