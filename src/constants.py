import os

__all__ = ["DISP_SIZE", "PFLD_SIZE", "CELL_SIZE", "BGM_PATH", "SFX_PATH", "BGI_PATH", "SPR_PATH"]

## SIZES ##
DISP_SIZE = (800, 600)
PFLD_SIZE = (DISP_SIZE[0] * 0.65, DISP_SIZE[1] * 0.98)  # 65% scr width, 85% scr height
CELL_SIZE = (PFLD_SIZE[0] / 23, PFLD_SIZE[0] / 23)  # Fit 15 bubbles across

## PATHS ##
BGM_PATH = os.path.join(os.curdir, 'resource', 'audio', 'bgm')
SFX_PATH = os.path.join(os.curdir, 'resource', 'audio', 'sfx')
BGI_PATH = os.path.join(os.curdir, 'resource', 'image', 'bg')
SPR_PATH = os.path.join(os.curdir, 'resource', 'image', 'sprites')
