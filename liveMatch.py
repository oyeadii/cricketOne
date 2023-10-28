import os
import json
import time
import pyotp
import pickle
import tkinter
import requests
import threading
import unicodedata
import customtkinter
from pathlib import Path
import tkinter.messagebox
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image, ImageTk
from selenium.webdriver import Chrome
from getmac import get_mac_address as gma
from multiprocessing import Process, freeze_support
from selenium.webdriver.chrome.options import Options


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

directory = os.getcwd()
directory = directory.replace("\\", "/")

options = Options()
# options.headless = True
try:
    browser = Chrome(relative_to_assets("chromedriver1.exe") ,options=options)
except:
    try:
        browser = Chrome(relative_to_assets("chromedriver2.exe") ,options=options)
    except: 
        try:
            browser = Chrome(relative_to_assets("chromedriver3.exe") ,options=options)
        except: pass


def nameCleaner(batsman_name):
        batsman_name = unicodedata.normalize('NFD', batsman_name).encode('ascii', 'ignore').decode("utf-8")
        if "-" in batsman_name:
            bb1 = batsman_name.lower().split("-")
            bbb = ""
            for z in range(len(bb1)-1):
                bbb += bb1[z][0]
            bbb+= "-"
            bbb += bb1[len(bb1)-1].replace("(c)", "")
        else:
            bb1 = batsman_name.lower().split(" ")
            bbb = ""
            for z in range(len(bb1)-1):
                bbb += bb1[z][0]
            bbb+= "-"
            bbb += bb1[len(bb1)-1].replace("(c)", "")
        return bbb

def countryCleaner(countryName):
    countryName = str(countryName).split(" ")
    if len(countryName) == 1:
        cc = countryName[0][0:3]
        cc = cc.lower()
    else:
        cc = ""
        for i in range(len(countryName)):
            cc += countryName[i][0]
        cc = cc.lower()  
    return cc

