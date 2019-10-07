import requests
import sys
import os
def signup(aadhar_no,age,name,phone_no):

    r = requests.get("http://127.0.0.1:8080/add_account?adhar_no={}&name={}&age={}&phone_no={}".format(aadhar_no,name,age,phone_no)).text
    files = {"img":open("hola.bmp",'rb').read()}

    account_no = r

    r2 = requests.post("http://127.0.0.1:8080/link_state?adhar_no={}&account_no={}".format(str(aadhar_no),str(account_no)),files=files)


    return r+","+r2.text
aadhar_no,age,name,phone_no = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
a = signup(aadhar_no,age,name,phone_no)
b = a.split(',')
print("  The Account No is {}      |     The Passcode is {}".format(b[0],b[1]))
