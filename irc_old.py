import re
import dcpu

def init(serv, conf, par):
    print "IRC is initializing..."
    global server
    global config
    global parent
    global dcpu
    server = serv
    config = conf
    parent = par
    dcpu = reload(dcpu)


def send(msg):
    print msg
    server.send(msg + "\r\n")

def privmsg(nick, chan, msg):

    lines = msg.split("\n")
    if len(lines) > 1:
        for line in lines:
            privmsg(nick, chan, line)
    elif msg != "":
        response = "PRIVMSG "

        if chan == config.nick:
            response += nick + " :" + msg
        else:
            response += chan + " :" + nick + ": " + msg

        send(response)

def onMsgToMe(nick, chan, msg):
    if re.match("reload.*", msg):
        privmsg(nick, chan, "Reloading in progress")
	parent.reload_now = True
    if re.match("hello.*", msg):
        privmsg(nick, chan, "Howdy!")
    if re.match("(how.*you|sup|what*up)", msg, re.IGNORECASE):
        privmsg(nick, chan, "I'm fine. How about you?")

execute_re = re.compile(">>(.+)")
assemble_re = re.compile(">>>(.+)")

def onPrivMsg(nick, chan, msg):
    parent.last_nick = nick
    parent.last_chan = chan
    print "Message from " + nick + " to " + chan + ": " + msg
    to_me_match = re.match("^" + config.nick + "[^ ]? (.+)", msg)
    assemble_match = assemble_re.match(msg)
    execute_match = execute_re.match(msg)

    if assemble_match:
        assembled = dcpu.assemble(assemble_match.group(1))
	if assembled[0] != "":
	    privmsg(nick, chan, ', '.join(assembled[0]))
	if assembled[1] != "":
            privmsg(nick, chan, assembled[1])
    elif execute_match:
        executed = dcpu.execute(execute_match.group(1))
        privmsg(nick, chan, executed)
    elif to_me_match or chan == config.nick:
        if to_me_match: msg = to_me_match.group(1)
        onMsgToMe(nick, chan, msg)

ping_re = re.compile("^PING :(.*)")
privmsg_re = re.compile("^:([^!@]+).+PRIVMSG ([^ ]+) :(.*)")

def onData(data):
    print(data)

    ping_match = ping_re.match(data)
    privmsg_match = privmsg_re.match(data)

    if ping_match:
        response = "PONG :" + ping_match.group(1)
        send(response)
    elif privmsg_match:
        onPrivMsg(privmsg_match.group(1), privmsg_match.group(2), privmsg_match.group(3))