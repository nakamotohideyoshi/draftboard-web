from fabric.api import env, warn_only
from fabric.contrib import django
from fabric import operations
from fabric import utils
from subprocess import check_output
from distutils.util import strtobool
from boto.s3.connection import S3Connection
import hashlib

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


ENVS = {
    'production': {
        'local_git_branch': 'master',
        'heroku_repo': 'draftboard-staging',  # currently draftboard-staging is the production server
    },
    'staging': {
        'local_git_branch': 'master',
        'heroku_repo': 'draftboard-staging',
    },
    'dev': {
        'heroku_repo': 'draftboard-dev',
    },
}

django.settings_module('mysite.settings.local')



def _confirm_env():
    """Confirms you want to run the commands on Heroku"""
    if not _confirm('Are you sure you want to run these commands on the %s environment? ' % env.environment):
        utils.abort('Aborting at user request')


def deploy():
    """fab [environment] deploy (pushes changes up to heroku)"""

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

    #
    # TODO
    # after git push, we should do a $> heroku run python manage.py migrate

def exportdb():
    """fab [environment] exportdb (exports the environment database to `/tmp/dfs_exported.dump`)"""

    operations.require('environment')

    if env.environment == 'local':
        _puts('Exporting local database to `/tmp/dfs_exported.dump`')
        operations.local('sudo -u postgres pg_dump -Fc --no-acl --no-owner %s > /tmp/dfs_exported.dump' % (env.db_name))


def flush_cache():
    """fab [environment] flush_cache (wipes redis)"""

    operations.require('environment')

    if env.environment == 'local':
        _puts('Flushing memcached')
        operations.local('python manage.py flush_cache --settings mysite.settings.local')
    else:
        if env.environment == 'production' and not _confirm('Are you sure you want to wipe memcached on the production server?'):
            utils.abort('Aborting at user request')

        operations.local('heroku run python manage.py flush_cache --app %s' % env.heroku_repo)


def flush_pyc():
    """fab local flush_pyc (removes all .pyc files, use if django is failing after switching branches)"""

    operations.require('environment')
    operations.local('find . -name "*.pyc" -delete')


def _get_local_git_db():
    """Add local git branch and db name for use when pushing"""

    _puts('Determining envirnoment git branch, dbname')
    env.local_git_branch = operations.local('git rev-parse --abbrev-ref HEAD', capture=True)
    env.db_name = 'dfs_' + env.local_git_branch


def importdb():
    """fab [environment] importdb --set db_dump=/path/to/database/dump --set db_url=https://path.com/to/database/dump
       (takes provided db and creates env db with it)"""
    # ./manage.py dumpdata --exclude=contenttypes -o test_fixture.json
    operations.require('environment')

    if env.environment == 'local':
        if 'db_dump' not in env:
            utils.abort('You need to add --set db_dump=/path/to/database/dump to the fab command')

        # copy db to tmp dir
        _puts('Copying local to /tmp to then run syncdb with')

        operations.local('cp %s /tmp/latest.dump' % env.db_dump)

        # then run the syncdb no-backup command for local
        env.no_backup = True
        syncdb()

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


def syncdb(app=None):
    """
    fab [environment] syncdb [--set no_backup=true]

    uses heroku pg:backups to capture a snapshot of the target server.
    downloads the snapshot, drops and does a pg_restore into our
    current branches database. (_get_local_git_db() sets the env.db_name)
    """

    operations.require('environment')

    if app is None:
        app = 'staging'

    target_server = ENVS[app]['heroku_repo']

    # quick disclaimer about overwriting the production db...
    if (env.environment == 'production'):
        utils.abort('You cannot sync the production database to itself')

    #
    # always wipe memcached before putting in new db
    # TODO fix with virtualenv
    # flush_cache()

    #
    # if we want a new version, then capture new backup of production
    if 'no_backup' not in env:
        _puts('Capturing new [%s] backup' % target_server)
        operations.local('heroku pg:backups capture --app %s' % target_server)

    #
    # pg_restore the downloaded .dump to the local "dfs_GITBRANCHNAME" database
    if env.environment != 'local':
        _puts('You can only drop&restore the database in your personal dev environment!'
              ' Currently your environment is: %s' % env.environment)
        return

    with warn_only():
        # download backup
        _puts('Pull latest [%s] backup down to local' % target_server)
        operations.local('curl -so /tmp/latest.dump `heroku pg:backups public-url --app %s`' % target_server)

        # drop local database
        _puts('Dropping local database: %s' % env.db_name)
        operations.local('sudo -u postgres dropdb -U postgres %s' % env.db_name)

        # [re]create empty local database, and pg_restore the backup into it
        _puts('Creating local database')
        operations.local('sudo -u postgres createdb -U postgres -T template0 %s' % env.db_name)
        operations.local('sudo -u postgres pg_restore --no-acl --no-owner -d %s /tmp/latest.dump' % env.db_name)

def _puts(message):
    """Extends puts to separate out what we're doing"""
    utils.puts('\n- %s' % message)


# Environments methods (required to run at least once for any method)

def local():
    """fab local [command]"""

    env.environment = 'local'
    _get_local_git_db()


def dev():
    """fab local [command]"""

    testing = ENVS['dev']

    env.environment = 'dev'
    env.heroku_repo = testing['heroku_repo']
    _get_local_git_db()


def testing():
    """fab local [command]"""

    testing = ENVS['testing']

    env.environment = 'testing'
    env.heroku_repo = testing['heroku_repo']
    _get_local_git_db()


def production():
    """fab production [command]"""

    production = ENVS['production']

    env.environment = 'production'
    env.local_git_branch = production['local_git_branch']
    env.heroku_repo = production['heroku_repo']
    _confirm_env()

