#!/bin/python
"""register host"""
import argparse
import os
import sys

if os.geteuid() == 0:
    print("Hey don't run script as root...")
    sys.exit()

#if socket.gethostname() != "correct.server.example.com":
#  print "Run script on correct server..."
#  exit()

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-f", "--fqdn", required=True, help="Host FQDN")
PARSER.add_argument("-o", "--os", required=True, help="SLES or RHEL")
PARSER.add_argument("-v", "--vlan", required=True, help="VLAN-ID")
PARSER.add_argument("-s", "--system", required=True, help="System name")
ARGS = vars(PARSER.parse_args())

# set some
LOGIN_USER = "fake_user"
LOGIN_PASSWORD_PATH = "/tmp/passfile"
SERVER = ARGS["fqdn"]
OS_INPUT = ARGS["os"]
VLAN = ARGS["vlan"]
SYSTEM = ARGS["system"]
INV_ID = SERVER[2:8]

def os_check():
    """return os version"""
    if OS_INPUT == "sles":
        return "SUSE Linux Enterprise Server"
    if OS_INPUT == "rhel":
        return "Red Hat Enterprise Linux"
    print("Abort script: Operating System not supported")
    sys.exit()

def print_variables():
    """print information"""
    print("--------------------")
    print("Inv-id: {}".format(INV_ID))
    print("FQDN: {}".format(SERVER))
    print("OS: {}".format(os_check()))
    print("VLAN: {}".format(VLAN))
    print("System: {}".format(SYSTEM))
    print("--------------------")

def yes_or_no(question):
    """return true or exit"""
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            print("Abort script...")
            sys.exit()

def login_cred():
    """return password"""
    if os.path.isfile(LOGIN_PASSWORD_PATH):
        login_pw = open(LOGIN_PASSWORD_PATH, "r")
        return login_pw.read()
    print(LOGIN_PASSWORD_PATH + " is missing..")
    sys.exit()

def payload(login_password):
    """return payload"""
    content_input = {
        "inv": INV_ID,
        "os": OS_INPUT,
        "user": LOGIN_USER,
        "pass": login_password.rstrip()
    }
    data = """\
<invid>{inv}</invid>
<operatingsystem>{os}</operatingsystem>
<user>{user}</user>
<pass>{pass}</pass>\
    """
    return data.format(**content_input)

def create_host(payload_output):
    """create host"""
    # make requests here
    print(payload_output)

def main():
    """run program"""
    print_variables()
    yes_or_no("Register host. Is above correct?")
    create_host(payload(login_cred()))

if __name__ == "__main__":
    main()
