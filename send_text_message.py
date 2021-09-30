from telethon.sync import TelegramClient
import pickle
import random
import pyfiglet
import os
from colorama import init, Fore
from telethon.tl.types import InputPeerUser, InputPeerChannel


init()

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN

info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '+' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
colors = [lg, w, r, cy]


def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Genisys')
    print(random.choice(colors) + logo + rs)


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


clr()
banner()
print(f'  {r}Version: {w}2.5 {r}| Author: {w}Cryptonian{rs}\n')

f = open('vars.txt', 'rb')
accs = []
while True:
    try:
        accs.append(pickle.load(f))
    except EOFError:
        f.close()
        break
print(f'{INPUT}{cy} Choose an account to scrape members\n')
i = 0
for acc in accs:
    print(f'{lg}({w}{i}{lg}) {acc[2]}')
    i += 1
ind = int(input(f'\n{INPUT}{cy} Enter choice: '))
api_id = accs[ind][0]
api_hash = accs[ind][1]
phone = accs[ind][2]

client = TelegramClient(phone, api_id, api_hash).start()

try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    receiver = InputPeerUser(1973139620, 5651917822031574305)

    # sending message using telegram client
    # client.send_message(receiver, "Hello from telebot", parse_mode='html')
    # client.send_file(receiver, '/Users/gangadharashetty/Desktop/test.png', parse_mode='html')
except Exception as e:

    # there may be many error coming in while like peer
    # error, wrong access_hash, flood_error, etc
    print(e);

# disconnecting the telegram session
client.disconnect()

