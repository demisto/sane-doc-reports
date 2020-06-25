import pathlib
from os import getenv

# Environment
from docx.shared import Mm

DEBUG = getenv('SANE_DEBUG', 'False') == 'True'

# Grid Constants
DATA_KEY = 'data'
LAYOUT_KEY = 'layout'
ROW_POSITION_KEY = 'rowPos'
COL_POSITION_KEY = 'columnPos'
HEIGHT_POSITION_KEY = 'h'
WIDTH_POSITION_KEY = 'w'
STYLE_KEY = 'style'
PAGEBREAK_KEY = 'pageBreakBefore'
SHOULD_HAVE_12_GRID = False
OLD_JSON_FORMAT_GRID_MAX = 10
MAX_RECOMMENDED_ROWS_COUNT = 10000
MAX_RECOMMENDED_COLS_COUNT = 50

# Page constants
TOP_MARGIN_PT = 10
BOTTOM_MARGIN_PT = 10
LEFT_MARGIN_PT = 25
RIGHT_MARGIN_PT = 15
PAPER_A4 = 'A4'
A4_MM_HEIGHT = Mm(297)
A4_MM_WIDTH = Mm(210)
PAPER_A3 = 'A3'
A3_MM_HEIGHT = Mm(420)
A3_MM_WIDTH = Mm(297)
PAPER_LETTER = 'letter'
LETTER_MM_HEIGHT = Mm(279)
LETTER_MM_WIDTH = Mm(216)

# Base Styles
DEFAULT_WORD_FONT = 'Arial'  # 'Source Sans Pro'
DEFAULT_WORD_FONT_FALLBACK = 'Arial'
DEFAULT_FONT_COLOR = '#38383d'
DEFAULT_TITLE_COLOR = '#7E7E7E'
BASE_HEADER_FONT_SIZE = 16
BASE_FONT_SIZE = 9
DEFAULT_TABLE_FONT_SIZE = 8
DEFAULT_TITLE_FONT_SIZE = 10
DEFAULT_LEGEND_FONT_SIZE = 7
DEFAULT_TABLE_STYLE = 'TableDemisto'
DEFAULT_COLORED_CELL_COLOR = '#f9f9fb'

# Chart Sizes:
SIZE_W_INCHES = 6
SIZE_H_INCHES = 3
DEFAULT_DPI = 300.0  # Print DPI
DEFAULT_DOC_PORTRAIT_WIDTH = 612
SMALL_RESIZE_FIX = 0.8

# List/Table constants
ORDERED_LIST_NAME = 'List Number'
UNORDERED_LIST_NAME = 'List Bullet'
MAX_MS_TABLE_COLS_LIMIT = 63

# Element constants
DEFAULT_ALPHA = 0.5
DEFAULT_BAR_WIDTH = 0.35
DEFAULT_BAR_ALPHA = 0.8
CHART_LABEL_NONE_STRING = "None"
X_AXIS_PADDING = 0.5
DEFAULT_FONT_AXIS_COLOR = "#545454"

DEFAULT_DURATION_LABEL_FONT_SIZE = 9
DEFAULT_DURATION_TITLE_FONT_SIZE = 10
DEFAULT_DURATION_FONT_SIZE = 15
DEFAULT_DURATION_TITLE = 'Duration'
DURATION_DAYS_LABEL = '\nDAYS'
DURATION_HOURS_LABEL = '\nHOURS'
DURATION_MINUTES_LABEL = '\nMINUTESS'
MAX_AXIS_LABELS = 32

TREND_MAIN_NUMBER_FONT_SIZE = 16
TREND_SECOND_NUMBER_FONT_SIZE = 11
DEFAULT_HR_DASHES_SIZE = 85

# PLOT constants
LEGEND_STYLE = 'legendStyle'

# ALIGNMENT
ALIGN_LEFT = 0
ALIGN_RIGHT = 2
ALIGN_CENTER = 1

# PYTHON-DOCX constants
PYDOCX_FONT_SIZE = 'fontSize'
PYDOCX_FONT = 'name'
PYDOCX_FONT_NAME = 'fontname'
PYDOCX_FONT_BOLD = 'bold'
PYDOCX_FONT_STRIKE = 'strikethrough'
PYDOCX_FONT_UNDERLINE = 'underline'
PYDOCX_FONT_ITALIC = 'italic'
PYDOCX_FONT_COLOR = 'color'
PYDOCX_TEXT_ALIGN = 'textAlign'
PYDOCX_BACKGROUND_COLOR = 'backgroundColor'

# Markdown section types constants
MD_TYPE_DIV = 'div'
MD_TYPE_CODE = 'code'
MD_TYPE_QUOTE = 'blockquote'
MD_TYPE_UNORDERED_LIST = 'ul'
MD_TYPE_ORDERED_LIST = 'ol'
MD_TYPE_LIST_ITEM = 'li'
MD_TYPE_INLINE_TEXT = 'span'
MD_TYPE_TEXT = 'p'
MD_TYPES_HEADERS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
MD_TYPE_LINK = 'a'
MD_TYPE_IMAGE = 'img'
MD_TYPE_HORIZONTAL_LINE = 'hr'
MD_TYPE_TABLE = 'table'
HTML_REDUNDANT_COLLAPSIBLE = ['p']
HTML_NOT_WRAPABLES = ['span', 'li', 'ul', 'ol', 'code', 'blockquote']
HTML_ATTRIBUTES = ['em', 'strong', 'del']
HTML_ATTR_MARKDOWN_MAP = {'em': 'italic', 'strong': 'bold',
                          'del': 'strikethrough'}
SHOULD_NEW_LINE = ['hr'] + MD_TYPES_HEADERS
MD_PAGE_BREAK = '\\pagebreak'

# Misc.
DOCX_TEMAPLTE_FILE = 'template.docx'
RESIZE_PLOT_ITEMS_AMOUNT_THRESHOLD = 10.0
XSOAR_LOGO_BASE64 = open(pathlib.Path(__file__).parent / './populate/logo.base64', 'r').read()
MAX_CUSTOMER_LOGO_HEIGHT_INCH = 1.5
MAX_CUSTOMER_LOGO_WIDTH_INCH = 2
LOGO_INDEX_RANGE = 10 # how far to check for logo types (removal) in the json
