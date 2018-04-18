from devops.utils.config import ConfigWrapper

config = ConfigWrapper()
print('hello {username}'.format(username=config.devops.username))
