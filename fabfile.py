from boto.s3.connection import S3Connection
from distutils.util import strtobool
from fabric import operations
from fabric import utils
from fabric.api import env, warn_only
from fabric.contrib import django
from subprocess import check_output
import hashlib



# CONSTANTS

ENVS = {
    'production': {
        'local_git_branch': 'master',
        'heroku_repo': 'draftboard-prod',
    },
    'delorean': {
        'heroku_repo': 'draftboard-delorean',
    },
    'dev': {
        'heroku_repo': 'draftboard-dev',
    },
}

# default to vagrant setup
env.virtual_machine_type = 'vagrant'


# INTERNAL METHODS

def _confirm(prompt='Continue?\n', failure_prompt='User cancelled task'):
    '''
    Prompt the user to continue. Repeat on unknown response. Raise
    ParseError on negative response
    '''
    response = input(prompt)

    try:
        response_bool = strtobool(response)
    except ValueError:
        print('Unkown Response. Confirm with y, yes, t, true, on or 1; cancel with n, no, f, false, off or 0.')
        _confirm(prompt, failure_prompt)

    if not response_bool:
        utils.abort(failure_prompt)

    return response_bool


def _confirm_env():
    """Confirms you want to run the commands on Heroku"""
    if not _confirm('Are you sure you want to run these commands on the %s environment? ' % env.environment):
        utils.abort('Aborting at user request')


def _db_drop_then_create(db_name):
    """Drops then creates database"""
    if env.virtual_machine_type == 'vagrant':
        dropCmd = 'sudo -u postgres dropdb --if-exists -U postgres %s' % db_name
        createCmd = 'sudo -u postgres createdb -U postgres -T template0 %s' % db_name
    else:
        dropCmd = 'dropdb --if-exists %s' % db_name
        createCmd = 'createdb -T template0 %s' % db_name

    operations.local(dropCmd)
    operations.local(createCmd)


def _db_restore(db_name, dump_path):
    """Restores db"""
    if env.virtual_machine_type == 'vagrant':
        cmd = 'sudo -u postgres pg_restore --no-acl --no-owner -d %s %s' % (db_name, dump_path)
    else:
        cmd = 'pg_restore --no-acl --no-owner -d %s %s' % (db_name, dump_path)

    operations.local(cmd)


def _db_export(db_name, dump_path='/tmp/dfs_exported.dump'):
    """exports a database to file"""

    operations.require('environment')

    if env.environment != 'local':
        utils.abort('You cannot export a remote db')

    pg_dump_cmd = 'pg_dump'
    if env.virtual_machine_type == 'vagrant':
        pg_dump_cmd = 'sudo -u postgres pg_dump'

    cmd = '%s -Fc --no-acl --no-owner %s > %s' % (pg_dump_cmd, db_name, dump_path)

    _puts('Exporting %s database to %s' % (db_name, dump_path))
    operations.local(cmd)


def _get_local_git_db():
    """Add local git branch and db name for use when pushing"""
    env.local_git_branch = operations.local('git rev-parse --abbrev-ref HEAD', capture=True)
    env.db_name = 'dfs_' + env.local_git_branch


def _importdb(db_name, db_dump):
    # drop, create, then import db
    _db_drop_then_create(db_name)
    _db_restore(db_name, db_dump)

    # flush out redis
    flush_cache()


def _puts(message):
    """Extends puts to separate out what we're doing"""
    utils.puts('\n- %s' % message)


def _python():
    """Returns the proper alias for python, depending on environment"""
    return 'python3' if env.virtual_machine_type == 'docker' else 'python'


def _show_progress(current_bytes, total_bytes):
    """Shortcut to print out progress of bytes being pulled down"""
    print('%s%%' % int(round(current_bytes / total_bytes * 100)))


# AVAILABLE FAB COMMANDS

