# Third Party Libraries
from kivy.animation import Animation
from kivy.app import App
from kivy.graphics.instructions import Image
from kivy.uix.boxlayout import BoxLayout

# New imports
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


import httplib2
import json
import pyperclip
import webbrowser
from urllib.request import urlopen
from json import dumps
from kivy.properties import ObjectProperty
from kivy.app import App
import time, threading
from kivy.uix.popup import Popup
from kivy.factory import Factory



apiMethod = "https://"
apiVersion = "/v22"
apiServer = "api.weaved.com"
apiKey = "WeavedDemoKey$2015"

# Internat - http
UID=""
UID2=""
debug=1


class PopupBox(Popup):
    pop_up_text = ObjectProperty()
    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message

databases = range(5)

class SimpleRoot(BoxLayout): # 2
    IMG_OFF = "bulboff.png"
    IMG_ON = "bulbon.png"
    bulb_img = ObjectProperty(None)

    def show_popup(self):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text('Vytvaram spojenie...')
        self.pop_up.open()

    def on_our_btn_release(self, text_input):
        text = Label(text="Ahoj, {}!".format(text_input))
        pop_up = Popup(title="VPN domáci disk!", content=text, size_hint=(.7, .7))
        pop_up.open()

    def something_that_takes_5_seconds_to_run(self):
        thistime = time.time()
        while thistime + 5 > time.time():  # 5 seconds
            time.sleep(1)
        # Once the long running task is done, close the pop up.
        self.pop_up.dismiss()

    def getToken(self):
        httplib2.debuglevel = 0
        http = httplib2.Http()
        content_type_header = "application/json"
        userName = input("User name:")
        password = input("Password:")
        loginURL = apiMethod + apiServer + apiVersion + "/api/user/login"
        loginHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey
        }
        try:
            response, content = http.request(loginURL + "/" + userName + "/" + password,
                                             'GET',
                                             headers=loginHeaders)
        except:
            print("Server not found.  Possible connection problem!")
            exit()
        # print (response)
        print("============================================================")
        print(content)
        # to string conversion
        cont2 = content.decode("utf-8")
        try:
            data = json.loads(cont2)
            if (data["status"] != "true"):
                print("Can't connect to Weaved server!")
                print(data["reason"])
                exit()

            token = data["token"]
        except KeyError:
            print("Connnection failed!")
            exit()

        print("Token = " + token)
        deviceListURL = apiMethod + apiServer + apiVersion + "/api/device/list/all"
        content_type_header = "application/json"
        deviceListHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            # you need to get token from a call to /user/login
            'token': token,
        }
        response, content = http.request(deviceListURL,
                                         'GET',
                                         headers=deviceListHeaders)
        print(content)
        # Once the long running task is done, close the pop up.
        self.pop_up.dismiss()

    def proxyConnect(UID, token):
        httplib2.debuglevel = 0
        http = httplib2.Http()
        content_type_header = "application/json"

        # this is equivalent to "whatismyip.com"
        my_ip = urlopen('http://ip.42.pl/raw').read()
        proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

        proxyHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            'token': token
        }

        proxyBody = {
            'deviceaddress': UID,
            'hostip': my_ip.decode("utf-8"),
            'wait': "true"
        }

        response, content = http.request(proxyConnectURL,
                                         'POST',
                                         headers=proxyHeaders,
                                         body=dumps(proxyBody),
                                         )
        try:
            content = content.decode("utf-8")

            if (debug):
                print(content)

            data = json.loads(content)["connection"]["proxy"]
            print(data)

            if "" in UID:  # only on http
                webbrowser.open(data, new=2)  # open page in browser

            if "proxy" in data:
                
                tmp = data.split(":")
                res = "ssh -l pi " + tmp[1].split("//")[1] + " -p " + tmp[2]
                print(res)
                data = res

            pyperclip.copy(data)
            spam = pyperclip.paste()

        except KeyError:
            print("Key Error exception!")
            print(content)

    def on_btn_create_connection(self):
        # self.getToken()
        # self.proxyConnect(UID,token)

        # Open the pop up
        self.show_popup()

        # Call some method that may take a while to run.
        # I'm using a thread to simulate this
        mythread = threading.Thread(target=self.getToken)
        mythread.start()



class SimpleApp(App):  # 1
    def build(self):
        # Return root widget
        return SimpleRoot()

if __name__ == "__main__":
    SimpleApp().run()