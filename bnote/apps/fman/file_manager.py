"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import collections
import configparser
import datetime
import os.path
import shlex
import subprocess
from pathlib import Path
import re
import time
import shutil

from debug.colored_log import ColoredLogger, FILE_MANAGER_LOG
from typing import Union, List

# Set up the logger for this file
log = ColoredLogger(__name__)
log.setLevel(FILE_MANAGER_LOG)

BNOTE_FOLDER = Path.home() / Path(".bnote")

DOCUMENTS_FOLDER = "bnote-documents"
BACKUPS_FOLDER = "bnote-backups"
CRASH_REPORT_FOLDER = "bnote-crash"
EXAM_FOLDER="bnote-examen"


class FileManager:

    # The .bnote path where all other folders will be created
    if not BNOTE_FOLDER.exists():
        try:
            log.info("call Path.mkdir({})".format(BNOTE_FOLDER))
            Path.mkdir(BNOTE_FOLDER)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(BNOTE_FOLDER, e))

    # The root path where all user documents will be saved
    __root_path = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER)
    if not __root_path.exists():
        try:
            log.info("call Path.mkdir({})".format(__root_path))
            Path.mkdir(__root_path)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__root_path, e))

    __usb_flash_drive_path = __root_path / Path("usb_flash_drive")
    # Add a symlink to /media, thus the user can access to his usb flash drive files.
    if not __usb_flash_drive_path.exists():
        log.info("call os.symlink(\"/media\", str({}), target_is_directory=True)".format(__usb_flash_drive_path))
        os.symlink("/media", str(__usb_flash_drive_path), target_is_directory=True)

    # The path used for temporary zipped file send to bluetooth
    __tmp_path = BNOTE_FOLDER / Path("tmp")
    if not __tmp_path.exists():
        try:
            log.info("call os.mkdir({})".format(__tmp_path))
            Path.mkdir(__tmp_path)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__tmp_path, e))

    # The real folder with the backup file
    __real_backup_path = BNOTE_FOLDER / Path(BACKUPS_FOLDER)
    if not __real_backup_path.exists():
        try:
            log.info("call Path.mkdir({})".format(__real_backup_path))
            Path.mkdir(__real_backup_path)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__real_backup_path, e))

    # symlink to backup folder will be in __root_path
    __backup_path = __root_path / Path("backup")
    if not __backup_path.exists():
        log.info("call os.symlink(str({}), str({}), target_is_directory=True)".format(__real_backup_path, __backup_path))
        os.symlink(str(__real_backup_path), str(__backup_path), target_is_directory=True)

    # The symlink to the real /bluetooth folder will be in __root_path
    __bluetooth_path = __root_path / Path("bluetooth")
    # Add a symlink to /bluetooth, thus the user can access to his transfered files.
    if not __bluetooth_path.exists():
        # FIXME : Il faut créer le dossier /bluetooth s'il n'existe pas mais avant vérifier
        #  qui doit avoir les droits et s'il ne faut pas qu'il soit créé par les outil Bluetoot eux même au moment
        #  de l'installation...
        log.info("call os.symlink(\"/bluetooth\", str({}), target_is_directory=True)".format(__bluetooth_path))
        os.symlink("/bluetooth", str(__bluetooth_path), target_is_directory=True)

    # The real folder with the crash file
    __real_crash_path = BNOTE_FOLDER / Path(CRASH_REPORT_FOLDER)
    if not __real_crash_path.exists():
        try:
            log.info("call Path.mkdir({})".format(__real_crash_path))
            Path.mkdir(__real_crash_path)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__real_crash_path, e))

    # symlink to crash folder will be in __root_path
    __crash_path = __root_path / Path("crash")
    if not __crash_path.exists():
        log.info("call os.symlink(str({}), str({}), target_is_directory=True)".format(__real_crash_path, __crash_path))
        os.symlink(str(__real_crash_path), str(__crash_path), target_is_directory=True)

    # The real folder with the examen file
    __real_examen_path = BNOTE_FOLDER / Path(EXAM_FOLDER)
    if not __real_examen_path.exists():
        try:
            log.info("call Path.mkdir({})".format(__real_examen_path))
            Path.mkdir(__real_examen_path)
        except OSError as e:
            log.warning("EXCEPTION Path.mkdir({}) : e={}".format(__real_examen_path, e))

    # symlink to examen folder will be in __root_path
    __examen_path = __root_path / Path("examen")
    if not __examen_path.exists():
        log.info(
            "call os.symlink(str({}), str({}), target_is_directory=True)".format(__real_examen_path, __examen_path))
        os.symlink(str(__real_examen_path), str(__examen_path), target_is_directory=True)

    log.info("All folders and symlink created in FileManager...")


    @classmethod
    def get_root_path(cls) -> Path:
        return cls.__root_path

    @classmethod
    def get_usb_flash_drive_path(cls) -> Path:
        return cls.__usb_flash_drive_path

    @classmethod
    def get_tmp_path(cls) -> Path:
        return cls.__tmp_path

    @classmethod
    def get_bluetooth_path(cls) -> Path:
        return cls.__bluetooth_path

    @classmethod
    def get_backup_path(cls) -> Path:
        return cls.__backup_path

    @classmethod
    def get_examen_path(cls) -> Path:
        return cls.__examen_path

    @classmethod
    def get_crash_path(cls) -> Path:
        return cls.__crash_path

    @staticmethod
    def umount_safely_usb_flash_drive(path) -> bool:
        try:
            # log.error(f"{path=}")
            if path.relative_to(FileManager.get_usb_flash_drive_path()):
                mount_point = path
                if path.parent != FileManager.get_usb_flash_drive_path():
                    # log.error(f"{path.parents=}")
                    # log.error(f"{len(path.parents)=}")
                    # for p in path.parents:
                    #     log.error(f"{p=}")
                    for index in range(0, len(path.parents)):
                        # log.error(f"{index=} {path.parents[index]=}")
                        if path.parents[index] == FileManager.get_usb_flash_drive_path():
                            mount_point = path.parents[index - 1]
                            break
                # log.error(f"{mount_point=}")
                # umount
                command_line = "sudo umount {}".format(str(mount_point))
                args = shlex.split(command_line)
                x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                x.wait()
                umount_results = x.stderr.read().decode("utf-8")
                # log.error(f"{umount_results=}")

                # Si le dossier est occupé (exemeple: on vient de lister le contenu de la clef en ssh)
                # umount_results='umount: /home/pi/.bnote/bnote-documents/usb_flash_drive/BOULOT: target is busy.\n'
                # Si pas le sudo on obtient
                # umount_results = 'umount: /media/BOULOT: umount failed: Opération non permise.\n'
                # Si la clef n'est pas montée et que le dossier existe (suite à un crash et un reboot)
                # umount_results = 'umount: /media/BOULOT: not mounted.\n'

                if umount_results == "" or umount_results.find("not mounted") != -1:
                    command_line = "sudo rmdir {}".format(str(mount_point))
                    args = shlex.split(command_line)
                    x = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    x.wait()
                    return True
        except ValueError as err:
            log.debug(f"{err=}")
            pass

        log.debug(" Return False !!!!!!!!!!!!!!!")
        return False

