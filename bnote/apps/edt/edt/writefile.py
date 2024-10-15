"""
Copyright (c)2021 eurobraille
This software is the proprietary of eurobraille and may not be copied,
distributed, published,or disclosed without express prior written permission.
"""


import time
import threading

# Setup the logger for this file
from .colored_log import ColoredLogger, EDITOR_WRITE_FILE_LOG
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
            fp = open(self._full_file_name, 'w')

            # Write txt file.
            cnt = 0
            while True:
                if self._get_line is None:
                    break
                line = self._get_line(cnt)
                if line is None:
                    # Exit from while (do ... While emulation)
                    log.info("End of document {} paragraphs".format(cnt))
                    break

                # Sleep 1 sec. just for test edition during file reading.
                # time.sleep(0.5)
                # Just to let others threads running.
                time.sleep(0.001)

                # print("Line {}: {}".format(cnt, line.strip()))
                fp.writelines(line + "\r\n")
                log.info("Write paragraph <{}>".format(line))
                cnt += 1
        except IOError as error:
            self.error = error
            log.warning("Write file IO exception:{}".format(self.error))
        finally:
            # print("end writing !")
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
