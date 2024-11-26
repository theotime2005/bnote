import json
import os
from datetime import datetime
from pathlib import Path

from bnote.stm32.braille_device_characteristics import braille_device_characteristics


BNOTE_FOLDER = Path.home() / Path(".bnote")
FILE_NAME = "examen.json"
FILE_PATH = BNOTE_FOLDER / Path(FILE_NAME)


class Examen:
    def __init__(self):
        self.data = dict()
        self.isActive = False
        # Check if file exists
        if FILE_NAME in os.listdir(BNOTE_FOLDER):
            self.isActive = True
            self.load_file()

    def load_file(self):
        try:
            with open(FILE_PATH, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.isActive = False

    def save(self):
        with open(FILE_PATH, 'w') as file:
            json.dump(self.data, file)
        # Remove folder
        os.remove(BNOTE_FOLDER / Path("bnote-exam") / "*")

    def compare_passwords(self, password) -> bool:
        """
        Compare passwords
        :param password: str
        :return: bool
        """
        p1, p2 = self.data['password'], password
        return p1 == p2

    def deactivate(self):
        os.remove(FILE_PATH)

class FileExam:
    def __init__(self, file, function, function_cancel):
        self.data = dict()
        # Done
        self.function = function
        # Open file
        with open(file, 'r') as f:
            self.data = json.load(f)
        try:
            if self.data['action'] == "activate":
                self.activate_examen_mode()
            elif self.data['action'] == "desactivate":
                self.desactivate_examen_mode()
            else:
                self.function_cancel(_("File is corrupted"))
        except Exception as e:
            self.function_cancel(_("File is corrupted"))

    def activate_examen_mode(self):
        """
        Activate examen mode
        """
        try:
            # The file generation doesn't exceded 4h
            generate_date = datetime.strptime(self.data['generate_date'], "%Y-%m-%d %H:%M")
            actual_date = datetime.now()
            if actual_date.year != generate_date.year or actual_date.month != generate_date.month or actual_date.day != generate_date.day:
                self.function_cancel(_("Date is expiered"))
                return
            if actual_date.hour - generate_date.hour > 4:
                self.function_cancel(_("Date is expiered"))
                return
            # check the integrity of file
            if not self.data.get('password', None):
                # Just notify that file is corrucpts not detail
                self.function_cancel(_("File is corrupted"))
                return
            # If editor is not active, math can not be activate
            if self.data['editor'] == False and self.data['math'] == True:
                self.function_cancel(_("Math can not be activated"))
                return
            exam_data = {
                "password": self.data['password'],
                "more_apps_menu": self.data['more_apps_menu'],
                "math": self.data['math'],
                "bluetooth": self.data['bluetooth'],
                "wifi": self.data['wifi'],
                "editor": self.data['editor']
            }
            # Remove folder content
            os.remove(BNOTE_FOLDER / Path("bnote-exam") / "*")
            # End
            self.function(exam_data)
        except Exception as e:
            self.function_cancel(_("File is corrupted"))

    def deactivate_examen_mode(self):
        try:
            # Check date
            generate_date = datetime.strptime(self.data['generate_date'], "%Y-%m-%d %H:%M")
            actual_date = datetime.now()
            if actual_date.year != generate_date.year or actual_date.month != generate_date.month or actual_date.day != generate_date.day:
                self.function_cancel(_("Date is expiered"))
                return
            if actual_date.hour - generate_date.hour > 4:
                self.function_cancel(_("Date is expiered"))
                return
            # If unlock with file, using the serial number of device
            serial_number = braille_device_characteristics.get_serial_number()
            if self.data['serial'] == serial_number:
                os.remove(FILE_PATH)
                self.function()
                return
        except Exception as e:
            self.function_cancel(_("File is corrupted"))
