"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import datetime
import requests
import threading


class SyncDate(threading.Thread):
    def __init__(self, function):
        threading.Thread.__init__(self)
        self.date = dict()
        self.function = function

    def run(self):
        current_date = self.get_current_date_time()
        self.date = self.transforme_date_time(current_date)
        if self.date:
            self.function(year=int(self.date['year']), month=int(self.date['month']), day=int(self.date['day']),
                          hour=int(self.date['hour']), minute=int(self.date['minute']), second=int(self.date['second']))

    def get_current_date_time(self):
        try:
            response = requests.get('http://worldtimeapi.org/api/ip')
            data = response.json()

            current_datetime = data['datetime']
            return current_datetime
        except Exception as e:
            print(f"Error: {e}")
            return None

    def transforme_date_time(self, date_str):
        if not date_str:
            return False

        # Utilisation du bon format pour strptime
        try:
            convert_date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        except Exception as e:
            print(f"Conversion Error: {e}")
            return False

        return {
            "year": convert_date.year,
            "month": convert_date.month,
            "day": convert_date.day,
            "hour": convert_date.hour,
            "minute": convert_date.minute,
            "second": convert_date.second
        }
