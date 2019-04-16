from os import getenv

# Environment
DEBUG = getenv('SANE_DOCX_DEBUG', 'False') == 'True'
DOMAIN = getenv('SANE_DOCX_DOMAIN', 'localhost')

# Constants
DATA_KEY = 'data'
LAYOUT_KEY = 'layout'
ROW_POSITION_KEY = 'rowPos'
COL_POSITION_KEY = 'columnPos'
HEIGHT_POSITION_KEY = 'h'
WIDTH_POSITION_KEY = 'w'
PAGE_GRID_HEIGHT = 12
STYLE_KEY = 'style'
PAGEBREAK_KEY = 'pageBreakBefore'
