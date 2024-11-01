"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from bnote.apps.fman.file_manager import FileManager, BNOTE_FOLDER, DOCUMENTS_FOLDER
from bnote.stm32.braille_device_characteristics import braille_device_characteristics
import os
import zipfile
import subprocess
from urllib.request import urlretrieve
from pathlib import Path
import shutil
import re
import tomllib
import threading
import requests
from bnote.tools.settings import Settings
import pkg_resources


from bnote.debug.colored_log import ColoredLogger, YAUPDATER_LOG

log = ColoredLogger(__name__)
log.setLevel(YAUPDATER_LOG)

# UPDATE_FOLDER_URL = 'https://update.eurobraille.fr/radio/download/bnote/bnote3.x.x/bnote3.0.5_next'
UPDATE_FOLDER_URL = Settings().data['update']['search_update_to']
INSTALL_FOLDER = Path("/home/pi/all_bnotes")

def test_new_source(source) -> bool:
    """
    Return True if the link is a valid source.
    :param source: the link to test.
    :return: Boolean
    """
    response = requests.get(source)
    if response.status_code == 200 and "bnote" in source:
        return True
    return False

def change_update_source():
    global UPDATE_FOLDER_URL
    UPDATE_FOLDER_URL = Settings().data['update']['search_update_to']

