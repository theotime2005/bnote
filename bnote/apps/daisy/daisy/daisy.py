"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import io
import os
import re
import sys
import logging
import zipfile
import xml.dom.minidom
from pathlib import Path
import tempfile

from .daisy_html2text import HTML2Text


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_stream = logging.StreamHandler(sys.stdout)
log_stream.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(log_stream)


class DaisyReaderException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class Parser:
    def __init__(self):
        self.document = None

    def parse(self, contents):
        self.document = xml.dom.minidom.parseString(contents)
        return self.document.documentElement

    def meta(self, with_scheme):
        meta_dict = {}
        head = self.document.getElementsByTagName("head")[0]
        metas = head.getElementsByTagName("meta")
        for meta in metas:
            attributes = meta.attributes
            name = meta.getAttribute("name")
            content = meta.getAttribute("content")
            if with_scheme:
                scheme = meta.getAttribute("scheme")
            if name == "":
                http_equiv = meta.getAttribute("http-equiv")
                if http_equiv == "":
                    continue
            else:
                names = name.split(":")
                if with_scheme:
                    if len(names) == 2:
                        NccParser._add_to_dict_of_dict(
                            meta_dict, names[0], names[1], (content, scheme)
                        )
                    else:
                        NccParser._add_to_dict_of_dict(
                            meta_dict, "", names[0], (content, scheme)
                        )
                else:
                    if len(names) == 2:
                        NccParser._add_to_dict_of_dict(
                            meta_dict, names[0], names[1], content
                        )
                    else:
                        NccParser._add_to_dict_of_dict(meta_dict, "", names[0], content)
        return meta_dict

    @staticmethod
    def _add_to_dict_of_dict(dictionary, key1, key2, value):
        if not key1 in dictionary.keys():
            dictionary[key1] = {}
        dictionary[key1][key2] = value

    @staticmethod
    def _node_text(node):
        nodelist = node.childNodes
        result = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                result.append(node.data)
        return "".join(result)


