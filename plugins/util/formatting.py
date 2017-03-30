def filesize(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
<<<<<<< HEAD
            return '{0:.2f}{1}{2}'.format(num, unit, suffix)
        num /= 1024.0
    return '{0:.1f}{}{}'.format(num, 'Yi', suffix)

def output(scriptname, fields=[], color=11):
    return '[{}] {}'.format(scriptname, ' - '.join(fields))
=======
            return "{0:.2f}{1}{2}".format(num, unit, suffix)
        num /= 1024.0
    return "{0:.1f}{}{}".format(num, 'Yi', suffix)
>>>>>>> 19cc49a2bf56d7a420b529988a8c5638cce5e648
