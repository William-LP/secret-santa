# Secret Santa

Allows you to throw a Secret Santa party without having someone knowing everyone's secret.

Just fill the `data.json` file an run `python main.py`. Nothing to install, code is ready to go.

## How to fill the json file

The first json part allow you to define what mailbox you gonna use to send the mail to all your guest as long as the smtp configuration.
Here a working example using gmail.
```json
"sender-email":"your-email@gmail.com",
"sender-password":"y0ur_$3cret-P@ssW0rD",
"smtp-server":"smtp.gmail.com",
"smtp-port":"465"
```        

The code will need to connect to your gmail account to please make sure to enable `less secure apps` connection :
https://myaccount.google.com/lesssecureapps

You can then set the price that'll be prompted in the mail as a spending recommendation, here 10€
```json
"average-price":"10\u20ac"
```
You can find more unicode currency symbole [here](https://www.rapidtables.com/code/text/unicode-characters.html).
| Symbol        | Unicode       |
| ------------- |:-------------:|
| €             | 	\u20AC      |
| $             |   \u0024      |
| £             |   \u00A3      |


Finally, you can setup guest details and interaction :
```json
"guest" :[
                {
                    "name":"Alice",
                    "email":"alice@gmail.com",
                    "wishgift":"a car",
                    "exception": ["Bob"]
                },
                {
                    "name":"Bob",
                    "email":"bob@gmail.com",
                    "wishgift":"a house",
                    "exception": []
                },
                {
                    "name":"Charlie",
                    "email":"charlie@gmail.com",
                    "wishgift":"a world trip",
                    "exception": []
                }
]
```        
`name` field will be used to manage exception and within email body (see below).

`email` as you might guess is the guest's email

`wishgift` allow guest to give a thematic for the wished present

`exception` field will prevent guest being assigned specific other guest.
This code will never assign `Bob` to `Alice` for example.

## How to update sent email

Just modify the hardcoded lines ```46``` to ```48``` in [main.py](main.py)

Email example :
```
Alice, tu dois offrir une voiture a Charlie pour 10€ environ. Bon courage !
```