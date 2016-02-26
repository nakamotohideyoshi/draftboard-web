#
# test/runners.py

import os
from subprocess import Popen, PIPE, check_output
from unittest.runner import (
    TextTestRunner
)
from unittest.suite import (
    TestSuite,
    _isnotsuite,
)
from django.test.runner import (
    DiscoverRunner,
    is_discoverable,
    reorder_suite,
)
from django.db import connection, connections, DEFAULT_DB_ALIAS
from django.conf import settings

class PgUtil:

    @staticmethod
    def clone_db(db_name, to_db_name, requires_sudo=False, close_connection=True):
        """
        this method performs a database copy, but the caller should be
        aware that you may not delete databases if there is an existing
        connection to them.

        use subprocess.Popen to pg_dump, and pg_restore into a db.

        warning: the 'to_db_name' will be 100% overwritten.

        note: if you get some errors that look like this, try calling with requires_sudo=True:

            > psql: FATAL:  database "vagrant" does not exist
            > psql: FATAL:  database "vagrant" does not exist
            > pg_restore: [archiver (db)] connection to database "xxxx" failed: FATAL:  database "xxxx" does not exist

        :param db_name: name of the db to copy from
        :param to_db_name: name of the db to place the copy into
        :param requires_sudo: whether python process requires root privileges (default: False)
        :param close_connection: whether to close the db connection prior to copy (default: True)
        """
        if close_connection:
            print('closed db connection prior to copy... ')
            connection.close()

        print('cloning db [%s] into [%s]' % (db_name, to_db_name))
        # turn the next lines of script into a function that takes requires_sudo as a boolean param
        #requires_sudo = True # if True, prepend 'sudo -u postgres ' to psql commands
        prepend_postgres_user = ''
        if requires_sudo: prepend_postgres_user = 'sudo -u postgres '
        # from django.utils.six import StringIO
        # dumpfile = StringIO()
        #db_name = 'dfs_codeship1'
        #template_db_name = 'template_%s' % db_name
        cmd_pg_dump = 'pg_dump -Fc --no-acl --no-owner %s' % db_name
        cmd_psql = '%spsql' % prepend_postgres_user
        statement_drop_db = r"DROP DATABASE IF EXISTS %s;" % to_db_name
        statement_create_db = r"CREATE DATABASE %s;" % to_db_name
        cmd_pg_restore = 'pg_restore --no-acl --no-owner -d %s' % to_db_name
        # 'dump' should be the postgres db dumpfile
        p = Popen(cmd_pg_dump.split(), stdout=PIPE)
        dump, e = p.communicate()
        p.stdout.close()
        if p.wait() != 0:
            print('p - (errors on next line)')
            print('    ', str(e))
        # drop the template database we are going to make (if it exists)
        #p2 = Popen(cmd_psql_drop.split(), stdin=PIPE)
        #p2_out, p2_err = p2.communicate(dump)
        #drop_output = check_output(cmd_psql_drop, shell=True)      # check_output requires sudo - wont have
        p2 = Popen(cmd_psql.split(), stdin=PIPE)
        o2, e2 = p2.communicate(statement_drop_db.encode('utf-8'))
        p2.stdin.close()
        if p2.wait() != 0:
            print('p2 - (errors on next line)')
            print('    ', str(e2))
        # create an empty db which we can restore the dump into
        #p3 = Popen(cmd_pg_create.split(), stdin=PIPE)
        #p3_out, p3_err = p3.communicate(dump)
        #create_output = check_output(cmd_psql_create, shell=True)  # check_output requires sudo - wont have
        p3 = Popen(cmd_psql.split(), stdin=PIPE)
        o3, e3 = p3.communicate(statement_create_db.encode('utf-8'))
        p3.stdin.close()
        if p3.wait() != 0:
            print('p3 - (errors on next line)')
            print('    ', str(e3))
        # pg_restore the dumped db into the template db we just created
        p4 = Popen(cmd_pg_restore.split(), stdin=PIPE)
        p4_out, p4_err = p4.communicate(dump)
        if p4_err is not None: print('pg_restore errors: %s' % str(p4_err))
        if p4_out is not None: print('pg_restore output: %s' % str(p4_out))
        p4.stdin.close()
        if p4.wait() != 0:
            print('p4 - (errors on next line)')
            print('    ', str(p4_err))

# class InlineAppTextTestRunner( TextTestRunner ):
#     """
#     override TextTestRunner -- the default runner for djangos DiscoverRunner.
#     we will set this class to the self.test_runner inside InlineAppDiscoverRunner
#
#     this class gives us the method pre_run() where we can copy
#     the template_db into the test db or do any pre-run extra setup.
#     """
#
#     def __init__(self, test_db, template_db, **kwargs):
#         super().__init__(**kwargs)
#         self.requires_sudo = settings.INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO
#         self.test_db = test_db
#         self.template_db = template_db
#
#     def run(self, test):
#         """ override parent run() to call pre_run() first """
#         self.pre_run()
#         super().run(test)
#
#     def pre_run(self):
#         """ take care of any setup things pre-run """
#
#         # we need to copy our template test-db back into
#         # the db this test is going to run on!
#         PgUtil.clone_db(self.template_db, self.test_db, self.requires_sudo)

