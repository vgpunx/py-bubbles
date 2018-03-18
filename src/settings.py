from configparser import ConfigParser
import os, sys, errno


class Settings:
    def __init__(self, filepath) -> None:
        # instantiate parser
        self.config = ConfigParser()
        self.load(filepath)

        # save the conf file path
        self.configFilePath = filepath

    def load(self):
        if not os.path.exist(self.configFilePath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.configFilePath)

        self.config.read(self.configFilePath)

    def save(self):
        with open(self.configFilePath, 'w') as fp:
            self.config.write(fp)

    def writeDefaults(self):
        # clear configparser contents
        self.config.clear()

        # this dict will become our default config file
        conf = {
            'INPUT': {
                'inputdevice': 'keyboard',
                'moveleft': 'K_A',
                'moveright': 'K_D',
                'accept': 'K_SPACE',
                'cancel': 'K_ESCAPE'
            },
            'VIDEO': {'displaysize': '800, 600', 'fullscreen': 'True'},
            'AUDIO': {'sfx_enabled': 'True', 'sfx_volume': '100', 'bgm_enabled': 'True', 'bgm_volume': '100'}
        }

        # load settings dict into parser
        self.config.read_dict(conf)

        # decide if we should make some noise
        if not self.configFilePath:
            raise ValueError('A valid configFilePath is required to write a default config.')
        elif not os.path.exists(self.configFilePath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.configFilePath)

        # write it out
        with open(self.configFilePath, 'w') as fp:
            self.config.write(fp)
