#
# util/loaddata.py

import os
from django.core.management.commands.loaddata import Command
from django.db.utils import DEFAULT_DB_ALIAS
from django.utils.six import StringIO
from django.core.management.color import no_style

#
# loads a fixture into a table
class LoadData:
    """
    Load a fixture programmatically. (Ie: without using manage.py).

    Usage:

        >>> from util.loaddata import LoadData
        >>> loader = LoadData('mysite/somefolder/one_apps_fixtures.json')
        >>> loader.load()

    """

    class InvalidFilenameException(Exception): pass

    def __init__(self, filename):
        # check if file exists
        if not os.path.isfile( filename ):
            raise self.InvalidFilenameException('[%s] does not exist'%filename)

        self.filenames = [ filename ]

    def load(self):
        """
        loads the fixtures which the object was instantiated with
        :return:
        """
        return self.load_fixtures(self.filenames)

    def load_fixtures(self, fixtures):
        stream          = StringIO()
        error_stream    = StringIO()
        loaddata        = Command()
        loaddata.style  = no_style()
        loaddata.execute(*fixtures, **{
            'stdout': stream,
            'stderr': error_stream,
            'ignore': True,
            'database': DEFAULT_DB_ALIAS,
            'verbosity': 1
        })
        return loaddata.loaded_object_count