# Return the list of the filenames for path (alpha sorted with folder first) or None if path does not exits.
    # See https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod
    @staticmethod
    def listdir(path, hide_hidden_file=True):
        if isinstance(path, str):
            path = Path(path)

        if path.exists():
            all_files = path.glob("*")

            file_list = []
            folder_list = []

            for file in all_files:
                if not hide_hidden_file or (hide_hidden_file and not file.name.startswith('.')):
                    if file.is_dir():
                        folder_list.append(file.name)
                    elif file.is_file():
                        file_list.append(file.name)

            log.debug("file_list={}".format(file_list))
            log.debug("folder_list={}".format(folder_list))

            # The 2 lists will be alphanumerically sorted.
            file_list = FileManager.sorted_alphanumeric(file_list)
            folder_list = FileManager.sorted_alphanumeric(folder_list)

            # Folders first and then files.
            sorted_file_and_folder_list = folder_list + file_list

            log.debug("sorted_file_and_folder_list={}".format(sorted_file_and_folder_list))
            log.debug("len(sorted_file_and_folder_list)={}".format(len(sorted_file_and_folder_list)))
            sorted_file_and_folder_path = []
            for txt in sorted_file_and_folder_list:
                sorted_file_and_folder_path.append(path / txt)
            log.debug(f"sorted_file_and_folder_path={sorted_file_and_folder_path}")

            return sorted_file_and_folder_path

    # See discussion https://stackoverflow.com/questions/4813061/non-alphanumeric-list-order-from-os-listdir
    @staticmethod
    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    # Create the file name. It can be relative to self.__current_path or absolute
    # Return True if success, False if error or None if the file already exits
    @staticmethod
    def create_file(name, test_existing=True):
        if isinstance(name, str):
            name = Path(name)

        if test_existing and name.exists():
            return None

        try:
            with name.open(mode="w+"):
                return True
        except IOError:
            pass

        return False

    # Create the folder path.
    # Return True if success, False if error (if we try to create more than 2 new folders levels)
    # or None if the folder already exits
    @staticmethod
    def create_folder(path):
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            try:
                path.mkdir()
                return True
            except IOError:
                return False

        return None

    @staticmethod
    def delete_file(name, move_to_trash=True):
        log.info("name={}".format(name))
        if isinstance(name, str):
            name = Path(name)

        if not name.exists():
            return False

        if str(name).startswith(str(FileManager.get_bluetooth_path())):
            real_name = name.resolve()
            # Use the shell to make the delete the file in bluetooth folder (root access)
            os.popen("sudo rm \"{}\"".format(str(real_name)))
            time.sleep(0.5)
            return True

        # if move_to_trash and not name.startswith(Trash.get_trash_path()):
        if move_to_trash and not str(name).startswith(str(Trash.get_trash_path())):
            if name.is_file():
                if Trash.move_to_trash(name):
                    # delete the hidden associated file
                    # head, tail = os.path.split(name)
                    hidden_filename = name.parent / "".join((".", name.name))
                    log.info("hidden_filename={}".format(hidden_filename))
                    if hidden_filename.exists():
                        return Trash.move_to_trash(hidden_filename)
                    else:
                        return True
                else:
                    return False
            # Trash a folder
            return Trash.move_to_trash(name)

        # Delete permanently
        return Trash.delete(name)

    @staticmethod
    def copy(src, dst, dirs_exist_ok=False):
        if isinstance(src, str):
            src = Path(src)
        if isinstance(dst, str):
            dst = Path(dst)

        real_src = src.resolve()
        real_dst = dst.resolve()
        return_dst = None
        if real_src.exists():
            # If user copy the file on itself we create a copy of the file with the generic_pattern
            if str(real_src) == str(real_dst):
                real_dst = FileManager.create_generic_filename(real_dst, _("({})"))
                if real_dst is None:
                    return
                log.info("new real_dst created={}".format(real_dst))

            if real_src.is_dir():
                try:
                    # Use the shell to make the copy of the folder
                    return_dst = shutil.copytree(str(real_src), str(real_dst), dirs_exist_ok=dirs_exist_ok)
                    log.info("{} copytree to {}".format(str(real_src), str(real_dst)))
                except PermissionError as error:
                    log.warning("PermissionError ={}".format(error))
                    pass
                except shutil.Error as err:
                    log.warning("Error in copytree ={}".format(err))
            else:
                try:
                    # Use the shell to make the copy of the file
                    return_dst = shutil.copy2(str(real_src), str(real_dst))
                    log.info("{} copy to {}".format(str(real_src), str(real_dst)))
                except PermissionError as error:
                    log.warning("PermissionError ={}".format(error))
                    pass
                except shutil.Error as err:
                    log.warning("Error in copytree ={}".format(err))
        if return_dst:
            return Path(return_dst)

    @staticmethod
    def move(src, dst, dirs_exist_ok=False):
        if isinstance(src, str):
            src = Path(src)
        if isinstance(dst, str):
            dst = Path(dst)

        real_src = src.resolve()
        real_dst = dst.resolve()

        return_dst = None
        # Ignore if real_src does not exists or if user ask to move file on itself.
        if real_src.exists() and str(real_src) != str(real_dst):
            if real_src.is_dir():
                # Use the shell to make the copy and remove of the file/folder
                try:
                    return_dst = shutil.copytree(str(real_src), str(real_dst), dirs_exist_ok=dirs_exist_ok)
                    shutil.rmtree(str(real_src))
                    log.info("{} copytree + rmtree to {}".format(str(real_src), str(real_dst)))
                except PermissionError as error:
                    log.warning("PermissionError in rmtree ={}".format(error))
                    pass
                except shutil.Error as err:
                    log.warning("Error in copytree + rmtree ={}".format(err))
            else:
                # Test if src (not real_src) start with the link to bluetooth (owner is root).
                # Remarque : sur la pi on ne peut pas avoir de dossier dans /bluetooth
                # car le pc n'envoie que des fichiers...
                if str(src).startswith(str(FileManager.get_bluetooth_path())):
                    # Use su to move files from bluetooth (owner is root)
                    # log.error("utilisation de sudo mv \"{}\" \"{}\"".format(real_src, real_dst))
                    # It works well on Rpi, but on PC only a copy is done (file remains in /bluetooth)
                    # PB on Rpi : sudo mv conserve les droits et on se retrouve avec un fichier appartenant à root.
                    # os.popen("sudo mv \"{}\" \"{}\"".format(real_src, real_dst))
                    log.info("shutil.copy2(\"{}\" \"{}\")".format(str(real_src), str(real_dst)))
                    # le fichier copié se retrouve avec pi:pi comme propriétaire.
                    return_dst = shutil.copy2(str(real_src), str(real_dst))
                    log.info("utilisation de sudo rm \"{}\"".format(str(real_src)))
                    os.popen("sudo rm \"{}\"".format(str(real_src)))
                else:
                    # Use the shell to make the move of the file
                    try:
                        return_dst = shutil.move(str(real_src), str(real_dst))
                        log.info("{} move to {}".format(str(real_src), str(real_dst)))
                    except PermissionError as error:
                        log.warning("PermissionError in move ={}".format(error))
                        log.warning("use shutil.copy2")
                        return_dst = shutil.copy2(str(real_src), str(real_dst))
                        pass
                    except shutil.Error as err:
                        log.warning("Error in move ={}".format(err))
        if return_dst:
            return Path(return_dst)

    @staticmethod
    def rename(filename, new_filename):
        if isinstance(filename, str):
            filename = Path(filename)

        if isinstance(new_filename, str):
            new_filename = Path(new_filename)

        if filename.exists() and not new_filename.exists():
            src = filename.resolve()
            dst = new_filename.resolve()

            if src.parent == dst.parent:
                try:
                    shutil.move(str(src), str(dst))
                    log.info("{} rename into {}".format(str(src), str(dst)))
                except shutil.Error as err:
                    log.warning("Error in rename ={}".format(err))

    @staticmethod
    def is_valid_filename(filename):
        if isinstance(filename, str):
            filename = Path(filename)

        # fm : Testé en dehors de la re, car je n'ai pas réussi à la coder correctement...
        if filename.name.find("/") != -1:
            return False

        # https://www.phonandroid.com/pourquoi-windows-10-interdit-dutiliser-certains-noms-de-fichiers-comme-aux-mp3-ou-con-jpg.html
        p = re.compile("[\\\:\?\*\"<>\|/]")
        if filename.name != "" and p.search(filename.name) is None:
            return True
        return False

    # Sample use :
    # FileManager file_manager
    # file_manager.create_generic_filename("/home/pi/toto.txt", _(" (copy {})")
    # will return "/home/pi/toto (copie 1).txt" for french language "if /home/pi/toto.txt" exists
    # or "/home/pi/toto (copie 2).txt" if "/home/pi/toto (copie 1).txt" also exist
    # etc until the counter reach 99
    # If i's not possible it return is None
    @staticmethod
    def create_generic_filename(base_name, generic_pattern):
        if isinstance(base_name, str):
            base_name = Path(base_name)

        filename = base_name
        index = 0
        while filename.exists():
            index += 1

            filename = filename.parent / (filename.stem + generic_pattern.format(index) + filename.suffix)
            if index == 100:
                return None

        return filename

    @staticmethod
    def file_to_unzip_already_exists(filename, to_path):
        if isinstance(filename, str):
            filename = Path(filename)

        if isinstance(to_path, str):
            to_path = Path(to_path)

        if to_path.exists():
            dst = to_path / filename
            if dst.exists():
                return True
            else:
                return False

        return False

    @staticmethod
    def files_and_folders_count(paths: Union[str, Path, List[str], List[Path]],
                                exclude_paths: Union[List[str], List[Path]] = [""]) -> int:
        count = 0

        # Convert into list
        if not isinstance(paths, collections.Iterable):
            paths = [paths]

        for path in paths:
            # Convert into Path
            path = Path(path)

            count += 1

            for item in path.glob("*"):
                if item not in exclude_paths:
                    if item.is_dir():
                        count += FileManager.files_and_folders_count(item, exclude_paths)
                        log.debug(f"{count=} {item=}")
                    elif item.is_file():
                        count += 1
                        log.debug(f"{count=} {item=}")

        log.debug(f"{count=} {paths=}")
        return count

    @staticmethod
    def clear_tmp_file():
        if len(FileManager.listdir(FileManager.get_tmp_path())):
            # Delete the tmp folder.
            FileManager.delete_file(FileManager.get_tmp_path(), move_to_trash=False)
            # Recreate the tmp folder
            try:
                log.warning("call os.mkdir({})".format(FileManager.get_tmp_path()))
                Path.mkdir(FileManager.get_tmp_path())
            except OSError as e:
                log.warning("EXCEPTION Path.mkdir({}) : e={}".format(FileManager.get_tmp_path(), e))


