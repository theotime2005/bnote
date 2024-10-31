"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
import requests
import threading

API_URL="https://timeapi.io/api"
class SyncDate(threading.Thread):
    def __init__(self, timezone, function):
        threading.Thread.__init__(self)
        self.timezone = timezone
        self.function = function

    def run(self):
        current_date = self.get_current_date_time()
        print(current_date)
        if current_date:
            self.function(year=int(current_date['year']), month=int(current_date['month']), day=int(current_date['day']), hour=int(current_date['hour']), minute=int(current_date['minute']), second=int(current_date['seconds']))

    def get_current_date_time(self):
        try:
            response = requests.get(f'{API_URL}/time/current/zone', params={'timeZone': self.timezone})
            data = response.json()
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None

def get_timezone_list(actual):
    """
    Return list of timezones and index of actual timezone
    :param actual: str
    :return: (list, str) | None
    """
    try:
        request = requests.get(f"{API_URL}/timezone/availabletimezones")
        response = request.json()
        index = response.index(actual)
        return (response, index)
    except Exception as e:
        print(f"Error: {e}")
        return None
