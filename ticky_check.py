#!/usr/bin/env python3
import re
import csv

per_user={}
errors={}
f = open("syslog.log", "r")
lines=f.readlines()

for line in lines:
  user=re.search(r"\(([\w||.]*)\)", line)
  e=re.search(r"ticky: ERROR ([\w ]*) ", line)
  per_user.setdefault(user.group(),{'error':0,'info':0})
  if(e is not None):
    errors.setdefault(e.group(), 0)
    errors[e.group()]+=1
    per_user[user.group()]['error']+=1
  i=re.search(r"ticky: INFO ([\w ]*) ", line)
  if(e is not None):
    per_user[user.group()]['info']+=1

errors_file = "error_message.csv"
try:
    with open(errors_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['Error','Count'])
        writer.writeheader()
        for value,key  in errors.items():
            writer.writerow({'Error':value,'Count':key})
except IOError:
    print("I/O error")

users_file = "user_statistics.csv"
try:
    with open(users_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['Username','Info','Error'])
        writer.writeheader()
        for value,key  in per_user.items():
            writer.writerow({'Username':value,'Info':key['info'],'Error':key['error']})
except IOError:
    print("I/O error")

