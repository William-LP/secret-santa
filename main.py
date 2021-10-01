import json
import copy
import random
import smtplib, ssl
from art import tprint

def smtp_config(json_data):
    return json_data['sender-email'],json_data['sender-password'],json_data['smtp-server'],json_data['smtp-port']

def get_field(json_data, guestname, field): 
    for guest in json_data['guest']:
        if guest['name'] == guestname:
            return guest[field]  

def load_json_file(jsonfile):    
    f = open (jsonfile, "r", encoding='utf-8') 
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

tprint("SECRET SANTA")
print()
print('+--------------------------------+')
print('+          CONFIGURATION         +')
print('+--------------------------------+')
try :
    jsonfile="data.json"
    data = load_json_file(jsonfile)
    print("- Chargement des paramètres : OK")
except Exception as e: 
    print(e)

try :
    guest_list=[]
    for guest in data['guest']: 
        guest_list.append(guest['name'])
    pairs=(match_guest(data, guest_list))
    print("- Création des couples aléatoire : OK")
except Exception as e: 
    print(e)    

try :
    sender_email,password,smtp_server,smtp_port = smtp_config(data)
    print("- Configuration SMTP : OK")
except Exception as e: 
    print(e)

try :
    context = ssl.create_default_context()    
    print("- Création d'un context SSL : OK")
except Exception as e: 
    print(e)



message = """Subject: SEN - Secret Santa

Oh oh ooohh...

{giver}, tu as été tiré au sort pour être le Père-Noël de {receiver}, et voilà sa commande :

{gift} !

Ta responsabilité est grande, je compte sur toi pour combler son souhait ;D

Je te donne rendez-vous le samedi 9 au soir pour offrir ta trouvaille et découvrir ce que t'as reservé TON Père Noël ;)

Bon courage !

Big Santa

Petit rappel des règles :
- Budget d'environ {price} pour le cadeau
- Ne revèle pas qui tu as tiré, cette personne devra le deviner le jour J
- On emballe le cadeau si c'est possible (papier cadeau, journal... peu importe)
"""


print()
print('+--------------------------------+')
print('+          ENVOIE DES MAILS      +')
print('+--------------------------------+')

with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
    server.login(sender_email, password)
    for giver, receiver in pairs:
        print("--> Envoie d'un mail à " + giver)
        email = get_field(data,giver,"email")
        gift = get_field(data,receiver,"wishgift")
        server.sendmail(
            sender_email,
            email,
            message.format(giver=giver,receiver=receiver,gift=gift.upper(),price=data['average-price']).encode('utf-8'),
        )   
print()
print("Fin d'envoie des mails ! Have fun ;)")
