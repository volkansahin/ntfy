from shlex import split
from subprocess import check_output, check_call, CalledProcessError, PIPE


def xscreensaver_detect():
    try:
        check_call(split('pgrep xscreensaver'), stdout=PIPE)
    except CalledProcessError:
        return False
    else:
        return True


def xscreensaver_is_locked():
    return 'screen locked' in check_output(split('xscreensaver-command -time'))


def is_locked():
    if xscreensaver_detect():
        return xscreensaver_is_locked()
    return True
