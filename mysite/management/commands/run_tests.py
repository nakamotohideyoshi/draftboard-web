#
# run_tests.py
#
# This is a wrapper to run each app in codeship.py's TEST_SANDBOXED_INSTALLED_APPS list

from django.core.management.base import BaseCommand
from django.core.management import call_command
from mysite.settings.codeship import TEST_SANDBOXED_INSTALLED_APPS
import subprocess
from django.contrib.auth.models import User

# call_command('my_command', 'foo', bar='baz')

class Command(BaseCommand):

    help = "run sandboxed django tests in the order defined in codeship.py"

    def handle(self, *args, **options):

        # (venv) vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo -u postgres psql -c "CREATE DATABASE template_dfs_pbpstats TEMPLATE dfs_pbpstats;"
        # CREATE DATABASE
        # (venv) vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo -u postgres psql -c "DROP DATABASE dfs_pbpstats;"
        # DROP DATABASE
        # (venv) vagrant@vagrant-ubuntu-trusty-64:/vagrant$ sudo -u postgres psql -c "CREATE DATABASE dfs_pbpstats TEMPLATE template_dfs_pbpstats;"
        # CREATE DATABASE
        # (venv) vagrant@vagrant-ubuntu-trusty-64:/vagrant$

        # for app in TEST_SANDBOXED_INSTALLED_APPS:
        #
        #     call_command('test', '%s.tests' % app)
        db_name = 'dfs_pbpstats'
        #db_name = 'dfs_pbpstats'
        dbdump_filename = 'bkup-db.dump'
        with open(dbdump_filename, 'w') as dumpfile:
            #subprocess.call("sudo -u postgres pg_dump -Fc --no-acl --no-owner %s" % db_name, stdout=dumpfile, shell=True)
            subprocess.call("pg_dump -Fc --no-acl --no-owner %s" % db_name, stdout=dumpfile, shell=True)

        user = User.objects.create(username='steveBobSteve')

        subprocess.call("psql < %s")

