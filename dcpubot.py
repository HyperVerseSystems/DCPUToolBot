#!/usr/bin/env python
import irc
import config
import dcpu

irc.connect(config.host, config.port, config.nick, config.password)
irc.join(config.chan)

def onAssemble(nick, user, host, chan, matches):
    print "Assembling"
    print matches.group()
    print matches.group(1)
    binary, errors = dcpu.assemble(matches.group(1))

    if binary:
        irc.privmsg(nick, chan, ', '.join(binary))
    if errors:
        irc.privmsg(nick, chan, errors)

irc.onPrivmsg(">>>(.+)", onAssemble)

def onDisassemble(nick, user, host, chan, matches):
    print "Disassembling"
    print matches.group()
    print matches.group(1)
    code = dcpu.disassemble(matches.group(1))

    if code:
        irc.privmsg(nick, chan, code)

irc.onPrivmsg("<<<(.+)", onDisassemble)

def onExecute(nick, user, host, chan, matches):
    executed, errors = dcpu.execute(matches.group(1))

    if executed:
        irc.privmsg(nick, chan, executed)
    if errors:
        irc.privmsg(nick, chan, errors)

irc.onPrivmsg(">>([^>].+)", onExecute)

def onHex(nick, user, host, chan, matches):
    converted = 0
    
    if matches.group(1) == "0b":
        converted = hex(int(matches.group(2), 2))
    else:
        converted = hex(int(matches.group(2)))

    irc.privmsg(nick, chan, converted)

irc.onPrivmsg(r"^hex\((0b)?(\d+)\)", onHex)

def onDec(nick, user, host, chan, matches):
    converted = 0
    
    if matches.group(1) == "0b":
        converted = str(int(matches.group(2), 2))
    elif matches.group(1) == "0x":
        converted = str(int(matches.group(2), 16))
    else:
        converted = str(int(matches.group(2)))

    irc.privmsg(nick, chan, converted)

irc.onPrivmsg(r"^dec\((0b|0x)?([0-9a-fA-F]+)\)", onDec)

def onBin(nick, user, host, chan, matches):
    converted = 0

    if matches.group(1) == "0x":
        converted = bin(int(matches.group(2), 16))
    else:
        converted = bin(int(matches.group(2), 16))

    irc.privmsg(nick, chan, converted)

irc.onPrivmsg(r"^bin\((0x)?([0-9a-fA-F]+)\)", onBin)

def onRudeness(nick, user, host, chan, matches):
    irc.privmsg(nick, chan, "Why don't you?")

irc.onMsgToMe(".*stfu.*", onRudeness)

def onHello(nick, user, host, chan, matches):
    irc.privmsg(nick, chan, "Howdy!")

irc.onMsgToMe(".*hello.*", onHello)

def onSup(nick, user, host, chan, matches):
    irc.privmsg(nick, chan, "I'm fine. How about you?")

irc.onMsgToMe(".*(how.*you|sup|what.*up).*", onSup)
