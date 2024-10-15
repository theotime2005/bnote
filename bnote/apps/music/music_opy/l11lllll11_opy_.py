"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import mido
from .l11ll1lll1_opy_ import *
from .l11llllll1_opy_ import *
from operator import itemgetter, attrgetter
class l11lll11l1_opy_:
    def __init__ (self, l1l1ll1ll_opy_):
        self._1l1lll11_opy_ = l1l1ll1ll_opy_
    def create_file(self, l11llll111_opy_):
        """structure of a midi_track_event
for program change : 0 = time counter, 1 = 1, 2 = 'program_change', 3 = value, 4 = 0 5 = 0
for tempo 0 = time counter, 1 = 2, 2 = 'set_tempo', 3 = value, 4 = 0, 5 = 0
for a note : 0 = time counter, 1 = 3, 2 = 'note_on' or 'note_off', 3 = midi_hight, 4 = velocity, 5 = duration, 6 = measure number, 7 = syllable
for karaoke : 0 = time counter, 1 = 4, 2 = 'lyrics', 3 = text value, 4 = 0, 5 = 0
events will be sorted according to time counter 0, message type 1, then message code 2 """
        l1llll11l1_opy_ = 1
        tempo = int(480 / l1llll11l1_opy_)
        l11ll1llll_opy_ = 115
        l11lll1l1l_opy_ = 0
        f = open ('trace_midi.txt', 'w', encoding='utf-8')
        mid = mido.MidiFile()
        l11llll1ll_opy_ = 0
        for element in self._1l1lll11_opy_.l1lll1ll1l_opy_:
            if element.t == "part":
                l11llll1ll_opy_ += 1
                l11lll11ll_opy_ = list()
                l11llll1l1_opy_ = mido.MidiTrack()
                mid.tracks.append(l11llll1l1_opy_)
                l11llll11l_opy_ = 0
