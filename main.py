import json
import copy
import random
import smtplib, ssl

def smtp_config(json_data):
    return json_data['sender-email'],json_data['sender-password'],json_data['smtp-server'],json_data['smtp-port']

def get_field(json_data, guestname, field): 
    for guest in json_data['guest']:
        if guest['name'] == guestname:
            return guest[field]  

def load_json_file(jsonfile):    
    f = open (jsonfile, "r") 
    data = json.loads(f.read()) 
    f.close() 
    return data

def match_guest(json_data, names):
        my_list = names
        choose = copy.copy(my_list)
        result = []
        for i in my_list:
            names = copy.copy(my_list) 
            exception = get_field(json_data, i, "exception")
            if exception:
                for e in exception:
                    names.pop(names.index(e))
            names.pop(names.index(i))
            chosen = random.choice(list(set(choose)&set(names)))
            result.append((i,chosen))
            choose.pop(choose.index(chosen))
        return result    

jsonfile="data.json"
data = load_json_file(jsonfile)

guest_list=[]
for guest in data['guest']: 
    guest_list.append(guest['name'])
pairs=(match_guest(data, guest_list))

sender_email,password,smtp_server,smtp_port = smtp_config(data)

message = """Subject: SEN - Secret Santa

{giver}, tu dois offrir {gift} a {receiver} pour {price} environ. Bon courage !"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(sender_email, password)
    for giver, receiver in pairs:
        email = get_field(data,giver,"email")
        gift = get_field(data,receiver,"wishgift")
        server.sendmail(
            sender_email,
            email,
            message.format(giver=giver,receiver=receiver,gift=gift,price=data['average-price']).encode('utf-8'),
        )    
