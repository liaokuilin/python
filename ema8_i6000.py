import requests,json
import time,datetime
import hashlib
from pyDes import des, CBC, PAD_PKCS5
import binascii
import base64
from zeep import Client
#sgcc I6000 demo

url='http://172.18.9.153:9071/businessSystem/services/ims?wsdl'

client=Client(wsdl=url)
# mobiles=['18621803633']
# msg=['aaaaaa']
#ss="""<?xml version="1.0" encoding="UTF-8"?><message><account>dh8577</account><password>3b5beffe6308ec422a7018be880d9897</password><msgid></msgid><phones>%s</phones><content>%s</content><sign></sign><subcode></subcode><sendtime></sendtime></message>"""%(mobiles,msg)
ss="""<?xml version="1.0" encoding="gb2312"?><info><CorporationCode>13</CorporationCode><Time></Time><api name="BusinessUserRegNum"></api><api name="BusinessSystemOnlineNum"></api><api name="BusinessDayLoginNum"></api><api name="BusinessVisitCount"></api><api name="BusinessSystemSessionNum"></api><api name="BusinessSystemResponseTime"></api><api name="BusinessSystemRunningTime"></api><api name="BusinessDataTableSpace"></api><api name="BusinessSystemDBTime"></api></info>
"""
#print(ss)
#print(dir(client.service))
print(client.service.getKPIValue(ss))
