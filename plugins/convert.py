from util import hook
import re

# <number>[ from] <unit> to <unit>
CONVERT_RE = r'([\d.,]+)( from)? ([°a-z]+) to ([°a-z]+)'


# add common names, abbreviations (and typos) for units
# the first one will be shown to the user
temperatures = [
    ['c', 'celsius'],  # shouldn't this be "°C"?
    ['f', 'fahrenheit'],
    ['K', 'kelvin']
]

lengths = [
    ['m', 'meter', 'metre', 'mt'],
    ['km', 'kms', 'kilometer', 'kilometre'],
    ['cm', 'cms', 'centimeter', 'centimetre'],
    ['in', 'inch', 'inches'],
    ['ft', 'feet', 'foot'],
    ['mi', 'mile', 'miles']
]


def find_unit(inp):
    for names in temperatures:
        if inp in names:
            return ('temperature', names[0])

    for names in lengths:
        if inp in names:
            return ('length', names[0])

    return ('unknown', False)


@hook.command
def convert(inp):
    "convert <number> <unit> to <unit> -- transform between different commonly used "

    match = re.search(CONVERT_RE, inp, re.I)

    if not match:
        return "[convert] cant understand that input. syntax: convert 123 f to c"

    number = match.group(1)
    source_unit = match.group(3).lower()
    target_unit = match.group(4).lower()

    try:
        number = float(number)
    except ValueError:
        return "[convert] input is not a number"

    source_type, source_unit = find_unit(source_unit)
    target_type, target_unit = find_unit(target_unit)

    if source_type == 'unknown' or target_type == 'unknown':
        return "[convert] unknown unit, try something else (or use wolfram alpha)"

    if source_unit == target_unit:
        return "[convert] nothing to transform because {} = {}".format(source_unit, target_unit)

    if source_type == 'temperature':
        if source_unit == 'c' and target_unit == 'f':
            conversion = 9.0 / 5.0 * number + 32
            return "[convert] {:.2f} °C = {:.2f} °F".format(number, conversion)
        elif source_unit == 'f' and target_unit == 'c':
            conversion = (number - 32) * 5.0 / 9.0
            return "[convert] {:.2f} °F = {:.2f} °C".format(number, conversion)

    return "[convert] cant transform {} to {}".format(source_unit, target_unit)
