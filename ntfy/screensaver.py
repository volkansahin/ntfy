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


def lightlocker_detect():
    try:
        check_call(split('pgrep light-locker'), stdout=PIPE)
    except CalledProcessError:
        return False
    else:
        return True


def lightlocker_is_active():
    return 'The screensaver is active' in check_output(split(
        'light-locker-command -q'))


def is_locked():
    if xscreensaver_detect():
        return xscreensaver_is_locked()
    if lightlocker_detect():
        return lightlocker_is_active()
    return True
