from fabric.api import env, warn_only
from fabric.contrib import django
from fabric import operations
from fabric import utils
from distutils.util import strtobool


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
        'heroku_repo': 'rio-dfs',
    },
    'testing': {
        'heroku_repo': 'draftboard-testing',
    },
    'ios_sandbox': {
        'heroku_repo': 'draftboard-ios-sandbox',
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
        env.environment,
        env.local_git_branch,
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


def syncdb():
    """fab [environment] syncdb [--set no_backup=true] (resets db for testing server with production db)"""

    operations.require('environment')

    if (env.environment == 'production'):
        utils.abort('You cannot sync the production database to itself')

    # always wipe memcached before putting in new db
    # TODO fix with virtualenv
    # flush_cache()

    # if we want a new version, then capture new backup of production
    if 'no_backup' not in env:
        _puts('Capturing new production backup')
        operations.local(
            'heroku pg:backups capture --app %s' % ENVS['production']['heroku_repo']
        )

        # pull down db to local
        if env.environment == 'local':
            _puts('Pull latest production down to local')
            operations.local('curl -so /tmp/latest.dump `heroku pg:backups public-url --app rio-dfs`')

    # restore locally
    if (env.environment == 'local'):
        with warn_only():
            _puts('Dropping local database')
            operations.local('sudo -u postgres dropdb -U postgres %s' % env.db_name)

            _puts('Creating local database')
            operations.local('sudo -u postgres createdb -U postgres -T template0 %s' % env.db_name)
            operations.local(
                'sudo -u postgres pg_restore --no-acl --no-owner -d %s /tmp/latest.dump' %
                env.db_name
            )


def _puts(message):
    """Extends puts to separate out what we're doing"""
    utils.puts('\n- %s' % message)


# Environments methods (required to run at least once for any method)

def local():
    """fab local [command]"""

    env.environment = 'local'
    _get_local_git_db()


def ios_sandbox():
    """fab local [command]"""

    testing = ENVS['ios_sandbox']

    env.environment = 'ios-sandbox'
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
    fab production pg_info
    """
    #_puts('heroku pg:info')
    #operations.local('sudo -u postgres dropdb -U postgres %s' % env.db_name)
    operations.local('heroku pg:info') # <<< "cbanister@coderden.com\ncalebriodfs\n"')

