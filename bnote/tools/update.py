"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import shutil

from apps.fman.file_manager import FileManager, BNOTE_FOLDER, DOCUMENTS_FOLDER
from stm32.braille_device_characteristics import braille_device_characteristics
import os.path
import re
from pathlib import Path
import zipfile

# Setup the logger for this file
from debug.colored_log import ColoredLogger, FILE_MANAGER_LOG
log = ColoredLogger(__name__)
log.setLevel(FILE_MANAGER_LOG)


class Update:

    __UPDATE_FILE_EXTENSION = ".update"
    __INSTALL_FOLDER = "bnote"
    __sources_path = Path.home() / Path(__INSTALL_FOLDER)

    @classmethod
    def get_update_file_extension(cls):
        return cls.__UPDATE_FILE_EXTENSION

    @classmethod
    def get_sources_path(cls):
        return cls.__sources_path

    @staticmethod
    def is_installable(file):
        if isinstance(file, str):
            file = Path(file)

        if file.suffix == Update.__UPDATE_FILE_EXTENSION:
            # Check file integrity of the zip file (It simply must contains bnote_start.py to be ok)
            try:
                update_zip_file = zipfile.ZipFile(file, 'r')
                info_list = update_zip_file.infolist()
                update_zip_file.close()
                for zip_info in info_list:
                    if zip_info.filename.find("bnote_start.py") != -1:
                        return True
            except zipfile.BadZipfile as e:
                log.warning("Error {}".format(e))

        return False

    @staticmethod
    def is_firmware_compliant(file):
        raw_update_version = Update.extract_version(file)
        current_raw_firmware_version = braille_device_characteristics.get_firmware_version()

        return Update.is_first_str_version_equal_or_greater(current_raw_firmware_version, raw_update_version)

    @staticmethod
    def is_sdcard_compliant(file):
        raw_update_version = Update.extract_version(file, version_key="__minimum_sdcard_version")
        if (Path().home() / Path("sdcard_version")).exists():
            with open(Path().home() / Path("sdcard_version"), 'r') as f:
                current_raw_sdcard_version = f.readline()
        else:
            # If sdcard_version file is not present, refuse update (the sdcard is probably dammaged)
            return False

        return Update.is_first_str_version_equal_or_greater(current_raw_sdcard_version, raw_update_version)

    @staticmethod
    def stage_number_from_type(stage_type):
        types = ('alpha', 'beta', 'rc')
        if stage_type == "":
            # Release version win 1 000 000.
            return 1000000
        elif stage_type in types:
            # Developpers version between 1 and 3.
            return types.index(stage_type) + 1
        else:
            # Others value are before alpha, beta and rc.
            return 0

    @staticmethod
    def is_first_str_version_equal_or_greater(first_str_version: str, second_str_version: str) -> bool:
        major_1, minor_1, fix_1, stage_type_1, stage_value_1 = list(Update.split_version1(first_str_version))
        major_2, minor_2, fix_2, stage_type_2, stage_value_2 = list(Update.split_version1(second_str_version))
        if major_1 > major_2:
            return True
        elif major_1 == major_2:
            if minor_1 > minor_2:
                return True
            elif minor_1 == minor_2:
                if fix_1 > fix_2:
                    return True
                elif fix_1 == fix_2:
                    stage_type_number_1 = Update.stage_number_from_type(stage_type_1)
                    stage_type_number_2 = Update.stage_number_from_type(stage_type_2)
                    if stage_type_number_1 > stage_type_number_2:
                        return True
                    elif stage_type_number_1 == stage_type_number_2:
                        if stage_value_1 >= stage_value_2:
                            return True
        return False

    @staticmethod
    def extract_version(file, version_key="__minimum_firmware_version") -> (str, str, str, str):
        if file.suffix == Update.__UPDATE_FILE_EXTENSION:
            # Check file integrity of the zip file (It simply must contains bnote_start.py to be ok)
            try:
                update_zip_file = zipfile.ZipFile(file, 'r')
                info_list = update_zip_file.infolist()
                for zip_info in info_list:
                    if zip_info.filename == "bnote/__init__.py":
                        extracted_file = update_zip_file.extract(zip_info, path=FileManager.get_tmp_path())
                        if extracted_file is not None:
                            if Path(extracted_file).exists():
                                with open(extracted_file, 'r') as version_file:
                                    lines = version_file.readlines()
                                    for line in lines:
                                        if line.strip().find(version_key) == 0:
                                            raw_version = line.strip().split('=')
                                            update_zip_file.close()
                                            return "=".join(raw_version[1:])
                update_zip_file.close()
            except zipfile.BadZipfile as e:
                log.warning("Error {}".format(e))
            except OSError as e:
                log.warning("Error {}".format(e))

            return ""

    """
    -> major value, minor value, fix value, stage type, stage value
    """
    @staticmethod
    def split_version1(raw_version_string) -> (int, int, int, str, int):
