import os
import json
import web
from job import Job

# URL structure: Regular expression that matches
# an URL + name of class which will handle the request.
urls = (
    '/fill', 'Fill',
    '/stop', 'Stop',
    '/info', 'Info',
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

class Info:
    def GET(self):
        data = web.input(path=[])

        # Memory
        f = open("/sys/fs/cgroup/memory/memory.limit_in_bytes")
        mem_byt = int(f.read())
        mem_gib = mem_byt / (1024. ** 3)

        # CPU
        cpu = os.cpu_count()

        # Disk
        st = os.statvfs(data.path[0])
        free_byt = st.f_bavail * st.f_frsize
        total_byt = st.f_blocks * st.f_frsize
        used_byt = (st.f_blocks - st.f_bfree) * st.f_frsize

        print("Requested path: ", data.path[0])

        return json.dumps({"cpu": cpu,
                           "mem": mem_gib,
                           "total_disk": total_byt / (1024. **3),
                           "free_disk": free_byt / (1024. **3),
                           "used_disk": used_byt / (1024. **3)})

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
