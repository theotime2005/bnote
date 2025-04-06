"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import json
import glob
import os
from bnote.debug.colored_log import ColoredLogger, WAVE_LOG

log = ColoredLogger(__name__)
log.setLevel(WAVE_LOG)


class Wave:
    def __init__(self):
        self.lang_voice_id = None

    def supported_languages(self):
        """
        gat a list of supported languages ["en_US", "fr_FR"...]
        """
        return self.lang_voice_id.keys()

    def voices_for_language(self, language):
        """
        get a list of tupple ((gender, voice_id), ...)
        """
        if language in self.lang_voice_id.keys():
            voices = self.lang_voice_id[language]
            return voices

    def convert_to_wave(
        self, text_to_speak, language, voice, file_name, speed, volume=None
    ):
        if language in self.lang_voice_id:
            if voice is None:
                # By default, take first voice.
                voice = self.lang_voice_id[language][0][1]
            self.to_wave(text_to_speak, language, voice, file_name, speed, volume)

    def to_wave(self, text_to_speak, language, voice, file_name, speed, volume):
        raise NotImplementedError


class PicoWave(Wave):

    def __init__(self):
        super().__init__()
        self.lang_voice_id = {
            "en_US": (("M", "en-US"),),
            "en_GB": (("M", "en-GB"),),
            "fr_FR": (("M", "fr-FR"),),
            "es_ES": (("M", "es-ES"),),
            "de_DE": (("M", "de-DE"),),
            "it_IT": (("M", "it-IT"),),
        }

    def to_wave(self, text_to_speak, language, voice, file_name, speed, volume):
        if volume is None:
            volume = 120
        process = os.popen(
            "pico2wave -l {} -w {} '{}'".format(
                voice,
                file_name,
                self.__effect(text_to_speak, volume=volume, speed=speed),
            )
        )
        # Wait execution
        process.read()

    @staticmethod
    def __effect(text, speed=100, pitch=100, volume=120):
        _speed = '<speed level="%s">%s</speed>' % (speed, text)
        _pitch = '<pitch level="%s">%s</pitch>' % (pitch, _speed)
        return '<volume level="%s">%s</volume>' % (volume, _pitch)


class ESpeakWave(Wave):
    def __init__(self):
        super().__init__()
        # cf http://espeak.sourceforge.net/languages.html
        self.lang_voice_id = {
            "ar_LB": (("M", "ar"),),
            "cs_CZ": (("M", "cs"),),
            "da_DK": (("M", "da"),),
            "de_CH": (("M", "de"),),
            "de_DE": (("M", "de"),),
            "el_GR": (("M", "el"),),
            "en_GB": (("M", "en"),),
            "en_US": (("M", "en-us"),),
            "es_ES": (("M", "es"),),
            "fr_CH": (("M", "fr"),),
            "fr_FR": (("M", "fr"),),
            # "he_IL": _("Hebrew (Israel)"),
            "hr_HR": (("M", "hr"),),
            "it_CH": (("M", "it"),),
            "it_IT": (("M", "it"),),
            "is_IS": (("M", "is"),),
            #  "lt_LT": _("Lithuanian (Lituania)"),
            "nb_NO": (("M", "no"),),
            "nl_BE": (("M", "nl"),),
            "nl_NL": (("M", "nl"),),
            "pl_PL": (("M", "pl"),),
            "pt_PT": (("M", "pt"),),
            "ru_RU": (("M", "ru"),),
            "sk_SK": (("M", "sk"),),
            "sl_SI": (("M", "sk"),),
            "sv_SE": (("M", "sv"),),
            "af_ZA": (("M", "af"),),
            #  "xh_ZA": (("M", "af"),), (Xhosa (South Africa))
            #  "zu_ZA": (("M", "af"),), (Zulu (South Africa))
            "sw_KE": (("M", "sw"),),
        }

    def to_wave(self, text_to_speak, language, voice, file_name, speed, volume):
        if volume is None:
            volume = 200
        process = os.popen(
            "espeak-ng -s {} -a {} -v {} '{}' -w {} 2>/dev/null".format(
                speed, volume, voice, text_to_speak, file_name
            )
        )
        # Wait execution
        process.read()


