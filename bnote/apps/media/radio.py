"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import time
import urllib.request
import urllib.error
import xml.sax
import xml.sax.saxutils
from xml.dom import minidom
from xml.dom.minidom import parseString
from io import StringIO

import vlc
import requests
from pathlib import Path
from bnote.apps.fman.file_manager import BNOTE_FOLDER
from bnote.stm32.braille_device_characteristics import braille_device_characteristics

from bnote.tools.io_util import Gpio

# Setup the logger for this file
from bnote.debug.colored_log import ColoredLogger, RADIO_LOG
from bnote.tools.settings import Settings
from bnote.tools.audio_player import AudioPlayer

log = ColoredLogger(__name__)
log.setLevel(RADIO_LOG)

RADIO_SERVER_URL = "https://update.eurobraille.fr/download/bnote/radio_list.xml"
RADIO_SERVER_LIST_FILE = BNOTE_FOLDER / Path("radio_server_list.xml")
RADIO_LOCAL_LIST_FILE = BNOTE_FOLDER / Path("radio_local_list.xml")


class ReadRadioContent:
    def __init__(self, filename, country):
        self._filename = filename
        self._country = country

    class RadioHandler(xml.sax.handler.ContentHandler):

        TAG_BODY = "body"
        TAG_ALL = "all"
        TAG_RADIO = "radio"

        def __init__(self, country, add_radio):
            xml.sax.handler.ContentHandler.__init__(self)
            # in xml 'body' part.
            self._is_body = False
            # in xml 'radio' tag.
            self._is_radio = False
            # in xml 'all' tag.
            self._is_all = False
            # in xml country (like 'fr_FR') tag.
            self._is_country = False
            # Current radio url.
            self._radio_data = ""
            # Current radio name.
            self._radio_name = ""
            # Current radio type 'user'/'server' if user definition / get from eurobraille server.
            self._radio_type = ""
            # Callback function to add a radio to the radio list.
            self._add_radio = add_radio
            # The country tag to parse xml file.
            self._country = country

        def startDocument(self):
            pass

        def startElement(self, name, attrs):
            # print(name)
            if name == ReadRadioContent.RadioHandler.TAG_BODY:
                self._is_body = True
            if name == ReadRadioContent.RadioHandler.TAG_ALL:
                self._is_all = True
            if name == self._country:
                self._is_country = True
            elif name == ReadRadioContent.RadioHandler.TAG_RADIO:
                self._is_radio = True
                # Parse span attribute 'title'
                self._radio_name = ""
                keys = attrs.keys()
                if "name" in keys:
                    self._radio_name = attrs.getValue("name")
                    log.info("RADIO NAME <{}>".format(self._radio_name))
                if "type" in keys:
                    self._radio_type = attrs.getValue("type")
                    log.info("RADIO TYPE <{}>".format(self._radio_name))
                else:
                    log.warning(
                        "!!! No radio type, select 'server' definition by default"
                    )
                    self._radio_type = "server"
                self._is_radio = True

        def endElement(self, name):
            if name == ReadRadioContent.RadioHandler.TAG_BODY:
                self._is_body = False
            elif name == ReadRadioContent.RadioHandler.TAG_ALL:
                self._is_all = False
            elif name == self._country:
                self._is_country = False
            elif name == ReadRadioContent.RadioHandler.TAG_RADIO:
                # Each end of paragraph indicates a end of line
                if self._is_body and (self._is_all or self._is_country):
                    log.info("url <{}>".format(self._radio_data))
                    self._add_radio(
                        self._radio_name, self._radio_data, self._radio_type
                    )
                self._radio_name = ""
                self._radio_data = ""
                self._radio_type = ""
                self._is_radio = False

        def characters(self, content):
            if self._is_body and self._is_radio:
                self._radio_data += content

    def read_radio(self, add_radio):
        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namespaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        # override the default ContextHandler
        handler = self.RadioHandler(self._country, add_radio)
        parser.setContentHandler(handler)
        parser.parse(self._filename)


class WriteRadioContent:
    def __init__(self, filename):
        self._filename = filename

    def write_radio(self, radio_dict, radio_type):
        output = StringIO()
        handler = xml.sax.saxutils.XMLGenerator(output, "UTF-8")
        handler.startDocument()
        handler.startElement(
            "html",
            {"xmlns": "http://www.w3.org/1999/xhtml", "xml:lang": "en", "lang": "en"},
        )
        handler.startElement("head", {})
        handler.startElement("meta", {"name": "document-type", "content": "Radio-List"})
        handler.endElement("meta")
        handler.startElement("meta", {"name": "copyright", "content": "euroBraille"})
        handler.endElement("meta")
        handler.endElement("head")
        handler.startElement("body", {})
        handler.startElement("all", {})
        # add radio tags.
        for radio_name in radio_dict.keys():
            if radio_dict[radio_name][0] == radio_type:
                # Add only radio of one type.
                handler.startElement(
                    "radio", {"name": radio_name, "type": radio_dict[radio_name][0]}
                )
                handler.characters(radio_dict[radio_name][1])
                handler.endElement("radio")
        handler.endElement("all")
        handler.endElement("body")
        handler.endElement("html")
        handler.endDocument()
        fp = open(self._filename, "w")
        parser = parseString(output.getvalue())
        fp.write(parser.toprettyxml())
        fp.close()


