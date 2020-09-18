import requests,json
import time,datetime
import hashlib
from pyDes import des, CBC, PAD_PKCS5
import binascii
import base64
from zeep import Client
"""北京国网企信通平台接口demo"""

class ema7_ws(object):
    url = 'http://172.18.9.153:18001/ctc-ema70/webServices/MasInterfaceForService?wsdl'
    service_id = '999999'
    miyao = '100C0769EF6DE126'
    def send_sms(self):
        client=Client(wsdl=self.url)
        # 毫秒级时间
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        TransationID = self.genenalSid()
        req_body = "<Body><ServiceNumber>666666</ServiceNumber><UserNumberList><RecPhone>18621803633</RecPhone></UserNumberList><SmsContent>豫章故郡，洪都新府。星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰。</SmsContent><Priority>1</Priority><SmsFmt>15</SmsFmt>\
                <AtTime></AtTime><ValidTime></ValidTime><ServiceCode>01</ServiceCode><ReportFlag>0</ReportFlag><Reserve></Reserve></Body>"
        en_body = self.encryption(req_body.strip())
        header = {
        'msgType':'SubmitSmsReq',
        'serviceID':self.service_id,
        'TransationID':TransationID,
        'TimeStamp':dt,
        'Version':'v1.0.1'
        }
        ss={
        "header":header,
        "body":en_body
        }
        r=client.service.submitSms(ss)
        #解密body        
        r.body=str(self.des_descrypt(base64.b64decode(r.body)),encoding='utf-8')
        return r


    #获取genenalSid
    def genenalSid(self):
        sid = str(int(time.time() * 1000))
        sid_len = len(sid) -16
        if sid_len > 0:
            sid = sid[sid_len:sid_len+16]
        elif sid_len < 0:
            for i in range(abs(sid_len)):
                sid = '0'+sid
        return sid


    #请求体加密
    def encryption(self,body):
        #先进行md5加密
        md5_body = self.md5(body) + body
        #des加密
        des_body = self.des_encrypt(md5_body)
        #base64加密
        base_body = base64.b64encode(bytearray([x for x in bytearray(des_body)]))
        return base_body


    def des_encrypt(self,s):
        """
        param s: 原始字符串
        param k: 秘钥
        """
        #s=bytes(s,encoding='utf-8')
        secret_key = bytearray.fromhex(self.miyao)
        print(secret_key)
        #iv = '\0\0\0\0\0\0\0\0'
        iv = bytes(8)
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s.encode('utf-8'), padmode=PAD_PKCS5) 
        return en
        #return base64.b64encode(bytearray([x for x in bytearray(en)]))


    def md5(self,s):
        m=hashlib.md5()
        m.update(bytes(s,encoding='utf-8'))
        return m.hexdigest()

    def des_descrypt(self,s):
        """
        DES 解密
        param s: 加密后的字符串，16进制
        param k: 秘钥
        """
        secret_key = bytearray.fromhex(self.miyao)
        #iv = '\0\0\0\0\0\0\0\0'
        iv = bytes(8)
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(s, padmode=PAD_PKCS5)
        return de


if __name__ == '__main__':
    #res=ema7_ws().send_sms()
    res=ema7_ws().encryption("今天是星期五")
    print(res)

