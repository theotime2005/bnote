"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""
from enum import Enum
import dbus
import sdbus
from pip._vendor.pyparsing import results
from sdbus_block.networkmanager import (
    ConnectionType,
    NetworkConnectionSettings,
    NetworkManager,
    NetworkManagerSettings,
    NetworkDeviceGeneric,
    NetworkDeviceWireless,
    IPv4Config,
    DeviceState,
    DeviceType,
    # DeviceCapabilitiesFlags,
    ActiveConnection,
    ConnectivityState,
    WiFiOperationMode,
    AccessPoint,
    NmSettingsInvalidConnectionError,
)


class WifiTools:
    def __init__(self):
        sdbus.set_default_bus(sdbus.sd_bus_open_system())

    from typing import Any, Dict, List, Optional, Tuple
    NetworkManagerAddressData = List[Dict[str, Tuple[str, Any]]]

    @staticmethod
    def __title(enum: Enum) -> str:
        """Get the name of an enum: 1st character is uppercase, rest lowercase"""
        return enum.name.title()

    def get_active_connection_uuid(self):
        """
        Get the UUID of the active connection.
        from https://github.com/NetworkManager/NetworkManager/blob/main/examples/python/dbus/get-active-connection-uuids.py
        return : ID, UUID of the active connection
        """
        bus = dbus.SystemBus()
        nm = NetworkManager()
        # Find all active connections.
        actives = nm.active_connections
        for a in actives:
            print(f"active: {a}")
            a_proxy = bus.get_object("org.freedesktop.NetworkManager", a)

            a_props = dbus.Interface(a_proxy, "org.freedesktop.DBus.Properties")

            # Grab the connection object path so we can get all the connection's settings
            connection_path = a_props.Get(
                "org.freedesktop.NetworkManager.Connection.Active", "Connection"
            )
            c_proxy = bus.get_object("org.freedesktop.NetworkManager", connection_path)
            connection = dbus.Interface(
                c_proxy, "org.freedesktop.NetworkManager.Settings.Connection"
            )
            settings = connection.GetSettings()
            # print(
            #     "%s (%s) - %s"
            #     % (
            #         settings["connection"]["id"],
            #         settings["connection"]["uuid"],
            #         settings["connection"]["type"],
            #     )
            # )
            if settings["connection"]["type"] == "802-11-wireless":
                return settings["connection"]["id"], settings["connection"]["uuid"]
        return None, None

    def delete_connection_by_uuid(self, uuid: str) -> bool:
        """Find and delete the connection identified by the given UUID"""
        try:
            NetworkManagerSettings().delete_connection_by_uuid(uuid)
        except NmSettingsInvalidConnectionError:
            log.error(f"Connection {uuid} for deletion not found")
            return False
        return True

    @staticmethod
    def network_active_connection():
        """
        Return the active connection
        { 'ssid':_, 'address':_, 'signal':_ }
        """
        result = {'ssid': "", 'address': "", 'signal': ""}
        try:
            nm = NetworkManager()
            devices_paths = nm.get_devices()
            for device_path in devices_paths:
                generic_dev = NetworkDeviceGeneric(device_path)
                # Create the strings for the columns using the names of the enums:
                dev = generic_dev.interface
                dev_type = WifiTools.__title(DeviceType(generic_dev.device_type))
                dev_state = WifiTools.__title(DeviceState(generic_dev.state))
                dev_connectivity = WifiTools.__title(ConnectivityState(generic_dev.ip4_connectivity))
                if dev == "wlan0" and dev_type == "Wifi":
                    # ActiveConnection() gets propertites from active connection path:
                    active_connection = ActiveConnection(generic_dev.active_connection)
                    ssid = active_connection.id
                    if active_connection.default:
                        ssid += " [primary connection]"
                    result['ssid'] = ssid
                    # ip v4 address
                    device_ip4_conf_path: str = generic_dev.ip4_config
                    ip4_conf = IPv4Config(device_ip4_conf_path)
                    address_data: WifiTools.NetworkManagerAddressData = ip4_conf.address_data
                    for inetaddr in address_data:
                        result['address'] = f'{inetaddr["address"][1]}/{inetaddr["prefix"][1]}'
                    # Signal strength
                    wifi = NetworkDeviceWireless(device_path)
                    ap = AccessPoint(wifi.active_access_point)
                    if ap.strength:
                        result['signal'] = ap.strength
        except sdbus.dbus_exceptions.DbusUnknownMethodError:
            pass
        finally:
            return result

    @staticmethod
    def network_favorites():
        """
        Use of NetworkConnectionSettings(path).get_profile()
        :return: list of device
            [{'name': _, 'uuid': _, 'type': _, 'interface-name': _,
             'ipv4_method', ['ipv4_address': _ ...], 'ipv4_route-metric': _,
             'ipv6_method': ['ipv6_address'],
             'ssid': _},
             {...}, ...
            ]
        """
        result = []
        networkmanager_settings = NetworkManagerSettings()
        for dbus_connection_path in networkmanager_settings.connections:
            profile = NetworkConnectionSettings(dbus_connection_path).get_profile()
            if profile and profile.connection and profile.connection.connection_type == ConnectionType.WIFI:
                favorite = {'name': profile.connection.connection_id,
                            'uuid': profile.connection.uuid,
                            'type': profile.connection.connection_type,
                            'interface-name': profile.connection.interface_name
                            }
                if profile.ipv4:
                    favorite['ipv4_method'] = profile.ipv4.method
                    favorite['ipv4_address'] = []
                    if profile.ipv4.address_data:
                        for address in profile.ipv4.address_data:
                            favorite['ipv4_address'].append(f'{address.address}/{address.prefix}')
                    if profile.ipv4.route_metric:
                        favorite['ipv4_route-metric'] = f'{profile.ipv4.route_metric}'
                if profile.ipv6:
                    favorite['ipv6_method'] = profile.ipv6.method
                favorite['ssid'] = profile.wireless.ssid.decode()
                result.append(favorite)
        return result

    # @staticmethod
    # def network_disconnect():
    #     """
    #     https://github.com/NetworkManager/NetworkManager/blob/main/examples/python/dbus/disconnect-device.py
    #     """
    #     interface = 'wlan0'
    #     bus = dbus.SystemBus()
    #     # Get a proxy for the base NetworkManager object
    #     proxy = bus.get_object(
    #         "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager"
    #     )
    #     manager = dbus.Interface(proxy, "org.freedesktop.NetworkManager")
    #     dpath = None
    #     # Find the device the user wants to disconnect
    #     devices = manager.GetDevices()
    #     for d in devices:
    #         dev_proxy = bus.get_object("org.freedesktop.NetworkManager", d)
    #         prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
    #         iface = prop_iface.Get("org.freedesktop.NetworkManager.Device", "Interface")
    #         if iface == interface:
    #             dpath = d
    #             break
    #     if not dpath or not len(dpath):
    #         raise Exception("NetworkManager knows nothing about %s" % interface)
    #     dev_proxy = bus.get_object("org.freedesktop.NetworkManager", dpath)
    #     dev_iface = dbus.Interface(dev_proxy, "org.freedesktop.NetworkManager.Device")
    #     prop_iface = dbus.Interface(dev_proxy, "org.freedesktop.DBus.Properties")
    #     # Make sure the device is connected before we try to disconnect it
    #     state = prop_iface.Get("org.freedesktop.NetworkManager.Device", "State")
    #     if state <= 3:
    #         raise Exception("Device %s isn't connected" % interface)
    #     # Tell NM to disconnect it
    #     dev_iface.Disconnect()
