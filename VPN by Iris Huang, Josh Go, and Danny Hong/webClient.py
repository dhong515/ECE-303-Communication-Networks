import requests
import sys
import json
from datetime import datetime


def main():
    # url = input("Please enter the url: \n")
    userName = input("Please enter the user name:\n")
    pload = {'username': userName}
    # Print messages
    url_final = "http://18.191.29.231:80" + "/?user=" + userName #you can put ur ec2 ip address here
    r = requests.get(url_final).json()
    print("You got the following messages:\n")
    for i in r['response']['messages']:
        output = i['sender'] + " : " + i['value'] + '\n'
        print(output)
    time = datetime.now().strftime('%m/%d/%y %H:%M:%S')

    while True:
        comm = input("Please enter your command (refresh, send or quit)\n")
        command = comm.split(':', 2)
        helper = datetime.strptime(time, '%m/%d/%y %H:%M:%S')
        if command[0] == 'refresh':  # display new messages only
            r = requests.get(url_final).json()
            for i in r['response']['messages']:
                tempTime = datetime.strptime(i["time"], '%m/%d/%y %H:%M:%S')
                if tempTime > helper:
                    output = i['sender'] + " : " + i['value'] + '\n'
                    print(output)
                time = datetime.now().strftime('%m/%d/%y %H:%M:%S')
        elif command[0] == 'quit':  # exit your program
            sys.exit()
        elif command[0] == 'send':  # Send option
            receiver = command[1]
            value = command[2]
            time = datetime.now().strftime('%m/%d/%y %H:%M:%S')
            request_body = {
                "sender": userName,
                "time": time,
                "receiver": receiver,
                "value": value
            }
            requests.post(url_final, json=request_body)
            print("Message Sent")
        else:
            print("Invalid command\n")


if __name__ == '__main__':
    main()





