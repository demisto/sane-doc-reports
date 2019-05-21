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

# Others
HTML_REDUNDANT_COLLAPSIBLE = ['p']
HTML_NOT_WRAPABLES = ['span', 'li', 'ul', 'ol', 'code', 'blockquote']
HTML_ATTRIBUTES = ['em', 'strong', 'del']
HTML_ATTR_MARKDOWN_MAP = {'em': 'italic', 'strong': 'bold',
                          'del': 'strikethrough'}

# Styles
DEFAULT_WORD_FONT = 'Verdana'

# Sizes:
SIZE_W_INCHES = 6
SIZE_H_INCHES = 3
DPI = 80

# List constants
ORDERED_LIST_NAME = 'List Number'
UNORDERED_LIST_NAME = 'List Bullet'

# Chart constants
DEFAULT_ALPHA = 0.5
DEFAULT_BAR_WIDTH = 0.35
DEFAULT_BAR_ALPHA = 0.8
DEFAULT_DPI = 100.0

# PYTHON-DOCX constants
PYDOCX_FONT_SIZE = 'fontSize'
PYDOCX_FONT_NAME = 'name'
PYDOCX_FONT_BOLD = 'bold'
PYDOCX_FONT_STRIKE = 'strikethrough'
PYDOCX_FONT_UNDERLINE = 'underline'
PYDOCX_FONT_ITALIC = 'italic'
PYDOCX_FONT_COLOR = 'color'
PYDOCX_TEXT_ALIGN = 'textAlign'


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