class MBrolaWave(Wave):
    def __init__(self):
        super().__init__()
        # cf https://github.com/numediart/MBROLA-voices
        self.lang_voice_id = {
            "ar_LB": (("M", "ar1"), ("M", "ar2")),
            "cs_CZ": (("F", "cz1"), ("M", "cz2")),
            # "da_DK": "da",
            "de_CH": (
                ("F", "de1"),
                ("M", "de2"),
                ("F", "de3"),
                ("M", "de4"),
                ("F", "de5"),
                ("M", "de6"),
                ("F", "de7"),
                ("M", "de8"),
            ),
            "de_DE": (
                ("F", "de1"),
                ("M", "de2"),
                ("F", "de3"),
                ("M", "de4"),
                ("F", "de5"),
                ("M", "de6"),
                ("F", "de7"),
                ("M", "de8"),
            ),
            "el_GR": (("M", "gr1"), ("M", "gr2")),
            "en_GB": (("M", "en1"),),
            "en_US": (("F", "us1"), ("M", "us2"), ("M", "us3")),
            "es_ES": (("M", "es1"), ("M", "es2"), ("F", "es3"), ("M", "es4")),
            "fr_CH": (
                ("M", "fr1"),
                ("F", "fr2"),
                ("M", "fr3"),
                ("M", "fr3"),
                ("F", "fr4"),
                ("M", "fr5"),
                ("M", "fr6"),
                ("M", "fr7"),
            ),
            "fr_FR": (
                ("M", "fr1"),
                ("F", "fr2"),
                ("M", "fr3"),
                ("M", "fr3"),
                ("F", "fr4"),
                ("M", "fr5"),
                ("M", "fr6"),
                ("M", "fr7"),
            ),
            "he_IL": (("M", "hb1"), ("F", "hb2")),
            "hr_HR": (("M", "cr1"),),
            "it_CH": (("M", "it1"), ("F", "it2"), ("M", "it3"), ("F", "it4")),
            "it_IT": (("M", "it1"), ("F", "it2"), ("M", "it3"), ("F", "it4")),
            "is_IS": (("M", "ic1"),),
            "lt_LT": (("M", "lt1"), ("M", "lt2")),
            # "nb_NO": "no",
            "nl_BE": (("M", "nl1"), ("M", "nl2"), ("F", "nl3")),
            "nl_NL": (("M", "nl1"), ("M", "nl2"), ("F", "nl3")),
            "pl_PL": (("F", "pl1"),),
            "pt_PT": (
                ("F", "pt1"),
                ("M", "br1"),
                ("M", "br2"),
                ("M", "br3"),
                ("F", "br4"),
            ),
            # "ru_RU": "ru",
            # "sl_SI": "sk",
            "sv_SE": (("M", "sw1"), ("F", "sw2")),
            "af_ZA": (("M", "af1"),),
            # "xh_ZA": "af", (Xhosa (South Africa))
            # "zu_ZA": "af", (Zulu (South Africa))
            # "sw_KE": "sw",
        }

    def to_wave(self, text_to_speak, language, voice, file_name, speed, volume):
        if volume is None:
            volume = 200
            process = os.popen(
                "espeak-ng -s {} -a {} -v mb/mb-{} '{}' -w {} 2>/dev/null".format(
                    speed, volume, voice, text_to_speak, file_name
                )
            )
            # Wait execution
            process.read()


