import logging
from woco import version

# define the version before the other imports since these need it
__version__ = version.__version__

logging.getLogger(__name__).addHandler(logging.NullHandler())
