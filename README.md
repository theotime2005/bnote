# bnote

## Description
- Applications : python application for bnote.

## development platform
- PyCharm

## version
A bnote version contains 3 numbers with '.' as separators.
A suffix is an, bn, rn for alpha, beta, or release version n (n is a number)
To avoid conflict with official version, the third number of non eurobraille version must start to 100.
by example, A custom version made from version bnote-3.1.2 becomes a bnote-3.1.100 with alpha version named bnote-3.1.100a1

The version is defined in pyproject.toml

## Some informations

- How start bnote from remote ide (pycharm, vscode...)
  
The root directory contains a __main__.py file and a __maindebug_.py file. The first one is the one that is launched by the service, and the second one is the one that should be launched in PyCharm. It allows stopping the bnote.service service when starting the application in PyCharm.

- Which language should be used for writing?
  
Throughout the project, the language used is English, so comments, labels, and variables must be in English. If the explanation we want to give is complicated to translate, we can exceptionally use native language.

- Is it possible to modify the .po files inside?

Yes, but label in the sources (_"...") that are already translated should not be changed to avoid ruining all the translations already done. For example, changing an uppercase letter to a lowercase letter in a message breaks the translation of that message.
