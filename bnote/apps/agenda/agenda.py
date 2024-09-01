"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import datetime
import os


def create_file():
    """
    create csv file contening 3 colunes
    """
    file = open("/home/pi/.bnote/my_agenda.csv", "w", encoding="utf-8")
    file.write("date;subject;content;todo")
    file.close()
    return True


class Listing:
    def __init__(self, data):
        self.date = data[0]
        self.subject = data[1]
        self.content = data[2]
        self.todo = data[3]


class Editing:
    def __init__(self):
        self.lst_not_treated = []
        self.lst = []
        self.lst_range = []

    def import_data(self):
        lst_elements = []
        lst_not_treated = []
        if not self.verify_file():
            return False
        f = open("/home/pi/.bnote/my_agenda.csv", "r", encoding="utf-8")
        f.readline()
        for line in f:
            data = line[:-1].split(";")
            lst_not_treated.append(data)
            h = Listing(data)
            lst_elements.append(h)
        self.lst = lst_elements
        self.lst_not_treated = lst_not_treated
        f.close()
        return lst_elements

    def display_list(self):
        if len(self.lst) == 0:
            # print("Aucun contenu")
            pass
        else:
            for element in self.lst:
                if element.todo == "0":
                    todo = "Non fait"
                elif element.todo == "1":
                    todo = "Fait"
                # print(element.date+" "+todo+": "+element.subject+" "+element.content)

    def add_element(self, date, subject, content):
        """
        Add new element to the agenda list
        """
        if self.verify_date(date) == False:
            # print("Il y a une erreure")
            return date
        self.lst_not_treated.append([date, subject, content, "0"])
        self.save_agenda()

    def delete_element(self, idx):
        self.lst_not_treated.remove(self.lst_not_treated[idx])
        self.save_agenda()

    def comute_todo(self, idx):

        changer = self.lst_not_treated[idx]
        if changer[3] == "0":
            changer[3] = "1"
        else:
            changer[3] = "0"
        self.lst_not_treated[idx] = changer
        self.save_agenda()

    def import_other_file(self, name):
        if not self.verify_file(name):
            return False
        double = 0
        f = open(name, "r", encoding="utf-8")
        f.readline()
        for line in f:
            if line[-1] != "\n":
                data = line.split(";")
            else:
                data = line[:-1].split(";")
            if self.search_double(self.lst_not_treated, data) == True:
                double += 1
            else:
                self.lst_not_treated.append(data)
        self.save_agenda()
        if double > 0:
            return double
        return True

    def verify_file(self, name="/home/pi/.bnote/my_agenda.csv") -> bool:
        if not self.verify_heading_file(name):
            return False
        f = open(name, "r", encoding="utf-8")
        f.readline()
        for line in f:
            if line[-1] != "\n":
                data = line.split(";")
            else:
                data = line[:-1].split(";")
            if len(data) != 4 or data[3] == ("0", "1"):
                return False
            elif self.verify_date(data[0]) == False:
                return False
        f.close()
        return True

    def verify_heading_file(self, name) -> bool:
        f = open(name, "r", encoding="utf-8")
        verify = f.readline()
        f.close()
        if verify != "date;subject;content;todo":
            if verify == "date;subject;content;todo\n":
                return True
            return False
        return True

    def export_file(self, name, dir_path):
        path = os.listdir(dir_path)
        for file in path:
            if file == name + ".csv":
                return "exist"
        self.range_element()
        file_name = str(dir_path) + "/" + name + ".csv"
        f = open(file_name, "w", encoding="utf-8")
        f.write("date;subject;content;todo")
        for element in self.lst_range:
            f.write("\n" + element[0] + ";" + element[1] + ";" + element[2] + ";" + element[3])
        f.close()
        return True

    def verify_date(self, date):
        if len(date) != 10:
            return "invalid length"

        for c in date:
            if not (c.isdigit() or c == "/"):
                return "invalid characters"

        day, month, year = map(int, date.split("/"))

        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if month < 1 or month > 12:
            return "invalid month"

        if day < 1 or day > days_in_month[month - 1]:
            return "invalid day"

        return True

    def range_element(self):
        """
        Range element of agenda in chronologic order
        """
        tmp = []
        # attribution de la date
        for element in self.lst_not_treated:
            date = element[0].split("/")
            tmp.append(
                [str(datetime.datetime(int(date[2]), int(date[1]), int(date[0]))), element[1], element[2], element[3]])
        tmp = sorted(tmp)
        # on remet dans la bonne syntax
        for el in tmp:
            d = el[0]
            d = d[:-9].split("-")
            d.reverse()
            d_end = str(d[0]) + "/" + str(d[1]) + "/" + str(d[2])
            el[0] = d_end
            self.lst_range.append(el)

    def modify_element(self, idx, date, subject, content, todo):
        self.lst_not_treated[idx] = [date, subject, content, todo]
        self.save_agenda()

    def search_double(self, lst, cible):
        """"
        Search double element in lst
        return False if element is not in lst
        return True if element is in lst
        """
        for element in lst:
            if element == cible:
                return True
        return False

    def save_agenda(self):
        self.range_element()
        f = open("/home/pi/.bnote/my_agenda.csv", "w", encoding="utf-8")
        f.write("date;subject;content;todo")
        for element in self.lst_range:
            f.write("\n" + element[0] + ";" + element[1] + ";" + element[2] + ";" + element[3])
        f.write("\n")
        f.close()
        self.__init__()
        return True


# --------------------------------
# détermination de l'existance du fichier
try:
    f = open("/home/pi/.bnote/my_agenda.csv", "r", encoding="utf-8")
    edition = Editing()
    f.close()
except FileNotFoundError:
    create_file()
    edition = Editing()