def pg_info():
    """
    fab pg_info
    """
    #_puts('heroku pg:info')
    #operations.local('sudo -u postgres dropdb -U postgres %s' % env.db_name)
    operations.local('heroku pg:info') # <<< "cbanister@coderden.com\ncalebriodfs\n"')

def heroku_restore_db():
    """

    """
    #operations.local("sudo apt-get update -y")
    operations.local("sudo pip3 install awscli")
    operations.local("sudo pip3 install --upgrade awscli")
    operations.local("aws configure <<< 'AKIAIJC5GEI5Y3BEMETQ\nAjurV5cjzhrd2ieJMhqUyJYXWObBDF6GPPAAi3G1\nus-east-1\n\n'")

# def tester():
#     """
#     --set arg1=someval
#     """
#     _puts('arg1: %s' % env.arg1)

def generate_replayer():
    """
    Command that generates a database dump consisting of data between two dates, and TimeMachine instances for every
    draft group between the two.

    The resulting dump will be /tmp/replayer.dump

    fab generate_replayer --set start=2016-03-01,end=2016-03-02
    """
    def _show_progress(current_bytes, total_bytes):
        print('%s%%' % int(round(current_bytes/total_bytes * 100)))

    # check we have needed parameters
    if 'start' not in env or 'end' not in env:
        utils.abort('You need to add --set start=[2016-03-01],end=[2016-03-02] to the fab command')

    # this key/value gives full access to s3, need to pare down to just the right bucket.
    AWS_ACCESS_KEY_ID = 'AKIAIJC5GEI5Y3BEMETQ'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'k6yjtzz2xuccqyn'

    c = S3Connection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket = c.get_bucket(AWS_STORAGE_BUCKET_NAME)

    # download, unzip start
    tmp_dir = '/tmp'

    startFilename = 'start.dump'
    startS3Filename = '%s-10-00-draftboard-staging-HEROKU_POSTGRESQL_ONYX_URL.dump.gz' % env.start
    keyStart = bucket.get_key('draftboard-staging/HEROKU_POSTGRESQL_ONYX_URL/%s' % startS3Filename)
    keyStart.get_contents_to_filename('%s/%s.gz' % (tmp_dir, startFilename), cb=_show_progress, num_cb=10)
    operations.local('gunzip %s/%s.gz' % (tmp_dir, startFilename))

    # download end
    endFilename = 'end.dump'
    endS3Filename = '%s-10-00-draftboard-staging-HEROKU_POSTGRESQL_ONYX_URL.dump.gz' % env.end
    keyEnd = bucket.get_key('draftboard-staging/HEROKU_POSTGRESQL_ONYX_URL/%s' % endS3Filename)
    keyEnd.get_contents_to_filename('%s/%s.gz' % (tmp_dir, endFilename), cb=_show_progress, num_cb=10)
    operations.local('gunzip %s/%s.gz' % (tmp_dir, endFilename))

    temp_db = 'generate_replayer'

    with warn_only():
        # load start into temporary db
        _puts('Restoring start db into %s' % temp_db)

        operations.local('sudo -u postgres dropdb -U postgres %s' % temp_db)
        operations.local('sudo -u postgres createdb -U postgres -T template0 %s' % temp_db)
        operations.local(
            'sudo -u postgres pg_restore --no-acl --no-owner -d %s %s/%s' % (temp_db, tmp_dir, startFilename)
        )

        # remove all updates
        operations.local(
            'sudo -u postgres psql -d %s -c "DROP TABLE replayer_update, replayer_replay;"' % (
                temp_db
            )
        )

    # load in needed tables from end
    _puts('Loading replay tables from end dump into %s' % temp_db)

    operations.local('sudo -u postgres pg_restore --no-acl --no-owner -d %s %s %s/%s' % (
        temp_db,
        '-t replayer_replay -t replayer_update',
        tmp_dir,
        endFilename
    ))

    # delete updates older than the time you did step 1 from replayer_update
    operations.local(
        'sudo -u postgres psql -d %s -c "DELETE FROM replayer_update WHERE ts < \'%s\';"' % (
            temp_db,
            env.start
        )
    )

    # loop through applicable draft_group rows and create time_machine rows, based on start and end dates
    operations.local(
        'DJANGO_SETTINGS_MODULE="mysite.settings.local_replayer_generation" python manage.py generate_timemachines %s %s' %
        (env.start, env.end)
    )

    # export finished db
    operations.local('sudo -u postgres pg_dump -Fc --no-acl --no-owner %s > /tmp/replayer_generated.dump' % temp_db)


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
    S3_FILE = env.s3file #'dfs_master_example.dump'

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

    # example:heroku pg:backups restore 'https://draftboard-db-dumps.s3.amazonaws.com/dfs_master.dump?Signature=Ft3MxTcq%2BySJ9Y7lkBp1Vig5sTY%3D&Expires=1449611209&AWSAccessKeyId=AKIAIJC5GEI5Y3BEMETQ&response-content-type=application/octet-stream' DATABASE_URL --app draftboard-staging --confirm draftboard-staging
    operations.local("heroku pg:backups restore '%s' DATABASE_URL --app draftboard-staging --confirm draftboard-staging" % url)

def db2s3():
    """
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
    db_dump_name = env.s3file #

    cmd = 'aws s3 cp %s s3://draftboard-db-dumps/%s' % (db_dump_name, db_dump_name)
    _puts('%s' % cmd)
    operations.local(cmd)

def s3ls():
    """
    list the dumps in s3://draftboard-db-dumps/
    """
    cmd = 'aws s3 ls s3://draftboard-db-dumps/'
    _puts('%s' % cmd)
    operations.local(cmd)
