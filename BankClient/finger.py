import os
import json
import base64
import time
import sys

name = sys.argv[1]
def getfinger(i):
	a=os.popen("java -jar finger.jar").readlines()
	for x in a:
		try:
			x=x.replace("\n","")
			x=json.loads(x)
			bmp=x["data"]
			bmp=base64.b64decode(bmp)
			f=open("{}.bmp".format(i), "wb")
			f.write(bmp)
			f.close()
			

		except:
			pass

getfinger(name)


