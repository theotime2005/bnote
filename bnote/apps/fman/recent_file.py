"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import os
import datetime
from pathlib import Path
from bnote.apps.fman.file_manager import FileManager, BNOTE_FOLDER
from bnote.tools.settings import Settings

NAME_FILE=BNOTE_FOLDER/Path("recent_file.trr")
if not Path.exists(NAME_FILE):
    f=open(NAME_FILE, "w", encoding="utf-8")
    f.close()

class RecentFile:
    def __init__(self):
        self.files=[]
        self.load_list()

    def load_list(self):
        name=False
        date=False
        path=False
        f=open(NAME_FILE, "r", encoding="utf-8")
        for line in f:
            if "name:" in line:
                name=line[6:-1]
            elif "date:" in line:
                date=line[6:-1]
            elif "path:" in line:
                path=line[6:-1]
            if name and date and path:
                lst = [name, date, path]
                self.files.append(lst)
                name = False
                date = False
                path = False
        f.close()

    def save_file(self):
        f=open(NAME_FILE, "w", encoding="utf-8")
        for files in self.files:
            writer="name: {}\ndate: {}\npath: {}\n\n".format(files[0],files[1],files[2])
            f.write(writer)
        f.close()

    def add_file_to_list(self, name, path):
        """
        Add element to the recent file list
        """
        if len(self.files)>=Settings().data['explorer']['number_recent_files']:
            self.files.remove(self.files[-1])
        double=self.double(name)
        if double:
            self.delete_file(name)
        date=str(datetime.datetime.now())
        self.files=[[name,date,path]]+self.files
        self.save_file()

    def delete_file(self, name):
        for index in range(len(self.files)):
            if self.files[index][0]==name:
                self.files.remove(self.files[index])
                return self.save_file()

    def delete_all(self):
        self.files=[]
        self.save_file()

    def double(self, name):
        for el in range(len(self.files)):
            # print(self.files[el][0])
            if self.files[el][0]==name:
                return True
        return False

    def send_list(self):
        return self.files