class YAUpdater:
    __WHL_ZIP_EXTENSION = ".whl.zip"
    __WHL_EXTENSION = ".whl"
    if not INSTALL_FOLDER.exists():
        try:
            Path.mkdir(INSTALL_FOLDER)
        except OSError as e:
            log.error(f"EXCEPTION Path.mkdir({INSTALL_FOLDER}) : e={e}")

    def __init__(self, file, extract_path=None, refresh_call_back=None, ended_call_back=None):
        self.extract_path = INSTALL_FOLDER if extract_path is None else extract_path
        self.refresh_call_back = refresh_call_back
        self.ended_call_back = ended_call_back
        # Launch yaupdater thread and return from init without waiting.
        self.start_thread(file)

    def start_thread(self, file):
        thread = threading.Thread(target=self._install_thread, args=(file, ))
        thread.start()

    @staticmethod
    def get_version(file) -> str:
        """
        Return the version of a whl.zip file
        """
        file = Path(file)
        version = ""
        bnote_whl_file = None
        # Must be a .zip file
        if file.is_file() and str(file).endswith(YAUpdater.__WHL_ZIP_EXTENSION):
            try:
                if zipfile.is_zipfile(file):
                    with zipfile.ZipFile(file, 'r') as archive:
                        for zip_file in archive.namelist():
                            if zip_file.startswith('bnote-') and zip_file.endswith(YAUpdater.__WHL_EXTENSION):
                                bnote_whl_file = Path(zip_file)
                                break
                    if bnote_whl_file:
                        log.error(f"{bnote_whl_file.stem=}")
                        # DP FIXME La version retournée est celle du nom de fichier, on pourrait aller chercher le fichier file.distinfo/METADATA ligne version=
                        pattern_version = r'bnote-(?P<version>\d+\.\d+\.\d+((a|b|rc)\d+)?)-py3-none-any'
                        match = re.match(pattern_version, str(bnote_whl_file.stem))
                        if match:
                            if 'version' in match.groupdict().keys() and match.group('version'):
                                version = match.group('version')
                                log.error(f"{version=}")
            except zipfile.BadZipfile as e:
                log.error(f"{file=}, {e}")
        return bnote_whl_file, version

    def download_update(self, download_url):
        # print(f"download_update {download_url=}")
        # Download the file from the download url (or get local file if start with "file:///")
        try:
            if self.refresh_call_back:
                self.refresh_call_back(_("download in progress..."))
            download_url = str(download_url)
            # print(f"{download_url.split('/')=}")
            filename = "/tmp/" + download_url.split("/")[-1]
            local_filename, headers = urlretrieve(download_url, filename=filename)
            # print(f"local_filename: {local_filename=}")
            # print(f"headers: {headers=}")
            return Path(local_filename)
        except:
            log.error(f"EXCEPTION download_update {download_url=}")

        return Path()

    def __extract_file(self, zip_file, file_name, write_filename):
        try:
            with zip_file.open(file_name) as file_in_zip:
                contains = file_in_zip.read()
            with open(str(write_filename), 'wb') as file_to_write:
                file_to_write.write(contains)
        except (IOError, OSError, PermissionError, FileNotFoundError) as e:
            log.error(f"open or write error on file : {e}")


    def extract_to_working_directory(self, archive_path, working_directory) -> bool:
        """
        Extract .whl file and __main__.py to working directory.
        """
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for file_name in zip_file.namelist():
                    if (file_name.startswith('bnote-') and file_name.endswith(YAUpdater.__WHL_EXTENSION)) or file_name.endswith('.py'):
                        write_filename = Path(Path(working_directory) / Path(file_name).name)
                        # Extract the file.
                        self.__extract_file(zip_file, file_name, write_filename)
                return True
        except zipfile.BadZipfile:
            log.error(f"Bad zip file {archive_path=}")
            if self.refresh_call_back:
                self.refresh_call_back(_(f"error: bad zip file {archive_path=}"))
                return False
        except KeyError:
            log.error(f"no file libraries.txt found in {archive_path=}")
            if self.refresh_call_back:
                self.refresh_call_back(_(f"no file libraries.txt found in {archive_path=}"))
                return False

    def extract_whl_folder(self, archive_path) -> bool:
        """
        Extract whl folder and add file to whl folder of sdcard.
        """
        try:
            with (zipfile.ZipFile(archive_path, 'r') as zip_file):
                log.error(f"{zip_file.namelist()=}")
                for file_name in zip_file.namelist():
                    file_path = Path(file_name).parts
                    if (len(file_path) > 1) and (file_path[-2] == 'whl' or file_path[-2] == 'zip'):
                        write_filename = Path(Path('/home/pi/whl') / Path(file_name).name)
                        # Extract the file.
                        self.__extract_file(zip_file, file_name, write_filename)
                return True
        except zipfile.BadZipfile:
            log.error(f"Bad zip file {archive_path=}")
            if self.refresh_call_back:
                self.refresh_call_back(_(f"error: bad zip file {archive_path=}"))
                return False
        except KeyError:
            log.error(f"No file libraries.txt found in {archive_path=}")
            if self.refresh_call_back:
                self.refresh_call_back(_(f"no file libraries.txt found in {archive_path=}"))
                return False

    def get_libraries_txt_file(self, archive_path):
        commands = []
        try:
            with (zipfile.ZipFile(archive_path) as zip_file):
                # files = zip_file.namelist()
                # log.error(f"{files=}")
                with zip_file.open('libraries.txt') as readfile:
                    data = readfile.read()
                    lines = data.splitlines()
                    # convert b"..." to string.
                    for line in lines:
                        commands.append(line.decode('utf-8').strip())
        except zipfile.BadZipfile:
            log.error(f"Bad zip file {archive_path=}")
        except KeyError:
            log.error(f"No file libraries.txt found in {archive_path=}")
        return commands

    def _install_bnote(self, archive_path, working_directory) -> bool:
        log.info(f"install_dependencies {working_directory=}")
        if not archive_path and len(archive_path) == 0:
            if self.refresh_call_back:
                self.refresh_call_back(_("error: no .whl file in update"))
            return False
        if self.refresh_call_back:
            self.refresh_call_back(_("install packages..."))
        command_lines = [
            "python -m venv venv",
            f"venv/bin/pip install  --no-index --find-links ~/whl {archive_path}",
        ]
        for command in command_lines:
            res = self._exec_command(working_directory, command)
            if not res:
                return False
        log.info(f"install_dependencies done")
        if self.refresh_call_back:
            self.refresh_call_back(_("install dependencies done"))
        return True

    def _install_thread(self, file):
        result = False
        # Download if needed
        if str(file).startswith("file://"):
            # juste pour éviter une copie dans /tmp quand le fichier est déja en local.
            archive_path = Path(file.removeprefix("file://"))
        else:
            archive_path = self.download_update(file)

        bnote_whl_file, version = self.get_version(archive_path)
        if version != "":
            if self.refresh_call_back:
                self.refresh_call_back(_("extract archive in progress..."))
            # Get the working_directory from the archive name ie when self.extract_path = "/home/pi/all_bnotes"
            working_directory = Path("/home/pi/all_bnotes/bnote-" + version)
            if working_directory.is_file():
                working_directory.unlink()
            if working_directory.exists() and working_directory.is_dir():
                shutil.rmtree(working_directory)
            working_directory.mkdir()
            # Extract whl folder and add file to whl folder of sdcard.
            if not self.extract_whl_folder(archive_path):
                return False
            # Extract .whl file and __main__.py to working directory.
            if not self.extract_to_working_directory(archive_path, working_directory):
                return False
            # Extract the archive into the self.extract_path folder
            command_lines = self.get_libraries_txt_file(archive_path)
            # # Install dependency and update the service if succeeded.
            if (self._upgrade_os(command_lines)
                    and self._install_bnote(Path(
                        working_directory / Path(bnote_whl_file.name)),
                        working_directory)):
                # Change bnote launched at startup.
                result = self.update_config_file(working_directory)
        # Inform caller.
        if self.ended_call_back:
            self.ended_call_back(result)

    @staticmethod
    def update_config_file(working_directory):
        # Pour mettre à jour le fichier de config su script:
        # pi@raspberrypi:~ $ cat start_bnote.sh
        # #!/bin/bash
        #
        # WORKING_DIRECTORY=$(cat /home/pi/working_directory.txt)
        #
        # cd $WORKING_DIRECTORY
        #
        # /home/pi/.local/bin/poetry install
        # /home/pi/.local/bin/poetry run bnote

        # Écrire le répertoire de travail dans un fichier
        with open("/home/pi/working_directory.txt", "w") as file:
            file.write(str(working_directory))
            return True
        return False

    @staticmethod
    def read_config_file():
        # Écrire le répertoire de travail dans un fichier
        with open("/home/pi/working_directory.txt", "r") as file:
            return file.read().strip()

    @staticmethod
    def get_version_from_pyproject_toml(pyproject_toml):
        pyproject_toml = Path(pyproject_toml)
        project_version = None
        # Check if file exists.
        if pyproject_toml.exists():
            try:
                # Read the file.
                with open(pyproject_toml, 'rb') as toml_file:
                    toml_data = tomllib.load(toml_file)

                # Extract projet version.
                try:
                    project_version = toml_data['project']['version']
                except KeyError:
                    pass
            except:
                pass
        return project_version

    @staticmethod
    def get_version_from_running_project(pyproject_toml):
        project_version = YAUpdater.get_version_from_pyproject_toml(pyproject_toml)
        if project_version is None:
            # Get version from bnote package.
            project_version = pkg_resources.get_distribution('bnote').version
        print(f"{project_version=}")
        return project_version

    def _upgrade_os(self, command_lines):
        """
        Execute a set of command lines to upgrade os.
        :return: True if all command done successfully
        """
        if self.refresh_call_back:
            self.refresh_call_back(_("linux os update"))
        res = self._exec_commands(command_lines)
        if self.refresh_call_back and res:
            self.refresh_call_back(_("linux os updates done"))
        return res

    def _exec_command(self, working_directory, command):
        # Command.
        command_list = command.split()
        # Copie de l'environnement actuel.
        env = os.environ.copy()
        env['DEBIAN_FRONTEND'] = 'noninteractive'
        # Execute command with folder as working directory.
        process = subprocess.Popen(command_list, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        # Wait execution.
        output, error = process.communicate()
        # Display output.
        #print("Command output:", output.decode())
        if error:
            error_string = f"Erreur {command}:\n{error.decode()}"
            log.error(error_string)
            if self.refresh_call_back:
                self.refresh_call_back(_(f"Error: {error_string}"))
            return False
        return True

    def _exec_commands(self, command_lines):
        """
        Execute a set of command lines to upgrade os.
        :return: True if all command done successfully
        """
        if self.refresh_call_back:
            self.refresh_call_back(_("linux os update"))
        for command in command_lines:
            if len(command) == 0 or command.startswith('#'):
                continue
            commande = f"{command}"
            try:
                # Exécute la commande apt-get en mode capture
                resultat = subprocess.run(commande, shell=True, check=True, stderr=subprocess.PIPE)
                erreur = resultat.stderr.decode('utf-8').strip()
            except subprocess.CalledProcessError as e:
                erreur = f"Erreur {command}:\n{e.stderr.decode('utf-8').strip()}"
            if erreur and not (erreur.startswith("W: ")):
                log.error(f"Erreur: {erreur}")
                if self.refresh_call_back:
                    self.refresh_call_back(_(f"error: {erreur}"))
                return False
            else:
                log.info(f"{command} successfully done")
        if self.refresh_call_back:
            self.refresh_call_back(_("linux os updates done"))
        return True


class YAUpdaterFinder:
    def __init__(self, is_developer=False, ended=None):
        self.is_developer = is_developer
        self.files = None
        self.file_to_install = None
        self.version_to_install = None
        self.ended = ended
        self.start_finding()

    def start_finding(self):
        self.files = None
        self.file_to_install = None
        self.version_to_install = None
        thread = threading.Thread(target=self.__find_list_thread)
        thread.start()

    def __on_end_thread(self, files, version_to_install, file_to_install):
        self.files = files
        self.version_to_install = version_to_install
        self.file_to_install = file_to_install
        if self.ended:
            self.ended()

    def __find_list_thread(self):
        files = []
        version_to_install = 'up_to_date'
        file_to_install = None
        try:
            response = requests.get(UPDATE_FOLDER_URL)
            response.raise_for_status()
            releases = response.json()
            current_version = YAUpdater.get_version_from_running_project("pyproject.toml")

            file_link = None
            for release in releases:
                # Get the link only for the update
                for asset in release['assets']:
                    if asset['content_type'] == "application/zip":
                        file_link = asset['browser_download_url']
                if not file_link:
                    self.version_to_install = "failed"
                    return
                file_version = release['tag_name']
                if file_version.startswith('v'):
                    file_version = file_version[1:]
                if self.is_allowed_version(file_version):
                    files.append({'version': file_version, 'link': file_link})
                    if not self.is_first_str_version_greater_or_equal(current_version, file_version):
                        if file_to_install is None or not self.is_first_str_version_greater_or_equal(version_to_install,
                                                                                                     file_version):
                            version_to_install = file_version
                            file_to_install = file_link
        except requests.exceptions.RequestException as err:
            print(f"Request error: {err}")
            version_to_install = 'failed'
        finally:
            self.__on_end_thread(files, version_to_install, file_to_install)

    def is_allowed_version(self, version):
        """
        If developper mode not active, check if version is a released version (not a, b or rc).
        """
        if self.is_developer:
            return True
        else:
            major, minor, fix, stage_type, stage_value = list(YAUpdaterFinder.split_version1(version))
            return stage_type == ''

    @staticmethod
    def is_first_str_version_greater_or_equal(first_str_version: str, second_str_version: str) -> bool:
        """
        return True if first_str_version > second_str_version
        """
        major_1, minor_1, fix_1, stage_type_1, stage_value_1 = list(YAUpdaterFinder.split_version1(first_str_version))
        major_2, minor_2, fix_2, stage_type_2, stage_value_2 = list(YAUpdaterFinder.split_version1(second_str_version))
        if major_1 > major_2:
            return True
        elif major_1 == major_2:
            if minor_1 > minor_2:
                return True
            elif minor_1 == minor_2:
                if fix_1 > fix_2:
                    return True
                elif fix_1 == fix_2:
                    stage_type_number_1 = YAUpdaterFinder.stage_number_from_type(stage_type_1)
                    stage_type_number_2 = YAUpdaterFinder.stage_number_from_type(stage_type_2)
                    if stage_type_number_1 > stage_type_number_2:
                        return True
                    elif stage_type_number_1 == stage_type_number_2:
                        if stage_value_1 >= stage_value_2:
                            return True
        return False

    @staticmethod
    def split_version1(raw_version_string) -> (int, int, int, str, int):
        # on accepte ici 3.10.50a10 mais aussi 3.10.50-a10 ou 3.10.50a.10 ou 3.10.50-a.10
        pattern = r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<fix>\d+)(-?(?P<stage_type>[a-zA-Z]*)\.?(?P<stage_value>\d+))?.*"
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
        # print(f"{raw_version_string}->{major}, {minor}, {fix}, {stage_type}, {stage_value}")
        return major, minor, fix, stage_type, stage_value

    @staticmethod
    def stage_number_from_type(stage_type):
        types_1 = ('alpha', 'beta', 'rc')
        types_2 = ('a', 'b', 'rc')
        if stage_type == "":
            # Release version win 1 000 000.
            return 1000000
        elif stage_type in types_1:
            # Developers version between 1 and 3.
            return types_1.index(stage_type) + 1
        elif stage_type in types_2:
            # Developers version between 1 and 3.
            return types_2.index(stage_type) + 1
        else:
            # Others value are before alpha, beta and rc.
            return 0


