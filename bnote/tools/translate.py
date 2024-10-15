"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""
import gettext
from pathlib import Path
import re
import locale
import sys

from apps.fman.file_manager import BNOTE_FOLDER, DOCUMENTS_FOLDER
from tools.singleton_meta import SingletonMeta

from debug.colored_log import ColoredLogger, TRANSLATE_LOG

log = ColoredLogger(__name__)
log.setLevel(TRANSLATE_LOG)


class Translate(metaclass=SingletonMeta):
    # https://docs.microsoft.com/en-us/openspecs/office_standards/ms-oe376/6c085406-a698-4e12-9d4d-c3b0ee3dbc4a
    bcp47_to_language_code_dict = {
        "ar_LB": ("3001",),
        "cs_CZ": ("405",),
        "da_DK": ("406",),
        "de_CH": ("807",),
        "de_DE": ("407",),
        "el_GR": ("408",),
        "en_GB": ("809",),
        "en_US": ("409",),
        "es_ES": ("40A", "C0A"),
        "fr_CH": ("100C",),
        "fr_FR": ("40C",),
        "he_IL": ("40D",),
        "hr_HR": ("41A",),
        "it_CH": ("810",),
        "it_IT": ("410",),
        "lt_LT": ("427",),
        "nb_NO": ("414",),
        "nl_BE": ("813",),
        "nl_NL": ("413",),
        "pl_PL": ("415",),
        "pt_PT": ("816",),
        "ru_RU": ("419",),
        "sl_SI": ("424",),
        "sv_SE": ("41D",),
    }

    # The languages code that bsuite knows and it associated user message
    languages_dict = {"ar_LB": "Arabic (Lebanon)",
                      "cs_CZ": "Czech (Czech Republic)",
                      "da_DK": "Danish (Denmark)",
                      "de_CH": "German (Switzerland)",
                      "de_DE": "German (Germany)",
                      "el_GR": "Greek (Greece)",
                      "en_GB": "English (United Kingdom)",
                      "en_US": "English (United States)",
                      "es_ES": "Spanish (Spain)",
                      "fr_CH": "French (Switzerland)",
                      "fr_FR": "French (France)",
                      "he_IL": "Hebrew (Israel)",
                      "hr_HR": "Croatian (Croatia)",
                      "it_CH": "Italian (Switzerland)",
                      "it_IT": "Italiano (Italy)",
                      "is_IS": "Islandic (Island)",
                      "lt_LT": "Lithuanian (Lituania)",
                      "nb_NO": "Norwegian (Norway)",
                      "nl_BE": "Dutch (Belgium)",
                      "nl_NL": "Dutch (Netherlands)",
                      "pl_PL": "Polish (Poland)",
                      "pt_PT": "Portuguese (Portugal)",
                      "ru_RU": "Russian (Russia)",
                      "sl_SI": "Slovenian (Slovenia)",
                      "sv_SE": "Swedish (Sweden)",
                      "af_ZA": "Afrikaans (South Africa)",
                      "xh_ZA": "Xhosa (South Africa)",
                      "zu_ZA": "Zulu (South Africa)",
                      "sw_KE": "Swahili (Kenya)",
                      "bu_US": "Unified braille (United States)",
                      "eo_ES": "Esperanto braille",
                      }

    def __init__(self):
        self.translate = None

    def gettext(self, message):
        return self.translate.gettext(message)

    def install_translation(self, language_country: str, translation_folder=None):
        try:
            log.info("language_country={}".format(language_country))

            user_translation_folder = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER) / Path("")
            user_file = user_translation_folder / Path("bnote_{}.mo".format(language_country))
            with user_file.open(mode="rb") as user_translation_file:
                user_translation = gettext.GNUTranslations(user_translation_file)
            # Installe self.gettext() dans l'espace de nom intégré et le lie à _()
            user_translation.install()
            self.translate = user_translation

            # Set the locale according to the wanted language.
            log.info("current locale is : locale.getlocale() returns {}".format(locale.getlocale()))
            locale.setlocale(locale.LC_ALL, (language_country, "UTF-8"))
            return
        except locale.Error:
            log.error("The language {} mut be installed on the computer to use it as locale".format(language_country))
            log.error("It can be installed with :")
            log.error("sudo apt-get install locales-all")
            return
        except IOError:
            pass

        try:
            if translation_folder is None:
                translation_folder = Path(sys.path[0]) / Path("translation")

            file = translation_folder / Path("bnote_{}.mo".format(language_country))
            log.info("file={}".format(file))

            # Create toto.txt file
            with file.open(mode="rb") as translation_file:
                translation = gettext.GNUTranslations(translation_file)
            # Installe self.gettext() dans l'espace de nom intégré et le lie à _()
            translation.install()
            self.translate = translation

            # Set the locale according to the wanted language.
            log.info("current locale is : locale.getlocale() returns {}".format(locale.getlocale()))
            locale.setlocale(locale.LC_ALL, (language_country, "UTF-8"))
            log.info("new current locale is : locale.getlocale() returns {}".format(locale.getlocale()))
        except locale.Error:
            log.error("The language {} mut be installed on the computer to use it as locale".format(language_country))
            log.error("It can be installed with :")
            log.error("sudo apt-get install locales-all")
            pass
        except IOError:
            log.error("IOError using file {}".format(file))
            translation = gettext.NullTranslations()
            translation.install()
            self.translate = translation
            pass

    @staticmethod
    def availables_translations(translation_folder=None):
        languages = []
        lang_pattern = re.compile("bnote_(.*).mo")

        user_translation_folder = BNOTE_FOLDER / Path(DOCUMENTS_FOLDER) / Path("")
        user_mo_files = user_translation_folder.glob("bnote_*.mo")
        for file in user_mo_files:
            result = re.search(lang_pattern, file.name)
            if result:
                languages.append(result.group(1))

        if translation_folder is None:
            translation_folder = Path(sys.path[0]) / Path("translation")
        mo_files = translation_folder.glob("bnote_*.mo")
        for file in mo_files:
            result = re.search(lang_pattern, file.name)
            if result:
                if not (result.group(1) in languages):
                    languages.append(result.group(1))

        return languages


_ = Translate().gettext
