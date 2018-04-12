from devops.utils.aqua_config import ConfigWrapper

config = ConfigWrapper()
print('hello {username}'.format(username=config.devops.username))
