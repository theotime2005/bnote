"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

from datetime import datetime
import pytz
import ntplib
import requests
import threading


class SyncDate(threading.Thread):
    def __init__(self, function):
        threading.Thread.__init__(self)
        self.date = dict()
        self.function = function

    def run(self):
        current_date = self.get_current_date_time()
        # self.date = self.transforme_date_time(current_date)
        self.date = current_date
        if self.date:
            self.function(
                year=self.date.year,
                month=self.date.month,
                day=self.date.day,
                hour=self.date.hour,
                minute=self.date.minute,
                second=self.date.second,
            )

    @staticmethod
    def get_current_date_time():
        # Utilise l'API `ip-api.com` pour obtenir des informations sur le fuseau horaire
        response = requests.get("http://ip-api.com/json/")

        if response.status_code == 200:
            data = response.json()
            timezone_str = data.get(
                "timezone", "UTC"
            )  # Récupère le fuseau horaire ou utilise UTC par défaut

            try:
                # Création d'un client NTP
                client = ntplib.NTPClient()

                # Requête au serveur NTP (Google NTP est utilisé ici)
                response = client.request("time.google.com", version=3)

                # Convertir le temps en objet datetime UTC
                utc_time = datetime.utcfromtimestamp(response.tx_time)

                # Ajuster au fuseau horaire local
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(
                    pytz.timezone(timezone_str)
                )
                return local_time
            except Exception as e:
                print(f"Erreur lors de la récupération de l'heure : {e}")
                return None
        else:
            print("Erreur : Impossible de récupérer l'heure.")
            return None

    @staticmethod
    def transforme_date_time(date_str):
        if not date_str:
            return False

        # Utilisation du bon format pour strptime
        try:
            convert_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        except Exception as e:
            print(f"Conversion Error: {e}")
            return False

        return {
            "year": convert_date.year,
            "month": convert_date.month,
            "day": convert_date.day,
            "hour": convert_date.hour,
            "minute": convert_date.minute,
            "second": convert_date.second,
        }
