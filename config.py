"""
Config settings for gunicorn.
"""

import multiprocessing

import sys, os.path as path
package_path = path.dirname(path.realpath(__file__))
sys.path.append(package_path)

from web.config \
    import PAPERTRAIL_HOST as HOST, PAPERTRAIL_PORT as PORT

## Server Socket
# bind = '0.0.0.0:5000'
bind = 'unix:/tmp/gunicorn.sock'

## Process Naming
proc_name = 'web'

## Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 300

## Logging
loglevel = 'info'
syslog = True
syslog_addr = 'udp://%s:%s' % (HOST, PORT)
syslog_facility = 'local0'
