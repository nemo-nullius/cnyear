import os
import sys
import pkg_resources
#pkg_dir = os.path.dirname(os.path.abspath(__file__))

CNYEARDB_PATH = pkg_resources.resource_filename('cnyeardb','cnyeardb.db')


from .cnyeardb_obj import Cnyeardb
from .cnyear_obj import Cnyear