# l11llll1l1_opy_.append(mido.MetaMessage('set_tempo', tempo = 1000000, time =0))
# l11llll1l1_opy_.append (mido.Message('program_change', l11lllllll_opy_=1, time=0))
                #if l11llll1ll_opy_ == 1:
                    #l11lll11ll_opy_.append([l11llll11l_opy_, 1, 'program_change', 53, 0, 0])
                #elif l11llll1ll_opy_ == 2:
                    #l11lll11ll_opy_.append([l11llll11l_opy_, 1, 'program_change', 54, 0, 0])
                #elif l11llll1ll_opy_ == 3:
                    #l11lll11ll_opy_.append([l11llll11l_opy_, 1, 'program_change', 54, 0, 0])
                #else:
                    #l11lll11ll_opy_.append([l11llll11l_opy_, 1, 'program_change', 1, 0, 0])
                for l11l11l11_opy_ in element.l11l1llll_opy_:
                    for event in l11l11l11_opy_.l11llll11_opy_:
                        if event.t == "note":
                            if not event.l1l11l111l_opy_:
                                if event.l1l1llllll_opy_ !=100:
                                    midi_hight = 12 + event.l1l1llllll_opy_ * 12 + l11ll1l1ll_opy_[event.step]
                                    if event.l1111l111_opy_:
                                        midi_hight += l11lllll1l_opy_[event.l1111l111_opy_]
                                    if not event.l11ll1lll_opy_:
                                        l11lll11ll_opy_.append([l11llll11l_opy_, 3, 'note_on', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, event.text])
                                        if l11ll1ll11_opy_.l11lll1ll1_opy_:
                                            l11lll11ll_opy_.append([l11llll11l_opy_, 4, 'lyrics', event.text, 0, 0])
                                        l11lll11ll_opy_.append([l11llll11l_opy_ + event.l1l1ll1ll1_opy_, 3, 'note_off', midi_hight, l11ll1llll_opy_, event.l1l1ll1ll1_opy_, l11l11l11_opy_.l1l111l111_opy_, ""])
                                        l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                    else:
                                        l11lll11ll_opy_.append([l11llll11l_opy_ - event.l1l1ll1ll1_opy_, 3, 'note_on', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, event.text])
                                        l11lll11ll_opy_.append([l11llll11l_opy_, 3, 'note_off', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, ""])
                                else:
                                    if not event.rest:
                                        l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                            else: # l1l11l111l_opy_
                                if event.l1l111l11l_opy_ == "start":
                                    if event.l1l1llllll_opy_ !=100:
                                        midi_hight = 12 + event.l1l1llllll_opy_ * 12 + l11ll1l1ll_opy_[event.step]
                                        if event.l1111l111_opy_:
                                            midi_hight += l11lllll1l_opy_[event.l1111l111_opy_]
                                        if not event.l11ll1lll_opy_:
                                            l11lll11ll_opy_.append([l11llll11l_opy_, 3, 'note_on', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, event.text])
                                            if l11ll1ll11_opy_.l11lll1ll1_opy_:
                                                l11lll11ll_opy_.append([l11llll11l_opy_, 4, 'lyrics', event.text, 0, 0])
                                            l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                            l11lll1l1l_opy_ += event.l1l1ll1ll1_opy_
                                        else:
                                            l11lll11ll_opy_.append([l11llll11l_opy_ - event.l1l1ll1ll1_opy_, 3, 'note_on', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, event.text])
                                    else:
                                        l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                elif event.l1l111l11l_opy_ == "stop":
                                    if event.l1l1llllll_opy_ !=100:
                                        midi_hight = 12 + event.l1l1llllll_opy_ * 12 + l11ll1l1ll_opy_[event.step]
                                        if event.l1111l111_opy_:
                                            midi_hight += l11lllll1l_opy_[event.l1111l111_opy_]
                                        if not event.l11ll1lll_opy_:
                                            l11lll11ll_opy_.append([l11llll11l_opy_ + event.l1l1ll1ll1_opy_, 3, 'note_off', midi_hight, l11ll1llll_opy_, l11lll1l1l_opy_ + event.l1l1ll1ll1_opy_, l11l11l11_opy_.l1l111l111_opy_, ""])
                                            l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                            l11lll1l1l_opy_ = 0
                                        else:
                                            l11lll11ll_opy_.append([l11llll11l_opy_, 3, 'note_off', midi_hight, l11ll1llll_opy_, 0, l11l11l11_opy_.l1l111l111_opy_, ""])
                                    else:
                                        l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                elif event.l1l111l11l_opy_ == "stop-start":
                                    if event.l1l1llllll_opy_ !=100:
                                        midi_hight = 12 + event.l1l1llllll_opy_ * 12 + l11ll1l1ll_opy_[event.step]
                                        if event.l1111l111_opy_:
                                            midi_hight += l11lllll1l_opy_[event.l1111l111_opy_]
                                        if not event.l11ll1lll_opy_:
                                            l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                                            l11lll1l1l_opy_ += event.l1l1ll1ll1_opy_
                                        else:
                                            l11lll1l1l_opy_ += event.l1l1ll1ll1_opy_
                                    else:
                                        l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                            if event.rest:
                                l11lll11ll_opy_.append([l11llll11l_opy_, 3, 'note_on', 1, 0, 0, l11l11l11_opy_.l1l111l111_opy_, event.text])
                                l11lll11ll_opy_.append([l11llll11l_opy_ + event.l1l1ll1ll1_opy_, 3, 'note_off', 1, 0, event.l1l1ll1ll1_opy_, l11l11l11_opy_.l1l111l111_opy_, ""])
                                l11llll11l_opy_ += event.l1l1ll1ll1_opy_
                        elif event.t == "backup":
                            l11llll11l_opy_ -= event.l1l1ll1ll1_opy_
                        elif event.t == "attributes":
                            for l1l1ll1l11_opy_ in event.l1l1lll11l_opy_:
                                if l1l1ll1l11_opy_.t == "divisions":
                                    l1llll11l1_opy_ = l1l1ll1l11_opy_.l1llll11l1_opy_
                                    tempo = int (480 / l1llll11l1_opy_)
                        elif event.t == "direction":
                            for l1l1ll1l11_opy_ in event.l11l1l111_opy_:
                                if l1l1ll1l11_opy_.t == "sound":
                                    if l1l1ll1l11_opy_.l1l11111ll_opy_ != "no":
                                        l11lll11ll_opy_.append([l11llll11l_opy_, 2, 'set_tempo', int(1000000 * 60 / int(l1l1ll1l11_opy_.l1l11111ll_opy_)), 0, 0])
                                elif l1l1ll1l11_opy_.t == "dynamics":
                                    l11ll1llll_opy_ = l11ll1ll1l_opy_[l1l1ll1l11_opy_.l1ll11l11l_opy_]
                                elif l1l1ll1l11_opy_.t == "metronome":
                                    l11lll11ll_opy_.append([l11llll11l_opy_, 2, 'set_tempo', int(1000000 * 60 / int(l1l1ll1l11_opy_.l111111l1_opy_)), 0, 0])
                        elif event.t == "karaoke" and l11ll1ll11_opy_.l11lll1111_opy_:
                            l11lll11ll_opy_.append([l11llll11l_opy_, 4, 'lyrics', event.l1l1lll1ll_opy_, 0, 0])
                f.write (str(l11lll11ll_opy_))
                l11lll1l11_opy_ = sorted (l11lll11ll_opy_, key=itemgetter(0,1,2))
                f.write ("\ntriée\n" + str(l11lll1l11_opy_))
                l11lll111l_opy_ = 0
                for l11lll1lll_opy_ in l11lll1l11_opy_:
                    l11lll111l_opy_ += l11lll1lll_opy_[5]
                    if l11lll111l_opy_ > l11lll1lll_opy_[0]:
                        l11lll1lll_opy_[5] = l11lll1lll_opy_[0] - (l11lll111l_opy_ - l11lll1lll_opy_[5])
                        l11lll111l_opy_ = l11lll1lll_opy_[0]
                f.write ("\narrangée\n" + str(l11lll1l11_opy_))
                f.write ("\ntrack\n")
                for message in l11lll1l11_opy_:
                    f.write (str(message[0]) + " " + str(message[1]) + " " + str(message[2]) + " " + str(message[3]) + " " + str(message[4]) + " " + str(message[5]) + "\n")
                    if message[1] == 3:
                        l11llll1l1_opy_.append(mido.Message(message[2], note=message[3], velocity=message[4], time=message[5] * tempo, channel=l11llll1ll_opy_))
                    elif message[1] == 2:
                        l11llll1l1_opy_.append(mido.MetaMessage(message[2], tempo=message[3], time=message[4]))
                    elif message[1] == 4:
                        l11llll1l1_opy_.append(mido.MetaMessage(message[2], text=message[3], time=message[4]))
                    elif message[1] == 1:
                        l11llll1l1_opy_.append(mido.Message(message[2], l11lllllll_opy_ = message[3], time=0, channel=l11llll1ll_opy_))
        mid.save(l11llll111_opy_)