def db2s3():
    """
    fab db2s3 --set s3file=thefilenameons3

    Upload a postgres dump to s3

        $> sudo pip3 install awscli
        $> sudo pip3 install --upgrade awscli
        $> aws configure
        AWS Access Key ID [None]: AKIAIJC5GEI5Y3BEMETQ
        AWS Secret Access Key [None]: AjurV5cjzhrd2ieJMhqUyJYXWObBDF6GPPAAi3G1
        Default region name [None]: us-east-1
        Default output format [None]:
        $> aws s3 cp dfs_master_example.dump s3://draftboard-db-dumps/dfs_master_example.dump    # <--- db2s3 does this cmd
        upload: ./dfs_master_example.dump to s3://draftboard-db-dumps/dfs_master_example.dump
        $>

    :param: --set s3file=thefilenameons3
    :return:
    """

    # filename on s3
    db_dump_name = env.s3file

    cmd = 'aws s3 cp %s s3://draftboard-db-dumps/%s' % (db_dump_name, db_dump_name)
    _puts('%s' % cmd)
    operations.local(cmd)


def deploy():
    """fab [env] deploy (pushes changes up to heroku)"""

    operations.require('environment')
    _puts('Git push to %s' % env.environment)
    operations.local('git push -f %s %s:master' % (
        env.heroku_repo,
        env.local_git_branch,
    ))

    # set the git hash so we can cache version localStorage
    git_hash = hashlib.md5(check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()).hexdigest()
    operations.local('heroku config:set GIT_COMMIT_UUID=%s -a %s' % (
        git_hash,
        env.heroku_repo
    ))


def exportdb():
    """
    fab [env] [virtual_machine_type] exportdb

    exports the environment database to `/tmp/dfs_exported.dump`
    """

    operations.require('environment')

    if env.environment == 'local':
        _db_export(env.db_name)


def flush_cache():
    """
    fab [env] [virtual_machine_type] flush_cache

    wipes redis
    """

    operations.require('environment')

    if env.environment == 'local':
        _puts('Flushing memcached')
        operations.local('%s manage.py flush_cache' % _python())  # use default settings here
    else:
        if env.environment == 'production' and not _confirm('Are you sure you want to wipe memcached on the production server?'):
            utils.abort('Aborting at user request')

        operations.local('heroku run %s manage.py flush_cache --app %s' % (_python(), env.heroku_repo))


def flush_pyc():
    """
    fab local [virtual_machine_type] flush_pyc

    removes all .pyc files, use if django is failing after switching branches
    """

    operations.require('environment')
    operations.local('find . -name "*.pyc" -delete')