class InlineAppTestSuite( TestSuite ):
    """
    override TextTestRunner -- the default runner for djangos DiscoverRunner.
    we will set this class to the self.test_runner inside InlineAppDiscoverRunner

    this class gives us the method pre_run() where we can copy
    the template_db into the test db or do any pre-run extra setup.
    """

    test_db_name        = None  # must be set before run() called
    template_db_name    = None  # must be set before run() called

    # for PgUtil.clone_db() to use the proper privileges
    requires_sudo       = settings.INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO

    class SetupException(Exception): pass

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def run(self, result, debug=False):
        """
        overrides TestSuite's run() method, with few changes,
        except that this method swaps in the template db before
        each test is run!
        """
        if self.test_db_name is None or self.template_db_name is None:
            err_msg = 'test_db_name & template_db_name must be set before run() can be called!'
            raise self.SetupException(err_msg)

        topLevel = False
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = topLevel = True

        for test in self:
            if result.shouldStop:
                break

            if _isnotsuite(test):
                self._tearDownPreviousClass(test, result)
                self._handleModuleFixture(test, result)
                self._handleClassSetUp(test, result)
                result._previousTestClass = test.__class__

                if (getattr(test.__class__, '_classSetupFailed', False) or
                    getattr(result, '_moduleSetUpFailed', False)):
                    continue

            if not debug:
                #
                # previous to the test execution,
                # copy our template test db into the test db
                # and then instantiate the test
                # TODO - db connection.close()
                PgUtil.clone_db(self.template_db_name, self.test_db_name, self.requires_sudo)
                # TODO - settings.DATABASES[self.connection.alias]["NAME"] = self.test_db_name
                # TODO - self.connection.settings_dict["NAME"] = self.test_db_name
                # TODO - not sure if we HAVE to do this, but try it with it and without it
                # connection.ensure_connection()

                #
                # now make the test
                test(result)
            else:
                test.debug()

        if topLevel:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False
        return result