class NccParser(Parser):
    """
    Class to parse a NCC XML file (Navigation Control Center).
    """

    header_keys = ["h1", "h2", "h3", "h4", "h5", "h6"]

    def __init__(self):
        super().__init__()

    def title(self) -> str:
        """
        Extract the title of the NCC document.
        """
        head = self.document.getElementsByTagName("head")[0]
        title = head.getElementsByTagName("title")[0]
        return NccParser._node_text(title)

    def meta(self):
        """
        Extract all metadata about the NCC document.
        Return:
            Dictionary of dictionnary with metadata about the NCC document (value is ('content' attribute, 'scheme' attribute)
        Example: {
        'dc': {
            'title': ('9782081230316 Ceux qui rêvent Daisy Audio TTS', ''), 'identifier': ('fr-20130719142517', ''), 'format': ('Daisy 2.02', ''),
            'date': ('2013-07-19', 'yyyy-mm-dd'), 'publisher': ('Dolphin EasyProducer', ''), 'creator': ('Unknown', ''), 'language': ('en', 'ISO 639'),
            'source': ('Unknown', ''), 'subject': ('9782081230316 Ceux qui rêvent Daisy Audio TTS', '')}, 'ncc': {'tocItems': ('216', ''),
            'generator': ('Dolphin EasyProducer 2.00 Build 046 + DolphinDaisy 1.01 Build 049', ''), 'totalTime': ('07:45:22', 'hh:mm:ss'),
            'pageFront': ('0', ''), 'pageNormal': ('182', ''), 'pageSpecial': ('0', ''), 'prodNotes': ('0', ''), 'sidebars': ('0', ''), 'footnotes': ('0', ''),
            'narrator': ('Alice, HQ 22k, French, SAPI 5, Acapela TTS 9.100 for Windows', ''), 'multimediaType': ('audioFullText', ''), 'setInfo': ('1 of 1', ''),
            'maxPageNormal': ('182', ''), 'depth': ('1', ''), 'charset': ('utf-8', ''), 'files': ('71', ''), 'kByteSize': ('166163', ''),
            'sourceDate': ('2013', 'yyyy'), 'sourceEdition': ('1', ''), 'sourcePublisher': ('Unknown', '')
            },
        'prod': {'genName': ('Dolphin EasyProducer', ''), 'genVer': ('2.00 Build 046', '')}}
        """
        return super().meta(with_scheme=True)

    def body_header(self):
        """
        Extract the header h1 to h6 tag from the body.
        Return:
            List of dictionary.
        Example:
            [
                {'name': 'h1', 'text': 'Ceux qui rêvent', 'class': 'title', 'id': 'gaex0001', 'href': 'gaex0001.smil#wvbt_0002'},
                {'name': 'h1', 'text': '\xa0', 'class': '', 'id': 'gaex0002', 'href': 'gaex0002.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'Dans la même collection :', 'class': '', 'id': 'gaex0003', 'href': 'gaex0003.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'Connaissez-vous Ukronie ?', 'class': '', 'id': 'gaex0004', 'href': 'gaex0004.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 1', 'class': '', 'id': 'gaex0005', 'href': 'gaex0005.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 2', 'class': '', 'id': 'gaex0006', 'href': 'gaex0006.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 3', 'class': '', 'id': 'gaex0007', 'href': 'gaex0007.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 4', 'class': '', 'id': 'gaex0008', 'href': 'gaex0008.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 5', 'class': '', 'id': 'gaex0009', 'href': 'gaex0009.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 6', 'class': '', 'id': 'gaex0010', 'href': 'gaex0010.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 7', 'class': '', 'id': 'gaex0011', 'href': 'gaex0011.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 8', 'class': '', 'id': 'gaex0012', 'href': 'gaex0012.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 9', 'class': '', 'id': 'gaex0013', 'href': 'gaex0013.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 10', 'class': '', 'id': 'gaex0014', 'href': 'gaex0014.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 11', 'class': '', 'id': 'gaex0015', 'href': 'gaex0015.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 12', 'class': '', 'id': 'gaex0016', 'href': 'gaex0016.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 13', 'class': '', 'id': 'gaex0017', 'href': 'gaex0017.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 14', 'class': '', 'id': 'gaex0018', 'href': 'gaex0018.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 15', 'class': '', 'id': 'gaex0019', 'href': 'gaex0019.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 16', 'class': '', 'id': 'gaex0020', 'href': 'gaex0020.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 17', 'class': '', 'id': 'gaex0021', 'href': 'gaex0021.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 18', 'class': '', 'id': 'gaex0022', 'href': 'gaex0022.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 19', 'class': '', 'id': 'gaex0023', 'href': 'gaex0023.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 20', 'class': '', 'id': 'gaex0024', 'href': 'gaex0024.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 21', 'class': '', 'id': 'gaex0025', 'href': 'gaex0025.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 22', 'class': '', 'id': 'gaex0026', 'href': 'gaex0026.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 23', 'class': '', 'id': 'gaex0027', 'href': 'gaex0027.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 24', 'class': '', 'id': 'gaex0028', 'href': 'gaex0028.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 25', 'class': '', 'id': 'gaex0029', 'href': 'gaex0029.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 26', 'class': '', 'id': 'gaex0030', 'href': 'gaex0030.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 27', 'class': '', 'id': 'gaex0031', 'href': 'gaex0031.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 28', 'class': '', 'id': 'gaex0032', 'href': 'gaex0032.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'CHAPITRE 29', 'class': '', 'id': 'gaex0033', 'href': 'gaex0033.smil#wvbt_0002'},
                {'name': 'h1', 'text': 'ÉPILOGUE', 'class': '', 'id': 'gaex0034', 'href': 'gaex0034.smil#wvbt_0002'}
            ]
        """
        header_list = []
        body = self.document.getElementsByTagName("body")[0]
        for body_element in body.childNodes:
            if body_element.nodeName in NccParser.header_keys:
                class_elt = body_element.getAttribute("class")
                id_elt = body_element.getAttribute("id")
                a = body_element.getElementsByTagName("a")[0]
                href_elt = a.getAttribute("href")
                header_list.append(
                    {
                        "name": body_element.nodeName,
                        "text": NccParser._node_text(a),
                        "class": class_elt,
                        "id": id_elt,
                        "href": href_elt,
                    }
                )
        return header_list

    def body_span(self, header_index):
        """
        Extract span list for one header of known index.
        Parameters:
            header_index: index of header in header_list
        Return:
            List of dictionaries.
        Example:
            [{'name': 'span', 'text': 'Ceux qui rêvent', 'class': 'page-normal', 'id': 'pg_0003', 'href': 'gaex0001.smil#wvbt_0002'}]
        """
        # DP FIXME div tag not handle
        span_list = []
        index = -1
        body = self.document.getElementsByTagName("body")[0]
        for body_element in body.childNodes:
            if index == header_index:
                if body_element.nodeName == "span":
                    class_elt = body_element.getAttribute("class")
                    id_elt = body_element.getAttribute("id")
                    a = self.document.getElementsByTagName("a")[0]
                    href_elt = a.getAttribute("href")
                    span_list.append(
                        {
                            "name": body_element.nodeName,
                            "text": NccParser._node_text(a),
                            "class": class_elt,
                            "id": id_elt,
                            "href": href_elt,
                        }
                    )
            if body_element.nodeName in NccParser.header_keys:
                index += 1
                if index > header_index:
                    break
        return span_list


