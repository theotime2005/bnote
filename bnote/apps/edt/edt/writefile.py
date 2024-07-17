"""
 bnote project
 Author : Eurobraille
 Date : 2024-07-16
 Licence : Ce fichier est libre de droit. Vous pouvez le modifier et le redistribuer à votre guise.
"""


import time
import threading

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_WRITE_FILE_LOG, logging
log = ColoredLogger(__name__, level=EDITOR_WRITE_FILE_LOG)


class WriteFile(threading.Thread):
    STATE_INSTANTIATE = 0
    STATE_RUNNING = 1
    STATE_ENDED = 2

    def __init__(self, full_file_name, get_line, on_end, function):
        threading.Thread.__init__(self)
        self._full_file_name = full_file_name
        self._get_line = get_line
        self._on_end = on_end
        self._function = function
        self.state = WriteFile.STATE_INSTANTIATE
        self.error = None

    def run(self):
        self.state = WriteFile.STATE_RUNNING

        fp = None
        try:
            if self._get_line is None:
                raise IOError("Error during editor access")
            fp = open(self._full_file_name, 'w')
            # Write txt file.
            cnt = 0
            while True:
                line = self._get_line(cnt)
                if line is None:
                    # Exit from while (do ... While emulation)
                    if EDITOR_WRITE_FILE_LOG <= logging.INFO:
                        log.info("End of document {} paragraphs".format(cnt))
                    break
                # Just to let others threads running.
                time.sleep(0.001)
                # print("Line {}: {}".format(cnt, line.strip()))
                fp.writelines(line + "\r\n")
                if EDITOR_WRITE_FILE_LOG <= logging.INFO:
                    log.info("Write paragraph <{}>".format(line))
                cnt += 1
        except IOError as error:
            self.error = error
            if EDITOR_WRITE_FILE_LOG <= logging.ERROR:
                log.error("Write file IO exception:{}".format(self.error))
        finally:
            if fp:
                fp.close()
            self.state = WriteFile.STATE_ENDED
            if self._on_end is not None:
                self._on_end(self.error, self._function)


# -----------------------------------------------
# Unitary test
def my_get_line(number):
    if number == 0:
        return "Line 1"
    elif number == 1:
        return "Line 2"
    elif number == 2:
        return "Line 3"
    else:
        return None


def main():
    print("--------------")
    print("Write file class:")
    print("--------------")

    writefile = WriteFile("test_unitary.txt", my_get_line, None, None)
    writefile.start()


if __name__ == "__main__":
    main()
