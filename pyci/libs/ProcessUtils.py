import subprocess
def process(cmd):
    process = subprocess.Popen(cmd, shell=True, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
    while process.poll() is None:
        for line in process.stdout.readlines():
            print(line.strip().decode('gbk'))
    print('Return:%s' % process.returncode)
    return process.returncode == 0