class MasterSmilParser(Parser):
    def __init__(self):
        super().__init__()

    def meta(self):
        """
        Extract all metadata about the NCC document.
        Return:
            Dictionary of dictionnary with metadata about the NCC document.
        Example:
            {
            'ncc': {'generator': 'Dolphin EasyProducer 2.00 Build 046 + DolphinDaisy 1.01 Build 049', 'timeInThisSmil': '07:45:22.291'},
            'dc': {'format': 'Daisy 2.02', 'title': '9782081230316 Ceux qui rêvent Daisy Audio TTS', 'identifier': 'fr-20130719142517'}
            }
        """
        return super().meta(with_scheme=False)

    def body_ref(self):
        """
        Extract all body ref  about the master.smil document.
        Return:
            List of dictionary.
        Example:
            [
                {'title': 'Ceux qui rêvent', 'src': 'gaex0001.smil#wvbt_0002', 'id': 'smil_0001'},
                {'title': '\xa0', 'src': 'gaex0002.smil#wvbt_0002', 'id': 'smil_0002'},
                 ...
                {'title': 'CHAPITRE 29', 'src': 'gaex0033.smil#wvbt_0002', 'id': 'smil_0033'},
                 {'title': 'ÉPILOGUE', 'src': 'gaex0034.smil#wvbt_0002', 'id': 'smil_0034'}
            ]
        """
        ref_list = []
        body = self.document.getElementsByTagName("body")[0]
        for body_element in body.childNodes:
            if body_element.nodeName == "ref":
                title_elt = body_element.getAttribute("title")
                src_elt = body_element.getAttribute("src")
                id_elt = body_element.getAttribute("id")
                ref_list.append({"title": title_elt, "src": src_elt, "id": id_elt})
        return ref_list


class SmilParser(Parser):
    def __init__(self):
        super().__init__()

    def meta(self):
        """
        Extract all metadata about the smil document.
        Return:
            Dictionary of dictionnary with metadata about the smil document.
        Example:
            {
            'dc': {
                'format': 'Daisy 2.02', 'title': '9782081230316 Ceux qui rêvent Daisy Audio TTS', 'identifier': 'fr-20130719142517'},
                'ncc': {'timeInThisSmil': '00:16:11.234', 'totalElapsedTime': '07:07:11.735',
                'generator': 'Dolphin EasyProducer 2.00 Build 046 + DolphinDaisy 1.01 Build 049'
                }
            '': {'title': 'CHAPITRE 28'}
            }
        """
        # DP FIXME layout tag not handle ?
        return super().meta(with_scheme=False)

    @staticmethod
    def __value_from_clip(clip_string):
        """
        Parse clip_begin or clip_end like 'npt=4.25s"
        """
        match = re.search(r"[-+]?\d*\.?\d+", clip_string)
        clip_value = "0"
        if match:
            clip_value = str(float(match.group()))
        return clip_value

    def body_seq(self):
        """
        Extract all body seq about the smil document.
        Return:
            List of dictionary.
        Example:
            [
                {'duration_value': '3.968', 'duration_unit': 's'})
                {'text_src': '9782081230316_ceux_qui_rvent_dai.html#wvbt_5902', 'text_id': 'wvbt_0242',
                 'audio_src': '32_CHAPITRE_28.mp3', 'clip-begin': 'npt=0.000s', 'clip-end': 'npt=1.632s', 'audio_id': 'audio_0001'},
                {'text_src': '9782081230316_ceux_qui_rvent_dai.html#wvbt_5903', 'text_id': 'wvbt_0243',
                 'audio_src': '32_CHAPITRE_28.mp3', 'clip-begin': 'npt=1.632s', 'clip-end': 'npt=12.831s', 'audio_id': 'audio_0002'},
                ...
                {'text_src': '9782081230316_ceux_qui_rvent_dai.html#wvbt_6141', 'text_id': 'wvbt_0331',
                 'audio_src': '32_CHAPITRE_28.mp3', 'clip-begin': 'npt=965.480s', 'clip-end': 'npt=971.234s', 'audio_id': 'audio_0240'}
            ]
        """
        seq_list = []
        body = self.document.getElementsByTagName("body")[0]
        seq = body.getElementsByTagName("seq")[0]
        duration_str = seq.getAttribute("dur")
        match = re.search(r"[-+]?\d*\.?\d+", duration_str)
        duration_value = "0"
        duration_unit = "s"
        if match:
            duration_value = str(float(match.group()))
            duration_unit = duration_str[match.end() :]
        seq_list.append(
            {"duration_value": duration_value, "duration_unit": duration_unit}
        )
        pars = seq.getElementsByTagName("par")
        for par in pars:
            endsync = par.getAttribute("endsync")
            par_id = par.getAttribute("id")
            par_dict = {"root": {"id": par_id, "endsync": endsync}}
            text = par.getElementsByTagName("text")[0]
            pars_audio = par.getElementsByTagName("audio")
            for par_audio in pars_audio:
                text_attributes = {
                    "text_src": text.getAttribute("src"),
                    "text_id": text.getAttribute("id"),
                    "region": text.getAttribute("region"),
                    "audio_src": par_audio.getAttribute("src"),
                    "clip-begin": SmilParser.__value_from_clip(
                        par_audio.getAttribute("clip-begin")
                    ),
                    "clip-end": SmilParser.__value_from_clip(
                        par_audio.getAttribute("clip-end")
                    ),
                    "audio_id": par_audio.getAttribute("id"),
                }
                seq_list.append(text_attributes)
        return seq_list


