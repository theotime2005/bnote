"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""

import mido
from .l1lll111lll_opy_ import *
from .l1lll11l1l1_opy_ import *
from operator import itemgetter, attrgetter


class l1lll11l1ll_opy_:
    def __init__(self, l1ll1l1ll_opy_):
        self._1lll111l_opy_ = l1ll1l1ll_opy_

    def create_file(self, l1ll1lllll1_opy_):
        """structure of a midi_track_event
        for program change : 0 = time counter, 1 = 1, 2 = 'program_change', 3 = value, 4 = 0 5 = 0
        for tempo 0 = time counter, 1 = 2, 2 = 'set_tempo', 3 = value, 4 = 0, 5 = 0
        for a note : 0 = time counter, 1 = 3, 2 = 'note_on' or 'note_off', 3 = midi_hight, 4 = velocity, 5 = duration, 6 = measure number, 7 = syllable
        for karaoke : 0 = time counter, 1 = 4, 2 = 'lyrics', 3 = text value, 4 = 0, 5 = 0
        events will be sorted according to time counter 0, message type 1, then message code 2
        """
        l111lll1l1_opy_ = 1
        # print(mido.l1lll111l1l_opy_())
        tempo = int(480 / l111lll1l1_opy_)
        l1ll1lll1l1_opy_ = 115
        l1lll11ll11_opy_ = 0
        f = open("trace_midi2.txt", "w", encoding="utf-8")
        mid = mido.MidiFile()
        l1lll11111l_opy_ = 0
        l1ll1llll1l_opy_ = list()
        for element in self._1lll111l_opy_.l1l111llll_opy_:
            if element.t == "part-list":
                for item in element.l111l1l1l1_opy_:
                    l1ll1llll1l_opy_.append(
                        [
                            int(item.l11l11llll_opy_) - 1,
                            int(item.l11lll1ll1_opy_) - 1,
                            int(item.l1llll1l1ll_opy_.split(".")[0]),
                        ]
                    )
            if element.t == "part":
                l1lll111l11_opy_ = 0
                l1lll11111l_opy_ += 1
                l1lll11ll1l_opy_ = list()
                l1ll1lll111_opy_ = mido.MidiTrack()
                mid.tracks.append(l1ll1lll111_opy_)
                l1ll1lll1ll_opy_ = 0
                l1lll11ll1l_opy_.append(
                    [
                        l1ll1lll1ll_opy_,
                        1,
                        "program_change",
                        l1ll1llll1l_opy_[l1lll11111l_opy_ - 1][0],
                        0,
                        0,
                    ]
                )
                l1lll11ll1l_opy_.append(
                    [
                        l1ll1lll1ll_opy_,
                        1,
                        "control_change",
                        l1ll1llll1l_opy_[l1lll11111l_opy_ - 1][2],
                        7,
                        0,
                    ]
                )
                l1lll1111l1_opy_ = False
                l1ll1ll1lll_opy_ = 0
                for l1lllll11ll_opy_ in element.l1lllllll11_opy_:
                    for event in l1lllll11ll_opy_.l111111lll_opy_:
                        if event.t == "note":
                            l1ll1ll1lll_opy_ += 1
                            # print("note", l1ll1ll1lll_opy_)
                            # print("chord during tie", l1lll1111l1_opy_)
                            if not event.rest:
                                # print("chord state", event.l1lll11l11l_opy_)
                                midi_hight = (
                                    12
                                    + event.l111ll1l11_opy_ * 12
                                    + l1lll11l111_opy_[event.step]
                                    + l1lll111l11_opy_
                                )
                                if event.l11l11l11l_opy_:
                                    midi_hight += l1lll11llll_opy_[
                                        event.l11l11l11l_opy_
                                    ]
                            if (
                                not event.rest
                                and l1lll1111l1_opy_
                                and event.l1llll111ll_opy_ == "start"
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ - event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        event.l1lll1ll1ll_opy_,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                            elif (
                                not event.rest
                                and l1lll1111l1_opy_
                                and event.l1llll111ll_opy_ == "stop"
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                            elif (
                                not event.rest
                                and l1lll1111l1_opy_
                                and event.l1llll111ll_opy_ == "no"
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ - event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        event.l1lll1ll1ll_opy_,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                            elif (
                                not event.rest
                                and not event.l11ll1l1l1_opy_
                                and not event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                                if l1ll1llll11_opy_.l1ll1ll1ll1_opy_:
                                    l1lll11ll1l_opy_.append(
                                        [
                                            l1ll1lll1ll_opy_,
                                            4,
                                            "lyrics",
                                            event.text,
                                            0,
                                            0,
                                        ]
                                    )
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ + event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        event.l1lll1ll1ll_opy_,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                                l1ll1lll1ll_opy_ += event.l1lll1ll1ll_opy_
                            elif (
                                not event.rest
                                and not event.l11ll1l1l1_opy_
                                and event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ - event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "start"
                                and not event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                                if l1ll1llll11_opy_.l1ll1ll1ll1_opy_:
                                    l1lll11ll1l_opy_.append(
                                        [
                                            l1ll1lll1ll_opy_,
                                            4,
                                            "lyrics",
                                            event.text,
                                            0,
                                            0,
                                        ]
                                    )
                                l1ll1lll1ll_opy_ += event.l1lll1ll1ll_opy_
                                l1lll11ll11_opy_ += event.l1lll1ll1ll_opy_
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "start"
                                and event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ - event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_on",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "stop-start"
                                and not event.l1lllllllll_opy_
                            ):
                                l1ll1lll1ll_opy_ += event.l1lll1ll1ll_opy_
                                l1lll11ll11_opy_ += event.l1lll1ll1ll_opy_
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "stop-start"
                                and event.l1lllllllll_opy_
                            ):
                                l1lll11ll11_opy_ += event.l1lll1ll1ll_opy_
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "stop"
                                and not event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ + event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        l1lll11ll11_opy_ + event.l1lll1ll1ll_opy_,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                                l1ll1lll1ll_opy_ += event.l1lll1ll1ll_opy_
                                l1lll11ll11_opy_ = 0
                            elif (
                                not event.rest
                                and event.l1llll111ll_opy_ == "stop"
                                and event.l1lllllllll_opy_
                            ):
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_off",
                                        midi_hight,
                                        l1ll1lll1l1_opy_,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                            if event.rest:
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_,
                                        3,
                                        "note_on",
                                        1,
                                        0,
                                        0,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        event.text,
                                    ]
                                )
                                l1lll11ll1l_opy_.append(
                                    [
                                        l1ll1lll1ll_opy_ + event.l1lll1ll1ll_opy_,
                                        3,
                                        "note_off",
                                        1,
                                        0,
                                        event.l1lll1ll1ll_opy_,
                                        l1lllll11ll_opy_.l11ll111ll_opy_,
                                        "",
                                    ]
                                )
                                l1ll1lll1ll_opy_ += event.l1lll1ll1ll_opy_
                            if event.l11ll1l1l1_opy_ and event.l1lll11l11l_opy_ == 1:
                                l1lll1111l1_opy_ = True
                            elif event.l1lll11l11l_opy_ == 3 and l1lll1111l1_opy_:
                                l1lll1111l1_opy_ = False
                        elif event.t == "backup":
                            l1ll1lll1ll_opy_ -= event.l1lll1ll1ll_opy_
                        elif event.t == "attributes":
                            for l11111l1l1_opy_ in event.l1l11l1111_opy_:
                                if l11111l1l1_opy_.t == "divisions":
                                    l111lll1l1_opy_ = l11111l1l1_opy_.l111lll1l1_opy_
                                    tempo = int(480 / l111lll1l1_opy_)
                                elif l11111l1l1_opy_.t == "transpose":
                                    l1lll111l11_opy_ = (
                                        l11111l1l1_opy_.l1l1l1111l_opy_
                                        + 12 * l11111l1l1_opy_.l111111l1l_opy_
                                    )
                        elif event.t == "direction":
                            for l11111l1l1_opy_ in event.l1111l11l1_opy_:
                                if l11111l1l1_opy_.t == "sound":
                                    if l11111l1l1_opy_.l1l11ll1l1_opy_ != "no":
                                        l1lll11ll1l_opy_.append(
                                            [
                                                l1ll1lll1ll_opy_,
                                                2,
                                                "set_tempo",
                                                int(
                                                    1000000
                                                    * 60
                                                    / int(
                                                        l11111l1l1_opy_.l1l11ll1l1_opy_
                                                    )
                                                ),
                                                0,
                                                0,
                                            ]
                                        )
                                elif l11111l1l1_opy_.t == "dynamics":
                                    l1ll1lll1l1_opy_ = l1ll1llllll_opy_[
                                        l11111l1l1_opy_.l1lll1llll1_opy_
                                    ]
                                elif l11111l1l1_opy_.t == "metronome":
                                    l1lll11ll1l_opy_.append(
                                        [
                                            l1ll1lll1ll_opy_,
                                            2,
                                            "set_tempo",
                                            int(
                                                1000000
                                                * 60
                                                / int(l11111l1l1_opy_.l1l111ll1l_opy_)
                                            ),
                                            0,
                                            0,
                                        ]
                                    )
                        elif event.t == "karaoke" and l1ll1llll11_opy_.l1lll1111ll_opy_:
                            l1lll11ll1l_opy_.append(
                                [
                                    l1ll1lll1ll_opy_,
                                    4,
                                    "lyrics",
                                    event.l11llllll1_opy_,
                                    0,
                                    0,
                                ]
                            )
                f.write(str(l1lll11ll1l_opy_))
                l1ll1lll11l_opy_ = sorted(l1lll11ll1l_opy_, key=itemgetter(0, 1, 2))
                f.write("\ntriée\n" + str(l1ll1lll11l_opy_))
                l1lll111ll1_opy_ = 0
                for l1lll111111_opy_ in l1ll1lll11l_opy_:
                    l1lll111ll1_opy_ += l1lll111111_opy_[5]
                    if l1lll111ll1_opy_ > l1lll111111_opy_[0]:
                        l1lll111111_opy_[5] = l1lll111111_opy_[0] - (
                            l1lll111ll1_opy_ - l1lll111111_opy_[5]
                        )
                        l1lll111ll1_opy_ = l1lll111111_opy_[0]
                f.write("\narrangée\n" + str(l1ll1lll11l_opy_))
                f.write("\ntrack\n")
                for message in l1ll1lll11l_opy_:
                    f.write(
                        str(message[0])
                        + " "
                        + str(message[1])
                        + " "
                        + str(message[2])
                        + " "
                        + str(message[3])
                        + " "
                        + str(message[4])
                        + " "
                        + str(message[5])
                        + "\n"
                    )
                    if message[1] == 3:
                        l1ll1lll111_opy_.append(
                            mido.Message(
                                message[2],
                                note=message[3],
                                velocity=message[4],
                                time=message[5] * tempo,
                                channel=l1ll1llll1l_opy_[l1lll11111l_opy_ - 1][1],
                            )
                        )
                    elif message[1] == 2:
                        l1ll1lll111_opy_.append(
                            mido.MetaMessage(
                                message[2], tempo=message[3], time=message[4]
                            )
                        )
                    elif message[1] == 4:
                        l1ll1lll111_opy_.append(
                            mido.MetaMessage(
                                message[2], text=message[3], time=message[4]
                            )
                        )
                    elif message[1] == 1 and message[2] == "program_change":
                        l1ll1lll111_opy_.append(
                            mido.Message(
                                message[2],
                                program=message[3],
                                channel=l1ll1llll1l_opy_[l1lll11111l_opy_ - 1][1],
                            )
                        )
                    elif message[1] == 1 and message[2] == "control_change":
                        l1ll1lll111_opy_.append(
                            mido.Message(
                                message[2],
                                control=message[4],
                                value=message[3],
                                channel=l1ll1llll1l_opy_[l1lll11111l_opy_ - 1][1],
                            )
                        )
        mid.save(l1ll1lllll1_opy_)
