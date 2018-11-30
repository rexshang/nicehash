import requests
from http import HTTPStatus
from enum import Enum
import sendgrid
import os
from sendgrid.helpers.mail import *
import schedule
import time
import argparse


url = 'https://api.nicehash.com/api?'
params = {'key': '98cbf48d-513b-c9c6-1d6f-9aeb3d95afda', 'id': '1343547'}
headers = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "gzip,  My Python requests library example client or username"
}

params['addr'] = '3AyBBeUKQVq4At1VAxjYAYv6BfPi8fNiSA'


algo = {
    0: 'Scrypt',
    1: 'SHA256',
    2: 'ScryptNf',
    3: 'X11',
    4: 'X13',
    5: 'Keccak',
    6: 'X15',
    7: 'Nist5',
    8: 'NeoScrypt',
    9: 'Lyra2RE',
    10: 'WhirlpoolX',
    11: 'Qubit',
    12: 'Quark',
    13: 'Axiom',
    14: 'Lyra2REv2',
    15: 'ScryptJaneNf16',
    16: 'Blake256r8',
    17: 'Blake256r14',
    18: 'Blake256r8vnl',
    19: 'Hodl',
    20: 'DaggerHashimoto',
    21: 'Decred',
    22: 'CryptoNight',
    23: 'Lbry',
    24: 'Equihash',
    25: 'Pascal',
    26: 'X11Gost',
    27: 'Sia',
    28: 'Blake2s',
    29: 'Skunk',
    30: 'CryptoNightV7',
    31: 'CryptoNightHeavy',
    32: 'Lyra2Z',
    33: 'X16R',
    34: 'CyrptoNightV8',
    35: 'SHA256AsicBoost',
    36: 'MAX',
    37: 'MAX',
    38: 'MAX',
    39: 'MAX',
    40: 'MAX',
    41: 'MAX',
    42: 'MAX',
    43: 'MAX'
}

loc = {
    0: 'EU',
    1: 'US',
    2: 'HK',
    3: 'JP',
    4: 'NA',
    5: 'NA',
    6: 'NA',
    7: 'NA',
    8: 'NA',
    9: 'NA'
}


class minerStatus:
    Name = 0
    Speed = 1
    Time = 2
    Xnsub = 3
    Diff = 4
    Location = 5
    Algo = 6


def getBalance():
    params['method'] = 'balance'

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        json_response = response.json()

        balances = json_response['result']
        for k, v in balances.items():
            v = float(v)
            print("{:20s} {:20.8f} BTC".format(k, v))

            if k == "balance_confirmed":
                return v
    else:
        print(response)


def getStatus():
    params['method'] = 'stats.provider.workers'

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == HTTPStatus.OK:
        json_response = response.json()

        miners = json_response['result']['workers']

        for miner in sorted(miners, key=lambda k: k[0], reverse=False):
            if miner[minerStatus.Algo] in algo:
                algorithm = algo[miner[minerStatus.Algo]]
            else:
                algorithm = ""

            if miner[minerStatus.Location] in loc:
                location = loc[miner[minerStatus.Location]]
            else:
                location = ""

            print("{:20s} algo: {:15s} {:10d} min, {:2s}".format(
                miner[minerStatus.Name], algorithm, miner[minerStatus.Time], location))
        # print(json_response['result'])
    else:
        print(response)

# params['method'] = 'stats.provider'

# response = requests.get(url, params=params, headers=headers)
# if response.status_code == HTTPStatus.OK:
#     json_response = response.json()
#     print(json_response['result']['stats'])

def sendMail(b):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("rshang@gmail.com")
    to_email = Email("rshang@gmail.com")
    subject = "NiceHash update"
    content = Content("text/plain", "You need to pay attention to your NiceHash account.  You now have {:9.8f}BTC.".format(b))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def job():
    b = getBalance()
    print("balance {:9.8f} ".format(b))

    if b > 0.001:
        print("great")
        sendMail(b)


def main(args):
    if args.server:
        schedule.every().day.at("07:30").do(job)

        while 1:
            schedule.run_pending()
            time.sleep(1)
    elif args.balance:
        getBalance()
    elif args.miner:
        getStatus()
    else:
        getStatus()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--miner', action='store_true',
                        help='get miner info')
    parser.add_argument('-b', '--balance', action='store_true',
                        help='get balance info')
    parser.add_argument(
        '-s', '--server', action='store_true', help='server mode')
    args = parser.parse_args()
    main(args)