# import os, popen2, time, shutil, sys
# from subprocess import check_output, Popen
# from optparse import make_option
#
# from django.core.management.base import BaseCommand, CommandError
# from django.conf import settings
#
# class Command(BaseCommand):
#
#     help = 'Dump database into a file. Only MySQL and PostgreSQL engines are supported.'
#
#     option_list = BaseCommand.option_list + (
#         make_option('--destination', dest='backup_directory', default='backups', help='Destination (path) where to place database dump file.'),
#         make_option('--filename', dest='filename',  default=False, help='Name of the file, or - for stdout'),
#         make_option('--db-name', dest='database_name', default='default', help='Name of database (as defined in settings.DATABASES[]) to dump.'),
#         make_option('--compress', dest='compression_command', help='Optional command to run (e.g., gzip) to compress output file.'),
#         make_option('--quiet', dest='quiet', action='store_true', default=False, help='Be silent.'),
#         make_option('--debug', dest='debug', action='store_true', default=False, help='Show commands that are being executed.'),
#         make_option('--pgpass', dest='pgpass', action='store_true', default=False, help='Use the ~/.pgdump file for password instead of prompting (PostgreSQL only).'),
#         make_option('--raw-args', dest='raw_args', default='', help='Argument(s) to pass to database dump command as is'),
#     )
#
#     OUTPUT_STDOUT = object()
#
#     def handle(self, *args, **options):
#         self.db_name = options.get('database_name', 'default')
#         self.compress = options.get('compression_command')
#         self.quiet = options.get('quiet')
#         self.debug = options.get('debug')
#         self.pgpass = options.get('pgpass')
#
#         if self.db_name not in settings.DATABASES:
#             raise CommandError('Database %s is not defined in settings.DATABASES' % self.db_name)
#
#         self.engine = settings.DATABASES[self.db_name].get('ENGINE')
#         self.db = settings.DATABASES[self.db_name].get('NAME')
#         self.user = settings.DATABASES[self.db_name].get('USER')
#         self.password = settings.DATABASES[self.db_name].get('PASSWORD')
#         self.host = settings.DATABASES[self.db_name].get('HOST')
#         self.port = settings.DATABASES[self.db_name].get('PORT')
#         self.excluded_tables = settings.DATABASES[self.db_name].get('DB_DUMP_EXCLUDED_TABLES', [])
#         self.empty_tables = settings.DATABASES[self.db_name].get('DB_DUMP_EMPTY_TABLES', [])
#
#         backup_directory = options['backup_directory']
#         filename = options['filename']
#
#         if not os.path.exists(backup_directory):
#             os.makedirs(backup_directory)
#
#         if not filename:
#             outfile = self.destination_filename(backup_directory, self.db)
#         elif filename == "-":
#             outfile = self.OUTPUT_STDOUT
#             self.quiet = True
#         else:
#             outfile = os.path.join(backup_directory, filename)
#
#         raw_args = options['raw_args']
#
#         if 'mysql' in self.engine:
#             self.do_mysql_backup(outfile, raw_args=raw_args)
#         elif 'postgresql' in self.engine:
#             self.do_postgresql_backup(outfile, raw_args=raw_args)
#         else:
#             raise CommandError('Backups of %s engine are not implemented.' % self.engine)
#
#         if self.compress:
#             self.run_command('%s %s' % (self.compress, outfile))
#
#     def destination_filename(self, backup_directory, database_name):
#         return os.path.join(backup_directory, '%s_backup_%s.sql' % (database_name, time.strftime('%Y%m%d-%H%M%S')))
#
#     def do_mysql_backup(self, outfile, raw_args=''):
#         if not self.quiet:
#             print 'Doing MySQL backup of database "%s" into %s' % (self.db, outfile)
#
#         main_args = []
#         if self.user:
#             main_args += ['--user=%s' % self.user]
#         if self.password:
#             main_args += ['--password=%s' % self.password]
#         if self.host:
#             main_args += ['--host=%s' % self.host]
#         if self.port:
#             main_args += ['--port=%s' % self.port]
#         if raw_args:
#             main_args += [raw_args]
#
#         excluded_args = main_args[:]
#         if self.excluded_tables or self.empty_tables:
#             excluded_args += ['--ignore-table=%s.%s' % (self.db, excluded_table) for excluded_table in self.excluded_tables + self.empty_tables]
#
#         command = 'mysqldump %s' % (' '.join(excluded_args + [self.db]))
#
#         if outfile != self.OUTPUT_STDOUT:
#             command += " > %s" % outfile
#
#         self.run_command(command)
#
#         if self.empty_tables:
#             no_data_args = main_args[:] + ['--no-data', self.db]
#             no_data_args += [empty_table for empty_table in self.empty_tables]
#
#             command = 'mysqldump %s' % (' '.join(no_data_args))
#
#             if outfile != self.OUTPUT_STDOUT:
#                 command += " >> %s" % outfile
#
#             self.run_command(command)
#
#     def run_command(self, command):
#         if self.debug:
#             print command
#
#         os.system(command)
#
#     def do_postgresql_backup(self, outfile, raw_args=''):
#         if not self.quiet:
#             print 'Doing PostgreSQL backup of database "%s" into %s' % (self.db, outfile)
#
#         main_args = []
#         if self.user:
#             main_args += ['--username=%s' % self.user]
#         if self.password and not self.pgpass:
#             main_args += ['--password']
#         if self.host:
#             main_args += ['--host=%s' % self.host]
#         if self.port:
#             main_args += ['--port=%s' % self.port]
#         if raw_args:
#             main_args += [raw_args]
#
#         excluded_args = main_args[:]
#         if self.excluded_tables or self.empty_tables:
#             excluded_args += ['--exclude-table=%s' % excluded_table for excluded_table in self.excluded_tables + self.empty_tables]
#
#         command = 'pg_dump %s %s' % (' '.join(excluded_args), self.db)
#
#         if outfile != self.OUTPUT_STDOUT:
#             command += ' > %s' % outfile
#
#         self.run_postgresql_command(command, outfile)
#
#         if self.empty_tables:
#             no_data_args = main_args[:] + ['--schema-only']
#             no_data_args += ['--table=%s' % empty_table for empty_table in self.empty_tables]
#             no_data_args += [self.db]
#
#             command = 'pg_dump %s %s' % (' '.join(no_data_args), self.db)
#
#             if outfile != self.OUTPUT_STDOUT:
#                 command += ' >> %s' % outfile
#
#             self.run_postgresql_command(command, outfile)
#
#     def run_postgresql_command(self, command, outfile):
#         if self.debug:
#             print command
#
#         pipe = popen2.Popen4(command)
#
#         if self.password:
#             pipe.tochild.write('%s\n' % self.password)
#             pipe.tochild.close()
#
#         if outfile == self.OUTPUT_STDOUT:
#             shutil.copyfileobj(pipe.fromchild, sys.stdout)
