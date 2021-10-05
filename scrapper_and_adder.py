from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, UserStatusRecently
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import csv
import traceback
import time
from telethon.sync import TelegramClient
import pickle
import random
import pyfiglet
import os
from colorama import init, Fore
from telethon.tl.types import InputPeerUser, InputPeerChannel


time_to_wait = 60
sleeper_time = 15*60
wait_after = 15

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

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('Choose a group to add members:')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

members = client.get_participants(target_group_entity, aggressive=True)

input_file = 'members/members.csv'
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

print(users)
print(members)

sleeper = 0

for user in users:
    if sleeper > wait_after:
        sleeper = 0
        time.sleep(sleeper_time)

    sleeper += 1

    flag = False
    for member in members:
        username = ''
        accept = True
        if member.username:
            username = member.username
        else:
            username = ''
        if (member.id == user['id']) or (username == user['username']) or (member.access_hash == user['access_hash']):
            print(f'User id: {user["id"]}   name: {username} already present in group')
            flag = True

    if flag:
        continue
    try:
        print("Adding {}".format(user['id']))
        user_to_add = InputPeerUser(user['id'], user['access_hash'])

        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting 60 Seconds...")
        time.sleep(time_to_wait)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
