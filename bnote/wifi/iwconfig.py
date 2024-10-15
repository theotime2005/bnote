import re
import subprocess

class IwConfig:

    def __init__(self):
        pass

    @staticmethod
    def __call_iwconfig():
        x = subprocess.Popen(["/sbin/iwconfig", "wlan0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()
        trace_back = x.stdout.read().decode("utf-8")
        # log.info(trace_back)
        scheme_re = re.compile(r'ESSID:"(?P<ssid>.*)"')
        res = scheme_re.findall(trace_back)
        if res and (len(res) == 1):
            return res[0]
        return None

    def ssid(self):
        ssid = self.__call_iwconfig()
        return ssid


def main():
    # print(res)
    # trace_back = ''.join(['lo        no wireless extensions.\n',
    #                       '\n',
    #                       'wlan0     IEEE 802.11  ESSID:off/any  \n',
    #                       '          Mode:Managed  Frequency:5.52 GHz  Access Point: D4:F8:29:7E:53:45   \n',
    #                       '          Bit Rate=6 Mb/s   Tx-Power=31 dBm   \n',
    #                       '          Retry short limit:7   RTS thr:off   Fragment thr:off\n',
    #                       '          Power Management:on\n',
    #                       '          Link Quality=40/70  Signal level=-70 dBm  \n',
    #                       '          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0\n',
    #                       '          Tx excessive retries:0  Invalid misc:0   Missed beacon:0\n'])
    # print(trace_back)
    iwconfig = IwConfig()
    print(iwconfig.ssid())

if __name__ == '__main__':
    main()



