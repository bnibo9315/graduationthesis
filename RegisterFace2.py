###############################################################################
#   Author : Thanh Quang Long
#   Date : 1, 4, 2020
#   Function main : register face -------
#   Version : 2.0
#   Copyright by 2020,Binbo
###############################################################################
from Tkinter import *
import tkMessageBox as messagebox
import tkSimpleDialog as simpledialog
import cv2
from PIL import Image, ImageTk
import time
import sys
import os
import ttk
import tkFileDialog as filedialog
import dlib

print("Binbo-debug cam..................")


class App:
    def __init__(self, window):
        #######################################################################
        self.window = window
        self.window.title("Camera Live")

        ########################## GUI #########################################
        self.window.call('wm', 'iconphoto', window._w,
                     ImageTk.PhotoImage(file='./img/logo/icon.ico'))
        self.text_welcome = Label(
            window, text="Facial Recognition System & User Information", fg='red', font=("Helvetica", 24, 'bold'))
        self.ico = ImageTk.PhotoImage(
            Image.open("./img/logo/logo.ico").resize((100, 100)))
        self.admin = ImageTk.PhotoImage(
            Image.open("./img/logo/admin_handsome.jpg").resize((650, 450,)))
        self.text_infor = Label(
            window, text="User Information", fg='red', font=("Helvetica", 24))
        self.text_detec = Label(
            window, text="Face Recognition", fg='red', font=("Helvetica", 24))
        self.text_username = Label(
            window, text="User Name :", fg='#00008B', font=("Helvetica", 17))
        self.text_rank = Label(
            window, text="Role :", fg='#00008B', font=("Helvetica", 17))
        self.guide = Label(window, text="User Guide: ",
                           fg='#DC143C', font=("Helvetica", 24, 'bold'))
        self.listuser = sorted(os.listdir("./database/users/"))
        self.status_count = "Number of people used : {} people".format(len(self.listuser))
        self.show_count = Label(
            self.window,text=self.status_count ,fg='#FF8C00', font=("Helvetica", 17 ,'bold'))
        self.text_guide_detail = """
            1. Input Your Username
            2. Choose Your Role
            3. Click Button 'Register Now!!!'
                to create new FaceLogin (database)
            4. Click Button 'Login Now!!!' to enabel
                Face Recognition
        """
        self.list = ttk.Combobox(window, width=10, values=[
            "Admin",
            "Users",
            "Visitor"], font=("Helvetica", 17))
        self.enFaceid = Button(window, text="Login Now!!!", fg="#008000", font=(
            "Helvetica", 15),command=lambda: self.startFaceId())
        self.refresh = ImageTk.PhotoImage(
            Image.open("./img/logo/refresh.png").resize((40, 40)))
        self.buttonrefresh = Button(window, image=self.refresh,command=  lambda : [self.window.destroy(),os.system("python RegisterFace2.py")])
        self.loading = Label(window, image=self.admin)
        self.quit = Button(window, text="Exit App", fg="#FF8C00", font=(
            "Helvetica", 15), command=lambda: self.window.destroy())
        self.register = Button(
            window, text="Register Now!!!", fg="#DC143C", font=("Helvetica", 15), command=lambda: self.process_files())
        self.logo = Label(window, image=self.ico)
        self.inputname = Entry(window, font=("Helvetica", 17))

        self.guide_detail = Canvas(window, width=480, height=300, bg='#F5F5DC')
        self.guide_detail.create_text(
            200, 100, text=self.text_guide_detail, font=("Helvetica", 17, 'bold'))
        ##Location obj#######################################################
        self.buttonrefresh.place(x=620, y =50)
        self.show_count.place(x=15, y=680)
        self.inputname.place(x=800, y=115, height=38, width=450)
        self.text_detec.place(x=200, y=50)
        self.text_infor.place(x=880, y=50)
        self.text_username.place(x=660, y=115)
        self.text_rank.place(x=660, y=165)
        self.list.place(x=750, y=165)
        self.register.place(x=850, y=210)
        self.quit.place(x=1050, y=210)
        self.logo.place(x=5, y=5)
        self.text_welcome.pack()
        self.loading.pack(side=LEFT, padx=0, pady=10)
        self.enFaceid.place(x=670, y=210)
        self.guide.place(x=850, y=300)
        self.guide_detail.place(x=750, y=350)
        ###############################Value##################################
        self.count = 0
        self.status = False
        self.window.geometry("1280x720")
        self.window.mainloop()
       #########################Live Stream Values ##########################

    #########################Create Database##################################
    # Create folder
    def process_files(self):
        if self.inputname.get() != "" and self.list.get() != "":
            self.rank = self.list.get()
            self.status = True
            
            
            if self.rank == "Admin":
                passadmin =simpledialog.askinteger("Key", "Key Admin")
                if passadmin is not None:
                    if passadmin == 810198 :
                        self.name = self.inputname.get()
                        self.image_path = "./database/admin/"
                    else:
                        messagebox.showerror("Error", "Key fails")
            else:
                self.name = self.inputname.get()
                self.image_path = "./database/users/" + self.name + "/"
                try:
                    os.makedirs(self.image_path)
                    self.ids = format(len(self.listuser) + 2 )
                    print(self.ids)
                except :
                    messagebox.showinfo(
                "Notice - Author : ThanhQuangLong", "Your name already exists ")
            self.cmd = "python3 client.py " + "register " + self.name + " " + self.image_path + " " + self.rank + " " + self.ids 
            ### Start Detect#####################################################
            os.system(self.cmd)
        else:
            messagebox.showinfo(
                "Notice - Author : ThanhQuangLong", "Pls input your username or select your rank")
            self.loading.pack(side=LEFT, padx=5, pady=50)

    def noticeDone(self):
        messagebox.showinfo(
            "Notice - Author : ThanhQuangLong", "!!!!!!!!!!!! Register Done !!!!!!!!!!!!")
        self.count = 0
        self.status = False
        self.rank = self.list.get()
        if self.rank == "Admin":
            self.name = self.inputname.get()
            self.image_path = "./database/admin/"
            self.status = True
        else:
            self.name = self.inputname.get() 
            self.image_path = "./database/" + self.name + "/"
            os.makedirs(self.image_path)
            self.status = True
        ### Start Detect#####################################################

    def startFaceId(self):
        print("Enable face recognition systems")
        if self.list.get() != "":
            self.rank = self.list.get()
            self.cmd = "python3 client.py " +"login " + self.rank 
            print(self.cmd)
            os.system(self.cmd)
        else:
            messagebox.showinfo(
                "Notice - Author : ThanhQuangLong", "Pls select your rank")

App(Tk())
