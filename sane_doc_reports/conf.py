from os import getenv

# Environment
DEBUG = getenv('SANE_DOCX_DEBUG', 'False') == 'True'

# Grid Constants
DATA_KEY = 'data'
LAYOUT_KEY = 'layout'
ROW_POSITION_KEY = 'rowPos'
COL_POSITION_KEY = 'columnPos'
HEIGHT_POSITION_KEY = 'h'
WIDTH_POSITION_KEY = 'w'
PAGE_GRID_HEIGHT = 12
STYLE_KEY = 'style'
PAGEBREAK_KEY = 'pageBreakBefore'

# Page margin constants
TOP_MARGIN_PT = 10
BOTTOM_MARGIN_PT = 10
LEFT_MARGIN_PT = 25
RIGHT_MARGIN_PT = 15

# Page size constants
A4_MM_HEIGHT = 297
A4_MM_WIDTH = 210
SHOULD_HAVE_12_GRID = False

# Sizes:
SIZE_W_INCHES = 6
SIZE_H_INCHES = 3
DPI = 80

# Chart constants
DEFAULT_ALPHA = 0.5
DEFAULT_BAR_WIDTH = 0.35
DEFAULT_BAR_ALPHA = 0.8
DEFAULT_DPI = 100.0
