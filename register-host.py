#!/bin/python
import argparse
import os
import socket

if os.geteuid() == 0:
  print("Hey don't run script as root...")
  exit()

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
login_user = "fake_user"
login_password_path = "/tmp/passfile"
server = args["fqdn"]
os_input = args["os"]
vlan =  args["vlan"]
system = args["system"]
inv_id = server[2:8]

def print_variables():
  print("--------------------")
  print("Inv-id: {}".format(inv_id))
  print("FQDN: {}".format(server))
  print("OS: {}".format(os_value))
  print("VLAN: {}".format(vlan))
  print("System: {}".format(system))
  print("--------------------")
 
def os_check():
  global os_value
  if os_input == "sles":
    os_value = "SUSE Linux Enterprise Server"
  elif os_input == "rhel":
    os_value = "Red Hat Enterprise Linux"
  else:
    print("Abort script: Operating System not supported")
    exit()
 
def yes_or_no(question):
  while "the answer is invalid":
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[:1] == 'y':
      return True
    if reply[:1] == 'n':
      print("Abort script...")
      exit()     

def login_cred():
  if os.path.isfile(login_password_path):
    login_pw = open(login_password_path,"r")
    return(login_pw.read())
  else:
    print(login_password_path + " is missing..")
    exit()

def payload(login_password):
  content_input = {
    "inv": inv_id,
    "os": os_input,
    "user": login_user,
    "pass": login_password.rstrip()
  }
  data="""\
<invid>{inv}</invid>
<operatingsystem>{os}</operatingsystem>
<user>{user}</user>
<pass>{pass}</pass>\
  """
  return(data.format(**content_input)) 

def create_host(payload_output):
  # make requests here
  print payload_output 

def main():
  os_check()
  print_variables()
  yes_or_no("Register host. Is above correct?")
  create_host(payload(login_cred()))

if __name__== "__main__":
  main()
