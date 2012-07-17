#!/usr/bin/env python
import socket
from os import chdir
from subprocess import check_output, CalledProcessError

from path import path

import ssh


def parse_args():
    """Parses arguments, returns ``(options, args)``."""
    from argparse import ArgumentParser

    parser = ArgumentParser(description="""\
Publish git repo in current path to github.""",
                           )
    parser.add_argument('-p', '--path', dest='repo_path', type=str)
    parser.add_argument('-n', '--name', dest='repo_name', type=str)
    parser.add_argument(nargs='?', dest='github_remote', type=str, default='github')
    args = parser.parse_args()
    
    return args


if __name__ == '__main__':
    args = parse_args()
    print args.github_remote

    if args.repo_path:
        chdir(path(args.repo_path).abspath())
    assert(path('.git').exists())
    cwd = path('.').abspath()
    if args.repo_name is None:
        args.repo_name = cwd.name

    cmd1 = '''curl -u cfobel https://api.github.com/user/repos -d '{"name": "%s"}' ''' % args.repo_name
    cmd2 = '''git remote add %s git@github.com:cfobel/%s.git''' % (args.github_remote, args.repo_name)
    cmd3 = '''git push -u %s master''' % (args.github_remote)
    cmd4 = '''git pull %s''' % (args.github_remote)

    for cmd in [cmd1, cmd2, cmd3, cmd4]:
        try:
            output = check_output(cmd, shell=True)
            print cmd
        except CalledProcessError:
            print output
