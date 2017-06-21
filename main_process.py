from threading import Thread
import subprocess
import signal
import time
import os


class MainThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.process = None

    def run(self):
        self.process = subprocess.Popen(
            ['python3', os.getcwd() + '/child_process.py'],
            stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=False, preexec_fn=os.setsid
        )

    def stop(self):
        # stop sends a flag to child process to exit loop
        pid = os.getpgid(self.process.pid)
        print ('Stopping process with pid: %s' % pid)
        self.process.stdin.write('kill\n'.encode())

    def kill(self):
        # kill stops the process in OS level
        # But for our example, the file will not close and do not write data
        pid = os.getpgid(self.process.pid)
        print ('Killing process with pid: %s' % pid)
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

    def send_message(self, message):
        if self.process is not None:
            print ('Sending [%s] to process %s' % (message, self.process.pid))
            self.process.stdin.write((message + '\n').encode())


if __name__ == '__main__':
    val = 0

    # create and start thread
    thread = MainThread()
    thread.start()

    # wait for subprocess creation
    time.sleep(2)

    # send some message to it
    while val < 5:
        thread.send_message(str(val))
        val += 1
        time.sleep(1)

    # send kill signal
    # thread.kill()

    # send stop signal
    thread.stop()

    # wait stop
    time.sleep(2)
