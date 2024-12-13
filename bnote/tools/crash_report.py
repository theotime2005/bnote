"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from bnote.stm32.braille_device_characteristics import braille_device_characteristics
from bnote.apps.fman.file_manager import FileManager
import bnote.__init__ as version
from datetime import datetime
from pathlib import Path
import re
import sys
import traceback

from bnote.debug.colored_log import ColoredLogger, CLIPBOARD_LOG

log = ColoredLogger(__name__)
log.setLevel(CLIPBOARD_LOG)

REPORT_A_CRASH = FileManager.get_tmp_path() / Path("report_a_crash")


def crash_encountered() -> bool:
    if REPORT_A_CRASH.exists():
        REPORT_A_CRASH.unlink()
        return True

    return False


def generate_report():
    except_type, exception_value, tb = sys.exc_info()

    # La date et l'heure sera utilisé dans le nom du fichier.
    now = datetime.now()
    date_time = "{}-{}-{} {}h{}m{}s".format(
        now.year,
        f"{now.month:02d}",
        f"{now.day:02d}",
        f"{now.hour:02d}",
        f"{now.minute:02d}",
        f"{now.second:02d}",
    )

    # Ce fichier sera effacé
    raw_crash_file_name = "raw_crash {}.txt".format(date_time)
    # Ce fichier sera conservé
    crash_file_name = FileManager.get_crash_path() / Path(
        "crash {}.txt".format(date_time)
    )

    __sdcard_version = "unknown"
    if (Path().home() / Path("sdcard_version")).exists():
        with open(Path().home() / Path("sdcard_version"), "r") as f:
            __sdcard_version = f.readline()

    # Sauvegarde la stack trace dans un fichier.
    with open(raw_crash_file_name, "w") as crash_report_file:
        traceback.print_tb(tb, file=crash_report_file)

    # Ajoute des infos et modifie les lignes pour masquer une partie du chemin des fichiers python
    # pour une meilleure lisibilité.
    with open(raw_crash_file_name, "r") as crash_report_file:
        with open(crash_file_name, "w") as crash_report_file_ok:
            lines = crash_report_file.readlines()

            header_lines = [
                "date={}\n".format(date_time),
                "applications={}\n".format(version.__version__),
                "firmware={}\n".format(
                    braille_device_characteristics.get_firmware_version()
                ),
                "sdcard={}\n".format(__sdcard_version),
                "serial={}\n".format(
                    braille_device_characteristics.get_serial_number()
                ),
                "exception type={}\n".format(except_type),
                "exception value={}\n".format(exception_value),
            ]
            crash_report_file_ok.writelines(header_lines)

            # recherche la partie de chemin avant "/bnote/"
            hide_bnote_path_pattern = re.compile("  (File .*/bnote/).*")

            for line in lines:
                m = hide_bnote_path_pattern.match(line)
                print(line)
                print(m)
                if m is not None:
                    line = line.replace(m[1], "File ")
                crash_report_file_ok.write(line)

    Path.unlink(Path(raw_crash_file_name))

    with open(REPORT_A_CRASH, "w") as report_a_crash:
        report_a_crash.write("report it...")


if __name__ == "__main__":
    try:
        a = 1 / 0
    except ZeroDivisionError:
        generate_report()
