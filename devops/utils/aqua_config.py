import os

from configparser import ConfigParser


if not os.path.exists('data'):
    os.makedirs('data')

SLOGAN = 'NOT CONFIGURED YET'


class ConfigWrapper:
    class SectionWrapper:
        def __init__(self, section, wrapper):
            self.section = section
            self.wrapper = wrapper

        def __getattr__(self, option):
            if not self.wrapper.config.has_option(self.section, option):
                self.wrapper.config.set(self.section, option, SLOGAN)
                self.wrapper.config.write(open(self.wrapper.path, 'w+'))
            if self.wrapper.config.get(self.section, option) in [SLOGAN]:
                raise Exception(
                    '[{section}/{option}] {slogan}'.format(section=self.section, option=option, slogan=SLOGAN)
                )
            return self.wrapper.config.get(self.section, option)

        def __getitem__(self, option):
            return self.__getattr__(option)

        def get(self, option, default):
            return self.config.get(self.section, option) if self.config.has_option(self.section, option) else default

    def __init__(self, path='data/config.ini'):
        self.config = ConfigParser()
        self.path = os.path.abspath(path)
        self.config.read(path) if os.path.exists(path) else print('{path} does not exist'.format(path=path))
        self.sections = {}

        if not os.path.exists(path):
            self.config.write(open(path, 'w+'))

    def __getattr__(self, section):
        if section not in self.sections and not self.config.has_section(section):
            self.config.add_section(section)
        self.sections[section] = ConfigWrapper.SectionWrapper(section, wrapper=self)
        return self.sections[section]

    def __getitem__(self, section):
        return self.__getattr__(section)



