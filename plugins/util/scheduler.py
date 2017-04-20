from util import hook
import sched, time

def check_for_timers(inp):
    split = inp.split(' ')
    timer = 0
    lastparam = split[-1].lower()
    if   'sec'   in lastparam: timer = int(split[-2])
    if   'min'   in lastparam: timer = int(split[-2]) * 60
    elif 'hour'  in lastparam: timer = int(split[-2]) * 60 * 60
    elif 'day'   in lastparam: timer = int(split[-2]) * 60 * 60 * 24
    elif 'week'  in lastparam: timer = int(split[-2]) * 60 * 60 * 24 * 7
    elif 'month' in lastparam: timer = int(split[-2]) * 60 * 60 * 24 * 30
    elif 'year'  in lastparam: timer = int(split[-2]) * 60 * 60 * 24 * 365
    elif  lastparam.isdigit(): timer = int(lastparam) * 60
    return timer

def execute(command, conn):
    conn.send(command)

def schedule(timer, priority, command, conn):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(timer, priority, execute, (command, conn))
    s.run()


#from datetime import datetime, timedelta

# def db_init(db):
#     db.execute("create table if not exists scheduler(id primary key, time, action)")
#     db.commit()


#split = inp.split(' ')
#timer = int(inp[0])
#action = " ".join(inp[1:])
#command = 'MODE {} -b {}'.format('#uguubot',action)


#run_at = now + timedelta(hours=3)
#delay = (run_at - now).total_seconds()

# now = datetime.now()
# print now
# change =  timedelta(weeks=0, days=0, hours=0, minutes=1, seconds=0)
# print change
# future = now + change
# print future

# now = datetime.now()
# run_at = now + timedelta(minutes=1)
# delay = (run_at - now).total_seconds()
# threading.Timer(delay, action('test')).start()
#command = 'PRIVMSG {} :{}'.format('#uguubot',inp)