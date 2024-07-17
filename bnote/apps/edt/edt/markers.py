"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


import string
from .coordinates import Coordinates
from .marker import Marker
from .pos import Pos
# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_MARKERS_LOG, logging
log = ColoredLogger(__name__, level=EDITOR_MARKERS_LOG)


# -----------------------------------------------
# Markers definition
class Markers:
    MAX_MARKERS = 50

    def __init__(self):
        self._markers = []

    # For print()
    def __str__(self):
        text = "\r\nMarkers list ------\r\n"
        if not self._markers:
            text += "No markers\r\n"
        else:
            for index, marker in enumerate(self._markers):
                text += "Marker{} {}\r\n".format(index, marker)
        text += "-------------------\r\n"
        return text

    def set_marker(self, marker):
        """
        Add a marker without control.
        """
        self._markers.append(marker)

    def add_marker(self, coo, paragraph):
        """
        Add a marker if no marker at this position.
        coo: Coordinates(column, line, paragraph)
        paragraph: Paragraph where marker is added.
        -> bool: True if marker added
        """
        res = False
        marker_index = paragraph.index_from_coordinates(Pos(coo.column, coo.line))
        marker_to_add = Marker(marker_index, coo.paragraph)
        if (self.find_marker(marker_to_add) != -1) | (len(self._markers) >= self.MAX_MARKERS):
            # Marker already exists or max number of marker reached
            if EDITOR_MARKERS_LOG <= logging.INFO:
                log.info("Marker already exists")
        else:
            if EDITOR_MARKERS_LOG <= logging.INFO:
                log.info("Add marker")
            self._markers.append(marker_to_add)
            res = True
        if EDITOR_MARKERS_LOG <= logging.INFO:
            log.info(self.__str__())
        return res

    def xml_render(self):
        """
        xml rendering for all markers.
        -> str
        """
        marker_template = string.Template('    <marker id="${id}" paragraph="${par}" index="${index}" />')
        return [marker_template.substitute(id=index, par=marker.paragraph, index=marker.index)
                for index, marker in enumerate(self._markers)]

    def find_marker(self, marker):
        """
        Find a marker.
        marker: Marker
        -> index in self.markers list
        """
        for index, marker_item in enumerate(self._markers):
            if marker == marker_item:
                return index
        return -1

    def remove_marker(self, coo, paragraph):
        """
        Remove a marker if no marker at this position.
        coo: Coordinates(column, line, paragraph)
        paragraph: Paragraph where marker is added.
        -> no return
        """
        marker_index = paragraph.index_from_coordinates(Pos(coo.column, coo.line))
        marker_to_remove = Marker(marker_index, coo.paragraph)
        if EDITOR_MARKERS_LOG <= logging.INFO:
            log.info("Remove marker")
        try:
            self._markers.remove(marker_to_remove)
        except ValueError:
            if EDITOR_MARKERS_LOG <= logging.WARNING:
                log.warning("no marker to delete")
        if EDITOR_MARKERS_LOG <= logging.INFO:
            log.info(self.__str__())

    def clear_marker(self):
        """
        Remove all marker.
        -> no return
        """
        if EDITOR_MARKERS_LOG <= logging.INFO:
            log.info("Clear all markers")
        self._markers.clear()

    def next_marker(self, coo, paragraphs):
        """
        Next marker.
        coo: Coordinates(column, line, paragraph)
        paragraphs: Paragraphs collection of paragraphs.
        -> coo: Coordinates(column, line, paragraph) of next marker
        """
        marker_index = paragraphs.paragraph(coo.paragraph).index_from_coordinates(Pos(coo.column, coo.line))
        current_position = Marker(marker_index, coo.paragraph)
        select_marker = None
        # Find nearest larger marker
        for marker in self._markers:
            if (marker > current_position) and ((not select_marker) or (marker < select_marker)):
                select_marker = marker
        # Find the first smaller marker
        if not select_marker:
            for marker in self._markers:
                if (not select_marker) or (marker < select_marker):
                    select_marker = marker
        if select_marker:
            pos = paragraphs.paragraph(select_marker.paragraph).coordinates_from_index(select_marker.index)
            return Coordinates(pos.x, pos.y, select_marker.paragraph)
        # No position found.
        return coo

    def previous_marker(self, coo, paragraphs):
        """
        Previous marker.
        coo: Coordinates(column, line, paragraph)
        paragraphs: Paragraphs collection of paragraphs.
        -> coo: Coordinates(column, line, paragraph) of next marker
        """
        marker_index = paragraphs.paragraph(coo.paragraph).index_from_coordinates(Pos(coo.column, coo.line))
        current_position = Marker(marker_index, coo.paragraph)
        select_marker = None
        # Find nearest smaller marker
        for marker in self._markers:
            if (marker < current_position) and ((not select_marker) or (marker > select_marker)):
                select_marker = marker
        # Find the last bigger marker
        if not select_marker:
            for marker in self._markers:
                if (not select_marker) or (marker > select_marker):
                    select_marker = marker
        if select_marker:
            pos = paragraphs.paragraph(select_marker.paragraph).coordinates_from_index(select_marker.index)
            return Coordinates(pos.x, pos.y, select_marker.paragraph)
        # No position found.
        return coo

    def extract(self, coo, paragraph, length):
        """
        Extract all marker in a paragraph
        coo: Coordinates(column, line, paragraph)
        paragraph: Paragraph
        length: int number of characters of the paragraph
        -> list of markers extracted.
        """
        paragraph_index = None
        markers_list = []
        markers_to_keep = []
        for marker in self._markers:
            if marker.paragraph == coo.paragraph:
                if not paragraph_index:
                    # Compute index of marker in original paragraph
                    paragraph_index = paragraph.index_from_coordinates(Pos(coo.column, coo.line))
                if paragraph_index <= marker.index <= paragraph_index + length:
                    # Extract marker and recompute index.
                    markers_list.append(Marker(marker.index - paragraph_index, marker.paragraph))
                else:
                    markers_to_keep.append(marker)
            else:
                markers_to_keep.append(marker)
        self._markers = markers_to_keep
        return markers_list

    def replace(self, coo, markers_list, offset):
        """
        Change a marker.
        coo: Coordinates(column, line, paragraph) for coo.paragraph
        markers_list: the list of markers to offset
        offset: value to add at marker index in paragraph
        """
        for marker in markers_list:
            self._markers.append(Marker(marker.index + offset, coo.paragraph))

    def insert_paragraphs(self, insertion_coo, paragraphs_number):
        """
        Insert a number of paragraphs before the position and move markers.
        insertion_coo: Coordinates(column, line, paragraph)
        paragraphs_number: int number of paragraphs to insert.
        -> No return
        """
        if EDITOR_MARKERS_LOG <= logging.DEBUG:
            log.debug("Marker : Insertion {} paragraphs at {}".format(paragraphs_number, insertion_coo))
        for marker in self._markers:
            if marker.paragraph >= insertion_coo.paragraph:
                marker.paragraph += paragraphs_number

    def delete_paragraphs(self, deletion_coo, paragraphs_number):
        """
        Delete a number of paragraphs before the position and move markers.
        deletion_coo: Coordinates(column, line, paragraph)
        paragraphs_number: int number of paragraphs to delete.
        -> No return
        """
        if EDITOR_MARKERS_LOG <= logging.DEBUG:
            log.debug("Marker : Delete {} lines at {}".format(paragraphs_number, deletion_coo))
        markers_to_keep = []
        # remove markers in the deleted bloc and shift the marker after the bloc.
        for marker in self._markers:
            if marker.paragraph < deletion_coo.paragraph:
                # Keep marker before deleted paragraph
                markers_to_keep.append(marker)
            elif marker.paragraph >= deletion_coo.paragraph + paragraphs_number:
                # move the marker situated after the deletion.
                marker.paragraph -= paragraphs_number
                # keep them
                markers_to_keep.append(marker)
        self._markers = markers_to_keep

    def insert_char_in_paragraph(self, insertion_coo, paragraph, characters_number):
        """
        Insert a number of characters in a paragraph
        insertion_coo: Coordinates(column, line, paragraph)
        paragraph: current paragraph where insertion is done
        characters_number: int number of characters to insert.
        -> No return
        """
        if EDITOR_MARKERS_LOG <= logging.DEBUG:
            log.debug("Marker : Insertion {} characters at {}".format(characters_number, insertion_coo))
        insert_index = None
        for marker in self._markers:
            if marker.paragraph == insertion_coo.paragraph:
                if not insert_index:
                    # Compute index of marker in original paragraph
                    insert_index = paragraph.index_from_coordinates(Pos(insertion_coo.column, insertion_coo.line))
                if insert_index <= marker.index:
                    marker.index += characters_number

    def delete_char_in_paragraph(self, deletion_coo, paragraph, characters_number):
        """
        Delete a number of characters in a paragraph
        deletion_coo: Coordinates(column, line, paragraph) of deletion
        paragraph: Paragraph original paragraph
        characters_number : Number of characters to delete
        -> No return
        """
        if EDITOR_MARKERS_LOG <= logging.DEBUG:
            log.debug("Marker : Delete {} lines at {}".format(characters_number, deletion_coo))
        if characters_number <= 0:
            return
        # Compute index of marker in original paragraph
        insert_index = paragraph.index_from_coordinates(Pos(deletion_coo.column, deletion_coo.line))
        markers_to_keep = []
        for marker in self._markers:
            if marker.paragraph == deletion_coo.paragraph:
                if insert_index <= marker.index:
                    if insert_index + characters_number <= marker.index:
                        marker.index -= characters_number
                        markers_to_keep.append(marker)
                    # else
                    # This category of marker are delete from the marker list.
                else:
                    markers_to_keep.append(marker)
            else:
                markers_to_keep.append(marker)
        self._markers = markers_to_keep

    def merge_paragraph(self, coo, next_paragraph):
        """
        Compute markers for merging paragraph with the next.
        coo: Coordinates(column, line, paragraph) of merge
        next_paragraph: Paragraph the next paragraph
        -> No return
        """
        markers_to_keep = []
        # The offset to add to all markers of next paragraph.
        offset = next_paragraph.index_from_coordinates(Pos(coo.column, coo.line))
        for marker in self._markers:
            if marker.paragraph == coo.paragraph + 1:
                # marker in the next paragraph => add offset to marker index
                marker.paragraph = coo.paragraph
                marker.index += offset
                markers_to_keep.append(marker)
            elif marker.paragraph > coo.paragraph + 1:
                # marker after paragraph to merge => decrement paragraph number of marker
                marker.paragraph -= 1
                markers_to_keep.append(marker)
            else:
                # marker before the next paragraph => keep marker, no change
                markers_to_keep.append(marker)
        self._markers = markers_to_keep

    def markers_list(self, paragraph, start_index, end_index):
        """
        Construct a list of int with all marker in paragraph between start_index and end_index.
        """
        indexes = list()
        for marker in self._markers:
            if marker.paragraph == paragraph:
                if start_index <= marker.index < end_index:
                    indexes.append(marker.index)
        return indexes
