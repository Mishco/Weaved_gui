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
import time, threading

from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.clock import Clock, mainthread

apiMethod = "https://"
apiVersion = "/v22"
apiServer = "api.weaved.com"
apiKey = "WeavedDemoKey$2015"

# Internat - http
UID="80:00:00:05:46:01:B3:E6"
UID2="80:00:00:05:46:01:B3:E7"
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
    text_input = ObjectProperty()
    token = ""

    def show_popup(self, text):
        self.pop_up = Factory.PopupBox()
        self.pop_up.update_pop_up_text(text)
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

        with open('pass.txt', 'r') as myfile:
            tmpData = myfile.read().replace('\n', ' ')

        userName = tmpData.partition(' ')[0].strip() # input("User name:")
        password = tmpData.partition(' ')[2].strip()  # input("Password:")

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
            print("Server not found. Possible connection problem!")
            self.show_popup("Server not found. Possible connection problem!")
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

            self.token = data["token"]
        except KeyError:
            print("Connnection failed!")
            exit()

        print("Token = " + self.token)
        deviceListURL = apiMethod + apiServer + apiVersion + "/api/device/list/all"
        content_type_header = "application/json"
        deviceListHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            # you need to get token from a call to /user/login
            'token': self.token,
        }
        response, content = http.request(deviceListURL,
                                         'GET',
                                         headers=deviceListHeaders)
        print(content)
        # Once the long running task is done, close the pop up.
        self.pop_up.dismiss()

    def proxyConnect(self):
        httplib2.debuglevel = 0
        http = httplib2.Http()
        content_type_header = "application/json"
        data = ""
        UID = UID2
        try:
            # this is equivalent to "whatismyip.com"
            my_ip = urlopen('http://ip.42.pl/raw').read()
        except:
            print("Error with connection, possible connection problem with network")
            #self.show_popup("Error with connection\n" + "possible connection problem with network")
            popup = Popup(title="Connection Error",
                          content=Label(text="Connection problem with your network")
                          ).open()


        proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

        proxyHeaders = {
            'Content-Type': content_type_header,
            'apikey': apiKey,
            'token': self.token
        }

        proxyBody = {
            'deviceaddress': UID,
            'hostip': my_ip.decode("utf-8"),
            'wait': "true"
        }
        content=""
        try:

            response, content = http.request(proxyConnectURL,
                                         'POST',
                                         headers=proxyHeaders,
                                         body=dumps(proxyBody),
                                         )
            content = content.decode("utf-8")

            if (debug):
                print(content)

            data = json.loads(content)["connection"]["proxy"]
            print(data)

            if "80:00:00:05:46:01:B3:E6" in UID:  # only on http
                webbrowser.open(data, new=2)  # open page in browser

            if "proxy" in data:
                tmp = data.split(":")
                res = "ssh -l pi " + tmp[1].split("//")[1] + " -p " + tmp[2]
                print(res)
                data = res

            pyperclip.copy(data)
            spam = pyperclip.paste()


        except:
            print("Key Error exception!")
            self.show_popup("Error: " + content)
            print(content)

        self.pop_up.dismiss()
        # set text_input to result
        self.text_input.text = data

    def on_btn_create_connection(self):
        # self.getToken()
        # self.proxyConnect(UID,token)

        # Open the pop up
        self.show_popup('Vytvaram spojenie...')

        # Call some method that may take a while to run.
        # I'm using a thread to simulate this
        mythread = threading.Thread(target=self.getToken)
        mythread.start()

    def on_btn_get_ssh_tunnel(self):
        # getting ssh path
        self.show_popup('Ziskavam SSH...')

        mythread = threading.Thread(target=self.proxyConnect)
        mythread.start()


    def check_network_and_find_rpi(self):
        # if is connect to local network just
        # get ip address of rpi
        no = ""


class SimpleApp(App):  # 1
    def build(self):
        # Return root widget
        return SimpleRoot()

if __name__ == "__main__":
    SimpleApp().run()