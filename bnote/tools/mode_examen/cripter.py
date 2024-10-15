"""
This script can be cript and decript a character string
"""

from random import randint

def encript(txt):
    """
    Encode the character string and return the character string encoding
    """
    txt_convert=txt[0]
    for index in range(1,len(txt)-1):
        character=txt[index]
        number=randint(0,9)
        new_character=chr(ord(character)+number)+str(number)
        txt_convert+=new_character
    txt_convert+=txt[-1]
    # On fait attention aux guillemets qui peuvent s'être glissées par là
    for index in range(len(txt_convert)):
        if txt_convert[index]=='"':
            txt_convert[index]="'"
            txt_convert[index+1]=34
    return txt_convert

def decript(txt):
    """
    Uncript the content of character string
    """
    txt_convert=txt[0]
    for index in range(1,len(txt)-1):
        if index%2!=0:
            number=int(txt[index+1])
            character=chr(ord(txt[index])-number)
            txt_convert+=character
    txt_convert+=txt[-1]
    return txt_convert