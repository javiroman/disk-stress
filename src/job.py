import random
import time

def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.
    """
    print(x)
    print(y)
    return (x > y) - (x < y)


class Job(dict):
    def __init__(self, priority, operation, output_file=None, size=None):
        dict.__init__(self)
        self.priority = int(priority)

        ctime = time.time()
        self["jobid"] = "JID-%s.%i" % (ctime, random.randint(1, 10000))
        self["creationtime"] = ctime

        self["priority"] = self.priority
        self["operation"] = operation
        self["file"] = output_file
        self["size"] = size

        self["nodename"] = ""
        self["status"] = ""
        self["stdout"] = ""
        self["stderr"] = ""
        return

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
