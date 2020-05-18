# Example of Queue with maxsize:
# http://agiliq.com/blog/2013/10/producer-consumer-problem-in-python/
import errno
import sys
import threading
import time


def workerThread(q, f):
    # dirty singleton
    if 'th' not in vars():
        th = StoppableThread(f)

    while True:
        # block if q es empty
        if q.empty():
            print("[Worker Thread waiting for jobs in queue ...]")

        next_job = q.get()

        if next_job["operation"] == "fill":
            th.daemon = True
            th.start()
        elif next_job["operation"] == "stop":
            th.stop()
            print("STOP OPERATION")
        else:
            print("UNKNOW OPERATION")

        print('job processed!!!!')

        # The count of unfinished tasks goes up whenever
        # an item is added (put) to the queue. The count
        # goes down whenever a consumer thread calls
        # task_done() to indicate that the item was
        # retrieved and all work on it is complete.
        # When the count of unfinished tasks drops to zero,
        # q.join() unblocks.
        q.task_done()


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, f):
        super(StoppableThread, self).__init__()
        self.file = f
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("FILLING DISK")
        write_str = "!" * 1024 * 1024 * 5  # 5MB
        output_path = self.file
        with open(output_path, "w") as f:
            while not self.stopped():
                try:
                    f.write(write_str)
                    #time.sleep(1)
                    f.flush()
                except IOError as err:
                    if err.errno == errno.ENOSPC:
                        write_str_len = len(write_str)
                        if write_str_len > 1:
                            write_str = write_str[:write_str_len / 2]
                        else:
                            break
                    else:
                        raise
