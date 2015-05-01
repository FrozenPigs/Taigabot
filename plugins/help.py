import re
from util import hook, user, web

@hook.command(autohelp=False)
def commands(inp, say=None, notice=None, input=None, conn=None, bot=None, db=None):
    "commands  -- Gives a list of commands/help for a command."
    funcs = {}
    disabled = bot.config.get('disabled_plugins', [])
    disabled_comm = bot.config.get('disabled_commands', [])
    for command, (func, args) in bot.commands.iteritems():
	fn = re.match(r'^plugins.(.+).py$', func._filename)

	if fn.group(1).lower() not in disabled and command not in disabled_comm: # Ignores disabled plugins and commands
		if args.get('channeladminonly', False) and not user.is_admin(input.mask, input.chan, db, bot):
			continue
		if args.get('adminonly', False) and not user.is_globaladmin(input.mask, input.chan, bot):
			continue
		if func.__doc__ is not None:
			if func in funcs:
				if len(funcs[func]) < len(command):
	                                funcs[func] = command
			else:
				funcs[func] = command

    commands = dict((value, key) for key, value in funcs.iteritems())

    if not inp:
        output = []
        well = []
	line = []
	help = "For detailed help, do '{}help <example>' where <example> "\
	       "is the name of the command you want help for.".format(conn.conf["command_prefix"])

        for command in commands:
            well.append(command)
        well.sort()

        for command in well:
		if output == [] and line == []:
			line.append("Commands you have access to ({}): {}".format(len(well), str(command)))
		else:
			line.append(str(command))
		if len(", ".join(line)) > 405:
			output.append(", ".join(line))
			line = []
	if len(line) > 0:
		output.append(", ".join(line))
	if len(output) == 1:
		output.append(help)
		for line in output:
			notice(line)
	else:
		output = ", ".join(output)
		haste = web.haste("{}\n\n{}".format(output, help))
		notice("Commands you have access to ({}): {}".format(len(well), haste))
    elif inp in commands:
	notice("{}{}".format(conn.conf["command_prefix"], commands[inp].__doc__))
    return


@hook.command('command', autohelp=False)
@hook.command(autohelp=False)
def help(inp, say=None, notice=None, input=None, conn=None, bot=None):
    if not inp:
        say("For help visit http://uguubot.com or see .COMMANDS")
    else:
        commands(inp, say, notice, input, conn, bot)
    return


# @hook.command(autohelp=False)
# def export(inp, say=None, notice=None, input=None, conn=None, bot=None):
#     #print bot.commands #.iteritems()
#     helptext = ''
#     for command, (func, args) in bot.commands.iteritems():
#         #print command.__doc__
#         helptext = helptext + u'{}\n'.format(func.__doc__).encode('utf-8')
            
#         #print '{} {} {}'.format(command,func,args)

#     with open('plugins/data/help.txt', 'a') as file:
#         file.write(u'{}\n'.format(helptext).encode('utf-8'))
#     file.close()
#     print helptext