class Radio:
    """
    Radio application.
    """

    def __init__(self):
        # Player parameters.
        self.url = None

        # Radio list parameters.
        self._radio_dict = {}

    """
    Player functions.
    """

    def start_radio(self, url):
        if url is None:
            return
        self.url = url
        AudioPlayer().radio_play(url)

    def stop_radio(self):
        AudioPlayer().stop()

    def is_playing(self):
        return AudioPlayer().is_playing()

    def restart_radio(self):
        if self.url:
            AudioPlayer().radio_play(self.url)

    def set_volume(self):
        if self.url:
            AudioPlayer().set_volume()

    @staticmethod
    def __pls_entry_generator(file):
        for line in file:
            line = line.decode("utf-8")
            if line.lower().startswith("file"):
                yield (line.split("=")[-1]).strip()

    @staticmethod
    def __asx_entry_generator(file):
        # use getElementsByTagName() to get tag
        refs = file.getElementsByTagName("ref")
        for ref in refs:
            try:
                url = ref.attributes["href"].value
            except KeyError as er:
                url = ""
            yield url

    def play_radio(self, name):
        if name not in self._radio_dict.keys():
            return
        url = self._radio_dict[name][1]
        file = Path(url)
        if file.suffix == ".pls" or file.suffix == ".asx":
            radio_list = []
            if file.suffix == ".pls":
                # print("!!! pls file !!!")
                try:
                    f = urllib.request.urlopen(url)
                except urllib.error.HTTPError as er:
                    return
                except urllib.error.URLError as er:
                    return
                for entry in self.__pls_entry_generator(f):
                    radio_list.append(entry)
            elif file.suffix == ".asx":
                # print("!!! asx file !!!")
                try:
                    f = urllib.request.urlopen(url)
                except urllib.error.HTTPError as er:
                    return er
                except urllib.error.URLError as er:
                    return er
                # parse an xml file by name
                file = minidom.parse(f)
                for entry in self.__asx_entry_generator(file):
                    radio_list.append(entry)
            # Try to play one radio of the list.
            for radio_url in radio_list:
                # print(f"try {radio_url}")
                self.start_radio(radio_url)
                time.sleep(2)
                if self.is_playing():
                    return
        else:
            self.start_radio(url)

    def is_playing_radio(self, name):
        return (
            name in self._radio_dict.keys()
            and self.is_playing()
            and (self.url == self._radio_dict[name][1])
        )

    """
    Radio list.
    """

    def get_web_list(self, url):
        self._radio_dict = {}
        try:
            r = requests.get(url)
            log.debug(f"write radio list {RADIO_SERVER_LIST_FILE}")
            with open(RADIO_SERVER_LIST_FILE, "wb") as f:
                f.write(r.content)
            return self.get_local_list()
        except requests.exceptions.ConnectionError as er:
            return er, None

    def get_local_list(self):
        self._radio_dict = {}
        try:
            if Path.exists(RADIO_SERVER_LIST_FILE):
                read_radio = ReadRadioContent(
                    filename=RADIO_SERVER_LIST_FILE,
                    country=braille_device_characteristics.get_message_language_country(),
                )
                read_radio.read_radio(self.add_radio)
            if Path.exists(RADIO_LOCAL_LIST_FILE):
                read_radio = ReadRadioContent(
                    filename=RADIO_LOCAL_LIST_FILE,
                    country=braille_device_characteristics.get_message_language_country(),
                )
                read_radio.read_radio(self.add_radio)
            log.info(self._radio_dict.keys())
            log.info(self._radio_dict.values())
            return None, self._radio_dict
        except ValueError as er:
            return er, None
        except xml.sax.SAXParseException as er:
            return er, None
        except xml.sax.SAXException as er:
            return er, None

    def add_radio(self, radio_name, radio_url, radio_type):
        if radio_name and (len(radio_name) != 0):
            self._radio_dict[radio_name] = (radio_type, radio_url.strip(" \r\n\t"))
            return self._radio_dict
        else:
            log.warning("!!! Try to add a radio with invalid name.")
            return None

    def write_user_file(self):
        writer = WriteRadioContent(RADIO_LOCAL_LIST_FILE)
        writer.write_radio(self._radio_dict, "user")

    def write_server_file(self):
        writer = WriteRadioContent(RADIO_SERVER_LIST_FILE)
        writer.write_radio(self._radio_dict, "server")

    def delete_radio(self, radio_name):
        if radio_name in self._radio_dict.keys():
            self._radio_dict.pop(radio_name)
            self.write_server_file()
            self.write_user_file()
        log.info(self._radio_dict.keys())
        log.info(self._radio_dict.values())
