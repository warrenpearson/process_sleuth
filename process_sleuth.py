import subprocess
import sys


class ProcessSleuth:
    def investigate(self):
        listen_cmd = ["netstat", "-t4nlp"]
        status, output, err = self.run(listen_cmd)

        if status == 0:
            output = sorted(output.split("\n"))
            for line in output:
                if not line.startswith("tcp"):
                    continue
                cols = line.split()
                self.check_process(cols[3], cols[6])

    def check_process(self, port, process):
        port = int(port.split(":")[-1])
        if port not in [22, 53]:
            pid, name = process.split("/", 1)
            print(f"port: {port} pid: {pid}")
            self.list_open(pid)
            print("-" * 20)

    def list_open(self, pid):
        self.print_process(pid)

        cmd = ["lsof", "-p", pid]
        status, output, err = self.run(cmd)

        if status == 0:
            output = sorted(output.split("\n"))
            for line in output:
                if pid in line:
                    cols = line.split()
                    if cols[3] != "mem" and ("cwd" in line or "txt" in line):
                        print(line)

    def print_process(self, pid):
        cmd = ["ps", "--pid", pid, "-F"]
        status, output, err = self.run(cmd)
        print(output)

    def run(self, cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        status = process.poll()
        out = stdout.decode(sys.stdin.encoding)
        err = stderr.decode(sys.stdin.encoding)
        return (status, out, err)


if __name__ == "__main__":
    ProcessSleuth().investigate()
