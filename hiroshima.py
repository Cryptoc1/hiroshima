#!/usr/bin/env python

##
#
# hiroshima.py
# This is the main front-end that pulls all network attacks into one interface. Enjoy.
# Samuel Steele (cryptoc1)
#
##

import networks, sys

_usage = "hiroshima help: \
            \n\tAttackable Networks: \
                \n\t\t+ Twitter \
                \n\t\t+ Instagram \
                \n\t\t+ AskFM \
            \n\tAttack Types: \
                \n\t\tTwitter: \
                    \n\t\t\t+ Favorite \
                    \n\t\t\t+ Reply \
                    \n\t\t\t+ Un-favorite \
                \n\t\tInstagram: \
                    \n\t\t\t+ Like \
                    \n\t\t\t+ Un-like \
                \n\t\tAskFM: \
                    \n\t\t\t+ Ask Question \
            \n\tCommands: \
                \n\t\tbegin :: enters the main-loop to attack \
                \n\t\texit :: exits the program \
                \n\t\thelp|? :: prints this help dialog \
                \n\t\tdelay <s> :: print the current delay, or set delay 's', in seconds, as the global delay"

_delay = 5

def prologue():
    print "For help, enter 'help', or '?'. To begin, enter 'begin', or 'exit' to exit."
    cmd = raw_input("> ").lower()
    if cmd == "help" or cmd == "?":
        print _usage
        prologue()
    elif cmd == "begin":
        main()
    elif cmd == "exit":
        sys.exit()
    elif cmd.split(' ')[0] == "delay":
        global _delay
        opts = cmd.split(' ')
        if len(opts) < 2:
            print "Current delay: " + str(_delay)
        else:
            _delay = opts[1]
            print "delay set to " + str(_delay)
        prologue()
    else:
        prologue()

def main():
    '''for i in range(0, len(sys.argv)):
        if sys.argv[i] == "--delay" or sys.argv[i] == "-d":
            delay = int(sys.argv[i+1])'''
    delay = _delay
    print "Enter a social network to attack"
    network = raw_input("> ").lower()
    if network == "instagram":
        instagram_attack(delay)
    elif network == "twitter":
        twitter_attack(delay)
    elif network == "askfm":
        askfm_attack(delay)
    else:
        main()

def instagram_attack(delay):
    insta = networks.Instagram(delay)
    if not insta.AUTH_IN_PREFS:
        print "In order for any actions to be preformed, you need to authorize hiroshima to use your Instagram account. Proceed? (Y/n)"
        prompt = raw_input("> ").lower()
    else:
        prompt = "y"
    if prompt == "y":
        if insta.login():
            print "Enter the username of your victim"
            username = raw_input("> ")
            print "Searching..."
            search = insta.search_users(username)
            print "I found this: "
            print insta.format_user_info(search)
            print "Is this the intended victim? (Y/n)"
            prompt = raw_input("> ").lower()
            if prompt == "y":
                if insta.set_victim(search):
                    print "Enter the attack type (" + insta.get_attack_types() + ")"
                    attack_type = raw_input("> ").lower()
                    if attack_type == "like":
                        print "Enter the number of photos to be liked (enter 'all' to like all)"
                        insta.like_attack(raw_input("> "))
                        print "Like attack complete."
                        prologue()
                    elif attack_type == "unlike":
                        print "Enter the number of photos to be liked (enter 'all' to unlike all)"
                        insta.unlike_attack(raw_input("> "))
                        print "Unlike attack complete."
                        prologue()
                    else:
                        print "Attack type not entered, starting attack over..."
                        instagram_attack()
                else:
                    print "There was an error setting the victim."
                    prologue()
            elif prompt == "n":
                print "Please check to make sure you have the correct username. (The attack will now start over)."
                instagram_attack()
            else:
                print "Unrecognized characters(s)"
                prologue()
        else:
            print "There was an error logging in."
            prologue()
    elif prompt == "n":
        print "Okay..."
        prologue()
    else:
        print "Unrecognized character(s)."
        prologue()