def generate_replayer():
    """
    fab [virtual_machine_type] generate_replayer --set start=2016-03-01,end=2016-03-02,[sport=mlb],[download=true]
    fab local docker generate_replayer --set start=2016-10-19,end=2016-10-20,sport=nba

    Command that generates a database dump consisting of data between two dates, and TimeMachine instances for every
    draft group between the two.

    The resulting dump will be /tmp/replayer.dump

    optional parameter to filter by sport, `--set sport=mlb`, choices are ['mlb', 'nhl', 'nba']
    optional parameter to download instances, `--set download=true`
    """

    # check we have needed parameters
    if 'start' not in env or 'end' not in env:
        utils.abort('You need to add --set start=[2016-03-01],end=[2016-03-02] to the fab command')

    tmp_dir = '/tmp'
    startFilename = 'start.dump'
    endFilename = 'end.dump'

    if 'download' in env and env.download == 'true':
        # this key/value gives full access to s3, need to pare down to just the right bucket.
        AWS_ACCESS_KEY_ID = 'AKIAIJC5GEI5Y3BEMETQ'
        AWS_SECRET_ACCESS_KEY = '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'
        AWS_STORAGE_BUCKET_NAME = 'k6yjtzz2xuccqyn'

        c = S3Connection(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        bucket = c.get_bucket(AWS_STORAGE_BUCKET_NAME)

        # download start
        startS3Filename = '%s' % env.start
        print("Downloading: %s" % startS3Filename)
        keyStart = bucket.get_key('pgbackups/%s' % startS3Filename)
        keyStart.get_contents_to_filename('%s/%s' % (tmp_dir, startFilename), cb=_show_progress, num_cb=10)
        # operations.local('gunzip %s/%s.gz' % (tmp_dir, startFilename))

        # download end
        endS3Filename = '%s' % env.end
        print("Downloading: %s" % startS3Filename)
        keyEnd = bucket.get_key('pgbackups/%s' % endS3Filename)
        keyEnd.get_contents_to_filename('%s/%s' % (tmp_dir, endFilename), cb=_show_progress, num_cb=10)
        # operations.local('gunzip %s/%s.gz' % (tmp_dir, endFilename))

    temp_db = 'generate_replayer'

    psql_user = ''
    if env.virtual_machine_type == 'vagrant':
        psql_user = 'sudo -u postgres'

    with warn_only():
        _importdb(temp_db, '%s/%s' % (tmp_dir, startFilename))

        # remove all updates
        operations.local(
            '%s psql -d %s -c "DROP TABLE replayer_update, replayer_replay;"' % (
                psql_user,
                temp_db
            )
        )

    # load in needed tables from end
    operations.local('%s pg_restore --no-acl --no-owner -d %s %s %s/%s' % (
        psql_user,
        temp_db,
        '-t replayer_replay -t replayer_update',
        tmp_dir,
        endFilename
    ))

    # delete updates older than the time you did step 1 from replayer_update
    operations.local(
        '%s psql -d %s -c "DELETE FROM replayer_update WHERE ts < \'%s\';"' % (
            psql_user,
            temp_db,
            env.start[:10]
        )
    )

    # remove all scheduled tasks except for contest pools
    operations.local('%s psql -d %s -c "update django_celery_beat_periodictask set enabled=\'f\';"' % (
        psql_user,
        temp_db
    ))

    # remove other sport replayer updates, time machines, if sport is chosen
    if 'sport' in env and env.sport in ['mlb', 'nba', 'nhl', 'nfl']:
        operations.local('%s psql -d %s -c "delete from replayer_update where ns not ILIKE \'%%%s%%\';"' % (
            psql_user,
            temp_db,
            env.sport
        ))
        operations.local('%s psql -d %s -c "delete from replayer_timemachine;"' % (
            psql_user,
            temp_db
        ))
        operations.local('''
            %s psql -d %s -c "update django_celery_beat_periodictask set enabled=\'t\' where
            task=\'contest.schedule.tasks.create_scheduled_contest_pools\' AND args ILIKE \'%%%s%%\';"
        ''' % (
            psql_user,
            temp_db,
            env.sport
        ))

    # loop through applicable draft_group rows and create time_machine rows, based on start and end dates
    operations.local(
        'DJANGO_SETTINGS_MODULE="mysite.settings.local_replayer_generation" %s manage.py generate_timemachines %s %s' %
        (_python(), env.start[:10], env.end[:10])
    )

    # export finished db
    _db_export(temp_db, '/tmp/replayer_generated.dump')


def heroku_restore_db():
    """
    fab heroku_restore_db

    Restore amazon s3 db into heroku
    """
    # operations.local("sudo apt-get update -y")
    operations.local("sudo pip3 install awscli")
    operations.local("sudo pip3 install --upgrade awscli")
    operations.local("aws configure <<< 'AKIAIJC5GEI5Y3BEMETQ\nAjurV5cjzhrd2ieJMhqUyJYXWObBDF6GPPAAi3G1\nus-east-1\n\n'")


def importdb():
    """
    fab [env] [virtual_machine_type] importdb --set db_dump=/path/to/database/dump,[db_url=https://path.com/to/database/dump]

    takes provided db and creates env db with it
    """
    operations.require('environment')

    if env.environment == 'local':
        if 'db_dump' not in env:
            utils.abort('You need to add --set db_dump=/path/to/database/dump to the fab command')

        _importdb(env.db_name, env.db_dump)

        return

    # otherwise we are replacing a heroku db SCARY
    # remove this ability on production once we have a staging, testing envs

    if 'db_url' not in env:
        utils.abort('You need to add --set db_url=https://path.com/to/database/dump to the fab command')

    _puts('Backing up %s db' % env.environment)
    operations.local(
        'heroku pg:backups capture --app %s' % ENVS[env.environment]['heroku_repo']
    )

    _puts('Wiping %s db' % env.environment)
    operations.local('heroku pg:reset DATABASE --app %s --confirm %s' % (
        ENVS[env.environment]['heroku_repo'],
        ENVS[env.environment]['heroku_repo']
    ))

    _puts('Creating %s db from uploaded backup' % env.environment)
    operations.local('heroku pg:backups restore %s --app %s %s --confirm %s' % (
        ENVS[env.environment]['database_url'],
        ENVS[env.environment]['heroku_repo'],
        env.db_url,
        ENVS[env.environment]['heroku_repo'],
    ))


def pg_info():
    """
    fab pg_info
    """
    # _puts('heroku pg:info')
    # operations.local('sudo -u postgres dropdb -U postgres %s' % env.db_name)
    operations.local('heroku pg:info')  # <<< "cbanister@coderden.com\ncalebriodfs\n"')


def restore_db():
    """
    To restore a postgres dump, you must have previously uploaded it with something like:

        $> sudo pip3 install awscli
        $> sudo pip3 install --upgrade awscli
        $> aws configure
        AWS Access Key ID [None]: AKIAIJC5GEI5Y3BEMETQ
        AWS Secret Access Key [None]: AjurV5cjzhrd2ieJMhqUyJYXWObBDF6GPPAAi3G1
        Default region name [None]: us-east-1
        Default output format [None]:
        $> aws s3 cp dfs_master_example.dump s3://draftboard-db-dumps/dfs_master_example.dump
        upload: ./dfs_master_example.dump to s3://draftboard-db-dumps/dfs_master_example.dump
        $>

    :param: --set s3file=thefilenameons3
    :return:
    """
    # filename on s3
    S3_FILE = env.s3file  # 'dfs_master_example.dump'

    AWS_ACCESS_KEY_ID = 'AKIAIJC5GEI5Y3BEMETQ'
    AWS_SECRET_ACCESS_KEY = 'AjurV5cjzhrd2ieJMhqUyJYXWObBDF6GPPAAi3G1'
    AWS_STORAGE_BUCKET_NAME = 'draftboard-db-dumps'

    connection = S3Connection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # reference http://boto.readthedocs.org/en/latest/ref/s3.html#boto.s3.key.Key.generate_url
    url = connection.generate_url(
        60,
        'GET',
        AWS_STORAGE_BUCKET_NAME,
        S3_FILE,
        response_headers={
            'response-content-type': 'application/octet-stream'
        })

    _puts('s3 url -> %s' % url)

    # example:heroku pg:backups restore 'https://draftboard-db-dumps.s3.amazonaws.com/dfs_master.dump?Signature=Ft3MxTcq%2BySJ9Y7lkBp1Vig5sTY%3D&Expires=1449611209&AWSAccessKeyId=AKIAIJC5GEI5Y3BEMETQ&response-content-type=application/octet-stream' DATABASE_URL --app draftboard-prod --confirm draftboard-prod
    operations.local("heroku pg:backups restore '%s' DATABASE_URL --app draftboard-delorean --confirm draftboard-delorean" % url)

def reset_replay():
    # /admin/replayer/timemachine/
    # 1. its always a good idea to turn off celerbeat (the scheduler)
    #    before loading the replay so nothing kicks of prematurely.
    #    the replay .dump SHOULD have all its cronned tasks disabled when its restored however.
    #    remember to turn celerybeat back on later if you disable it initially.
    operations.local("heroku maintenance:on --app draftboard-delorean")
    operations.local("heroku ps:scale --app draftboard-delorean heroku ps:scale --app draftboard-delorean web=0 purger=0 celery300=0 celeryrt=0 celerybeat=0 celery=0")

    # works - restores the draftboard-delorean postgres db with the public dump
    #         just be careful not to use the INPROGRESS one which
    operations.local("heroku pg:backups --app draftboard-delorean restore 'https://s3.amazonaws.com/draftboard-db-dumps/nfl_replay_aug_11_645pm_est.dump' DATABASE_URL --confirm draftboard-delorean")

    # we are going to want to always trigger the following things:
    operations.local("heroku run --app draftboard-delorean python manage.py flush_cache")
    operations.local("heroku run --app draftboard-delorean python manage.py migrate")

    # sets the server time to ~3 hours before the 'ts' field of the first Update in /admin/replayer/update/
    operations.local("heroku run --app draftboard-delorean python manage.py set_time_before_replay_start")

    # these processes should be running before you start the replay using /admin/replayer/timemachine/
    # you may find that you want more than web dyno, but the rest should be totally fine for running a replay.
    operations.local("heroku ps:scale --app draftboard-delorean web=2 purger=2")
    operations.local("heroku ps:scale --app draftboard-delorean celeryrt=1 celerybeat=1")

    # you can turn maintenance off as early as now
    operations.local("heroku maintenance:off --app draftboard-delorean")

def s3ls():
    """
    list the dumps in s3://draftboard-db-dumps/
    """
    cmd = 'aws s3 ls s3://draftboard-db-dumps/'
    _puts('%s' % cmd)
    operations.local(cmd)


def syncdb(app=None):
    """
    fab [env] syncdb [--set no_backup=true]

    uses heroku pg:backups to capture a snapshot of the target server.
    downloads the snapshot, drops and does a pg_restore into our
    current branches database. (_get_local_git_db() sets the env.db_name)
    """

    operations.require('environment')

    if app is None:
        app = 'production'

    target_server = ENVS[app]['heroku_repo']

    # quick disclaimer about overwriting the production db...
    if (env.environment == 'production'):
        utils.abort('You cannot sync the production database to itself')

    # if we want a new version, then capture new backup of production
    if 'no_backup' not in env:
        _puts('Capturing new [%s] backup' % target_server)
        operations.local('heroku pg:backups capture --app %s' % target_server)

    # pg_restore the downloaded .dump to the local "dfs_GITBRANCHNAME" database
    if env.environment != 'local':
        _puts('You can only drop&restore the database in your personal dev environment!'
              ' Currently your environment is: %s' % env.environment)
        return

    with warn_only():
        # download backup
        _puts('Pull latest [%s] backup down to local' % target_server)
        operations.local('curl -o /tmp/latest.dump `heroku pg:backups public-url --app %s`' % target_server)

        # import database
        _importdb(env.db_name, '/tmp/latest.dump')


# Environments methods (required to run at least once for any method)

def local():
    """fab local [virtual_machine_type] [command]"""

    env.environment = 'local'
    _get_local_git_db()


def dev():
    """fab dev [virtual_machine_type] [command]"""

    testing = ENVS['dev']

    env.environment = 'dev'
    env.heroku_repo = testing['heroku_repo']
    _get_local_git_db()


def delorean():
    """fab testing [virtual_machine_type] [command]"""

    delorean = ENVS['delorean']

    env.environment = 'delorean'
    env.heroku_repo = delorean['heroku_repo']
    _get_local_git_db()


def production():
    """fab production [virtual_machine_type] [command]"""

    production = ENVS['production']

    env.environment = 'production'
    env.local_git_branch = production['local_git_branch']
    env.heroku_repo = production['heroku_repo']
    _confirm_env()


# Virtual machine prefs

def docker():
    """fab [env] docker [command]"""

    env.virtual_machine_type = 'docker'


def vagrant():
    """fab [env] vagrant [command]"""

    # default to local settings
    django.settings_module('mysite.settings.local')
    env.virtual_machine_type = 'vagrant'
