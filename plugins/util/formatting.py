def filesize(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return '{0:.2f}{1}{2}'.format(num, unit, suffix)
		num /= 1024.0
	return '{0:.1f}{}{}'.format(num, 'Yi', suffix)

def output(scriptname, fields=[], color=11):
	return '\x0F\x02{}\x02: {}'.format(scriptname, ' \x03{}\x02|\x02\x03 '.format(color).join(fields))
