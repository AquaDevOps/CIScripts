from devops.utils.aqua_config import ConfigWrapper

config = ConfigWrapper()
print('{username} identified by {password}'.format(username=config.devops.username, password=config.devops.password))
