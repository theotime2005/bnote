"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import os
import subprocess
import threading

# To be able to download files from Eole, the swap must be increases to 1000Mo (instead of the original size of 100Mo)
SWAP_FILE_SIZE = 1000


def do_update_swap_file():
    try:
        # print(f"call update_swap_size")
        update_swap_size(SWAP_FILE_SIZE)
    except Exception as e:
        print(f"{e=}")
        pass


# Update the swap size to wanted_size.
def update_swap_size(wanted_size):
    if update_swap_size_in_conf_file(wanted_size):
        # Call in a thread "_thread_cleanup" with 1 as name argument.
        x = threading.Thread(target=thread_update_swap_file)
        x.start()
    else:
        print(f"swapfile is already up to date")


def thread_update_swap_file():
    print(f"sudo dphys-swapfile swapoff")
    os.system("sudo dphys-swapfile swapoff")
    print(f"sudo dphys-swapfile setup")
    os.system("sudo dphys-swapfile setup")
    print(f"sudo dphys-swapfile swapon")
    os.system("sudo dphys-swapfile swapon")


# Update the conf swap file to the new size and return True is the size was modified.
def update_swap_size_in_conf_file(new_size_mb) -> bool:
    file_modified = False
    # Chemin vers le fichier de configuration du swap
    swapfile_path = "/etc/dphys-swapfile"

    # Lecture du contenu du fichier de configuration du swap
    with open(swapfile_path, "r") as file:
        lines = file.readlines()

    # print(f"{lines=}")

    # Recherche de la ligne spécifiant la taille du swap
    for i, line in enumerate(lines):
        if line.startswith("CONF_SWAPSIZE="):
            if line != f"CONF_SWAPSIZE={new_size_mb}\n":
                lines[i] = f"CONF_SWAPSIZE={new_size_mb}\n"
                file_modified = True
            break

    # print(f"{file_modified=}")
    # print(f"{lines=}")
    if file_modified:
        # Écriture des modifications dans le fichier de configuration du swap
        write_file_with_sudo(swapfile_path, lines)

    # print(f"{file_modified=}")
    return file_modified


def write_file_with_sudo(file_path, lines):
    # Création de la commande pour écrire dans le fichier avec sudo
    command = ["sudo", "tee", file_path]

    # Ouverture d'un processus avec sudo et écriture des lignes dans le fichier
    with subprocess.Popen(command, stdin=subprocess.PIPE) as proc:
        proc.communicate(input="".join(lines).encode())