class DaisyReader:
    NCC_FILE = "ncc.html"
    MASTER_SMIL_FILE = "master.smil"

    def __init__(self, zip_file_name):
        self.zip_file_name = zip_file_name
        self.ncc_title = None
        self.ncc_meta_dict = None
        self.ncc_header_list = None
        self.ncc_span_list = None
        # Folder container in zip
        self.folder = None
        self.temp_folder = Path(tempfile.mkdtemp(prefix="bsuite_daisy_"))
        logger.info(f"Temp folder: {self.temp_folder}")
        # If this 2 parameters stay to None, it is because master.smil file does not exist in the daisy zip.
        self.master_smil_meta_dict = None
        self.master_smil_ref_list = None

        self.text_tags_dict = None

    def setup(self):
        with zipfile.ZipFile(self.zip_file_name) as zip_file:
            files = zip_file.namelist()
            ncc_file = self.__search_ncc_file(files)
            if ncc_file is None:
                raise DaisyReaderException("ERROR: No ncc file found.")
            self.folder = Path(ncc_file).parent
            # Read ncc file in a buffer with utf-8 encoding.
            ncc_contents = self.__read_file(zip_file, Path(ncc_file))
            ncc_parser = NccParser()
            ncc_parser.parse(ncc_contents)
            self.ncc_title = ncc_parser.title()
            self.ncc_meta_dict = ncc_parser.meta()
            self.ncc_header_list = ncc_parser.body_header()
            self.ncc_span_list = ncc_parser.body_span(2)
            # Read master_smil file.
            try:
                self.master_smil_meta_dict, self.master_smil_ref_list = (
                    self.__read_master_file(zip_file, files)
                )
            except DaisyReaderException:
                self.master_smil_meta_dict, self.master_smil_ref_list = None, None
            self.text_tags_dict = self.__smil_seq_concatenation(zip_file, files)

    def __del__(self):
        if Path(self.temp_folder).exists():
            self.__delete_folder(Path(self.temp_folder))

    @staticmethod
    def daisy_zip_check(zip_file_name):
        """
        Check if a file ncc.html is present in the zip file.
        :param zip_file_name: The zip filename
        :return: True if the ncc.html file exists.
        """
        ncc_file = None
        with zipfile.ZipFile(zip_file_name) as zip_file:
            files = zip_file.namelist()
            ncc_file = DaisyReader.__search_ncc_file(files)
        return ncc_file is not None

    @staticmethod
    def __delete_folder(pth):
        """
        Delete temporary folder
        """
        for sub in pth.iterdir():
            if sub.is_dir():
                DaisyReader.__delete_folder(sub)
            else:
                sub.unlink()
        pth.rmdir()

    def is_text_file(self):
        # if no master.smil file => No text in daisy file (DP FIXME ? to verify)
        return self.master_smil_ref_list is not None

    def properties(self):
        title = self.ncc_title
        creator = identifier = total_time = "?"
        if "identifier" in self.ncc_meta_dict["dc"].keys():
            identifier = self.ncc_meta_dict["dc"]["identifier"][0]
        if "creator" in self.ncc_meta_dict["dc"].keys():
            creator = self.ncc_meta_dict["dc"]["creator"][0]
        if "totalTime" in self.ncc_meta_dict["ncc"].keys():
            total_time = self.ncc_meta_dict["ncc"]["totalTime"][0]
        return {
            "title": title,
            "identifier": identifier,
            "creator": creator,
            "total_time": total_time,
        }

    def mp3_next(self, mp3_file):
        """
        Search the next mp3 file.
        Return: mp3 full file name and time offset or None
        """
        mp3_file = Path(mp3_file).name
        file_found = False
        for tag, zip_mp3 in self.text_tags_dict.items():
            if zip_mp3 is not None:
                zip_mp3_file, time_offset = zip_mp3
                if not file_found:
                    if zip_mp3_file is not None and (zip_mp3_file == mp3_file):
                        file_found = True
                else:
                    if zip_mp3_file is not None and (zip_mp3_file != mp3_file):
                        return zip_mp3_file, time_offset

    # def mp3_previous(self, mp3_file):
    #     """
    #     Search the next mp3 file.
    #     Return: mp3 full file name  or None
    #     """
    #     mp3_file = Path(mp3_file).name
    #     previous_zip_mp3 = None
    #     for tag, zip_mp3 in self.text_tags_dict.items():
    #         if zip_mp3 is not None:
    #             zip_mp3_file, time_offset = zip_mp3
    #             if zip_mp3_file is not None:
    #                 if zip_mp3_file == mp3_file:
    #                     return previous_zip_mp3
    #                 else:
    #                     previous_zip_mp3 = zip_mp3

    def tag_from_offset(self, mp3_file, offset):
        """
        Search the tag for mp3 file and an offset in sec.
        Return: tag or None
        """
        mp3_file = Path(mp3_file).name
        # logger.error(f"{mp3_file=}, {offset=}")
        file_found = False
        previous_tag = None
        for tag, zip_mp3 in self.text_tags_dict.items():
            if zip_mp3 is not None:
                zip_mp3_file, time_offset = zip_mp3
                if zip_mp3_file == mp3_file:
                    if not file_found:
                        if zip_mp3_file is not None and (zip_mp3_file == mp3_file):
                            file_found = True
                    if file_found:
                        if float(time_offset) == float(offset):
                            return tag
                        elif float(time_offset) > float(offset):
                            return previous_tag
                        else:
                            previous_tag = tag
        return previous_tag

    def mp3_from_tag(self, daisy_tag):
        """
        Find the mp3 file and offset in sec. associated to a text tag.
        :param daisy_tag: str
        Return: (mp3 file name, clip begin in sec.) or None
        """
        if daisy_tag in self.text_tags_dict:
            zip_mp3 = self.text_tags_dict[daisy_tag]
            if zip_mp3 is not None:
                zip_mp3_file, time_offset = zip_mp3
                return self.mp3_file_extract(zip_mp3_file), time_offset

    def mp3_file_extract(self, zip_mp3_file):
        (Path(self.temp_folder, self.folder)).mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(self.zip_file_name) as zip_file:
            zip_file.extract(
                Path(self.folder, zip_mp3_file).as_posix(), str(self.temp_folder)
            )
            return Path(self.temp_folder) / Path(self.folder) / Path(zip_mp3_file)

    # def mp3_from_tag(self, daisy_tag):
    # Without self.text_tags_dict
    # with (zipfile.ZipFile(self.zip_file_name) as zip_file):
    #     # Get list of files in zip.
    #     files = zip_file.namelist()
    #     # Get list of smil files
    #     smil_files = self.__search_smil_files(files)
    #     # Return mp3 file corresponding to daisy_tag
    #     zip_mp3 =  self.__find_mp3(zip_file, smil_files, daisy_tag)
    #     if zip_mp3 is not None:
    #         zip_mp3_file, time_offset = zip_mp3
    #         Path(self.temp_folder + '/' + self.folder).mkdir(parents=True, exist_ok=True)
    #         zip_file.extract(self.folder + '/' + zip_mp3_file, str(self.temp_folder))
    #         return self.temp_folder + '/' + self.folder + '/' + zip_mp3_file, time_offset

    def __smil_seq_concatenation(self, zip_file, files):
        text_tags_dict = {}
        # Get list of smil files
        smil_files = self.__search_smil_files(files)
        for smil_file in smil_files:
            smil_contents = self.__read_file(zip_file, smil_file)
            smil_parser = SmilParser()
            smil_parser.parse(smil_contents)
            smil_seq_list = smil_parser.body_seq()
            for index, smil_seq in enumerate(smil_seq_list):
                if (
                    (index != 0)
                    and ("text_src" in smil_seq.keys())
                    and ("audio_src" in smil_seq.keys())
                ):
                    text_tag = smil_seq["text_src"].split("#")[1]
                    if text_tag not in text_tags_dict:
                        text_tags_dict[text_tag] = (
                            smil_seq["audio_src"],
                            smil_seq["clip-begin"],
                        )
        return text_tags_dict

    @staticmethod
    def __read_file(zip_file, filename):
        # Encoding research
        encoding = "utf-8"
        with zip_file.open(str(filename.as_posix())) as readfile:
            data = readfile.read()
            line = data.splitlines()[0]
            match = re.search('encoding="(.+?)"', str(line))
            if match is not None:
                encoding = match.group(1).lower()
                if encoding == "iso-8859-1":
                    encoding = "cp1252"
        # return document string
        return data.decode(encoding)

    def __read_master_file(self, zip_file, files):
        master_smil_file = self.__search_master_smil_file(files)
        if master_smil_file is None:
            raise DaisyReaderException("ERROR: No master.smil file found.")
        master_smil_contents = self.__read_file(zip_file, Path(master_smil_file))
        master_smil_parser = MasterSmilParser()
        master_smil_parser.parse(master_smil_contents)
        master_smil_meta_dict = master_smil_parser.meta()
        master_smil_ref = master_smil_parser.body_ref()
        return master_smil_meta_dict, master_smil_ref

    def read_file(self, append_paragraph):
        """
        Read daisy file.
        Use callback function append_paragraph to register the paragraph tag and paragraph text.
        Return :
        """
        with zipfile.ZipFile(self.zip_file_name) as zip_file:
            files = zip_file.namelist()
            ncc_file = self.__search_ncc_file(files)
            if ncc_file is None:
                raise DaisyReaderException("ERROR: No ncc file found.")
            folder = os.path.dirname(ncc_file)
            try:
                paragraphs = self.__read_html_file(zip_file, folder)
            except DaisyReaderException:
                paragraphs = self.__get_summary_from_ncc()
            for paragraph in paragraphs:
                append_paragraph(paragraph)

    def read_summary(self):
        """
        Return:
             Summary : [ (level, id, text) ]
        """
        return self.__get_summary_from_ncc(with_level=True)

    # Useless : Total duration is in self.ncc_meta_dict['ncc']['totalTime'][0]
    # def total_duration(self):
    #     """
    #     Scan all smil file to compute playing duration.
    #     Return : int in sec.
    #     """
    #
    #     def convert_seconds(seconds):
    #         hours, seconds_remaining = divmod(seconds, 3600)
    #         minutes, seconds = divmod(seconds_remaining, 60)
    #         return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
    #
    #     with (zipfile.ZipFile(self.zip_file_name) as zip_file):
    #         files = zip_file.namelist()
    #         smil_files = self.__search_smil_files(files)
    #         duration = 0.0
    #         unit = 's'
    #         for smil_file in smil_files:
    #             smil_contents = self.__read_file(zip_file, smil_file)
    #             smil_parser = SmilParser()
    #             smil_parser.parse(smil_contents)
    #             smil_seq_list = smil_parser.body_seq()
    #             value, unit = smil_seq_list[0]['duration_value'], smil_seq_list[0]['duration_unit']
    #             duration += float(value)
    #         if unit.lower() == 's':
    #             duration = convert_seconds(duration)
    #     return duration

    def tag_from_smil_name(self, summary_id):
        for item in self.ncc_header_list:
            if item["id"] == summary_id:
                # get smil file
                smil_file = self.extract_file(item, "href")
                with zipfile.ZipFile(self.zip_file_name) as zip_file:
                    smil_contents = self.__read_file(zip_file, smil_file)
                    smil_parser = SmilParser()
                    smil_parser.parse(smil_contents)
                    smil_seq_list = smil_parser.body_seq()
                    return smil_seq_list[1]["text_src"].split("#")[1]

    def __search_text_file(self, zip_file, folder, files):
        if (self.master_smil_ref_list is None) or (len(self.master_smil_ref_list) == 0):
            raise DaisyReaderException("ERROR: master.smil file empty")
        filename, marker = DaisyReader.__unpack_smil_text_arg(
            self.master_smil_ref_list[0]["src"]
        )
        smil_file = Path(folder) / Path(filename)
        smil_contents = self.__read_file(zip_file, smil_file)
        smil_parser = SmilParser()
        smil_parser.parse(smil_contents)
        smil_seq_list = smil_parser.body_seq()
        if len(smil_seq_list) < 2:
            raise DaisyReaderException("ERROR: invalid smil body")
        return smil_seq_list[1]["text_src"]

    def __get_summary_from_ncc(self, with_level=False):
        paragraphs = []
        for item in self.ncc_header_list:
            if with_level:
                paragraph = (item["name"], item["id"], str(item["text"]))
            else:
                paragraph = (item["id"], str(item["text"]))
            paragraphs.append(paragraph)
        return paragraphs

    def __read_html_file(self, zip_file, folder):
        text_file = self.__search_text_file(zip_file, folder, self.master_smil_ref_list)
        html_text_file, marker = DaisyReader.__unpack_smil_text_arg(text_file)
        if html_text_file == DaisyReader.NCC_FILE:
            raise DaisyReaderException("ERROR: Text file is ncc.html")
        html_text_file = Path(folder) / Path(html_text_file)
        html_contents = self.__read_file(zip_file, html_text_file)
        html_text = HTML2Text().handle(html_contents)
        # Concate sentence segment.
        current_tag = None
        text_concatenation = ""
        paragraphs = []
        previous_empty = False
        for text in html_text:
            text_tag, text_content = text
            # logging.critical(f"{text_tag}: {text_content}")
            if text_tag is not None:
                current_tag = text_tag
            text_seg = text_content.split("\n")
            for text in text_seg:
                if len(text) > 0:
                    paragraphs.append((current_tag, text))
                    previous_empty = False
                elif not previous_empty:
                    paragraphs.append((None, text))
                    previous_empty = True
        return paragraphs

    def inspect(self):
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>> NCC file")
        logger.info(f"{self.ncc_title=}")
        logger.info("self.ncc_meta_dict=")
        for dico in self.ncc_meta_dict.items():
            logger.info(dico)
        logger.info(f"{self.ncc_header_list=}")
        for item in self.ncc_header_list:
            logger.info(item)
        logger.info("self.ncc_span_list=")
        for item in self.ncc_span_list:
            logger.info(item)
        # Read master_smil file.
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>> master.smil file")
        logger.info("self.master_smil_meta_dict=")
        if self.master_smil_meta_dict is None:
            logger.warning("No master.smil file")
        else:
            for dico in self.master_smil_meta_dict.items():
                logger.info(dico)
        logger.info("self.master_smil_ref_list=")
        if self.master_smil_ref_list is None:
            logger.warning("No master.smil file")
        else:
            for item in self.master_smil_ref_list:
                logger.info(item)

        # log ordered smil files
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>> smil files list")
        with zipfile.ZipFile(self.zip_file_name) as zip_file:
            files = zip_file.namelist()
            smil_files = self.__search_smil_files(files)
            for smil_file in smil_files:
                logger.info(smil_file)

        for key, value in self.text_tags_dict.items():
            logger.info(f"{key}: {value}")
        return
        mp3_files = self.mp3_from_tag("wvbt_0007")
        logger.info(f"mp3_files={mp3_files}")

        # Find the smil files.
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>> smil file example")
        with zipfile.ZipFile(self.zip_file_name) as zip_file:
            files = zip_file.namelist()
            smil_files = self.__search_smil_files(files)

            logger.critical(f"{smil_files=}")
            smil_contents = self.__read_file(zip_file, smil_files[0])
            smil_parser = SmilParser()
            smil_parser.parse(smil_contents)
            logger.info(f">>>>>>>>>>>>>>>>>>>>>>>> {smil_files[0]} meta")
            smil_meta_dict = smil_parser.meta()
            for item in smil_meta_dict:
                logger.info(item)
            logger.info(f">>>>>>>>>>>>>>>>>>>>>>>> {smil_files[0]} seq_list")
            smil_seq_list = smil_parser.body_seq()
            for item in smil_seq_list:
                logger.info(item)

        # Read one smil file.
        with zipfile.ZipFile(self.zip_file_name) as zip:
            files = zip.namelist()
            ncc_file = DaisyReader.__search_ncc_file(files)
            if ncc_file is None:
                raise DaisyReaderException("ERROR: No ncc file found.")

            logger.info(">>>>>>>>>>>>>>>>>>>>>>>> gaex0032.smil file example")
            folder = os.path.dirname(ncc_file)
            smil_file = folder + "/gaex0032.smil"
            logger.info(f"{smil_file=}")
            smil_contents = self.__read_file(zip, smil_file)
            smil_parser = SmilParser()
            smil_parser.parse(smil_contents)
            smil_meta_dict = smil_parser.meta()
            logger.info(f"{smil_meta_dict=}")
            smil_seq_list = smil_parser.body_seq()
            logger.info(f"{smil_seq_list=}")
        #
        #     # Read HTML text file.
        #     logger.info(">>>>>>>>>>>>>>>>>>>>>>>> html text file")
        #     paragraphs = self.__read_html_file(zip, folder)
        #     for index, text in enumerate(paragraphs):
        #         logger.info(text)
        #         if index > 30:
        #             break

    @staticmethod
    def __unpack_smil_text_arg(smil_text_arg):
        text_segments = smil_text_arg.split("#")
        if len(text_segments) != 2:
            raise DaisyReaderException("ERROR: invalid text arg in smil")
        return text_segments[0], text_segments[1]

    @staticmethod
    def __search_ncc_file(files):
        """
        Search the Navigation Control Center in files list.
        """
        for file in files:
            if file.lower().endswith(DaisyReader.NCC_FILE):
                logger.info(file)
                return file

    @staticmethod
    def __search_master_smil_file(files):
        """
        Search the Navigation Control Center in files list.
        Param: files - List of files in the zip.
        Return : complete file name.
        """
        for file in files:
            if file.lower().endswith(DaisyReader.MASTER_SMIL_FILE):
                logger.info(file)
                return file

    def extract_file(self, smil_item, key):
        smil_file = smil_item[key].split("#")[0]
        return Path(self.folder) / Path(smil_file)

    def __search_smil_files(self, files):
        """
        Construct a list of all smil file except master.smil.
        Return: list of complete file names.
        """
        # return [file for file in files if file.lower().endswith(".smil") and not file.lower().endswith("master.smil")]
        smil_files = []
        if self.master_smil_ref_list is None:
            # Extract smil from ncc.html
            for item in self.ncc_header_list:
                smil_files.append(self.extract_file(item, "href"))
        else:
            # Extract smil from master.smil
            for item in self.master_smil_ref_list:
                smil_files.append(self.extract_file(item, "src"))
        return smil_files

    def __find_mp3(self, zip_file, smil_files, daisy_tag):
        for smil_file in smil_files:
            smil_contents = self.__read_file(zip_file, smil_file)
            smil_parser = SmilParser()
            smil_parser.parse(smil_contents)
            smil_seq_list = smil_parser.body_seq()
            for index, smil_seq in enumerate(smil_seq_list):
                logger.info(f"Processing {smil_seq}")
                if (
                    (index != 0)
                    and ("text_src" in smil_seq.keys())
                    and (smil_seq["text_src"].split("#")[1] == daisy_tag)
                ) and ("audio_src" in smil_seq.keys()):
                    return smil_seq["audio_src"], smil_seq["clip-begin"]
        raise DaisyReaderException(f"no daisy tag found {daisy_tag}")


# logger.info("Start")
# zip_file = "A_Ceux_qui_revent.zip"
#
# reader = DaisyReader(zip_file)
# reader.inspect()

# with zipfile.ZipFile(zip_file, 'r') as zip:
#     files = zip.namelist()
#     for file in files:
#         logger.info(file)
#         file_info = zip.getinfo(file)
#         logger.info(file_info)
