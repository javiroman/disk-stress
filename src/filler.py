#!/usr/bin/env python3
from queue import PriorityQueue

__version__ = "0.0.1"

import sys

if sys.version_info[0] < 3:
    raise Exception("I need Python 3 for living")

import optparse
import threading
from restserver import RestServer
from worker import workerThread

runQueue = PriorityQueue()

class FillerApplication():
    """docstring for ClassName"""

    def __init__(self):
        self._parse_args()

    def _parse_args(self):
        usage = "usage: %prog [options]"
        version = "Disk Filler version: %s" % __version__

        parser = optparse.OptionParser(usage=usage, version=version)
        parser.add_option("-v", "--verbose",
                          action="store_true",
                          dest="verbose",
                          help="Set verbosity output")

        parser.add_option("-a", "--attach",
                          action="store",
                          dest="attach",
                          default="127.0.0.1",
                          help="URL for attaching the web server")

        parser.add_option("-p", "--port",
                          action="store",
                          dest="port",
                          default="8080",
                          help="URL for attaching the web server")

        parser.add_option("-o", "--output",
                          action="store",
                          dest="output",
                          default="/tmp/output.dat",
                          help="File for data output")

        (self.options, args) = parser.parse_args()

        if self.options.verbose:
            print("Verbose output enabled")

        print("Enabled API rest at .%s:%s." % (self.options.attach,
              self.options.port))
        print("Enabled output to file: .%s." % self.options.output)

    def run(self):
        worker = threading.Thread(target=workerThread,
                                  args=(runQueue, self.options.output))
        worker.daemon = True
        worker.start()

        rest_server = RestServer(runQueue, self.options)
        rest_server.run()


if __name__ == "__main__":
    app = FillerApplication()
    sys.exit(app.run())