class InlineAppDiscoverRunner( DiscoverRunner ):
    """
    A django test runner which extends djangos default DiscoverRunner
    which runs each apps tests in order, but doesnt need to
    do a migrate before each app's tests are run!
    """

    clone_db_prefix = 'template_'

    # test_suite = TestSuite
    test_suite = InlineAppTestSuite
    # test_runner = unittest.TextTestRunner
    # test_loader = defaultTestLoader
    # reorder_by = (TestCase, SimpleTestCase)

    def __init__(self, **kwargs):
        """pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=False,
                 reverse=False, debug_sql=False, """
        super().__init__(**kwargs)
        print(self.__class__.__name__, 'testing...')
        self.requires_sudo = settings.INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO

    # @classmethod
    # def add_arguments(cls, parser):
    #     parser.add_argument('-t', '--top-level-directory',
    #         action='store', dest='top_level', default=None,
    #         help='Top level of project for unittest discovery.')
    #     parser.add_argument('-p', '--pattern', action='store', dest='pattern',
    #         default="test*.py",
    #         help='The test matching pattern. Defaults to test*.py.')
    #     parser.add_argument('-k', '--keepdb', action='store_true', dest='keepdb',
    #         default=False,
    #         help='Preserves the test DB between runs.')
    #     parser.add_argument('-r', '--reverse', action='store_true', dest='reverse',
    #         default=False,
    #         help='Reverses test cases order.')
    #     parser.add_argument('-d', '--debug-sql', action='store_true', dest='debug_sql',
    #         default=False,
    #         help='Prints logged SQL queries on failure.')

    # def setup_test_environment(self, **kwargs):
    #     """
    #     override DiscoverRunner setup_test_environment
    #     """
    #     #
    #     #################################### original code
    #     # setup_test_environment()
    #     # settings.DEBUG = False
    #     # unittest.installHandler()
    #     ####################################
    #     super().setup_test_environment(**kwargs)

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        suite = self.test_suite()
        test_labels = test_labels or ['.']
        extra_tests = extra_tests or []

        discover_kwargs = {}
        if self.pattern is not None:
            discover_kwargs['pattern'] = self.pattern
        if self.top_level is not None:
            discover_kwargs['top_level_dir'] = self.top_level

        for label in test_labels:
            kwargs = discover_kwargs.copy()
            tests = None

            label_as_path = os.path.abspath(label)

            # if a module, or "module.ClassName[.method_name]", just run those
            if not os.path.exists(label_as_path):
                tests = self.test_loader.loadTestsFromName(label)
            elif os.path.isdir(label_as_path) and not self.top_level:
                # Try to be a bit smarter than unittest about finding the
                # default top-level for a given directory path, to avoid
                # breaking relative imports. (Unittest's default is to set
                # top-level equal to the path, which means relative imports
                # will result in "Attempted relative import in non-package.").

                # We'd be happy to skip this and require dotted module paths
                # (which don't cause this problem) instead of file paths (which
                # do), but in the case of a directory in the cwd, which would
                # be equally valid if considered as a top-level module or as a
                # directory path, unittest unfortunately prefers the latter.

                top_level = label_as_path
                while True:
                    init_py = os.path.join(top_level, '__init__.py')
                    if os.path.exists(init_py):
                        try_next = os.path.dirname(top_level)
                        if try_next == top_level:
                            # __init__.py all the way down? give up.
                            break
                        top_level = try_next
                        continue
                    break
                kwargs['top_level_dir'] = top_level

            if not (tests and tests.countTestCases()) and is_discoverable(label):
                # Try discovery if path is a package or directory
                tests = self.test_loader.discover(start_dir=label, **kwargs)

                # Make unittest forget the top-level dir it calculated from this
                # run, to support running tests from two different top-levels.
                self.test_loader._top_level_dir = None

            suite.addTests(tests)

        for test in extra_tests:
            suite.addTest(test)

        # return reorder_suite(suite, self.reorder_by, self.reverse)
        return suite

    # def setup_databases(self, **kwargs):
    #     """  this is called right before run_suite(suite) in run_tests() """
    #     return setup_databases(
    #         self.verbosity, self.interactive, self.keepdb, self.debug_sql,
    #         **kwargs
    #     )

    # def get_resultclass(self):
    #     return DebugSQLTextTestResult if self.debug_sql else None

    # def run_suite(self, suite, **kwargs):
    #     """
    #     overrides (do not call super().run_suite()!) behavior so
    #     we can pass extra params to the  ????
    #     """
    #     resultclass = self.get_resultclass()
    #     return self.test_runner(
    #         verbosity=self.verbosity,
    #         failfast=self.failfast,
    #         resultclass=resultclass,
    #     ).run(suite)

    # def teardown_databases(self, old_config, **kwargs):
    #     """
    #     Destroy any databases used during testing
    #     Destroys all the non-mirror databases.
    #     """
    #     old_names, mirrors = old_config
    #     for connection, old_name, destroy in old_names:
    #         if destroy:
    #             connection.creation.destroy_test_db(old_name, self.verbosity, self.keepdb)

    # def teardown_test_environment(self, **kwargs):
    #     unittest.removeHandler()
    #     teardown_test_environment()

    # def suite_result(self, suite, result, **kwargs):
    #     return len(result.failures) + len(result.errors)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.

        Test labels should be dotted Python paths to test modules, test
        classes, or test methods.

        A list of 'extra' tests may also be provided; these tests
        will be added to the test suite.

        Returns the number of tests that failed.
        """

        # 1. basically, i want to make a template of test_DB_NAME during setup_databases (and a cache snapshot?)
        # 2. everytime we run into a new test, load that (and cache?)

        # Given 1 & 2, I need to subclass unittest.runner.TextTestRunner
        #  and construct it with the template dbs / caches i want it to install
        #  before it runs each test!

        print('>>> setup_test_environment')
        self.setup_test_environment()                           # templates, mail
        print('>>> build_suite')
        suite = self.build_suite(test_labels, extra_tests)      # find tests.py's basically

        # sets up django settings.DATABASES (creates new test db, and runs manage.py migrate on it).
        print('>>> setup_databases')
        original_dbs, mirrors = self.setup_databases()
        old_config = (original_dbs, mirrors)
        #original_db_name = original_dbs[0][1] # get the db name that we are running tests for (ie: dfs_master)
        # In [10]: connections[DEFAULT_DB_ALIAS].creation.test_db_signature()
        # Out[10]: ('', '', 'django.db.backends.postgresql_psycopg2', 'test_dfs_codeship1')

        x, y, z, test_db_name = connections[DEFAULT_DB_ALIAS].creation.test_db_signature() # get the test db name from the connection in the original db
        print('>>> test_db_name: %s' % test_db_name)

        # custom - copy the 'test_XXXX' db to 'template_test_XXXX'
        template_db_name = self.clone_db_prefix + test_db_name # TODO - copy it, and get it so we can pass it to run_suite()
        print('>>> clone_db: %s' % template_db_name)
        connection.close()
        PgUtil.clone_db(test_db_name, template_db_name, requires_sudo=settings.INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO)

        # MANDATORY to set these in the suite before its run() method can be called
        suite.test_db_name = test_db_name
        suite.template_db_name = template_db_name

        print('>>> run_suite')
        result = self.run_suite(suite)

        print('>>> teardown_databases')
        self.teardown_databases(old_config)
        # tear down template test db
        # TODO - we should probably destroy the template test db, but its not required

        self.teardown_test_environment()
        return self.suite_result(suite, result)




        #
        # unittest.suite has this method which we may need to override for our db cloning to work
        # def run(self, result):
        #     for test in self:
        #         if result.shouldStop:
        #             break
        #         test(result)
        #     return result