# Trash.__real_trash_path "/home/pi/bnote-trash" : Contient les 2 dossiers files et info
# Trash.__trash_files_path "/home/pi/bnote-trash/files" ; Contient les fichiers et dossier effacer (nom génériques
#                                                          créé si doublon)
# Trash.__trash_info_path "/home/pi/bnote-trash/info" : Contient les fichiers .trashinfo (avec info emplacement
#                                                        d'origine pour restaurer). Il y a 1 fichier pour chaque
#                                                        fichier/dossier directement enfant de Trash.__trash_files_path
#
class Trash:

    __TRASH_INFO_EXTENSION = ".trashinfo"
    __TRASH_FOLDER = "bnote-trash"

    __real_trash_path = BNOTE_FOLDER / __TRASH_FOLDER
    if not __real_trash_path.exists():
        try:
            __real_trash_path.mkdir()
        except OSError as e:
            log.warning("EXCEPTION os.mkdir({}) : e={}".format(__real_trash_path, e))

    __trash_files_path = __real_trash_path / "files"
    if not __trash_files_path.exists():
        try:
            __trash_files_path.mkdir()
        except OSError as e:
            log.warning("EXCEPTION os.mkdir({}) : e={}".format(__trash_files_path, e))

    __trash_info_path = __real_trash_path / "info"
    if not __trash_info_path.exists():
        try:
            __trash_info_path.mkdir()
        except OSError as e:
            log.warning("EXCEPTION os.mkdir({}) : e={}".format(__trash_info_path, e))

    # symlink to trash folder will be in __root_path
    __trash_path = FileManager.get_root_path() / "trash"
    if not __trash_path.exists():
        log.info("call os.symlink({}, {}, target_is_directory=True)".format(__real_trash_path, __trash_path))
        os.symlink(str(__trash_files_path), str(__trash_path), target_is_directory=True)

    @classmethod
    def get_trash_path(cls):
        return cls.__trash_path

    @classmethod
    def get_trash_info_path(cls):
        return cls.__trash_info_path

    @staticmethod
    def move_to_trash(filename):
        if isinstance(filename, str):
            filename = Path(filename)

        # Get the real path
        src = filename.resolve()

        if not src.is_symlink():
            try:
                file_in_trash = Trash.__trash_files_path / src.name
                if file_in_trash.exists():
                    file_in_trash = FileManager.create_generic_filename(file_in_trash, ".{}")

                # Move the src into the __trash_files_path
                file_in_trash = FileManager.move(src, file_in_trash)
                log.info("file_in_trash={}".format(file_in_trash))

                trash_info_filename = Trash.__trash_info_path / (file_in_trash.name + Trash.__TRASH_INFO_EXTENSION)
                log.info("trash_info_filename={}".format(trash_info_filename))

                # https: // deusyss.developpez.com / tutoriels / Python / les - modules - de - configuration /
                trash_info = configparser.ConfigParser()
                trash_info['Trash Info'] = {}
                trash_info['Trash Info']['Path'] = str(src)
                trash_info['Trash Info']['DeletionDate'] = str(datetime.datetime.now())
                # Create a trashinfo file in the __trash_info_path
                with open(trash_info_filename, 'w') as configfile:
                    trash_info.write(configfile)
                return True

            except IOError:
                return False

        return None

    @staticmethod
    def delete(name):
        if isinstance(name, str):
            name = Path(name)

        if name.is_file():
            try:
                os.remove(str(name))
                trash_info_file = Trash.__trash_info_path / (name.name + Trash.__TRASH_INFO_EXTENSION)
                if trash_info_file.exists():
                    os.remove(str(trash_info_file))

                # delete the hidden associated file
                hidden_filename = name.parent / ("." + name.name)
                log.info("hidden_filename={}".format(hidden_filename))
                if hidden_filename.exists():
                    os.remove(str(hidden_filename))
                    trash_info_file = Trash.__trash_info_path / (hidden_filename.name + Trash.__TRASH_INFO_EXTENSION)
                    if trash_info_file.exists():
                        os.remove(str(trash_info_file))
                return True
            except IOError:
                return False
        if name.is_dir() and not name.is_symlink():
            try:
                shutil.rmtree(str(name))
                trash_info_file = Trash.__trash_info_path / (name.name + Trash.__TRASH_INFO_EXTENSION)
                if trash_info_file.exists():
                    os.remove(str(trash_info_file))

                return True
            except OSError as error:
                log.warning("OSError={}".format(error))
                return False

    @staticmethod
    def empty_the_trash():
        files = FileManager.listdir(Trash.get_trash_path())
        for file in files:
            Trash.delete(file)

    @staticmethod
    def original_file(file):
        trash_info = configparser.ConfigParser()
        relative_file = str(file).replace(str(Trash.get_trash_path()) + os.path.sep, "")
        relative_path = os.path.dirname(relative_file)

        # top level entry of Trash.get_trash_path()
        if not relative_path:
            trash_info.read(Trash.trash_info_file(file))
            try:
                original_path = trash_info['Trash Info']['path']
            except KeyError:
                log.warning("KeyError exception !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                original_path = os.path.basename(file)
                pass
        # inside a Trash.get_trash_path() sub folder
        else:
            trash_info.read(Trash.trash_info_file(file))
            try:
                original_path = os.path.join(trash_info['Trash Info']['path'],
                                             relative_file[relative_file.find(os.path.sep) + 1:])
            except KeyError:
                original_path = os.path.basename(file)
                pass

        log.info("original_path={}".format(original_path))
        return Path(original_path)

    @staticmethod
    def deletion_date(file):
        trash_info = configparser.ConfigParser()
        trash_info.read(Trash.trash_info_file(file))
        deletion_date_str = ""
        try:
            deletion_date_str = trash_info['Trash Info']['DeletionDate']
        except KeyError:
            log.warning("KeyError exception !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            pass

        log.info("deletion_date_str={}".format(deletion_date_str))
        # from https://stackabuse.com/converting-strings-to-datetime-in-python/
        return datetime.datetime.strptime(deletion_date_str, '%Y-%m-%d %H:%M:%S.%f')

    @staticmethod
    def trash_info_file(file):
        if file.parent.samefile(Trash.get_trash_path()):
            return Trash.get_trash_info_path() / (file.name + Trash.__TRASH_INFO_EXTENSION)
        else:
            relative_dir_name = str(file.parent).replace(str(Trash.get_trash_path()) + os.path.sep, "")
            trash_info_basename = Path(relative_dir_name).parts[0]
            return Trash.get_trash_info_path() / (trash_info_basename + Trash.__TRASH_INFO_EXTENSION)
