import requests
import sys

def add(account_no,amount):
    p = requests.get("http://127.0.0.1:8080/add_balance?amount={}&account_no={}".format(amount,account_no)).text
    if p == 'abc':
        return "Added Successfully"
    else:
        return "false"

account_no,amount = sys.argv[1],sys.argv[2]

print(add(account_no,amount))
