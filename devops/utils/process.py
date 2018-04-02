import subprocess


def process(cmd, cwd=None):
    instance = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, cwd=cwd)
    while instance.poll() is None:
        for line in instance.stdout.readlines():
            print(line.strip().decode('gbk'))
    print('Return:%s' % instance.returncode)
    return instance.returncode == 0
