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
    current_settigns_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.base")
    print('current_settings_module:', current_settigns_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
