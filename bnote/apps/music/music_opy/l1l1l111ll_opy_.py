#! /usr/bin/python
license = (
'''_opy_Copyright 2014, 2015, 2016, 2017, 2018 Jacques de Hooge, GEATEC engineering, www.geatec.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''
)
import re
import os
import sys
import errno
import keyword
import importlib
import random
import codecs
import shutil
# =========== l1111l1l1_opy_ l1l1l111l1_opy_
l1l1l11lll_opy_ = sys.version_info [0] == 2
if l1l1l11lll_opy_:
    import __builtin__ as l111111ll_opy_
else:
    import builtins as l111111ll_opy_
l1ll1ll1ll_opy_ = 'opy'
l1ll1lllll_opy_ = '1.1.29'
random.seed ()
l1lll11111_opy_ = 2048
l1ll1111l1_opy_ = l1lll11111_opy_
l111l11l1_opy_ = 7
print ('{} (TM) Configurable Multi Module Python Obfuscator Version {}'.format (l1ll1ll1ll_opy_.capitalize (), l1ll1lllll_opy_))
print ('Copyright (C) Geatec Engineering. License: Apache 2.0 at  http://www.apache.org/licenses/LICENSE-2.0\n')
def l1l1l111ll_opy_(args=sys.argv):
    global l1ll1l1111_opy_
    global l1ll1111l1_opy_
    global l1l1l1l111_opy_
    global l1l1l11l11_opy_
    def l1l1l1l1l1_opy_ (l11ll111l_opy_, open = False):
        try:
            os.makedirs (l11ll111l_opy_.rsplit ('/', 1) [0])
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        if open:
            return codecs.open (l11ll111l_opy_, encoding = 'utf-8', mode = 'w')
    def l1ll1l1l11_opy_ (l1llll11ll_opy_, name):
        return '{0}{1}{2}'.format (
            '__' if name.startswith ('__') else '_' if name.startswith ('_') else 'l',
            bin (l1llll11ll_opy_) [2:] .replace ('0', 'l'),
            l111ll1ll_opy_
        )
    def l111llll1_opy_ (l11ll1l1l_opy_):
        global l1ll1111l1_opy_
        if l1l1l11lll_opy_:
            l1l1ll11ll_opy_ = l1ll11111l_opy_ () .join ([l1l1l1ll11_opy_ (l1lll11111_opy_ + ord (char) + (l11111lll_opy_ + l1ll1111l1_opy_) % l111l11l1_opy_) for l11111lll_opy_, char in enumerate (l11ll1l1l_opy_)])
            l1lllll11l_opy_ = l1l1l1ll11_opy_ (l1ll1111l1_opy_)
        else:
            l1l1ll11ll_opy_ = str () .join ([chr (l1lll11111_opy_ + ord (char) + (l11111lll_opy_ + l1ll1111l1_opy_) % l111l11l1_opy_) for l11111lll_opy_, char in enumerate (l11ll1l1l_opy_)])
            l1lllll11l_opy_ = chr (l1ll1111l1_opy_)
        l1l1lll111_opy_ = l1ll1111l1_opy_ % len (l11ll1l1l_opy_)
        l1l1llll1l_opy_ = l1l1ll11ll_opy_ [:-l1l1lll111_opy_] + l1l1ll11ll_opy_ [-l1l1lll111_opy_:]
        l11l1ll1l_opy_ = l1l1llll1l_opy_ + l1lllll11l_opy_
        l1ll1111l1_opy_ += 1
        return 'u"' + l11l1ll1l_opy_ + '"'
    def l1lll1l1ll_opy_ (l1111l11l_opy_):
        return '''
import sys
isPython2{0} = sys.version_info [0] == 2
charBase{0} = {1}
charModulus{0} = {2}
def unScramble{0} (keyedStringLiteral):
    global stringNr{0}
    stringNr = ord (keyedStringLiteral [-1])
    rotatedStringLiteral = keyedStringLiteral [:-1]
    rotationDistance = stringNr % len (rotatedStringLiteral)
    recodedStringLiteral = rotatedStringLiteral [:rotationDistance] + rotatedStringLiteral [rotationDistance:]
    if isPython2{0}:
        stringLiteral = unicode () .join ([unichr (ord (char) - charBase{0} - (charIndex + stringNr) % charModulus{0}) for charIndex, char in enumerate (recodedStringLiteral)])
    else:
        stringLiteral = str () .join ([chr (ord (char) - charBase{0} - (charIndex + stringNr) % charModulus{0}) for charIndex, char in enumerate (recodedStringLiteral)])
    return eval (stringLiteral)
    '''.format (l1111llll_opy_, l1lll11111_opy_, l111l11l1_opy_)
    def l1llll1l1l_opy_ (l1ll111l1l_opy_):
        print (r'''
===============================================================================
{0} will obfuscate your extensive, real world, multi module Python source code for free!
And YOU choose per project what to obfuscate and what not, by editting the config file.
- BACKUP YOUR CODE AND VALUABLE DATA TO AN OFF-LINE MEDIUM FIRST TO PREVENT ACCIDENTAL LOSS OF WORK!!!
Then copy the default config file to the source top directory <topdir> and run {0} from there.
It will generate an obfuscation directory <topdir>/../<topdir>_{1}
- At first some identifiers may be obfuscated that shouldn't be, e.g. some of those imported from external modules.
Adapt your config file to avoid this, e.g. by adding external module names that will be recursively scanned for identifiers.
You may also exclude certain words or files in your project from obfuscation explicitly.
- Source directory, obfuscation directory and config file path can also be supplied as command line parameters.
The config file path should be something like C:/config_files/opy.cnf, so including the file name and extension.
opy [<source directory> [<target directory> [<config file path>]]]
- Comments and string literals can be marked as plain, bypassing obfuscation
Be sure to take a look at the comments in the config file opy_config.txt to discover all features.
Known limitations:
- A comment after a string literal should be preceded by whitespace
- A ' or " inside a string literal should be escaped with \ rather then doubled
- If the pep8_comments option is False (the default), a {2} in a string literal can only be used at the start, so use 'p''{2}''r' rather than 'p{2}r'
- If the pep8_comments option is set to True, however, only a <blank><blank>{2}<blank> cannot be used in the middle or at the end of a string literal
- Obfuscation of string literals is unsuitable for sensitive information since it can be trivially broken
- No renaming backdoor support for methods starting with __ (non-overridable methods, also known as private methods)
Licence:
{3}
===============================================================================
        '''.format (l1ll1ll1ll_opy_.capitalize (), l1ll1ll1ll_opy_, r'#', license))
        exit (l1ll111l1l_opy_)
    if len (args) > 1:
        for l11l111ll_opy_ in '?', '-h', '--help':
            if l11l111ll_opy_ in args [1]:
                l1llll1l1l_opy_ (0)
        l1ll1l11ll_opy_ = args [1] .replace ('\\', '/')
    else:
        l1ll1l11ll_opy_ = os.getcwd () .replace ('\\', '/')
    if len (args) > 2:
        l1111l111_opy_ = args [2] .replace ('\\', '/')
    else:
        l1111l111_opy_ = '{0}/{1}_{2}'.format (* (l1ll1l11ll_opy_.rsplit ('/', 1) + [l1ll1ll1ll_opy_]))
    if len (args) > 3:
        l1l1ll11l1_opy_ = args [3] .replace ('\\', '/')
    else:
        l1l1ll11l1_opy_ = '{0}/{1}_config.txt'.format (l1ll1l11ll_opy_, l1ll1ll1ll_opy_)
    try:
        l1lllll111_opy_ = open (l1l1ll11l1_opy_)
    except Exception as exception:
        print (exception)
        l1llll1l1l_opy_ (1)
    exec (l1lllll111_opy_.read (), globals (), locals ())
    l1lllll111_opy_.close ()
    l1llll1111_opy_ = locals ()
    def l1ll1l11l1_opy_ (l1l1l1l1ll_opy_, default):
        try:
            return l1llll1111_opy_ [l1l1l1l1ll_opy_]
        except:
            return default
    l111l111l_opy_ = l1ll1l11l1_opy_ ('obfuscate_strings', False)
    l1l1l1ll1l_opy_ = l1ll1l11l1_opy_ ('ascii_strings', False)
    l111ll1ll_opy_ = l1ll1l11l1_opy_ ('obfuscated_name_tail', '_{}_'.format (l1ll1ll1ll_opy_))
    l1111llll_opy_ = l1ll1l11l1_opy_ ('plain_marker', '_{}_'.format (l1ll1ll1ll_opy_))
    l1l1lll1ll_opy_ = l1ll1l11l1_opy_ ('pep8_comments', True)
    l11111l11_opy_ = l1ll1l11l1_opy_ ('source_extensions', 'py pyx') .split ()
    l1ll111l11_opy_ = l1ll1l11l1_opy_ ('skip_extensions', 'pyc') .split ()
    l1ll1ll111_opy_ = l1ll1l11l1_opy_ ('skip_path_fragments', '') .split ()
    l1llll1ll1_opy_ = l1ll1l11l1_opy_ ('external_modules', '') .split ()
    l1111ll1l_opy_ = l1ll1l11l1_opy_ ('plain_files', '') .split ()
    l111111l1_opy_ = l1ll1l11l1_opy_ ('plain_names', '') .split ()
    l1llll1lll_opy_ = [
        '{0}/{1}'.format (directory.replace ('\\', '/'), l1llllll1l_opy_)
        for directory, l1ll11l1ll_opy_, l1lll1ll1l_opy_ in os.walk (l1ll1l11ll_opy_)
        for l1llllll1l_opy_ in l1lll1ll1l_opy_
    ]
    def l1lll11ll1_opy_ (l1lll1ll11_opy_):
        for l1llllll11_opy_ in l1ll1ll111_opy_:
            if l1llllll11_opy_ in l1lll1ll11_opy_:
                return True
        return False
    l11l1l11l_opy_ = [l1lll1ll11_opy_ for l1lll1ll11_opy_ in l1llll1lll_opy_ if not l1lll11ll1_opy_ (l1lll1ll11_opy_)]
    l1l1l11l1l_opy_ = re.compile (r'^{0}!'.format (r'#'))
    l1lll1lll1_opy_ = re.compile ('coding[:=]\s*([-\w.]+)')
    l1l1lll11l_opy_ = re.compile ('.*{0}.*'.format (l1111llll_opy_), re.DOTALL)
    def l11l1l1l1_opy_ (l1lllllll1_opy_):
        comment = l1lllllll1_opy_.group (0)
        if l1l1lll11l_opy_.search (comment):
            l11ll1111_opy_.append (comment.replace (l1111llll_opy_, ''))
            return l1ll1lll1l_opy_
        else:
            return ''
    def l1l1llllll_opy_ (l1lllllll1_opy_):
        global l1l1l1l111_opy_
        l1l1l1l111_opy_ += 1
        return l11ll1111_opy_ [l1l1l1l111_opy_]
    l1llll11l1_opy_ = (
            re.compile (r'{0}{1}{2}.*?$'.format (
                r"(?<!')",
                r'(?<!")',
                r'  # '  # l111ll1l1_opy_ to l1lll1llll_opy_ l11l11111_opy_ l11111111_opy_ comment should start l11ll11ll_opy_ this.
            ), re.MULTILINE)
        if l1l1lll1ll_opy_ else
            re.compile (r'{0}{1}{2}.*?$'.format (
                r"(?<!')",
                r'(?<!")',
                r'#'
            ), re.MULTILINE)
    )
    l1ll1lll1l_opy_ = '_{0}_c_'.format (l1ll1ll1ll_opy_)
    l1ll11llll_opy_ = re.compile (r'{0}'.format (l1ll1lll1l_opy_))
    l1ll111ll1_opy_ = re.compile (r'.*{0}.*'.format (l1111llll_opy_))
    def l11l11ll1_opy_ (l1lllllll1_opy_):
        string = l1lllllll1_opy_.group (0)
        if l111l111l_opy_:
            if l1ll111ll1_opy_.search (string): # l1ll1l1ll1_opy_, l1ll11l111_opy_ no l11ll11l1_opy_ for l11ll1l11_opy_
                l1lll11l1l_opy_.append (string.replace (l1111llll_opy_, ''))
                return l1l1lllll1_opy_
            else:
                l1lll11l1l_opy_.append (l111llll1_opy_ (string))
                return 'unScramble{0} ({1})'.format (l1111llll_opy_, l1l1lllll1_opy_)
        else:
            l1lll11l1l_opy_.append (string)
            return l1l1lllll1_opy_
    def l111l1111_opy_ (l1lllllll1_opy_):
        global l1ll1l1111_opy_
        l1ll1l1111_opy_ += 1
        return l1lll11l1l_opy_ [l1ll1l1111_opy_]
    l1l1ll1l1l_opy_ = re.compile (r'([ru]|ru|ur)?(({0})|({1})|({2})|({3}))'.format (
        r"'''.*?(?<![^\\]\\)(?<![^\\]\')'''",
        r'""".*?(?<![^\\]\\)(?<![^\\]\")"""',
        r"'.*?(?<![^\\]\\)'",
        r'".*?(?<![^\\]\\)"'
    ), re.MULTILINE | re.DOTALL | re.VERBOSE)
    l1l1lllll1_opy_ = '_{0}_s_'.format (l1ll1ll1ll_opy_)
    l1lll1l111_opy_ = re.compile (r'{0}'.format (l1l1lllll1_opy_))
    def l11111ll1_opy_ (l1lllllll1_opy_):
        l11l11l11_opy_ = l1lllllll1_opy_.group (0)
        if l11l11l11_opy_:
            global l1l1l11l11_opy_
            l1ll111lll_opy_ [l1l1l11l11_opy_:l1l1l11l11_opy_] = [l11l11l11_opy_]
            l1l1l11l11_opy_ += 1
        return ''
    l1111111l_opy_ = re.compile ('from\s*__future__\s*import\s*\w+.*$', re.MULTILINE)
    l1l1ll1lll_opy_ = re.compile (r'''
        \b
        (?!{0})
        (?!{1})
        [^\d\W]
        \w*
        (?<!__)
        (?<!{0})
        (?<!{1})
        \b
    '''.format (l1ll1lll1l_opy_, l1l1lllll1_opy_), re.VERBOSE) # l111ll111_opy_ l11l1l111_opy_
    l1l1ll1ll1_opy_ = re.compile (r'\bchr\b')
    l11l11l1l_opy_ = set (keyword.kwlist + ['__init__'] + l111111l1_opy_)
    l1ll1llll1_opy_ = ['{0}/{1}'.format (l1ll1l11ll_opy_, l11l111l1_opy_) for l11l111l1_opy_ in l1111ll1l_opy_]
    l1lll1l11l_opy_ = [l1llll111l_opy_ for l1llll111l_opy_ in l1ll1llll1_opy_ if os.path.exists (l1llll111l_opy_)]
    for l1llll111l_opy_ in l1lll1l11l_opy_:
        l1l1ll1l11_opy_ = open (l1llll111l_opy_)
        content = l1l1ll1l11_opy_.read ()
        l1l1ll1l11_opy_.close ()
        content = l1llll11l1_opy_.sub ('', content)
        content = l1l1ll1l1l_opy_.sub ('', content)
        l11l11l1l_opy_.update (re.findall (l1l1ll1lll_opy_, content))
    class l111l1l11_opy_:
        def __init__ (self):
            for l11l1lll1_opy_ in l1llll1ll1_opy_:
                l1ll11l11l_opy_ = l11l1lll1_opy_.replace ('.', l1111llll_opy_)
                try:
                    exec (
                        '''
import {0} as currentModule
                        '''.format (l11l1lll1_opy_),
                        globals ()
                    )
                    setattr (self, l1ll11l11l_opy_, l1ll1lll11_opy_)
                except Exception as exception:
                    print (exception)
                    setattr (self, l1ll11l11l_opy_, None) # l1l1l1llll_opy_ l111l1lll_opy_ l111l11ll_opy_ the l1ll11ll1l_opy_ name will be l11l1l1ll_opy_
                    print ('Warning: could not inspect external module {0}'.format (l11l1lll1_opy_))
    l1l1l11ll1_opy_ = l111l1l11_opy_ ()
    l111lllll_opy_ = set ()
    def l1lll111l1_opy_ (l1ll1111ll_opy_):
        if l1ll1111ll_opy_ in l111lllll_opy_:
            return
        else:
            l111lllll_opy_.update ([l1ll1111ll_opy_])
        try:
            l1ll1l111l_opy_ = list (l1ll1111ll_opy_.__dict__)
        except:
            l1ll1l111l_opy_ = []
        try:
            if l1l1l11lll_opy_:
                l1l1lll1l1_opy_ = list (l1ll1111ll_opy_.l1lll11l11_opy_.co_varnames)
            else:
                l1l1lll1l1_opy_ = list (l1ll1111ll_opy_.__code__.co_varnames)
        except:
            l1l1lll1l1_opy_ = []
        l11l11lll_opy_ = [getattr (l1ll1111ll_opy_, l1ll11l11l_opy_) for l1ll11l11l_opy_ in l1ll1l111l_opy_]
        l1l1l1l11l_opy_ = (l1111llll_opy_.join (l1ll1l111l_opy_)) .split (l1111llll_opy_) # l1lll1l1l1_opy_ module name chunks that l1ll1ll1l1_opy_ l1lll11lll_opy_ by l1ll1ll11l_opy_
        l1111l1ll_opy_ = set ([entry for entry in (l1l1lll1l1_opy_ + l1l1l1l11l_opy_) if not (entry.startswith ('__') and entry.endswith ('__'))])
        l11l11l1l_opy_.update (l1111l1ll_opy_)
        for l1ll11ll1l_opy_ in l11l11lll_opy_:
            try:
                l1lll111l1_opy_ (l1ll11ll1l_opy_)
            except:
                pass
    l1lll111l1_opy_ (l111111ll_opy_)
    l1lll111l1_opy_ (l1l1l11ll1_opy_)
    l11l1llll_opy_ = list (l11l11l1l_opy_)
    l11l1llll_opy_.sort (key = lambda s: s.lower ())
    l1ll11l1l1_opy_ = []
    l1ll1l1lll_opy_ = []
    for l1lll1ll11_opy_ in l11l1l11l_opy_:
        if l1lll1ll11_opy_ == l1l1ll11l1_opy_:
            continue
        l1l1ll111l_opy_, l11111l1l_opy_ = l1lll1ll11_opy_.rsplit ('/', 1)
        l1ll1l1l1l_opy_, l1l1ll1111_opy_ = (l11111l1l_opy_.rsplit ('.', 1) + ['']) [ : 2]
        l111l1ll1_opy_ =  l1lll1ll11_opy_ [len (l1ll1l11ll_opy_) : ]
        if l1l1ll1111_opy_ in l11111l11_opy_ and not l1lll1ll11_opy_ in l1lll1l11l_opy_:
            l1111l11l_opy_ = random.randrange (64)
            l1111ll11_opy_ = codecs.open (l1lll1ll11_opy_, encoding = 'utf-8')
            content = l1111ll11_opy_.read ()
            l1111ll11_opy_.close ()
            l11ll1111_opy_ = []
            l1ll111lll_opy_ = content.split ('\n', 2)
            l1l1l11l11_opy_ = 0
            l1l1l1lll1_opy_ = True
            if len (l1ll111lll_opy_) > 0:
                if l1l1l11l1l_opy_.search (l1ll111lll_opy_ [0]):
                    l1l1l11l11_opy_ += 1
                    if len (l1ll111lll_opy_) > 1 and l1lll1lll1_opy_.search (l1ll111lll_opy_ [1]):
                        l1l1l11l11_opy_ += 1
                        l1l1l1lll1_opy_ = False
                elif l1lll1lll1_opy_.search (l1ll111lll_opy_ [0]):
                    l1l1l11l11_opy_ += 1
                    l1l1l1lll1_opy_ = False
            if l111l111l_opy_ and l1l1l1lll1_opy_:
                l1ll111lll_opy_ [l1l1l11l11_opy_:l1l1l11l11_opy_] = ['# coding: UTF-8']
                l1l1l11l11_opy_ += 1
            if l111l111l_opy_:
                l111l1l1l_opy_ = '\n'.join ([l1lll1l1ll_opy_ (l1111l11l_opy_)] + l1ll111lll_opy_ [l1l1l11l11_opy_:])
            else:
                l111l1l1l_opy_ = '\n'.join (l1ll111lll_opy_ [l1l1l11l11_opy_:])
            l111l1l1l_opy_ = l1llll11l1_opy_.sub (l11l1l1l1_opy_, l111l1l1l_opy_)
            l1lll11l1l_opy_ = []
            l111l1l1l_opy_ = l1l1ll1l1l_opy_.sub (l11l11ll1_opy_, l111l1l1l_opy_)
            l111l1l1l_opy_ = l1111111l_opy_.sub (l11111ll1_opy_, l111l1l1l_opy_)
            l111lll11_opy_ = set (re.findall (l1l1ll1lll_opy_, l111l1l1l_opy_) + [l1ll1l1l1l_opy_])
            l1llll1l11_opy_ = l111lll11_opy_.difference (l1ll11l1l1_opy_).difference (l11l11l1l_opy_)
            l1lll111ll_opy_ = list (l1llll1l11_opy_)
            l1lllll1l1_opy_ = [re.compile (r'\b{0}\b'.format (l111ll11l_opy_)) for l111ll11l_opy_ in l1lll111ll_opy_]
            l1ll11l1l1_opy_ += l1lll111ll_opy_
            l1ll1l1lll_opy_ += l1lllll1l1_opy_
            for l1llll11ll_opy_, l1ll11ll11_opy_ in enumerate (l1ll1l1lll_opy_):
                l111l1l1l_opy_ = l1ll11ll11_opy_.sub (
                    l1ll1l1l11_opy_ (l1llll11ll_opy_, l1ll11l1l1_opy_ [l1llll11ll_opy_]),
                    l111l1l1l_opy_
                )
            l1ll1l1111_opy_ = -1
            l111l1l1l_opy_ = l1lll1l111_opy_.sub (l111l1111_opy_, l111l1l1l_opy_)
            l1l1l1l111_opy_ = -1
            l111l1l1l_opy_ = l1ll11llll_opy_.sub (l1l1llllll_opy_, l111l1l1l_opy_)
            content = '\n'.join (l1ll111lll_opy_ [:l1l1l11l11_opy_] + [l111l1l1l_opy_])
            content = '\n'.join ([line for line in [line.rstrip () for line in content.split ('\n')] if line])
            try:
                l1llllllll_opy_ = l1ll1l1l11_opy_ (l1ll11l1l1_opy_.index (l1ll1l1l1l_opy_), l1ll1l1l1l_opy_)
            except: # l1lllll1ll_opy_ in list, e.g. l11l1ll11_opy_ module name
                l1llllllll_opy_ = l1ll1l1l1l_opy_
            l1l1llll11_opy_ = l111l1ll1_opy_.split ('/')
            for index in range (len (l1l1llll11_opy_)):
                try:
                    l1l1llll11_opy_ [index] = l1ll1l1l11_opy_ (l1ll11l1l1_opy_.index (l1l1llll11_opy_ [index]), l1l1llll11_opy_ [index])
                except: # l1lllll1ll_opy_ in list
                    pass
            l111l1ll1_opy_ = '/'.join (l1l1llll11_opy_)
            l1lll1111l_opy_ = '{0}{1}'.format (l1111l111_opy_, l111l1ll1_opy_) .rsplit ('/', 1) [0]
            l111lll1l_opy_ = l1l1l1l1l1_opy_ ('{0}/{1}.{2}'.format (l1lll1111l_opy_, l1llllllll_opy_, l1l1ll1111_opy_), open = True)
            l111lll1l_opy_.write (content)
            l111lll1l_opy_.close ()
        elif not l1l1ll1111_opy_ in l1ll111l11_opy_:
            l1lll1111l_opy_ = '{0}{1}'.format (l1111l111_opy_, l111l1ll1_opy_) .rsplit ('/', 1) [0]
            l1ll111111_opy_ = '{0}/{1}'.format (l1lll1111l_opy_, l11111l1l_opy_)
            l1l1l1l1l1_opy_ (l1ll111111_opy_)
            shutil.copyfile (l1lll1ll11_opy_, l1ll111111_opy_)
    def l11l1111l_opy_(l1ll11lll1_opy_, l1111lll1_opy_):
        """
        Copie un dossier et ses sous-dossiers vers un autre emplacement.
        Args:
            source_dir (str): Chemin du dossier source.
            destination_dir (str): Chemin du dossier de destination.
        """
        shutil.copytree(l1ll11lll1_opy_, l1111lll1_opy_)
    l1111lll1_opy_ = "../../bnote/bnote/apps/music/music_opy"
    try:
        shutil.rmtree(l1111lll1_opy_, ignore_errors=True)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    l11l1111l_opy_(l1lll1111l_opy_, l1111lll1_opy_)
    print ('Obfuscated words: {0}'.format (len (l1ll11l1l1_opy_)))
if __name__ == '__main__':
    l1l1l111ll_opy_ ()