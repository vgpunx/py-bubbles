import os
from src.settings import Settings

__all__ = [
    "DISP_SIZE", "PFLD_SIZE", "CELL_SIZE", "DISP_FSCR", "BGM_PATH", "SFX_PATH", "BGI_PATH", "SPR_PATH",
    "BGM_ENABLED", "SFX_ENABLED", "SFX_VOLUME", "BGM_VOLUME", "INPUT_DEV", "MV_UP", "MV_LEFT", "MV_DOWN",
    "MV_RIGHT", "ACCEPT", "CANCEL", "config", "DEBUG", "ALL_TYPEPROPERTIES"
    ]

## GROK THE CONFIG FILE ##
config = Settings(os.path.join(os.curdir, 'config.ini'))  # config file location hardcoding is intentional

## DISPLAY ##
DISP_SIZE = (config['VIDEO'].getint('display_width'), config['VIDEO'].getint('display_height'))
PFLD_SIZE = (DISP_SIZE[0] * 0.65, DISP_SIZE[1] * 0.98)  # 65% scr width, 85% scr height
CELL_SIZE = (PFLD_SIZE[0] / 23, PFLD_SIZE[0] / 23)  # Fit 15 bubbles across
DISP_FSCR = config['VIDEO'].getboolean('fullscreen')

## AUDIO ##
BGM_ENABLED = config['AUDIO'].getboolean('bgm_enabled')
SFX_ENABLED = config['AUDIO'].getboolean('sfx_enabled')
BGM_VOLUME = config['AUDIO'].getint('bgm_volume') / 100
SFX_VOLUME = config['AUDIO'].getint('sfx_volume') / 100

## INPUT ##
INPUT_DEV = config['INPUT']['inputdevice']
MV_UP = config['INPUT']['moveup']
MV_LEFT = config['INPUT']['moveleft']
MV_DOWN = config['INPUT']['movedown']
MV_RIGHT = config['INPUT']['moveright']
ACCEPT = config['INPUT']['accept']
CANCEL = config['INPUT']['cancel']

## PATHS ##
BGM_PATH = os.path.join(os.curdir, 'resource', 'audio', 'bgm')
SFX_PATH = os.path.join(os.curdir, 'resource', 'audio', 'sfx')
BGI_PATH = os.path.join(os.curdir, 'resource', 'image', 'bkg')
SPR_PATH = os.path.join(os.curdir, 'resource', 'image', 'sprites')

## GAME PROPERTIES ##
ALL_TYPEPROPERTIES = ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'VIOLET', 'GRAY', 'WHITE')

## DEBUG MODE ##
DEBUG = False