#        pattern = r"^(?P<major>\d+)?\.?(?P<minor>\d+)?\.?(?P<fix>\d+)?-?(?P<stage_type>alpha|beta|rc)?\.?(?P<stage_value>\d+)?.*"
        pattern = r"^(?P<major>\d+)?\.?(?P<minor>\d+)?\.?(?P<fix>\d+)?-?(?P<stage_type>[a-zA-Z]*)?\.?(?P<stage_value>\d+)?.*"
        match = re.match(pattern, raw_version_string)
        major = minor = fix = stage_value = 0
        stage_type = ""
        if match:
            # print(f"{match}")
            # print(f"{match.groupdict()=}")
            # print(f"{match.group('major')=}-{match.group('minor')=}-{match.group('fix')=}")
            if 'major' in match.groupdict().keys() and match.group('major'):
                major = int(match.group('major'))
            if 'minor' in match.groupdict().keys() and match.group('minor'):
                minor = int(match.group('minor'))
            if 'fix' in match.groupdict().keys() and match.group('fix'):
                fix = int(match.group('fix'))
            if 'stage_type' in match.groupdict().keys() and match.group('stage_type'):
                stage_type = match.group('stage_type')
                if 'stage_value' in match.groupdict().keys() and match.group('stage_value'):
                    stage_value = int(match.group('stage_value'))
        print(f"{raw_version_string}->{major}, {minor}, {fix}, {stage_type}, {stage_value}")
        return major, minor, fix, stage_type, stage_value

    @staticmethod
    def install(file):
        # Install only on the RPi
        # if str(Path.home()) != "/home/pi":
        #     log.error("Not a RPi")
        #     return False

        if not os.path.exists(file):
            log.warning("file {} does not exist".format(file))
            return False

        try:
            # Open the zip archive file
            __zip_file = zipfile.ZipFile(file, 'r')
            name_list = __zip_file.namelist()
            # The update file must be an archive with bnote_start.py inside.
            if "bnote_start.py" in name_list:
                log.info("OK")
                FileManager.delete_file(Update.__sources_path, move_to_trash=False)
                if not Update.__sources_path.exists():
                    FileManager.create_folder(Update.__sources_path)

                __zip_file.extractall(Update.__sources_path)

                # Move the documentation.
                Update.move_documentation()
                return True
            else:
                log.warning("bnote_start.py not in archive...")
                log.warning("name_list={}".format(name_list))
                return False
        except zipfile.BadZipfile as e:
            log.warning("Error {}".format(e))
            return False
        except OSError as e:
            log.warning("Error {}".format(e))
            return False

        return False

    @staticmethod
    def move_documentation():
        # The folder extracted from the .update zip file (located in /hom/pi/bnote/bnote-documents)
        documentation_src_path = Update.__sources_path / Path("bnote-documents")
        if documentation_src_path.exists():
            # The folder "/home/pi/.bnote/note-documents
            documentation_dst_path = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER)

            # Copy the files (and folders)
            shutil.copytree(documentation_src_path, documentation_dst_path, ignore=ignore_existing_file,
                            dirs_exist_ok=True)

            # Delete permanently the source folder.
            FileManager.delete_file(Update.__sources_path / Path("bnote-documents"), move_to_trash=False)


def ignore_existing_file(folder, files):
    # log.error(f"{folder=}, {files=}")
    ignore_files = []
    documentation_src_path = Update.get_sources_path() / Path("bnote-documents")
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
