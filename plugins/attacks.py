from util import hook, textgen, text
import random
import json

color_codes = {
    "<r>": "\x02\x0305",
    "<g>": "\x02\x0303",
    "<y>": "\x02"
}

with open("plugins/data/8ball_responses.txt") as f:
    responses = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/larts.txt") as f:
    larts = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/insults.txt") as f:
    insults = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/flirts.txt") as f:
    flirts = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/yiffs.txt") as f:
    yiffs = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/lewd.txt") as f:
    lewds = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/trolls.txt") as f:
    trolls = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/slogans.txt") as f:
    slogans = [line.strip() for line in f.readlines() if not line.startswith("//")]


with open("plugins/data/fortunes.txt") as f:
    fortunes = [line.strip() for line in f.readlines() if not line.startswith("//")]

with open("plugins/data/keks.txt") as f:
    keks = [line.strip() for line in f.readlines() if not line.startswith("//")]

with open("plugins/data/moists.txt") as f:
    moists = [line.strip() for line in f.readlines() if not line.startswith("//")]


@hook.command
def add(inp,notice=None):
    #inp = inp.split('add')[1]
    command = inp.split(' ')[0]
    text = inp.replace(command,'').strip()
    if 'loli' in command: command = 'lolis'
    elif 'insult' in command: command = 'insults'
    elif 'kek' in command: command = 'keks'
    elif 'flirt' in command: command = 'flirts'
    elif 'moist' in command: command = 'moists'
    elif 'lewd' in command: command = 'lewds'
    else: 
        notice('Invalid command')
        return

    with open('plugins/data/{}.txt'.format(command), 'a') as file:
        file.write('{}\n'.format(inp))

    notice('{} added.'.format(command))
    return


def get_generator(_json, variables):
    data = json.loads(_json)
    return textgen.TextGenerator(data["templates"], data["parts"], variables=variables)


def send_phrase(inp,attack,nick,conn,me,notice):
    target = inp.strip()

    if " " in target: 
        notice("Invalid username!")
        return

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() == "itself": target = nick

    values = {"user": target,"nick": conn.nick}
    phrase = random.choice(attack)
    print phrase
    # act out the message
    me(phrase.format(**values))
    return


@hook.command('8ball')
def eightball(input, me=None):
    """8ball <question> -- The all knowing magic eight ball,
    =in electronic form. Ask and it shall be answered!"""
    magic = text.multiword_replace(random.choice(responses), color_codes)
    me("shakes the magic 8 ball... {}".format(magic))
    return


@hook.command
def lart(inp, me=None, nick=None, conn=None, notice=None):
    """lart <user> -- LARTs <user>."""
    send_phrase(inp,larts,nick,conn,me,notice)
    return


@hook.command
def insult(inp, me=None, nick=None, conn=None, notice=None):
    """kill <user> -- Makes the bot kill <user>."""
    send_phrase(inp,insults,nick,conn,me,notice)
    return


@hook.command
def flirt(inp, me=None, nick=None, conn=None, notice=None):
    """kill <user> -- Makes the bot kill <user>."""
    send_phrase(inp,flirts,nick,conn,me,notice)
    return


@hook.command(autohelp=False)
def yiff(inp, me=None, nick=None, conn=None, notice=None):
    """yiff <user> -- yiffs <user>."""
    send_phrase(inp,yiffs,nick,conn,me,notice)
    return


@hook.command(autohelp=False)
def lewd(inp, me=None, nick=None, conn=None, notice=None):
    """lewd <user> -- lewd <user>."""
    if len(inp) == 0:
        return 'ヽ(◔ ◡ ◔)ノ.･ﾟ*｡･+☆LEWD☆'.decode('UTF-8')
    else:    
        send_phrase(inp,lewds,nick,conn,me,notice)
    return

@hook.command('wailord', autohelp=False)
@hook.command(autohelp=False)
def troll(inp, me=None, nick=None, conn=None, notice=None):
    """troll."""
    return u'{}'.format(random.choice(trolls))


@hook.command
def kill(inp, me=None, nick=None, conn=None, notice=None):
    """kill <user> -- Makes the bot kill <user>."""
    target = inp.strip()

    if " " in target:
        notice("Invalid username!")
        return

    # if the user is trying to make the bot kill itself, kill them
    if target.lower() == conn.nick.lower() or target.lower() == "itself":
        target = nick

    variables = {
        "user": target
    }

    with open("plugins/data/kills.json") as f:
        generator = get_generator(f.read(), variables)

    # act out the message
    me(generator.generate_string())
    return


@hook.command
def slap(inp, me=None, nick=None, conn=None, notice=None):
    """slap <user> -- Makes the bot slap <user>."""
    target = inp.strip()

    if " " in target:
        notice("Invalid username!")
        return

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() == "itself":
        target = nick

    variables = {
        "user": target
    }

    with open("plugins/data/slaps.json") as f:
        generator = get_generator(f.read(), variables)

    # act out the message
    me(generator.generate_string())
    return


