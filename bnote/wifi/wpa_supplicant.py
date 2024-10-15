import re
import subprocess

from pbkdf2 import PBKDF2

from debug.colored_log import ColoredLogger, WIFI_LOG

log = ColoredLogger(__name__)
log.setLevel(WIFI_LOG)

class Scheme:
    def __init__(self, ssid, psk):
        self.__options = {'ssid': ssid, 'psk': psk}

    def ssid(self):
        return self.__options['ssid'].replace('"', '')

    def psk(self):
        return self.__options['psk']

    def __str__(self):
        """
        Returns the representation of a scheme that you would need
        in the /etc/wpa_supplicant/wpa_supplicant.conf file.
        Something like this :
        network={
            ssid=ssid_name
            psk=encrypted_password
        }
        """
        iface = "network={"
        options = ''.join('\n    {k}={v}'.format(k=k, v=v) for k, v in self.__options.items())
        return "".join([iface, options, "\n}\n\n"])


class WpaSupplicant:

    interface = '/etc/wpa_supplicant/wpa_supplicant.conf'
    #interface = 'wpa_supplicant.conf'

    def __init__(self, interface=None):
        if interface is None:
            self.interface = WpaSupplicant.interface
        else:
            self.interface = interface
        self.__country, self.__header, self.__schemes = self._read_interface(self.interface)
        log.info(f"{self.__country=}, {self.__header=}, {self.__schemes=}")

    @staticmethod
    def countries():
        # https://www.thinkpenguin.com/gnu-linux/country-code-list
        wifi_country = {
            'AF': 'AFGHANISTAN',
            'AX': 'ÅLAND ISLANDS',
            'AL': 'ALBANIA',
            'DZ': 'ALGERIA',
            'AS': 'AMERICAN SAMOA',
            'AD': 'ANDORRA',
            'AO': 'ANGOLA',
            'AI': 'ANGUILLA',
            'AQ': 'ANTARCTICA',
            'AG': 'ANTIGUA AND BARBUDA',
            'AR': 'ARGENTINA',
            'AM': 'ARMENIA',
            'AW': 'ARUBA',
            'AU': 'AUSTRALIA',
            'AT': 'AUSTRIA',
            'AZ': 'AZERBAIJAN',
            'BS': 'BAHAMAS',
            'BH': 'BAHRAIN',
            'BD': 'BANGLADESH',
            'BB': 'BARBADOS',
            'BY': 'BELARUS',
            'BE': 'BELGIUM',
            'BZ': 'BELIZE',
            'BJ': 'BENIN',
            'BM': 'BERMUDA',
            'BT': 'BHUTAN',
            'BO': 'BOLIVIA',
            'BQ': 'BONAIRE',
            'BA': 'BOSNIA AND HERZEGOVINA',
            'BW': 'BOTSWANA',
            'BV': 'BOUVET ISLAND',
            'BR': 'BRAZIL',
            'IO': 'BRITISH INDIAN OCEAN TERRITORY',
            'BN': 'BRUNEI DARUSSALAM',
            'BG': 'BULGARIA',
            'BF': 'BURKINA FASO',
            'BI': 'BURUNDI',
            'KH': 'CAMBODIA',
            'CM': 'CAMEROON',
            'CA': 'CANADA',
            'CV': 'CAPE VERDE',
            'KY': 'CAYMAN ISLANDS',
            'CF': 'CENTRAL AFRICAN REPUBLIC',
            'TD': 'CHAD',
            'CL': 'CHILE',
            'CN': 'CHINA',
            'CX': 'CHRISTMAS ISLAND',
            'CC': 'COCOS (KEELING) ISLANDS',
            'CO': 'COLOMBIA',
            'KM': 'COMOROS',
            'CG': 'CONGO',
            'CD': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE',
            'CK': 'COOK ISLANDS',
            'CR': 'COSTA RICA',
            'CI': "COTE D'IVOIRE",
            'HR': 'CROATIA',
            'CU': 'CUBA',
            'CW': 'CURACAO',
            'CY': 'CYPRUS',
            'CZ': 'CZECH REPUBLIC',
            'DK': 'DENMARK',
            'DJ': 'DJIBOUTI',
            'DM': 'DOMINICA',
            'DO': 'DOMINICAN REPUBLIC',
            'EC': 'ECUADOR',
            'EG': 'EGYPT',
            'SV': 'EL SALVADOR',
            'GQ': 'EQUATORIAL GUINEA',
            'ER': 'ERITREA',
            'EE': 'ESTONIA',
            'ET': 'ETHIOPIA',
            'FK': 'FALKLAND ISLANDS (MALVINAS)',
            'FO': 'FAROE ISLANDS',
            'FJ': 'FIJI',
            'FI': 'FINLAND',
            'FR': 'FRANCE',
            'GF': 'FRENCH GUIANA',
            'PF': 'FRENCH POLYNESIA',
            'TF': 'FRENCH SOUTHERN TERRITORIES',
            'GA': 'GABON',
            'GM': 'GAMBIA',
            'GE': 'GEORGIA',
            'DE': 'GERMANY',
            'GH': 'GHANA',
            'GI': 'GIBRALTAR',
            'GR': 'GREECE',
            'GL': 'GREENLAND',
            'GD': 'GRENADA',
            'GP': 'GUADELOUPE',
            'GU': 'GUAM',
            'GT': 'GUATEMALA',
            'GG': 'GUERNSEY',
            'GN': 'GUINEA',
            'GW': 'GUINEA-BISSAU',
            'GY': 'GUYANA',
            'HT': 'HAITI',
            'HM': 'HEARD ISLAND AND MCDONALD ISLANDS',
            'VA': 'HOLY SEE (VATICAN CITY STATE)',
            'HN': 'HONDURAS',
            'HK': 'HONG KONG',
            'HU': 'HUNGARY',
            'IS': 'ICELAND',
            'IN': 'INDIA',
            'ID': 'INDONESIA',
            'IR': 'IRAN, ISLAMIC REPUBLIC OF',
            'IQ': 'IRAQ',
            'IE': 'IRELAND',
            'IM': 'ISLE OF MAN',
            'IL': 'ISRAEL',
            'IT': 'ITALY',
            'JM': 'JAMAICA',
            'JP': 'JAPAN',
            'JE': 'JERSEY',
            'JO': 'JORDAN',
            'KZ': 'KAZAKHSTAN',
            'KE': 'KENYA',
            'KI': 'KIRIBATI',
            'KP': "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
            'KR': 'KOREA, REPUBLIC OF',
            'KW': 'KUWAIT',
            'KG': 'KYRGYZSTAN',
            'LA': "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
            'LV': 'LATVIA',
            'LB': 'LEBANON',
            'LS': 'LESOTHO',
            'LR': 'LIBERIA',
            'LY': 'LIBYAN ARAB JAMAHIRIYA',
            'LI': 'LIECHTENSTEIN',
            'LT': 'LITHUANIA',
            'LU': 'LUXEMBOURG',
            'MO': 'MACAO',
            'MK': 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF',
            'MG': 'MADAGASCAR',
            'MW': 'MALAWI',
            'MY': 'MALAYSIA',
            'MV': 'MALDIVES',
            'ML': 'MALI',
            'MT': 'MALTA',
            'MH': 'MARSHALL ISLANDS',
            'MQ': 'MARTINIQUE',
            'MR': 'MAURITANIA',
            'MU': 'MAURITIUS',
            'YT': 'MAYOTTE',
            'MX': 'MEXICO',
            'FM': 'MICRONESIA, FEDERATED STATES OF',
            'MD': 'MOLDOVA',
            'MC': 'MONACO',
            'MN': 'MONGOLIA',
            'ME': 'MONTENEGRO',
            'MS': 'MONTSERRAT',
            'MA': 'MOROCCO',
            'MZ': 'MOZAMBIQUE',
            'MM': 'MYANMAR',
            'NA': 'NAMIBIA',
            'NR': 'NAURU',
            'NP': 'NEPAL',
            'NL': 'NETHERLANDS',
            'NC': 'NEW CALEDONIA',
            'NZ': 'NEW ZEALAND',
            'NI': 'NICARAGUA',
            'NE': 'NIGER',
            'NG': 'NIGERIA',
            'NU': 'NIUE',
            'NF': 'NORFOLK ISLAND',
            'MP': 'NORTHERN MARIANA ISLANDS',
            'NO': 'NORWAY',
            'OM': 'OMAN',
            'PK': 'PAKISTAN',
            'PW': 'PALAU',
            'PS': 'PALESTINIAN TERRITORY, OCCUPIED',
            'PA': 'PANAMA',
            'PG': 'PAPUA NEW GUINEA',
            'PY': 'PARAGUAY',
            'PE': 'PERU',
            'PH': 'PHILIPPINES',
            'PN': 'PITCAIRN',
            'PL': 'POLAND',
            'PT': 'PORTUGAL',
            'PR': 'PUERTO RICO',
            'QA': 'QATA',
            'RE': 'REUNION',
            'RO': 'ROMANIA',
            'RU': 'RUSSIAN FEDERATION',
            'RW': 'RWANDA',
            'BL': 'SAINT BARTHELEMY',
            'SH': 'SAINT HELENA',
            'KN': 'SAINT KITTS AND NEVIS',
            'LC': 'SAINT LUCIA',
            'MF': 'SAINT MARTIN',
            'PM': 'SAINT PIERRE AND MIQUELON',
            'VC': 'SAINT VINCENT AND THE GRENADINES',
            'WS': 'SAMOA',
            'SM': 'SAN MARINO',
            'ST': 'SAO TOME AND PRINCIPE',
            'SA': 'SAUDI ARABIA',
            'SN': 'SENEGAL',
            'RS': 'SERBIA',
            'SC': 'SEYCHELLES',
            'SL': 'SIERRA LEONE',
            'SX': 'SINT MAARTEN',
            'SG': 'SINGAPORE',
            'SK': 'SLOVAKIA',
            'SI': 'SLOVENIA',
            'SB': 'SOLOMON ISLANDS',
            'SO': 'SOMALIA',
            'ZA': 'SOUTH AFRICA',
            'GS': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
            'ES': 'SPAIN',
            'LK': 'SRI LANKA',
            'SD': 'SUDAN',
            'SR': 'SURINAME',
            'SJ': 'SVALBARD AND JAN MAYEN',
            'SZ': 'SWAZILAND',
            'SE': 'SWEDEN',
            'CH': 'SWITZERLAND',
            'SY': 'SYRIAN ARAB REPUBLIC',
            'TW': 'TAIWAN',
            'TJ': 'TAJIKISTAN',
            'TZ': 'TANZANIA, UNITED REPUBLIC OF',
            'TH': 'THAILAND',
            'TL': 'TIMOR-LESTE',
            'TG': 'TOGO',
            'TK': 'TOKELAU',
            'TO': 'TONGA',
            'TT': 'TRINIDAD AND TOBAGO',
            'TN': 'TUNISIA',
            'TR': 'TURKEY',
            'TM': 'TURKMENISTAN',
            'TC': 'TURKS AND CAICOS ISLANDS',
            'TV': 'TUVALU',
            'UG': 'UGANDA',
            'UA': 'UKRAINE',
            'AE': 'UNITED ARAB EMIRATES',
            'GB': 'UNITED KINGDOM',
            'US': 'UNITED STATES',
            'UM': 'UNITED STATES MINOR OUTLYING ISLANDS',
            'UY': 'URUGUAY',
            'UZ': 'UZBEKISTAN',
            'VU': 'VANUATU',
            'VE': 'VENEZUELA',
            'VN': 'VIET NAM',
            'VG': 'VIRGIN ISLANDS, BRITISH',
            'VI': 'VIRGIN ISLANDS, U.S.',
            'WF': 'WALLIS AND FUTUNA',
            'EH': 'WESTERN SAHARA',
            'YE': 'YEMEN',
            'ZM': 'ZAMBIA',
            'ZW': 'ZIMBABWE',
        }
        return wifi_country

    def ssids(self):
        ssids_list = []
        for scheme in self.__schemes:
            ssids_list.append(scheme.ssid())
        return ssids_list

    def schemes(self):
        return self.__schemes

    def country(self):
        return self.__country

    def set_country(self, language):
        self.__country = language
        x = subprocess.Popen(["sudo", "raspi-config", "nonint", "do_wifi_country", language], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()
        trace_back = x.stdout.read().decode("utf-8")
        log.info(f"{trace_back=}")
        err = x.stderr.read().decode("utf-8")
        if err != "":
            log.info(f"raspi_config do_wifi_country : error={err}")
        # Restore pi owner to handle favorite from bnote apps.
        x = subprocess.Popen(["sudo", "chown", "pi:pi", WpaSupplicant.interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        x.wait()


    @staticmethod
    def encrypt_password(ssid, password):
        return PBKDF2(password, ssid, 4096).hexread(32)

    def _read_interface(self, interface):
        scheme_re = re.compile(r'[.*\s*]+network=\{\s+ssid=(?P<ssid>.*)\s+psk=(?P<psk>.*)\s\}')
        header_re = re.compile(r'.*network=\{')

        country, header, schemes = "", "", []
        with open(interface, 'r') as f:
            content = f.read()
            res = header_re.search(content)
            if res:
                start, end = res.regs[0]
                header = content[0: start]
                # print(header)
                networks = scheme_re.findall(content)
                for network in networks:
                    ssid, psk = network
                    # print(ssid, psk)
                    schemes.append(Scheme(ssid, psk))
            else:
                header = content
            if len(header) > 0:
                regex_country = r'((country)=(\w+))'
                pattern_country = re.compile(regex_country)
                res = pattern_country.findall(header)
                if res:
                    # res is something like that : [('country=FR', 'country', 'FR')]
                    country = res[0][2]

        return country, header, schemes

    def __index_of(self, ssid):
        for index, scheme in enumerate(self.__schemes):
            if scheme.ssid() == ssid:
                return index, scheme
        return None, None

    def set_first(self, index):
        if index is not None and (index >= 0):
            scheme = self.__schemes.pop(index)
            self.__schemes.insert(0, scheme)

    def add(self, index, ssid, psk):
        if index is None or (index < 0):
            # If invalid index, the insertion point is 0.
            index = 0
        # Remove ssid if exists before add the same.
        deleted_index = self.delete_id(ssid)
        if deleted_index and deleted_index < index:
            # backward address if an ssid before insertion point is deleted.
            index -= 1
            # add quotes to ssid.
        quoted_ssid = "".join(['"', ssid, '"'])
        self.__schemes.insert(index, Scheme(quoted_ssid, psk))

    def delete(self, index):
        if index is not None and (index >= 0):
            self.__schemes.pop(index)

    def delete_id(self, ssid):
        index, scheme = self.__index_of(ssid)
        if index is not None:
            self.delete(index)
        return index

    def save(self):
        """
        Writes the configuration file.
        """
        with open(self.interface, 'w') as f:
            f.write(self.__header)
            for scheme in self.__schemes:
                f.write(str(scheme))
        # Copy the new wpa_supplicant.conf file using sudo
        # DP FIXME for test keep a copy of the file to avoid owner modification of wpa_supplicant.conf ?
        # os.popen(f"sudo cp wpa_supplicant.conf {self.interface}")


def main():
    # wpa_supplicant = WpaSupplicant("./wpa_supplicant.conf")
    # print(wpa_supplicant.ssids())
    # ssid = "ssid_test"
    # password = "123456"
    # psk = wpa_supplicant.encrypt_password(password, ssid)
    # wpa_supplicant.add(0, ssid, psk)
    # wpa_supplicant.save()

    line = "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=FR\n"
    regex_language = r'((country)=(\w+))'
    pattern_network = re.compile(regex_language)
    res = pattern_network.findall(line)
    print(res[0][2])

    line2 = "abc\ndef\nnetwork={\nssid=livebox\npsk=123456\n}\nnetwork={\nssid=totobox\npsk=654321\n}hij"
    # regex_network = r'(network=\{\s+\S+\s\})+'
    # Isolate "network={...}"
    regex_network = r'(network=\{\s[(ssid|psk)=(\w+)\s]+\})'
    print("regex 1 -------------------")
    print(f"{regex_network=}")
    pattern_network = re.compile(regex_network)
    res = pattern_network.findall(line2)
    print(res)
    print("-------------------")

    line1 = "abc\nnetwork={\nssid=value1\npsk=value2\nkeyword1=value3\nkeyword3=value4\n}\n"
    print("regex 2 -------------------")
    keywords = ['ssid', 'psk']
    any_keyword = '|'.join(map(re.escape, keywords))
    regex = r"((" + any_keyword + r")=(\w+))+"
    print(f"{regex=}")
    pattern = re.compile(regex)
    print(pattern.search(line1))
    print("-------------------")
    print(pattern.findall(line1))


if __name__ == '__main__':
    main()

