import configparser
import os, errno


class Settings(configparser.ConfigParser):
    def __init__(self, filepath):
        configparser.ConfigParser.__init__(self)
        # save the conf file path
        self.configFilePath = filepath
        self.load()

    def load(self):
        if not os.path.exists(self.configFilePath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.configFilePath)

        self.read(self.configFilePath)

    def save(self):
        with open(self.configFilePath, 'w') as fp:
            self.write(fp)

    def writeDefaults(self):
        # clear configparser contents
        self.clear()

        # this dict will become our default config file
        conf = {
            'INPUT': {
                'inputdevice': 'keyboard',
                'moveup': 'W',
                'moveleft': 'A',
                'movedown': 'S',
                'moveright': 'D',
                'accept': 'SPACE',
                'cancel': 'ESCAPE'
            },
            'VIDEO': {'display_width': '800', 'display_height': '600', 'fullscreen': 'True'},
            'AUDIO': {'sfx_enabled': 'True', 'sfx_volume': '100', 'bgm_enabled': 'True', 'bgm_volume': '100'}
        }

        # load settings dict into parser
        self.read_dict(conf)

        # decide if we should make some noise
        if not self.configFilePath:
            raise ValueError('A valid configFilePath is required to write a default config.')
        elif not os.path.exists(self.configFilePath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.configFilePath)

        # write it out
        with open(self.configFilePath, 'w') as fp:
            self.write(fp)