class CerenceWave(Wave):
    PROMPTER_BASE_DIR = "/usr/local/bin"
    PROMPTER_CONFIG_DIR = "/usr/local/lib/cerence/voices/config"
    PROMPTER_CONFIG_FILE = PROMPTER_CONFIG_DIR + "/" + "prompterconfig.json"
    PROMPTER_VOICE_DIR = "/usr/local/lib/cerence/voices/vocalizer/languages"

    json_config = {}
    try:
        with open(PROMPTER_CONFIG_FILE, "r") as json_file:
            json_config = json.load(json_file)
    except FileNotFoundError as exception:
        log.error(f"{exception=}")
        log.error("Use default values")
        pass
    except json.JSONDecodeError as exception:
        log.error(f"{exception=}")
        log.error("Use default values")
        pass

    def __init__(self):
        super().__init__()
        # Le nom de la voix doit correspondre au 'useCaseName' passé en paramètre à prompter_to_wave.
        # Ce useCaseName est utilisé dans prompterconfig.json pour définir une voix.
        self.lang_voice_id = {
            "ar_LB": (
                ("F", "laila"),
                ("M", "maged"),
                ("F", "mariam"),
                ("M", "tarik"),
            ),
            "cs_CZ": (
                ("F", "iveta"),
                ("F", "zuzana"),
            ),
            "da_DK": (
                ("M", "magnus"),
                ("F", "sara"),
            ),
            "de_DE": (
                ("F", "anna"),
                ("M", "markus"),
                ("F", "petra"),
                ("M", "yannick"),
            ),
            "el_GR": (
                ("F", "melina"),
                ("M", "nikos"),
            ),
            "en_GB": (
                ("M", "daniel"),
                ("F", "kate"),
                ("M", "malcolm"),
                ("M", "oliver"),
                ("F", "serena"),
                ("F", "stephanie"),
            ),
            "en_US": (
                ("F", "allison"),
                ("F", "ava"),
                ("M", "evan"),
                ("M", "nathan"),
                ("F", "samantha"),
                ("F", "susan"),
                ("M", "tom"),
                ("F", "zoe"),
            ),
            "es_ES": (
                ("M", "jorge"),
                ("F", "marisol"),
                ("F", "monica"),
            ),
            "fr_FR": (
                ("F", "audrey"),
                ("F", "aurélie"),
                ("M", "thomas"),
            ),
            "he_IL": (("F", "carmit"),),
            "hr_HR": (("F", "lana"),),
            # "is_IS": (("M", ""),),
            "it_IT": (
                ("F", "alice"),
                ("F", "emma"),
                ("M", "luca"),
                ("F", "paola"),
            ),
            # "lt_LT": (("M", ""),),
            "nb_NO": (
                ("M", "henrik"),
                ("F", "nora"),
            ),
            "nl_BE": (("F", "ellen"),),
            "nl_NL": (
                ("F", "claire"),
                ("M", "xander"),
            ),
            "pl_PL": (
                ("F", "ewa"),
                ("M", "krzysztof"),
                ("F", "zosia"),
            ),
            "pt_PT": (
                ("F", "catarina"),
                ("F", "joana"),
                ("M", "joaquim"),
            ),
            # "ru_RU": (("M", ""),),
            "sl_SI": (("F", "tina"),),
            "sv_SE": (
                ("F", "alva"),
                ("F", "klara"),
                ("M", "oskar"),
            ),
            # "af_ZA": (("M", ""),),
            # "xh_ZA": (("M", ""),), #(Xhosa (South Africa))
            # "zu_ZA": (("M", ""),), #(Zulu (South Africa))
            # "sw_KE": (("M", ""),),
        }

    def to_wave(self, text_to_speak, language, voice, file_name, speed, volume):
        # Do not try to speak if the voice is not installed.
        if self.is_voice_installed(voice):

            # Construct the command line
            # prompter_to_wave --speedRate=150 --useCaseName="audrey" --textToSpeak="bonjour il fait beau" --audioScenario=file --configDir="/usr/local/lib/cerence/voices/config"
            # export LD_LIBRARY_PATH="/usr/local/openssl-1.1.1/lib:/usr/local/lib/cerence:$LD_LIBRARY_PATH" && prompter_to_wave --speedRate=150 --useCaseName="audrey" --textToSpeak="bonjour il fait beau" --audioScenario=file --configDir="/usr/local/lib/cerence/voices/config"
            command_line = 'export LD_LIBRARY_PATH="/usr/local/openssl-1.1.1/lib:/usr/local/lib/cerence:$LD_LIBRARY_PATH" && prompter_to_wave --useCaseName="{}" --textToSpeak="{}" --audioScenario=file --configDir="{}" --speedRate={}'.format(
                voice, text_to_speak, CerenceWave.PROMPTER_CONFIG_DIR, speed
            )

            # Convert the text into wave file.
            process = os.popen(command_line)

            # Wait execution
            process.read()

    # Return True if the voice can be found as 'usecase' in the json config and if an associated
    # .dat file exists.
    def is_voice_installed(self, voice):
        """
        exemple for the input
        voice='thomas'
        usecase={'name': 'thomas', 'type': 'local', 'local': {'voice_config': {'uses': 'vc_thomas'}, 'enabled_markers': 'textunit, word'}}
        voice_type={'voice_config': {'uses': 'vc_thomas'}, 'enabled_markers': 'textunit, word'}
        voice_type['voice_config']['uses']='vc_thomas'
        voice_config={'name': 'vc_thomas', 'language': 'frf', 'voice': 'thomas', 'operating_point': 'embedded-high'}
        file_name_pattern='/usr/local/lib/cerence/voices/vocalizer/languages/frf/speech/components/frf_thomas_embedded-high_*.dat'
        ['/usr/local/lib/cerence/voices/vocalizer/languages/frf/speech/components/frf_thomas_embedded-high_3-0-0.dat']
        """
        voice_config_name = None
        if "usecase" in CerenceWave.json_config:
            for usecase in CerenceWave.json_config["usecase"]:
                if "name" in usecase and usecase["name"] == voice:
                    if "type" in usecase and usecase["type"] == "local":
                        if "local" in usecase:
                            voice_type = usecase["local"]
                            # print(f"{voice_type=}")
                            if (
                                "voice_config" in voice_type
                                and "uses" in voice_type["voice_config"]
                            ):
                                voice_config_name = voice_type["voice_config"]["uses"]

        if "voice_config" in CerenceWave.json_config:
            for voice_config in CerenceWave.json_config["voice_config"]:
                if "name" in voice_config and voice_config["name"] == voice_config_name:
                    file_name_pattern = "".join(
                        (
                            CerenceWave.PROMPTER_VOICE_DIR,
                            "/",
                            voice_config["language"],
                            "/",
                            "speech/components/",
                            voice_config["language"],
                            "_",
                            voice_config["voice"],
                            "_",
                            voice_config["operating_point"],
                            "_*.dat",
                        )
                    )
                    if len(glob.glob(file_name_pattern)):
                        return True

        return False
