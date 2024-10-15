'''
 Major version. Minor version. Fix version
 Developper version is allways followed by the stage : -beta.n, -alpha.n, -rc.n
 All release version lost the developper version's extension
 Example : 1.0.0-alpha.0 < 1.0.0-alpha.1 < 1.0.0-alpha.8 < 1.0.0-beta.1 < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
 Other stage like "-fm.1" or "-toto" by example are ordered before beta version.
 Version in anothers forms are not tolerate !
 '''
__version__ = "2.4.0-alpha.1"
__minimum_firmware_version = "2.2.0"
__minimum_sdcard_version = "2.2.1-rc.6"
