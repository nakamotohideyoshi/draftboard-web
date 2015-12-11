#!/usr/bin/env /home/vagrant/venv/bin/python3
import os
import sys

if __name__ == "__main__":
    #
    # os.environ.setdefault() -
    #
    # source: https://docs.python.org/3.4/library/stdtypes.html#dict.setdefault
    #
    #   If key is in the dictionary, return its value.
    #   If not, insert key with a value of default and return default.
    #   default defaults to None.

    #
    # DJANGO_SETTINGS_MODULE is set in ubuntu in the
    #    /etc/profile
    current_settings_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.base")
    print('current_settings_module:', current_settings_module)

    #
    # *** if you want manage.py to print out whether or not its running on CodeShip:
    # running_on_codeship = os.environ.get('CI', None)
    # print('running_on_codehip: %s' % str(running_on_codeship))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
