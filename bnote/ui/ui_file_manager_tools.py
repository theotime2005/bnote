"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
# Set up the logger for this file
import os
from pathlib import Path

from bnote.apps.bnote_app import BnoteApp
from bnote.apps.fman.file_manager import Trash, FileManager
from bnote.debug.colored_log import ColoredLogger, UI_LOG

log = ColoredLogger(__name__)
log.setLevel(UI_LOG)


class UiFileManagerTools:

    def _ui_file_name(self, braille_type, filename):
        log.debug(f"filename={filename}")
        if os.path.exists(filename):
            if os.path.isdir(filename):
                if filename != Trash.get_trash_path() and str(filename).startswith(str(Trash.get_trash_path())):
                    log.debug("trash")
                    original_path = Trash.original_file(filename)
                    deletion_date = Trash.deletion_date(filename)
                    msg, pos = self._convert_to_braille_text(braille_type, _("deleted on {}").format(deletion_date.strftime(_("%A %d %B %Y %H:%M:%S"))))
                    friendly_name = UiFileManagerTools.friendly_file_name(original_path, True)
                    return "".join((_("d "), original_path.name,
                                    self._convert_file_to_braille_text(braille_type, " ({}) ".format(friendly_name)),
                                    msg))
                else:
                    # Use a translated name for specials folders.
                    if filename in (FileManager.get_backup_path(), FileManager.get_bluetooth_path(),
                                    FileManager.get_documents_path(), FileManager.get_crash_path(),
                                    FileManager.get_usb_flash_drive_path(), Trash.get_trash_path(),
                                    FileManager.get_settings_path(),
                                     FileManager.get_exam_path()):
                        # Translate the specials folders.
                        friendly_name = UiFileManagerTools.friendly_file_name(filename, True)
                    else:
                        friendly_name = filename.name
                    return "".join((_("d "), self._convert_file_to_braille_text(braille_type, friendly_name)))
            elif os.path.isfile(filename):
                if str(filename).startswith(str(Trash.get_trash_path())):
                    log.debug("trash")
                    original_path = Trash.original_file(filename)
                    deletion_date = Trash.deletion_date(filename)
                    msg, pos = self._convert_to_braille_text(braille_type, _("deleted on {}").format(deletion_date.strftime(_("%A %d %B %Y %H:%M:%S"))))
                    return "".join((_("f "), original_path.name,
                                    self._convert_file_to_braille_text(braille_type, " ({}) ".format(UiFileManagerTools.friendly_file_name(original_path, True))),
                                    msg))
                else:
                    return "".join((_("f "),
                                    self._convert_file_to_braille_text(braille_type, filename.name),
                                    UiFileManagerTools.__get_file_size(filename)))
        return filename.name

    def _convert_to_braille_text(self, braille_type, text, pos=-1) -> (str, int):
        if braille_type == 'grade1':
            if pos >= 0:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade1(text, pos)
            else:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade1(text)
                pos = -1
            log.debug("grade1:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
        elif braille_type == 'grade2':
            if pos >= 0:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade2(text, pos)
            else:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade2(text)
                pos = -1
            log.debug("grade2:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
        else:
            text_grade = text
        return text_grade, pos

    def _convert_file_to_braille_text(self, braille_type, filename):
        p = Path(filename)
        parts = p.parts
        braille_text = None
        if len(parts) > 1:
            # Treat path element
            for part in parts[0: len(parts) - 1]:
                part_braille_text, pos = self._convert_to_braille_text(braille_type, part)
                if braille_text:
                    braille_text = "/".join([braille_text, part_braille_text])
                else:
                    braille_text = part_braille_text
        # Treat file name
        part = parts[len(parts) - 1]
        if braille_text:
            braille_text = "/".join([braille_text, self._convert_file_name_to_braille_text(braille_type, part)])
        else:
            braille_text = self._convert_file_name_to_braille_text(braille_type, part)
        return braille_text

    def _convert_file_name_to_braille(self, braille_type, file) -> (str, str):
        """
        Convert a file name in braille string.
        """
        path_file = Path(file)
        file_name = path_file.stem
        file_suffix = path_file.suffix
        text_name, braille_name, pos = BnoteApp.lou.convert_to_braille(braille_type, file_name)
        text_suffix, braille_suffix, pos = self._convert_suffix_to_braille(braille_type, file_suffix)
        if len(braille_suffix) > 1:
            # Remove separator dot in suffix
            braille_suffix = braille_suffix[1: len(braille_suffix)]
        text_separator, braille_separator, pos = BnoteApp.lou.convert_to_braille(braille_type, ".")
        if braille_suffix != "":
            return braille_name, "".join([braille_name, braille_separator, braille_suffix])
        else:
            return braille_name, braille_name

    def _convert_file_name_to_braille_text(self, braille_type, file) -> (str):
        """
        Convert a file name in braille string.
        """
        path_file = Path(file)
        file_name = path_file.stem
        file_suffix = path_file.suffix
        text_name, pos = self._convert_to_braille_text(braille_type, file_name)
        text_suffix, pos = self._convert_suffix_to_braille_text(braille_type, file_suffix)
        return "".join([text_name, text_suffix])

    def _convert_suffix_to_braille_text(self, braille_type, text, pos=-1) -> (str, int):
        if braille_type == 'grade1' or braille_type == 'grade2':
            if pos >= 0:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade1(text, pos)
            else:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.text_to_grade1(text)
                pos = -1
            log.debug("grade1:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
        else:
            text_grade = text
        return text_grade, pos

    def _convert_suffix_to_braille(self, braille_type, text, pos=-1) -> (str, str, int):
        """
        Conversion for suffix of files.
        """
        text_grade, pos = self._convert_suffix_to_braille_text(braille_type, text, pos)
        if braille_type == 'grade1' or braille_type == 'grade2':
            braille = BnoteApp.lou.to_dots_6(text_grade)
        else:
            braille = BnoteApp.lou.to_dots_8(text_grade)
        return text_grade, braille, pos

    def _convert_suffix_to_text(self, braille_type, braille, pos=-1):
        """
        Conversion for suffix of files.
        """
        if braille_type == 'grade1' or braille_type == 'grade2':
            if pos >= 0:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.grade1_to_text(braille, pos)
            else:
                (text_grade, index1_origin, index_text, pos) = BnoteApp.lou.grade1_to_text(braille)
                pos = -1
            log.debug("grade1:<{}>, {}, {}, {}".format(text_grade, index1_origin, index_text, pos))
        else:
            text_grade = BnoteApp.lou.to_text_8(braille)
        return text_grade, pos


    @staticmethod
    def friendly_file_name(filename, replace_backup=False):
        """
            The name to present to user in message dialog box to report error / success of operation.
        """
        log.debug(f"FileManager.get_tmp_path()={FileManager.get_tmp_path()}")
        log.debug(f"filename={filename}")
        friendly_name = str(filename).replace(str(FileManager.get_tmp_path()) + os.path.sep, "")
        if replace_backup:
            friendly_name = friendly_name.replace(str(FileManager.get_backup_path()) + os.path.sep, "")

        friendly_name = friendly_name.replace(str(Trash.get_trash_path()), _("trash"))
        friendly_name = friendly_name.replace(str(FileManager.get_bluetooth_path()), _("bluetooth"))
        friendly_name = friendly_name.replace(str(FileManager.get_backup_path()), _("my backups"))
        friendly_name = friendly_name.replace(str(FileManager.get_usb_flash_drive_path()), _("usb flash drives"))
        friendly_name = friendly_name.replace(str(FileManager.get_documents_path()), _("my Documents"))
        friendly_name = friendly_name.replace(str(FileManager.get_crash_path()), _("crash"))
        friendly_name = friendly_name.replace(str(FileManager.get_settings_path()), _("settings"))
        friendly_name = friendly_name.replace(str(FileManager.get_exam_path()), _("examen"))
        # Always try to replace main folder after the documents sub folder (like symbolic link
        # on trash / bluetooth / backup / usb flash drive that are located inside main folder.)
        friendly_name = friendly_name.replace(str(FileManager.get_main_folder_path()), _("bnote"))

        return friendly_name

    @staticmethod
    def __get_file_size(full_file_name) -> str:
        if os.path.exists(full_file_name):
            if os.path.isfile(full_file_name):
                size = os.path.getsize(full_file_name)
                if size < 1000:
                    return "".join((" ({} ".format(size), _("bytes"), ")"))
                elif size < 1000000:
                    return "".join((" ({:.1f} ".format(size / 1000), _("Kb"), ")"))
                elif size < 1000000000:
                    return "".join((" ({:.1f} ".format(size / 1000000), _("Mb"), ")"))
                elif size < 1000000000000:
                    return "".join((" ({:.1f} ".format(size / 1000000000), _("Gb"), ")"))
                else:
                    return "".join((" ({} ".format(size), _("bytes"), ")"))

        return ""
