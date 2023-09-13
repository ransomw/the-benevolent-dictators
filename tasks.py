"""
may need modifications according to OS

see
https://github.com/pyinvoke/invoke/issues/752
"""
import os

from invoke import task


@task
def clean(c, docs=False, bytecode=False, extra=''):
    """Remove build artifacts"""
    if not os.path.exists("/bin/bash"):
        c.config.run.shell = "/bin/sh"

    patterns = ['dist']
    if docs:
        patterns.append('site')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def build(c, docs=False):
    """Create python package and documentation"""
    if not os.path.exists("/bin/bash"):
        c.config.run.shell = "/bin/sh"

    c.run("python -m build")
    if docs:
        c.run("mkdocs build", env={'PYTHONPATH': '.'})