url_live = None 
initer = 0
def liveFunc(url):
    global initer
    if initer==0:
        browser.get(url)
        time.sleep(10)
    initer+=1
    start = time.time()
    live_data = {}
    p1b = 0
    p2b = 0
    try:
        live_data["match_name"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/div/div").text
    except:
        live_data["match_name"] = ""
    try:
        country1 = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[1]/div[2]/div[1]").text
        countryCheck = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/div/div/div[2]/span[3]").text.replace(" ", "")
        if country1 == countryCheck:
            country2 = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/div/div/div[2]/span[5]").text.replace(" ", "")
        else:
            country2 = countryCheck
        live_data["team1"] = country1
        country1 = country1.lower().replace(" ", "")
    except:
        live_data["team1"] = ""
    try:
        live_data["team1_rw"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[1]/div[2]/div[2]/div/span[1]").text
    except:
        live_data["team1_rw"] = ""
    try:
        live_data["team1_overs"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[1]/div[2]/div[2]/div/span[2]").text
    except:
        live_data["team1_overs"] = ""
    try:
        live_data["crr"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div/div/div[1]/span[1]/span").text
    except:
        live_data["crr"] = ""
    try:
        live_data["rrr"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div/div/div[1]/span[2]/span").text
    except:
        live_data["rrr"] = ""
    try:
        live_data["dashboard"] = browser.find_element("xpath", "/html/body/app-root/div[1]/app-match-details/div[2]/div[3]/app-match-details-wrapper/div/div/div/div[2]/div[1]/span").text
    except:
        try:
            live_data["dashboard"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[2]/div/span").text
        except:
            live_data["dashboard"] = ""
    try:
        live_data["result"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div/div/div[2]").text
    except:
        live_data["result"] = ""
    try:
        # country2 = browser.find_element("xpath", '/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div[1]/div').text
        live_data["team2"] = country2
        country2 = country2.lower().replace(" ", "")
    except:
        live_data["team2"] = ""
    try:
        live_data["team2_rw"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div[2]/div/span[2]").text
    except:
        live_data["team2_rw"] = ""
    try:
        live_data["team2_overs"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[2]/app-match-details-wrapper/div/div/div[3]/div[1]/div[2]/div/span[1]").text
    except:
        live_data["team2_overs"] = ""
    
    try:
        live_data["partnership"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[1]/span[2]").text
    except:
        live_data["partnership"] = ""
    try:
        p1_name = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[2]/div/div[2]/a/p").text
        p1_name = nameCleaner(p1_name)
        try:
            browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[2]/div/div[4]")
            live_data["p1"] = p1_name.replace("-", " ").upper()
            p1b = 100
        except:
            live_data["p1"] = p1_name.replace("-", " ").upper()
            p1b = -100
    except:
        live_data["p1"] = ""
    try:   
        p1_rb = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[2]/div/div[3]/div[2]").text
        p1_rb = p1_rb.split("(")
        live_data["p1_runs"] = p1_rb[0]
        live_data["p1_balls"] = p1_rb[1][:-1]
    except:
        live_data["p1_runs"] = ""
        live_data["p1_balls"] = ""
    try:
        live_data["p1_sr"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[3]/div[1]/span[2]").text
    except:
        live_data["p1_sr"] = ""
    try:
        live_data["p1_4s"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[3]/div[3]/div[1]/span[2]").text
    except:
        live_data["p1_4s"] = ""
    try:
        live_data["p1_6s"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[1]/div[3]/div[3]/div[2]/span[2]").text
    except:
        live_data["p1_6s"] = ""
    try:
        p2_name = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[2]/div/div[2]/a/p").text
        p2_name = nameCleaner(p2_name)
        try:
            browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[2]/div/div[4]").text
            live_data["p2"] = p2_name.replace("-", " ").upper()
            p2b = 100
        except:
            live_data["p2"] = p2_name.replace("-", " ").upper()
            p2b = -100
    except:
        live_data["p2"] = ""
    try:
        p2_rb = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[2]/div/div[3]/div[2]").text
        p2_rb = p2_rb.split("(")
        live_data["p2_runs"] = p2_rb[0]
        live_data["p2_balls"] = p2_rb[1][:-1]
    except:
        live_data["p2_runs"] = ""
        live_data["p2_balls"] = ""
    try:
        live_data["p2_sr"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[3]/div[1]/span[2]").text
    except:
        live_data["p2_sr"] = ""
    try:
        live_data["p2_4s"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[3]/div[3]/div[1]/span[2]").text
    except:
        live_data["p2_4s"] = ""
    try:
        live_data["p2_6s"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[2]/div[3]/div[3]/div[2]/span[2]").text
    except:
        live_data["p2_6s"] = ""
    try:
        b1_name = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[3]/div[2]/div/div[2]/a/p").text
        b1_name = nameCleaner(b1_name)
        live_data["b1"] = b1_name.replace("-", " ").upper()
    except:
        live_data["b1"] = ""
    try:
        live_data["b1_rw"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/p[1]").text
    except:
        live_data["b1_rw"] = ""
    try:
        live_data["b1_overs"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[3]/div[2]/div/div[1]/div[1]/p[2]").text
    except:
        live_data["b1_overs"] = ""
    try:
        live_data["b1_ec"] = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[1]/div[3]/div[3]/div/span[2]").text
    except:
        live_data["b1_ec"] = ""
    
    
    overs = browser.find_elements("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[2]/div[2]/div")
    try:
        if len(overs) > 1:
            last_over = overs[len(overs)-2].text
            last_over = last_over.replace("\n", "   ").split(":")[1]
            last_over = last_over.replace("   ", "", 1)
            live_data["last_over"] = last_over
        else:
            live_data["last_over"] = ""
    except:
        live_data["last_over"] = ""
    try:
        this_over = overs[len(overs)-1].text
        this_over = this_over.replace("\n", "   ").split(":")[1]
        this_over = this_over.replace("   ", "", 1)
        live_data["this_over"] = this_over
    except:
        live_data["this_over"] = ""

    try:
        d1 = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[3]/div/div[1]/div/div/div/div/div/div/div/div[1]/div").get_attribute('textContent')
        d2 = browser.find_element("xpath", "/html/body/app-root/div/app-match-details/div[3]/app-match-live/div/div[3]/div/div[1]/div/div/div/div/div/div/div/div[2]").get_attribute('textContent')
        live_data["last_wicket"] = d1 + "  " + d2
    except:
        live_data["last_wicket"] = ""
    try:
        if live_data["team1"] != "":
            live_data["t1_img"] = directory + f"/img/flags/{country1}.png"
        else:
            live_data["t1_img"] = directory + f"/img/empty.png"
        if live_data["team2"] != "":
            live_data["t2_img"] = directory + f"/img/flags/{country2}.png"
        else:
            live_data["t2_img"] = directory + f"/img/empty.png"
        if live_data["p1"] != "":
            live_data["p1_img"] = directory + f"/img/{country1}/{p1_name}.png"
        else:
            live_data["p1_img"] = directory + f"/img/empty.png"
        if live_data["p2"] != "":
            live_data["p2_img"] = directory + f"/img/{country1}/{p2_name}.png"
        else:
            live_data["p2_img"] = directory + f"/img/empty.png"
        if live_data["b1"] != "":
            live_data["b1_img"] = directory + f"/img/{country2}/{b1_name}.png"
        else:
            live_data["b1_img"] = directory + f"/img/empty.png"
    except:
        pass
    try:
        if p1b == 100:
            live_data["p1bimg"] = directory + "/img/bat.png"
        elif p1b == -100:
            live_data["p1bimg"] = directory + "/img/nobat.png"
        if p2b == 100:
            live_data["p2bimg"] = directory + "/img/bat.png"
        elif p2b == -100:
            live_data["p2bimg"] = directory + "/img/nobat.png"
    except:
        pass

    try:
        with open("innings.json", "w") as outfile:
            json.dump({"selection1":[live_data]}, outfile)
    except:
        pass
    end = time.time()
    print(end-start)

condition = True
def starter():
    global condition
    while condition:
        if url_live is None:
            return 0     
        liveFunc(url_live)
        
# ============================================================================================================================================
# tkinter
# ============================================================================================================================================
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    try:
        WIDTH = 780
        HEIGHT = 520
        def load_image(self, path, image_size):
            """ load rectangular image with path relative to PATH """
            return ImageTk.PhotoImage(Image.open(relative_to_assets(path)).resize((image_size, image_size)))

        def __init__(self):
            super().__init__()
            self.base32secret = 'PZMNG3U6FDUBGFGKCYDZ5VUIDA2SG3OB'
            self.totp = pyotp.TOTP(self.base32secret)
            self.otp = self.totp.now()
            self.mac_address = gma()
            print(self.otp)
            self.limit = 3
            self.daysgone=0
            self.otp1 = "0"
            self.title("DGN Cricket")
            self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
            self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
            self.iconbitmap(False, relative_to_assets('favicon.ico'))
            # ============ create two frames ============

            # configure grid layout (2x1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.frame_left = customtkinter.CTkFrame(master=self,
                                                    width=180,
                                                    corner_radius=0)
            self.frame_left.grid(row=0, column=0, sticky="nswe")

            self.frame_right = customtkinter.CTkFrame(master=self)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            # ============ frame_left ============

            # configure grid layout (1x11)
            self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
            self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
            self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
            self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

            self.home_image = self.load_image("logo.png", 80)
            self.label_0 = customtkinter.CTkLabel(master=self.frame_left,
                                                text_font=("Roboto Medium", -25),
                                                image=self.home_image)  # font name and size in px
            self.label_0.grid(row=1, column=0)

            self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                                text="DGN Cricket v1.0",
                                                text_font=("Roboto Medium", -25))  # font name and size in px
            self.label_1.grid(row=2, column=0, pady=10, padx=10)

            self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
            self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

            self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                            values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode)
            self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

            # ============ frame_right ============

            # configure grid layout (3x7)
            self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
            self.frame_right.rowconfigure(7, weight=10)
            self.frame_right.columnconfigure((0, 1), weight=1)
            self.frame_right.columnconfigure(2, weight=0)

            self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
            self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=1, pady=20, padx=20, sticky="nsew")

            # ============ frame_info ============

            # configure grid layout (1x1)
            self.frame_info.rowconfigure(0, weight=1)
            self.frame_info.columnconfigure(0, weight=1)

            self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                    text="We provide the fastest ball-by-ball\n" +
                                                            "score that is at par with live action.",
                                                    height=80,
                                                    corner_radius=6,  # <- custom corner radius
                                                    fg_color=("#0077B6", "#0077B6"),
                                                    text_font=("Roboto Medium", -18),  # <- custom tuple-color
                                                    justify=tkinter.LEFT)
            self.label_info_1.grid(column=0, row=1, sticky="nwe", padx=5, pady=5)
            # ============ frame_right ============
            if os.path.exists(directory+'/vfile.dat'):
                v1 = str(pickle.load(open(directory+'/vfile.dat', "rb")))
                v1 = v1.split(" ")
                if v1[2] == gma():
                    d1 = datetime.strptime(v1[1], "%Y%m%d")
                    d2 = datetime.strptime(self.get_date(), "%Y%m%d")
                    self.daysgone = (d2-d1).days
                    if self.daysgone < self.limit:
                        self.label_99 = customtkinter.CTkLabel(master=self.frame_left,
                                                    text=f"Expires in: {self.limit-self.daysgone} days",
                                                    text_font=("Roboto Medium", -15),
                                                    corner_radius=6,
                                                    fg_color=("#0077B6", "#0077B6"))  # font name and size in px
                        self.label_99.grid(row=3, column=0, pady=5, padx=10)

                        var = tkinter.StringVar()
                        def printinput(*args):
                            global url_live
                            url_live = var.get()
                            if url_live == "Live URL":
                                url_live = None
                        var.trace("w", printinput)
                        self.entry_1 = customtkinter.CTkEntry(master=self.frame_right,
                                                            width=120,
                                                            placeholder_text="Live URL",
                                                            textvariable=var)
                        self.entry_1.grid(row=3, column=0, columnspan=2, padx=20, sticky="we")
                        self.entry_1.insert(0, "Live URL")

                        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                        text="Start",
                                                        border_width=2,  # <- custom border_width
                                                        fg_color=None,  # <- no fg_color
                                                        command=self.start)
                        self.button_5.grid(row=3, column=2, columnspan=1, pady=20,padx=20, sticky="we")
                else:
                    os.remove(directory+'/vfile.dat')
            else:
                var4 = tkinter.StringVar()
                
                def printinput_3(*args):
                    self.otp1= var4.get()
                var4.trace("w", printinput_3)
                self.entry_66 = customtkinter.CTkEntry(master=self.frame_right,
                                                        width=120,
                                                        placeholder_text="Enter Activation Key",
                                                        textvariable=var4,)
                self.entry_66.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="we")
                self.entry_66.insert(0, "Enter Activation Key")

                self.button_55 = customtkinter.CTkButton(master=self.frame_right,
                                                    text="Activate",
                                                    border_width=2,  # <- custom border_width
                                                    fg_color=None,  # <- no fg_color
                                                    command=self.activation)
                self.button_55.grid(row=3, column=2, columnspan=1, pady=20,padx=20, sticky="we")     
            self.label_77 = customtkinter.CTkLabel(master=self.frame_right,
                                                text="",
                                                text_font=("Roboto Medium", -18),
                                                corner_radius=6,
                                                fg_color=("white", "gray38"))  # font name and size in px
            self.label_77.grid(row=8, column=0, pady=10, padx=10, columnspan=3, sticky="we")

            self.home_image_1 = self.load_image("logo1.png", 120)
            self.label_888 = customtkinter.CTkLabel(master=self.frame_right,
                                                image=self.home_image_1)  # font name and size in px
            self.label_888.grid(row=0, column=2)

            self.button_6 = customtkinter.CTkButton(master=self.frame_right,
                                                    text="Exit",
                                                    border_width=2,  # <- custom border_width
                                                    fg_color=None,  # <- no fg_color
                                                    command=self.stop)
            self.button_6.grid(row=4, column=2, columnspan=1,pady=20, padx=20, sticky="we")

            # set default values
            self.optionmenu_1.set("Dark")

        # def status_updater(self):
        #     self.label_000.configure(text=f"Live: {live_status}\n"+
        #                                   f"Match-Info: {match_status}\n"+
        #                                   f"Scoreboard: {scoreboard_status}")
        
        def get_date(self):
            r=requests.get("https://www.calendardate.com/todays.htm")
            soup = BeautifulSoup(r.text, 'html.parser')
            a = soup.find_all(id='tprg')[6].text
            a= a.replace('-', " ")
            a= a.replace(' ', '')
            return a

        def start(self):
            t = threading.Thread(target=starter)
            t.start()

        def stop(self):
            print ("Stop")
            global condition
            condition=False
            self.destroy()
            browser.close()
            browser.quit()

        def change_appearance_mode(self, new_appearance_mode):
            customtkinter.set_appearance_mode(new_appearance_mode)

        def on_closing(self, event=0):
            self.destroy()

        def activation(self):
            if self.totp.now() == self.otp1:
                self.label_111 = customtkinter.CTkLabel(master=self.frame_right,
                                                text="Product Activated Successfully. Restart the App and Enjoy !!",
                                                text_font=("Roboto Medium", -15),
                                                corner_radius=6,
                                                fg_color=("green", "green"))  # font name and size in px
                self.label_111.grid(row=2, column=0, pady=10, padx=10, sticky="we", columnspan=3)
                self.myvar = "sdfaydyfwdqedfyewqtdfas" + " " +self.get_date() + " " + self.mac_address
                pickle.dump(self.myvar, open(directory+"/vfile.dat", "wb"))
            else:
                self.label_111 = customtkinter.CTkLabel(master=self.frame_right,
                                                text="Activation Failed! Try Again.",
                                                text_font=("Roboto Medium", -15),
                                                corner_radius=6,
                                                fg_color=("red", "red"))  # font name and size in px
                self.label_111.grid(row=2, column=0, pady=10, padx=10, sticky="we", columnspan=3)
    except:
        pass

if __name__ == "__main__":
    freeze_support()
    app = App()
    app.mainloop()