"""
Hacky, library and usage specific tricks to infer decent defaults.
"""
import os
import subprocess
import sys

def dfl_local_dir():
    """
    Infers a default local directory, which is ~/track/<project name>,
    where the project name is guessed according to the following rules.

    If we detect we're in a repository, the project name is the repository name
    (git only for now).

    If we're not in a repository, and the script file sys.argv[0] is non-null,
    then that is used.

    Otherwise, we just say it's "unknown"
    """
    project_name = git_repo()
    if not project_name and sys.argv:
        project_name = sys.argv[0]
    if not project_name:
        project_name = "unknown"
    dirpath = os.path.join("~", "track", project_name)
    return os.path.expanduser(dirpath)

def git_repo():
    """
    Returns the git repository root if the cwd is in a repo, else None
    """
    try:
        reldir = subprocess.check_output(
            ['git', 'rev-parse', '--git-dir'])
        reldir = reldir.decode('utf-8')
        return os.path.basename(os.path.dirname(os.path.abspath(reldir)))
    except subprocess.CalledProcessError:
        return None
