"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import threading
import time

from bnote.braille.lou import Lou


class WriteBrfFile(threading.Thread):
    def __init__(
        self,
        get_line,
        full_file_name,
        language,
        braille_type,
        line_length,
        page_line,
        max_page,
        first_page,
        braille_table,
        on_end,
    ):
        threading.Thread.__init__(self)
        self._get_line = get_line
        self.file_name = full_file_name
        # On récupère le chemin du fichier et on supprime l'extention
        self.path_name = self.file_name[:-4]
        self.language = language
        self.braille_type = braille_type
        self.line_length = line_length
        self.page_line = page_line
        self.max_page = max_page
        self.braille_document = []
        self.first_origine_first_page = first_page
        self.first_page = []
        self.page_document = []
        self.braille_table = braille_table
        self.on_end = on_end

    def run(self) -> None:
        self.get_title(self.first_origine_first_page)
        document_original = self.import_and_convert_file()
        self.page_document = self._cut_document(document_original)
        self._get_volume()
        self.construct_document()

    def get_title(self, first_page):
        page = first_page.split("\n")[1:]
        for line in page:
            new_line = self.delete_strange_characters(line)
            self.first_page.append(
                Lou(self.language).convert_to_braille(self.braille_type, new_line)[1]
            )

    def import_and_convert_file(self):
        file_convert = []
        if self._get_line is None:
            raise IOError("Error during editor access")
        cnt = 0
        while True:
            line = self._get_line(cnt)
            if line is None:
                # last line reached.
                break
            line_convert = self.delete_strange_characters(line)
            file_convert.append(
                Lou(self.language).convert_to_braille(self.braille_type, line_convert)[
                    1
                ]
            )
            # Just to let others threads running.
            time.sleep(0.001)
            # Next line.
            cnt += 1
        return file_convert

    @staticmethod
    def delete_strange_characters(line):
        # On pourra ajouter les caractères à la liste
        character_lst = ["\t", chr(65279), "\n"]
        new_line = ""
        for c in line:
            if not c in character_lst:
                new_line += c
        return new_line

    def __get_space(self, line, page_number):
        space_number = self.line_length - len(line) - len(str(page_number))
        spaces = ""
        for _ in range(space_number):
            spaces += chr(10240)
        spaces += Lou(self.language).convert_to_braille(
            self.braille_type, str(page_number)
        )[1]
        return spaces

    def __get_lines(self, line_number):
        line = self.page_line - line_number
        lines = []
        for _ in range(line):
            lines.append("")
        return lines

    def _cut_document(self, content):
        # start with lines
        lines = []
        while content:
            my_line = content[0]
            if len(my_line) > self.line_length:
                cutter = self.line_length
                while my_line[cutter] != chr(10240):
                    cutter -= 1
                lines.append(my_line[:cutter])
                content[0] = my_line[cutter + 1 :]
            else:
                lines.append(my_line)
                content.remove(my_line)
        # Continue with page
        pages = []
        page_count = 1
        if len(lines) > self.page_line:
            while lines:
                new_page = lines[: self.page_line]
                if page_count >= 2:
                    new_page[0] += "{}".format(
                        self.__get_space(new_page[0], page_count)
                    )
                pages.append(new_page)
                lines = lines[self.page_line :]
                page_count += 1
        else:
            pages.append(lines)
        return pages

    def _get_volume(self):
        if len(self.page_document) > self.max_page:
            volume = 1
            while self.page_document:
                new_volume = self.page_document[: self.max_page]
                volume_number = _("Volume {}").format(volume)
                volume_title = Lou(self.language).convert_to_braille(
                    self.braille_type, "\n{}\n".format(volume_number)
                )[1]
                volume_to_insert = self._cut_document(
                    self.first_page
                    + [volume_title]
                    + self.__get_lines(len(self.first_page + [volume_title]))
                )
                new_volume = volume_to_insert + new_volume
                self.braille_document.append(new_volume)
                self.page_document = self.page_document[self.max_page :]
                volume += 1
        else:
            first_page = self._cut_document(self.first_page)
            self.braille_document.append(first_page + self.page_document)

    def construct_document(self):
        if len(self.braille_document) >= 2:
            folder_name = "{}_braille".format(self.path_name)
            try:
                os.mkdir(folder_name)  # Create folder with volumes
            except FileExistsError:
                self.on_end("exist")
                return False
            cpt = 1
            for volume in self.braille_document:
                name_file = _("Volume {}").format(cpt)
                self._create_file(volume, "{}/{}.brf".format(folder_name, name_file))
                cpt += 1
            self.on_end("success")
        else:
            if not self.braille_document:
                return
            book = self.braille_document[0]
            self._create_file(book, "{}_braille.brf".format(self.path_name))
            self.on_end("success")

    def _create_file(self, file, name):
        if not self.braille_table:
            self.braille_table = self.braille_type
        f = open(name, "w", encoding="cp1252")
        for page in file:
            for line in page:
                new_line = ""
                for c in line:
                    new_line += Lou(self.braille_table).to_text_6(c)
                f.write("{}\n".format(new_line))
        f.close()
