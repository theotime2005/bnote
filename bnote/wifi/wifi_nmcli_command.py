"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import re
import shlex
import subprocess

# Set up the logger for this file
from bnote.debug.colored_log import ColoredLogger, SETTING_APP_LOG

log = ColoredLogger(__name__)
log.setLevel(SETTING_APP_LOG)


class WifiNmcliCommand:
    @staticmethod
    def network_scan():
        """
        Scan visibles access points.
        Return List of dictionary for each access point.
            [{'in-use':'*' or '', 'ssid':_, 'bssid':_, 'level':_}, ...]
        """
        desc_device = []
        arguments = "-f IN-USE,SSID,BSSID,Signal device wifi list"
        err_code, out = WifiNmcliCommand.__execute_command(arguments)
        if err_code == 0:
            # print(f"{results=}")
            # results is a string like this :
            # 'SSID          BSSID              SIGNAL \nHUAWEI_P10    14:9D:09:3D:53:17  100    \nLivebox-5340  D4:F8:29:7E:53:40  60     \nPixel_3441    86:4E:68:6B:D9:A4  59     \nLivebox-5340  D4:F8:29:7E:53:45  59     \n'
            devices_lines = out.strip().split("\n")
            # Find position of SSID and BSSID in first line.
            header = devices_lines[0]
            ssid_start = header.find("SSID")
            bssid_start = header.find("BSSID")
            signal_start = header.find("SIGNAL")
            if ssid_start == -1 or bssid_start == -1 or signal_start == -1:
                log.error(f"nmcli error {ssid_start=} {bssid_start=} {signal_start=}")
                return desc_device
            if len(devices_lines) >= 2:
                # Parcourir les lignes suivantes pour extraire les SSID
                already_seen = set()
                for devices_line in devices_lines[1:]:
                    if len(devices_line) > signal_start:
                        in_use = devices_line[:ssid_start].strip()
                        ssid = devices_line[ssid_start:bssid_start].strip()
                        bssid = devices_line[bssid_start:signal_start].strip()
                        level = devices_line[signal_start:].strip()
                        if ssid not in already_seen:
                            desc_device.append(
                                {
                                    "in-use": in_use,
                                    "ssid": ssid,
                                    "bssid": bssid,
                                    "level": level,
                                }
                            )
                            already_seen.add(ssid)
        return desc_device

    @staticmethod
    def network_add(ssid, password):
        command_line = f"dev wifi con '{ssid}' password '{password}'"
        err_code, out = WifiNmcliCommand.__execute_command(command_line)
        return err_code == 0

    @staticmethod
    def network_remove(ssid):
        command_line = f"con delete '{ssid}'"
        err_code, out = WifiNmcliCommand.__execute_command(command_line)
        return err_code == 0

    @staticmethod
    def network_up(ssid):
        command_line = f"con up '{ssid}'"
        err_code, out = WifiNmcliCommand.__execute_command(command_line)
        return err_code == 0

    @staticmethod
    def network_on_off(on=None):
        """
        Wifi on/off function.
        no param : return wifi state
        on : True to activate wifi device, False to deactivate.
        Return : wifi state or execution confirmation.
        """
        if on is None:
            command_line = f"r wifi"
            err_code, out = WifiNmcliCommand.__execute_command(command_line)
            if (err_code == 0) and (out.strip() == "enabled"):
                return True
            else:
                return False
        else:
            if on:
                command_line = f"r wifi on"
            else:
                command_line = f"r wifi off"
            err_code, x = WifiNmcliCommand.__execute_command(command_line)
            return err_code == 0

    @staticmethod
    def __execute_command(arguments):
        """
        Execute an nmcli command with arguments passed.
        Returns 0, out if successful, 1, out otherwise with out as strings return from subprocess.
        """
        command = ["nmcli"] + shlex.split(arguments)
        try:
            with subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            ) as x:
                x.wait()
                if x.returncode != 0:
                    log.error(f"Error nmcli {x.returncode}: {x.stderr}")
                    return 1, x.stderr.read().decode("utf-8")
                out = x.stdout.read().decode("utf-8")
                x.kill()
                # print(f"nmcli {out}")
                return 0, out
        except subprocess.CalledProcessError as e:
            log.error(f"Error nmcli: {e.stderr.decode('utf-8')}")
            return 1, None
