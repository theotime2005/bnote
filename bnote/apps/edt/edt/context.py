"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from pathlib import Path

from bnote.apps.fman.file_manager import FileManager

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_LOG

log = ColoredLogger(__name__, level=EDITOR_LOG)


class Context:
    # --------- KEYS FOR CONTEXT FILES
    CONTEXT_FILE_EDITOR = ".edt_context{}.ctx"
    CONTEXT_DOC_EDITOR = ".doc_context{}"

    KEY_FOCUSED = "Focused"
    KEY_FILENAME = "Filename"
    KEY_SAVENAME = "Save"

    KEY_MODIFIED = "Modified"
    KEY_NOT_MODIFIED = "Not modified"

    def __init__(self):
        pass

    # Find the first context file not used.
    @staticmethod
    def free_context_file():
        # Register file in document to open when pi restart.
        # The root path where all user documents will be saved
        index = 1
        current_folder = FileManager.get_root_path()
        while True:
            context_file = current_folder / Context.CONTEXT_FILE_EDITOR.format(index)
            if not context_file.exists():
                break
            index += 1
        return context_file

    # Find the first context file written.
    @staticmethod
    def first_context_file():
        # The root path where all user documents will be saved
        index = 1
        current_folder = FileManager.get_root_path()
        context_file = None
        while index < 10:
            context_file = current_folder / Context.CONTEXT_FILE_EDITOR.format(index)
            if context_file.exists():
                break
            index += 1

        if index != 10:
            return context_file

    @staticmethod
    def free_doc_file(extension):
        # Find a temporary file name
        index = 1
        current_folder = FileManager.get_root_path()
        while True:
            doc_file = current_folder / "".join(
                [Context.CONTEXT_DOC_EDITOR.format(index), extension]
            )
            if not doc_file.exists():
                break
            index += 1
        return doc_file

    @staticmethod
    def write_context_file(context_file, modified, focused, file, doc_file):
        if modified:
            context_file.write_text(
                "{0}\n{1}={4}\n{2}={5}\n{3}={6}".format(
                    Context.KEY_MODIFIED,
                    Context.KEY_FOCUSED,
                    Context.KEY_FILENAME,
                    Context.KEY_SAVENAME,
                    focused,
                    file,
                    doc_file,
                )
            )
        else:
            context_file.write_text(
                "{0}\n{1}={3}\n{2}={4}\n".format(
                    Context.KEY_NOT_MODIFIED,
                    Context.KEY_FOCUSED,
                    Context.KEY_FILENAME,
                    focused,
                    file,
                )
            )

    @staticmethod
    def _delete_all_context_files(generic_name):
        index = 1
        current_folder = FileManager.get_root_path()
        while True:
            context_file = current_folder / generic_name.format(index)
            if context_file.exists():
                # Delete the file
                context_file.unlink()
            else:
                break
            index += 1

    # Clean up all context files.
    @staticmethod
    def clean_up_context_files():
        # Delete all context files.
        Context._delete_all_context_files(Context.CONTEXT_FILE_EDITOR)
        # Delete all doc files.
        Context._delete_all_context_files(Context.CONTEXT_DOC_EDITOR)
        # Delete all .doc files
        Context._delete_all_context_files("." + Context.CONTEXT_DOC_EDITOR)

    @staticmethod
    def _get_arg(lines, arg_to_find):
        for line in lines:
            args = line.split("=")
            if (len(args) == 2) and (args[0] == arg_to_find):
                return args[1]

    @staticmethod
    def parse_context_file(context_file):
        is_modified = False
        is_focused = False
        file_name = None
        save_name = None
        context = context_file.read_text()
        log.info("context is {}".format(context))
        lines = context.split("\n")
        if len(lines) > 1:
            if Context._get_arg(lines, Context.KEY_FOCUSED) == "True":
                is_focused = True
            if lines[0] == Context.KEY_NOT_MODIFIED:
                # Restore a not modified file.
                is_modified = False
                log.info(
                    "file to open is {}".format(
                        Context._get_arg(lines, Context.KEY_FILENAME)
                    )
                )
                log.info(
                    "file focus is {}".format(
                        Context._get_arg(lines, Context.KEY_FOCUSED)
                    )
                )
                file_name = Context._get_arg(lines, Context.KEY_FILENAME)
            else:
                # Restore a modified file
                is_modified = True
                file_name = Context._get_arg(lines, Context.KEY_FILENAME)
                save_name = Context._get_arg(lines, Context.KEY_SAVENAME)
        return is_modified, is_focused, file_name, save_name

    @staticmethod
    def write_integrity_file():
        # Write integrity file to specify successful shutdown.
        integrity_file = FileManager.get_root_path() / ".integrity"
        integrity_file.write_text("Context saved.\nYou know what ? I'm happy !")

    @staticmethod
    def is_integrity_then_delete():
        integrity_file = FileManager.get_root_path() / ".integrity"
        if integrity_file.exists():
            # Delete context file.
            integrity_file.unlink()
            return True
        else:
            return False