@hook.command
def slogan(inp):
    """slogan <word> -- Makes a slogan for <word>."""
    out = random.choice(slogans)
    if inp.lower() and out.startswith("<text>"):
        inp = text.capitalize_first(inp)

    return out.replace('<text>', inp)


@hook.command(autohelp=False)
def fortune(inp):
    "fortune -- Fortune cookies on demand."
    return random.choice(fortunes)


@hook.command(autohelp=False)
def topkek(inp,me=None):
    "fortune -- Fortune cookies on demand."
    me(random.choice(keks))
    return

@hook.command(autohelp=False)
def loli(inp,me=None):
    "loli -- Returns a loli."
    with open("plugins/data/lolis.txt",) as f:
        lolis = [line.strip() for line in f.readlines() if not line.startswith("//")]

    print lolis[10]

    try: me("\x02\x034NSFW\x034\x02 {}".format(random.choice(lolis)))
    except: return "No lolis saved."
    return

@hook.command(autohelp=False)
def moistcake(inp,me=None):
    "moistcake -- Moists on demand."
    me(random.choice(moists))
    return

benders = ["Bite my shiny, metal ass!", "Bite my glorious, golden ass!", "Bite my shiny, colossal ass!", "Bite my splintery, wooden ass!", "Lick my frozen, metal ass!", "Like most of life's problems, this one can be solved with bending.", "Cheese it!", "Well, I'm boned.", "Hey, sexy mama...wanna kill all humans?", "Oh! Your! God!", "He's pending for a bending!", "This is the worst kind of discrimination - the kind against me!", "In case of emergency, my ass can be used as a flotation device.", "In order to get busy at maximum efficiency, I need a girl with a big, 400-ton booty.", "I'm sick of shaking my booty for these fat jerks!", "Bite my red-hot glowing ass!", "All I know is, this gold says it was the best mission ever.", "Hey, guess what you're all accessories to.", "Well, I don't have anything else planned for today. Let's get drunk!", "Oh, no room for Bender, huh? Fine! I'll go build my own lunar lander! With blackjack and hookers! In fact, forget the lunar lander and the blackjack! Ah, screw the whole thing.", "I found it in the street! Like all the food I cook.", "I can't stand idly by while poor people get free food!", "Congratulations Fry, you've snagged the perfect girlfriend. Amy's rich, she's probably got other characteristics...", "You may need to metaphorically make a deal with the devil. By 'devil' I mean robot devil and by 'metaphorically' I mean get your coat.", "Boy, who knew a cooler could also make a handy wang coffin?", "Call me old fashioned but I like a dump to be as memorable as it is devastating.", "My life, and by extension everyone else's is meaningless.", "Do I preach to you while you're lying stoned in the gutter? No.", "Everybody's a jerk. You, me, this jerk.", "I hate the people that love me and they hate me.", "I've personalized each of your meals. Amy, you're cute, so I baked you a pony!", "Ahh, computer dating. It's like pimping, but you rarely have to use the phrase, 'upside your head'.", "Court’s kinda fun when it’s not my ass on the line!", "Maybe you can interface with my ass! By biting it!", "Well, I'll go build my own theme park! With blackjack and hookers! In fact, forget the park!", "  Compare your lives to mine and then kill yourself!", "I would give up my 8 other senses, even smision, for a sense of taste!", "Stupid anti-pimping laws!", "Blackmail’s such an ugly word. I prefer extortion. The x makes it sound cool.", "Great is ok, but amazing would be great!", "The pie is ready. You guys like swarms of things, right?", "Fry cracked corn, and I don't care; Leela cracked corn, I still don't care; Bender cracked corn, and he is great! Take that you stupid corn!", "Stay away from our women. You got metal fever, baby, metal fever!", "If it ain't black and white, peck, scratch and bite.", "Life is hilariously cruel.", "Pardon me, brother. Care to donate to the anti-mugging you fund?", "I love this planet. I've got wealth, fame, and access to the depths of sleaze that those things bring.", "C'mon, it's just like making love. Y'know, left, down, rotate sixty-two degrees, engage rotors...", "Oh my God, I'm so excited I wish I could wet my pants.", "Argh. The laws of science be a harsh mistress.", "In the event of an emergency, my ass can be used as a floatation device.", "Hey, I got a busted ass here! I don't see anyone kissing it.", "I'm a fraud - a poor, lazy, sexy fraud.", "This'll show those filthy bastards who's loveable!"]

@hook.command(autohelp=False)
def bender(inp,me=None):
    "bender -- Bender quotes."
    me(random.choice(benders))
    return




