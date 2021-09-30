from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import sys
import pickle
import random
import pyfiglet
import os
import datetime
from colorama import init, Fore
from telethon.tl.types import UserStatusRecently

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



channels = {d.entity.username: d.entity
            for d in client.get_dialogs()
            if d.is_channel}
# for u in channels:
#     print(u)
# choose the one that I want list users from
channel = channels['frontrowsale']

# get all the users and print them
for u in client.get_participants(channel):
    print(u.id, u.first_name, u.last_name, u.username)