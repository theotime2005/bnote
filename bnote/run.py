"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import time
import shutil
from pathlib import Path
import pkg_resources
from bnote.tools import bt_util
from bnote.tools.settings import Settings
from bnote.bnote_start import BnoteThread
from bnote.apps.fman.file_manager import BNOTE_FOLDER, DOCUMENTS_FOLDER

from bnote.debug.colored_log import ColoredLogger, BNOTE_LOG

log = ColoredLogger(__name__)
log.setLevel(BNOTE_LOG)


def main(debug=False):
    log.error(f"Start bnote ...{debug=}")
    # print(f"{YAUpdater.get_version_from_pyproject_toml('pyproject.toml')}")
    if debug:
        # If bnote_start is running, stop bnote service.
        print(f"Call os.popen('sudo systemctl stop bnote.service')")
        os.popen('sudo systemctl stop bnote.service')
        # Wait 5 second for service stopping.
        time.sleep(5)
    # Set the bnote device visibility to nearby Bluetooth devices
    bt_util.set_discoverable(Settings().data['bluetooth']['bnote_visible'])
    # disable NTP (Network Time Protocol)
    os.popen('sudo timedatectl set-ntp false')
    # #115 : move documentation from updated sources.
    try:
        move_documentation(debug)
    # A bare 'except' is used here because we don't want that the move_documentation to prevent bnote from starting.
    except:
        log.error("Error during move documentation !!!")
    bnote_thread = BnoteThread(debug)
    bnote_thread.start()
    # Delete the failed_launch.txt file used to return to orinal bnote if current update do not start 3 times.
    failed_launch_file = Path("./failed_launch.txt")
    if failed_launch_file.exists():
        failed_launch_file.unlink()
    # End of starter but BnoteThread is running.
    print("goodbye")
    log.info("goodbye.")


def move_documentation(debug):
    # The folder extracted from the bnote package.
    # (located in/home/pi/bnote/venv/lib/python3.11/site-packages/bnote)
    if debug:
        # In debug session, the documentation is not moved.
        return
    documentation_src_path = Path(pkg_resources.resource_filename('bnote', 'bnote-documents'))
    if documentation_src_path.exists():
        # The folder "/home/pi/.bnote/note-documents
        documentation_dst_path = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER)
        # Copy the files (and folders)
        shutil.copytree(documentation_src_path, documentation_dst_path, ignore=ignore_existing_file,
                        dirs_exist_ok=True)
        # Delete permanently the source folder.
        shutil.rmtree(documentation_src_path)


def ignore_existing_file(folder, files):
    # log.error(f"{folder=}, {files=}")
    ignore_files = []
    documentation_src_path = Path(pkg_resources.resource_filename('bnote', 'bnote-documents'))
    # log.error(f"{documentation_src_path=}")
    relative_path = Path(folder).relative_to(documentation_src_path)
    # log.error(f"{relative_path=}")
    for file in files:
        dest_file = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER) / relative_path / file
        # Add to ignore file list the file that already exist in destination.
        if dest_file.exists() and dest_file.is_file():
            ignore_files.append(file)
    # log.error(f"{ignore_files=}")
    return ignore_files


if __name__ == '__main__':
    main()
