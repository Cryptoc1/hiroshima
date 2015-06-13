#!/usr/bin/env python

##
# 
# hiroshima.py
# This is the main front-end that pulls all network attacks into one interface. Enjoy.
# Samuel Steele (cryptoc1)
#
##

import networks
import os, sys

DEVMODE = True

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
                    \n\t\t\t+ Ask Question"

def prologue():
    print "For help, enter 'help', or '?'. To begin, enter 'begin'."
    cmd = raw_input("> ").lower()
    if cmd == "help" or cmd == "?":
        print _usage
        prologue()
    elif cmd == "begin":
        main()
    else:
        prologue()

def main():
    print "Enter a social network to attack"
    network = raw_input("> ").lower()
    if network == "instagram":
        instagram_attack()
    elif network == "twitter":
        twitter_attack()
    elif network == "askfm":
        askfm_attack()
    else:
        main()

def instagram_attack():
    insta = networks.Instagram()
    print "In order for any actions to be preformed, you need to authorize hiroshima to use your Instagram account. Proceed? (Y/n)"
    prompt = raw_input("> ").lower()
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
                print "Unrecognized input."
                prologue()
        else:
            print "There was an error logining in."
            prologue()

    elif prompt == "n":
        print "Okay..."
        prologue()
    else:
        print "Unrecognized character(s)."
        prologue()

def twitter_attack():
    pass

def askfm_attack():
    print "Enter the username"
    username = raw_input("> ")
    ask = networks.AskFM(username)
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
