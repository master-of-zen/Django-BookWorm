#!/usr/bin/env python3
import subprocess
import os
path = os.getcwd() + '/manage.py'

try:
    subprocess.run([path, 'runserver'])

except KeyboardInterrupt:
    print(f'\n Server Stoped')
    os._exit()
