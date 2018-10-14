import os
import sys
pkg_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(pkg_dir+'/../')
#print(sys.path)

from .tools import debug
debug(pkg_dir)

from .cnyeardb_obj import Cnyeardb