class YAVersionFinder:

    @staticmethod
    def get_version_from_venv(venv_path):
        import subprocess

        package_name = 'bnote'
        result = subprocess.run(
            [f'{venv_path}/venv/bin/pip', 'show', package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            # Extract version
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split('Version: ')[1]
            return None
        else:
            return None

    @staticmethod
    def find_versions():
        """
        Find the list of executable version of bnote.
        :return: list of executable versions as
         {version_name: (folder, is_erasable), ...}
         as
         {"3.0.0b7(update)": ("/home/pi/all_bnotes/bnote3.0.0b7", True)}
        """
        # Find original version.
        original_folder = "/home/pi/bnote"
        version = YAVersionFinder.get_version_from_venv(original_folder)
        if version:
            list_of_versions = {version + "(original)": (Path(original_folder), False), }
        else:
            list_of_versions = {"bnote(original)": (Path(original_folder), False), }
        # Find developer version.
        developer_folder = Path("/home/pi/develop")
        if developer_folder.exists():
            for d in developer_folder.iterdir():
                if d.is_dir():
                    version = YAUpdater.get_version_from_running_project(Path(d) / Path('pyproject.toml'))
                    if version is None:
                        version = YAVersionFinder.get_version_from_venv(developer_folder)
                    list_of_versions[version + "(developer)"] = (d, False)
        # Find all bnotes version.
        all_bnote_folder = Path("/home/pi/all_bnotes")
        for d in all_bnote_folder.iterdir():
            if d.is_dir():
                parts = d.name.split('-')
                if (len(parts) != 2) or (parts[0] != 'bnote'):
                    # forget non-compliant name.
                    continue
                version = parts[1]
                if len(version) > 0:
                    list_of_versions[version + "(update)"] = (d, True)
        # Tag the current version.
        current_dir = Path(os.getcwd())
        old_version = old_path = None
        for version, value in list_of_versions.items():
            if value[0] == current_dir:
                old_version = version
                old_value = value
                break
        if old_version:
            # print(f"current version = {old_version}")
            del list_of_versions[old_version]
            list_of_versions['*' + old_version] = old_value
        return list_of_versions

    @staticmethod
    def remove_version(folder):
        # Remove new version when installation failed.
        shutil.rmtree(folder)
        return True
