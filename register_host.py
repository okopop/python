#!/bin/python
"""register host"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import argparse
import os
import sys

if os.geteuid() == 0:
    print("Hey don't run script as root...")
    sys.exit()

#if socket.gethostname() != "correct.server.example.com":
#  print "Run script on correct server..."
#  exit()

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fqdn", required=True, help="Host FQDN")
parser.add_argument("-o", "--os", required=True, help="SLES or RHEL")
parser.add_argument("-v", "--vlan", required=True, help="VLAN-ID")
parser.add_argument("-s", "--system", required=True, help="System name")
args = vars(parser.parse_args())

# set some
LOGIN_USER = "fake_user"
LOGIN_PASSWORD_PATH = "/tmp/passfile"
server = args["fqdn"]
os_input = args["os"]
vlan = args["vlan"]
system = args["system"]
inv_id = server[2:8]

def os_check():
    if os_input == "sles":
        global OS_VALUE = "SUSE Linux Enterprise Server"
    elif os_input == "rhel":
        global OS_VALUE = "Red Hat Enterprise Linux"
    else:
        print("Abort script: Operating System not supported")
        sys.exit()

def print_variables():
    print("--------------------")
    print("Inv-id: {}".format(inv_id))
    print("FQDN: {}".format(server))
    print("OS: {}".format(OS_VALUE))
    print("VLAN: {}".format(vlan))
    print("System: {}".format(system))
    print("--------------------")

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            print("Abort script...")
            sys.exit()

def login_cred():
    if os.path.isfile(LOGIN_PASSWORD_PATH):
        login_pw = open(LOGIN_PASSWORD_PATH, "r")
        return login_pw.read()
    print(LOGIN_PASSWORD_PATH + " is missing..")
    sys.exit()

def payload(login_password):
    content_input = {
        "inv": inv_id,
        "os": os_input,
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
    # make requests here
    print(payload_output)

def main():
    os_check()
    print_variables()
    yes_or_no("Register host. Is above correct?")
    create_host(payload(login_cred()))

if __name__ == "__main__":
    main()
