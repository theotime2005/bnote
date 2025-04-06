"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from .editor import Editor

from .colored_log import ColoredLogger, EDITOR_DAISY_LOG, logging

log = ColoredLogger(__name__, level=EDITOR_DAISY_LOG)


class EditorDaisy(Editor):
    """
    This class add functionalities to bnote typed braille editor :
        - Handle Daisy summary,
        - Handle Daisy paragraph with tag.
    """

    def __init__(self, width, paragraphs, is_read_only=True):
        self.document_structure = []
        paragraphs_data = []
        for paragraph in paragraphs:
            paragraph_tag, paragraph_data = paragraph
            paragraphs_data.append(paragraph_data)
            self.document_structure.append(paragraph_tag)
        super().__init__(width, paragraphs_data, is_read_only=is_read_only)

    def append_paragraph(self, paragraph):
        paragraph_tag, paragraph_data = paragraph
        # log.critical(f"add paragraph:{paragraph_tag=}-{paragraph_data=}")
        self.document_structure.append(paragraph_tag)
        super().append_paragraph(paragraph_data)

    def daisy_tag(self, index):
        """
        Returns the tag of a paragraph known by its index in document.
        """
        if index < len(self.document_structure):
            return self.document_structure[index]

    def set_caret_on_tag(self, paragraph_tag):
        try:
            index = self.document_structure.index(paragraph_tag)
            self.set_caret_on_paragraph(index)
        except ValueError:
            log.error(f"invalid tag: <{paragraph_tag}>")

    def current_summary_index(self, text_tag_list):
        """
        Returns the index in a text tag list of current caret position.
        """
        start_pos_caret, end_pos_caret = self.caret_as_paragraph_position()
        for paragraph_index in range(end_pos_caret.x, -1, -1):
            daisy_tag = self.daisy_tag(paragraph_index)
            # log.critical(f"{daisy_tag=}")
            if daisy_tag in text_tag_list:
                return text_tag_list.index(daisy_tag)
