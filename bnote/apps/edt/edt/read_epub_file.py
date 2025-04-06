"""
bnote project
Author : Eurobraille
Date : 2024-07-16
Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, Comment

# Setup the logger for this file
from .colored_log import ColoredLogger, READ_EPUB_FILE_LOG, logging

log = ColoredLogger(__name__, level=READ_EPUB_FILE_LOG)

# Installer depuis pycharm File>Settings>Project>Python interpreter: EbookLib et bs4
# Installer en ligne de commande BeautifulSoup
# fm@esys-inspiron-5720:~/.pyenv/versions/3.8.4/bin$ ./pip3.8 install beautifulsoup4

#  This code comes from https://medium.com/@zazazakaria18/turn-your-ebook-to-text-with-python-in-seconds-2a1e42804913


class ReadEpubFile:
    blacklist = [
        "[document]",
        "noscript",
        "header",
        "html",
        "meta",
        "head",
        "input",
        "script",
    ]

    def __init__(self, full_file_name):
        self._full_file_name = full_file_name

    def read_file(self, append_paragraph):
        book = epub.read_epub(self._full_file_name)
        chapters = []
        # Build a dict with item's id as key and item's content as value
        chapters_dict = {}
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters_dict[item.get_id()] = item.get_content()

        # book.spine décrit l'ordre d'apparition des différents éléments dans le livre
        for spine in book.spine:
            if spine[0] in chapters_dict:
                chapters.append(chapters_dict[spine[0]])

        for html in chapters:
            soup = BeautifulSoup(html, "html.parser")
            with_marker = True

            # First : remove the comments (<!--   -->)
            comments = soup.findAll(text=lambda text: isinstance(text, Comment))
            [comment.extract() for comment in comments]

            # Get all the text
            all_text = soup.find_all(text=True)

            line_parts = []
            for t in all_text:
                if t.parent.name not in ReadEpubFile.blacklist:
                    if READ_EPUB_FILE_LOG <= logging.DEBUG:
                        log.debug("t = <{}>".format(t))
                    if t == "\n":
                        # Joindre avec un " " génère parfois trop d'espace mais c'est mieux que d'avoir
                        # des mots qui sont collés les uns au autre dans certains ouvrages.
                        line = " ".join(line_parts)
                        # Remplace espace insécable par espace classique
                        line = line.replace("\xa0", " ")
                        # Remplace '\n' au sein du texte par espace classique.
                        line = line.replace("\n", " ")
                        # Certain epub ont déja des espaces de part et d'autre des morceaux de textes, d'autre pas...
                        while line.find("  ") != -1:
                            line = line.replace("  ", " ")
                        if READ_EPUB_FILE_LOG <= logging.DEBUG:
                            log.debug("line_parts=<{}>".format(line_parts))
                            log.debug("line=<{}>".format(line))
                        # Ignore les lignes vides
                        if len(line):
                            append_paragraph(line, with_marker)
                            with_marker = False
                        line_parts = []
                    else:
                        line_parts.append("{}".format(t))
