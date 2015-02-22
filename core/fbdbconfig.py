from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

__author__ = 'holynoob'


class FBDBConfig:
    def __init__(self, configuration_file):
        self._conf_file = configuration_file
        self._parser = None
        self._loaded = False
        self.db_path = ""
        self.db_name = ""
        self.load()


    def load(self):
        #create parser
        self._parser = SafeConfigParser()
        #read configuration file
        self._parser.read(self._conf_file)
        #init configuration values
        self._loaded = True
        self._readConf()


    def isLoaded(self):
        return self._loaded


    def get_option(self, section, option):
        try:
            return self._parser.get(section, option)
        except NoSectionError, errSection:
            print "Error: " + errSection.message
        except NoOptionError, errOption:
            print "Error: " + errOption.message

    def _readConf(self):

        try:
            self.db_name = self._parser.get('GLOBAL', 'db')
            self.db_path = os.getcwd() + '/' + self.db_name

        except NoSectionError, errSection:
            print "Error: " + errSection.message
        except NoOptionError, errOption:
            print "Error: " + errOption.message