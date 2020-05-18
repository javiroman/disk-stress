import errno
import sys
import web
from job import Job

# URL structure: Regular expression that matches
# an URL + name of class which will handle the request.
urls = (
    '/fill', 'Fill',
    '/stop', 'Stop',
    '/erase', 'Remove',
    '/status', 'Status',
    '/', 'index'
)


# Dirty trick for global REST classes
runQueue = None
options = None

class Fill:
    def GET(self):
        data = web.input(size=[])
        j = Job(5, 'fill', options.output, data.size[0])
        runQueue.put(j)
        return j["jobid"]

class Stop:
    def GET(self):
        j = Job(1, 'stop')
        runQueue.put(j)
        return j["jobid"]

class RestServer():
    def __init__(self, q, opt):
        self.opt = opt
        global runQueue
        global options
        options = opt
        runQueue = q
        print("[RestServer listening ...]")

    def run(self):
        # WebService entry point.
        webapp = web.application(urls, globals())
        web.httpserver.runsimple(webapp.wsgifunc(),
                                 (self.opt.attach, int(self.opt.port)))
