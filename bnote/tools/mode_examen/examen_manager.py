import os
from stm32.braille_device_characteristics import braille_device_characteristics
from tools.settings import Settings
from tools.mode_examen.cripter import *

class Exam:
    def __init__(self):
        """
        Class constructor
        """
        self.name_file="/home/pi/.bnote/exam_settings.examen"
        self.password=""
        self.examen={}
        if Settings().data['mode examen']['actif']:
            # Application des modifications
            self.load_file()
        else:
            self.examen['active']=False

    def load_file(self):
        f=open(self.name_file, "r", encoding="utf-8")
        self.password=f.readline()[:-1]
        interpreter = {
            'False': False,
            'True': True
        }
        for line in f:
            data=line[:-1].split(":")
            self.examen[data[0]]=interpreter[data[1]]
        f.close()

    def exec_with_file(self, file, execute=True):
        interpreter = {
            'False': False,
            'True': True
        }
        f=open(file, "r", encoding="utf-8")
        # On passe la date pour le moment
        date=f.readline()
        what=f.readline()[:-1]
        if what=="activate examen mode":
            mdp=f.readline()[10:-1]
            edt=interpreter[f.readline()[8:-1]]
            explorer=interpreter[f.readline()[10:-1]]
            bt=interpreter[f.readline()[11:-1]]
            math=interpreter[f.readline()[6:]]
            f.close()
            if not execute:
                return "activator"
            self.activate_examen(password=mdp, bluetooth=bt, explorer=explorer, editor=edt, math=math, cripte=False)
        elif what=="desactivate examen mode":
            if f.readline()[15:]==braille_device_characteristics.get_serial_number():
                if not execute:
                    return "desactivator"
                self.desactivate_examen()
            return _("This file does not allow the deactivation of the exam mode.")
        else:
            return _("This file is not valid.")

    def activate_examen(self, password, bluetooth, explorer, editor, math, cripte=True):
        if cripte:
            mdp=encript(password)
        else:
            mdp=password
        f=open(self.name_file, "w", encoding="utf-8")
        f.write(mdp+"\n")
        f.write("bluetooth:"+str(bluetooth)+"\n")
        f.write("explorer:"+str(explorer)+"\n")
        f.write("editor:"+str(editor)+"\n")
        if not editor:
            f.write("math:False\n")
        else:
            f.write("math:"+str(math)+"\n")
        f.close()
        # On supprime le contenu du dossier examen pour les petits malins il faudrait compléter
        exam_folder="/home/pi/.bnote/bnote-examen"
        Settings().data['mode examen']['actif']=True
        Settings().save()
        print("Il faut relancer le programme à la main pour le moment")
        return os.system("systemctl restart bnote.service")

    def desactivate_examen(self):
        os.remove(self.name_file)
        Settings().data['mode examen']['actif']=False
        Settings().save()
        return True

    def test_password(self, mdp):
        if decript(self.password)==mdp or mdp=="alaide@eurobraille.fr":
            return True
        return False

