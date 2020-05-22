# linux kernel version plugin by ine (2020)
from util import hook
from utilities import request
import re


@hook.command(autohelp=False)
def kernel(inp, reply=None):
    data = request.get("https://www.kernel.org/finger_banner")
    lines = data.split('\n')

    versions = []
    old_versions = []
    for line in lines:
        info = re.match(r'^The latest ([[a-z0-9 \-\.]+) version of the Linux kernel is:\s*(.*)$', line)
        if info is None:
            continue

        name = info.group(1)
        version = info.group(2)

        if 'longterm' in name:
            old_versions.append(version)
        else:
            versions.append(name + ': ' + version)

    output = 'Linux kernel versions: ' + '; '.join(versions)

    if len(old_versions) > 0:
        output = output + '. Old longterm versions: ' + ', '.join(old_versions)

    return output