def twitter_attack(delay):
    twit = networks.Twitter(delay)
    if not twit.AUTH_IN_PREFS:
        print "In order for any actions to be preformed, you need to authorize hiroshima to use your Twitter account. Proceed? (Y/n)"
        prompt = raw_input("> ").lower()
    else:
        prompt = "y"
    if prompt == "y":
        if twit.login():
            print "Enter the username of your victim."
            username = raw_input("> ")
            print "Searching..."
            search = twit.search_users(username)
            print "I found this: "
            print twit.format_user_info(search)
            print "Is this the intended victim? (Y/n)"
            prompt = raw_input("> ").lower()
            if prompt == "y":
                if twit.set_victim(search):
                    print "Enter attack type (" + twit.get_attack_types() + ")"
                    attack_type = raw_input("> ").lower()
                    if attack_type == "favorite" or attack_type == "fav" or attack_type == "fave":
                        print "Enter the number of tweets to favorite."
                        count = int(raw_input("> "))
                        print "Include retweets by the victim? (Y/n)"
                        cmd = raw_input("> ").lower()
                        if cmd == "y":
                            print "Include mentions? (Y/n)"
                            cmd = raw_input("> ").lower()
                            if cmd == "y":
                                twit.fav_attack(count, True, True)
                            elif cmd == "n":
                                twit.fav_attack(count, True, False)
                            else:
                                print "Unrecognized character(s)"
                                prologue()
                        elif cmd == "n":
                            print "Include mentions? (Y/n)"
                            cmd = raw_input("> ").lower()
                            if cmd == "y":
                                twit.fav_attack(count, False, True)
                            elif cmd == "n":
                                twit.fav_attack(count, False, False)
                            else:
                                print "Unrecognized character(s)"
                                prologue()
                        else:
                            print "Unrecognized character(s)"
                            prologue()
                        print "Favorite attack complete."
                        prologue()
                    elif attack_type == "reply":
                        print "Enter tweet text (remember the 140 character limit)."
                        text = raw_input("> ")
                        if len(text) > 140:
                            print "Text length excedes (140) character limit, starting over."
                            twitter_attack()
                        else:
                            print "Enter the number of tweets to reply to."
                            twit.reply_attack(text, raw_input("> "))
                            print "Reply attack complete."
                            prologue()
                    elif attack_type == "retweet" or attack_type == "rt":
                        print "Enter the number of tweets to be retweeted."
                        count = int(raw_input("> "))
                        print "Include retweets by the victim? (Y/n)"
                        cmd = raw_input("> ").lower()
                        if cmd == "y":
                            print "Include mentions? (Y/n)"
                            cmd = raw_input("> ").lower()
                            if cmd == "y":
                                twit.rewtweet_attack(count, True, True)
                            elif cmd == "n":
                                twit.rewtweet_attack(count, True, False)
                            else:
                                print "Unrecognized character(s)"
                                prologue()
                        elif cmd == "n":
                            print "Include mentions? (Y/n)"
                            cmd = raw_input("> ").lower()
                            if cmd == "y":
                                twit.rewtweet_attack(count, False, True)
                            elif cmd == "n":
                                twit.rewtweet_attack(count, False, False)
                            else:
                                print "Unrecognized character(s)"
                                prologue()
                        else:
                            print "Unrecognized character(s)"
                            prologue()
                        print "Retweet attack complete."
                        prologue()
                    else:
                        print "Attack type not entered, starting attack over..."
                        twitter_attack()
                else:
                    print "There was an error setting the victim."
                    prologue()
            elif prompt == "n":
                print "Please check to make sure you have the correct username. (The attack will now start over)."
                twitter_attack()
            else:
                print "Unrecognized character(s)"
                prologue()
        else:
            print "There was an error logging in."
            prologue()
    elif prompt == "n":
        print "Okay..."
        prologue()
    else:
        print "Unrecognized character(s)"
        prologue()

def askfm_attack(delay):
    print "Enter the username"
    username = raw_input("> ")
    ask = networks.AskFM(username, delay)
    print "Enter the question to be asked"
    query = raw_input("> ")
    print "Enter the number of times the question should be asked"
    count = raw_input("> ")
    print "About to ask @" + username + " \"" + query + "\", " + count + " times. Proceed? (Y/n)"
    prompt = raw_input("> ").lower()
    if prompt == "y":
        ask.ask_question(query, int(count))
    elif prompt == "n":
        print "Aborting attack."
    else:
        print "Unrecognized character(s), restarting attack."
        askfm_attack()
    print "ask.fm attack complete."
    prologue()

if __name__ == "__main__":
    print "Hello, and welcome to Hiroshima: A Social Spammer."
    prologue()
