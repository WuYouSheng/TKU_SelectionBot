import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import *

import cryptocode
import sys
import threading
import platform
global ScrollBar
global window
window = tk.Tk()
global AddToList_Action
AddToList_Action = []
global AddToList_OpenCourse
AddToList_OpenCourse = []
global ExchangeFirst
ExchangeFirst = 0
global ExchangeSecond
ExchangeSecond = 0
global RemoveItem
RemoveItem = 0
working_dir = os.path.dirname(os.path.realpath(__file__))
global Login_Path
Login_Path = working_dir+"/Module_Addition/ProgramPlugin_1.info"
global Selective_Path
Selective_Path = working_dir+"/Module_Addition/ProgramPlugin_2.info"
global SelectionMode_Path
SelectionMode_Path = working_dir+"/Module_Addition/ProgramPlugin_3.info"
Record = 0

def LoadTheLoginInformation():
    global Record,Login_Path
    try:
        with open(Login_Path, 'r') as f:
            global Login
            Login = f.read().splitlines()
            for i in range(len(Login)):
                if (i+1)==1 or (i+1)==3:
                    pass
                elif (i+1)==2:
                    global Account_Login_Record
                    Account_Login_Record = str(Login[i])#解密
                    Account_textbox.insert(0, Account_Login_Record)
                    Record = 1
                else:
                    global Password_Login_Record
                    Password_Login_Record = str(Login[i])#解密
                    Password_textbox.insert(0, Password_Login_Record)
    except FileNotFoundError:
        Record = 0
        messagebox.showinfo("提示","偵測到程式遭修改\n請聯絡負責人")
        os._exit()
    return
def LoginSavingInformation():
    global Record
    global Account
    Account = Account_textbox.get()#加密
    #print(Account)
    Password = Password_textbox.get()#加密
    #print(Password)
    global Login_Path
    try:
        if(Account!="" and Password!= ""):
            with open(Login_Path, 'w') as f:
                f.write('Account')
                f.write('\n')
                f.write(Account)
                f.write('\n')
                f.write('Password')
                f.write('\n')
                f.write(Password)
                Record = 1
        else:
            messagebox.showinfo("提示", "輸入錯誤請重試")

    except:
        messagebox.showinfo("提示", "我們偵測到了你嘗試修改程式\n請聯絡負責人")
        os._exit()

def SelectiveSaving():
    global Selective_Path
    try:
        if (Selective_Path):
            with open(Selective_Path, 'w') as f:
                f.write('')
            for i in range(len(AddToList_Action)):
                with open(Selective_Path, 'a') as f:
                    f.write(AddToList_Action[i])
                    f.write('\n')
                    f.write(AddToList_OpenCourse[i])
                    f.write('\n')
            messagebox.showinfo("提示","選課清單儲存成功")
        else:
            messagebox.showinfo("提示","儲存路徑錯誤請重試")
    except:
        messagebox.showinfo("提示", "我們偵測到了您嘗試修改過程式\n請聯絡搶課負責人")
    return
def LoadSelectivedList():
    global Selective_Path
    try:
        with open(Selective_Path, 'r') as f:
            global Selection
            Selection = f.read().splitlines()
            for i in range(len(Selection)):
                if (i+1)%2==1:
                    AddToList_Action.append(str(Selection[i]))
                elif (i+1)%2==0:
                    AddToList_OpenCourse.append(str(Selection[i]))
    except FileNotFoundError:
        pass
    return
def LoginInformatioSavingConfirmBox():
    global Record
    Account = Account_textbox.get()
    Password = Password_textbox.get()
    if (Record==1 and Account !="" and Password !=""):
        LoginSavingInformation()
        messagebox.showinfo("提示", "密碼更新成功")
    elif Account =="" or Password =="":
        messagebox.showinfo("提示", "學號或密碼不能留空")
    elif (Record==0 and Account !="" and Password !=""):
        '''MsgBox = tk.messagebox.askquestion("提示","請問你確定儲存學號密碼嗎?\n學號只能綁定一次喔!\n學號未來是不能修改\n\nP.S.密碼可以修改")
        if MsgBox =="yes":
            LoginSavingInformation()
            Account_textbox.config(state='disable')
            messagebox.showinfo("提示", "學號密碼設定成功")
        else:
            pass'''
        messagebox.showinfo("提示", "學號密碼設定成功")
def build_GUI():
    #Build A GUI Window
    window.title("選課設定")
    window.geometry('380x540')
    window.resizable(False, True)

    #LoginTitle
    LoginTitle = tk.Label(window,width=30,text="登入資訊",font=("normal",15),compound="center")
    LoginTitle.place(x=190,y=20,anchor=CENTER)
    AccountInformation()
    PasswordInformation()

    #Button
    #LoginSaving Button
    Save_Button = tk.Button(text="儲存登入資訊",command=LoginInformatioSavingConfirmBox)
    Save_Button.place(x=190, y=115, anchor=CENTER)
    LoadTheLoginInformation()

    #SelectiveSaving_Button
    #SelectiveTitle
    SelectiveTitle = tk.Label(width=30,text="加退選資訊",font=("normal",15),compound="center")
    SelectiveTitle.place(x=190, y=165, anchor=CENTER)
    LoadSelectivedList()
    showList()
    Options()
    window.mainloop()

#Login Information
def AccountInformation():
    #Account
    Label_Account_textbox = tk.Label(width=6,text="學號",compound="center")
    Label_Account_textbox.place(x=60,y=40)
    global Account_textbox
    Account_textbox = tk.Entry(window)
    Account_textbox.pack()
    Account_textbox.place(x=120,y=40)
def PasswordInformation():
    # Password
    Label_Password_textbox = tk.Label(width=6, text="密碼", compound="center")
    Label_Password_textbox.place(x=60,y=70)
    global Password_textbox
    Password_textbox = tk.Entry(window)
    Password_textbox.pack()
    Password_textbox.place(x=120,y=70)

#Action
def Drop():
    Remove_Target = int(Revise_Remove_Box.get()) - 1
    if (Remove_Target<len(AddToList_Action) and Remove_Target>=0):
        initial()
        AddToList_Action.pop(Remove_Target)
        AddToList_OpenCourse.pop(Remove_Target)
        #Clear TextBox
        Revise_Remove_Box.delete(0, END)
        showList()
        #messagebox.showinfo("提示", "刪除成功")
    else:
        messagebox.showinfo("提示", "輸入錯誤，請重試")
    return
def Exchange():
    FirstIndex = int(Revise_ExchangeFirst_Box.get()) - 1
    SecondIndex = int(Revise_ExchangeSecond_Box.get()) - 1
    if (FirstIndex < len(AddToList_Action) and FirstIndex >= 0 and SecondIndex < len(AddToList_Action) and SecondIndex >= 0 and SecondIndex!= FirstIndex):
        AddToList_Action[FirstIndex], AddToList_Action[SecondIndex] = AddToList_Action[SecondIndex], AddToList_Action[FirstIndex]
        AddToList_OpenCourse[FirstIndex], AddToList_OpenCourse[SecondIndex] = AddToList_OpenCourse[SecondIndex], AddToList_OpenCourse[FirstIndex]
        # Clear TextBox
        Revise_ExchangeFirst_Box.delete(0, END)
        Revise_ExchangeSecond_Box.delete(0, END)
        showList()
        messagebox.showinfo("提示", "交換成功")
    else:
        messagebox.showinfo("提示", "輸入錯誤，請重試")
    return
def initial():
    y_axis = 270
    for i in range(len(AddToList_Action)):
        y_axis = y_axis + 30
        temp = tk.Label(window,width=2,height=3,text="",font=("normal",10),compound="center")
        temp.pack()
        temp.place(x=55,y=y_axis,anchor=CENTER)

        temp_1 = tk.Label(window,width=7,height=3,text="",font=("normal",10),compound="center")
        temp_1.pack()
        temp_1.place(x=100,y=y_axis,anchor=CENTER)

        temp_2 = tk.Label(window, width=7,height=3,text="", font=("normal",10),compound="center")
        temp_2.pack()
        temp_2.place(x=170, y=y_axis,anchor=CENTER)

#Selective Information
def Options():
    # Options
    global Optional_Selective
    Optional_Selective = ttk.Combobox(window,state="readonly", width=5, values=["加選", "退選"])
    Optional_Selective.pack()
    Optional_Selective.place(x=100, y=195, anchor=CENTER)
    Optional_Selective.current(0)

    #OpenCourseBox
    global OpenCourseBox
    OpenCourseBox = tk.Entry(window,width=15)
    OpenCourseBox.pack()
    OpenCourseBox.place(x=220,y=195,anchor=CENTER)

    #AddButton
    AddButton = tk.Button(text="加入清單",command=AddToList)
    AddButton.place(x=190, y=225, anchor=CENTER)

    #================================================================================================================
    #List
    Number_Column = tk.Label(window,width=2,height=3,text="#",font=("normal",10),compound="center")
    Number_Column.pack()
    Number_Column.place(x=55,y=270,anchor=CENTER)

    Action_Column = tk.Label(window,width=7,height=3,text="操作",font=("normal",10),compound="center")
    Action_Column.pack()
    Action_Column.place(x=100,y=270,anchor=CENTER)

    CourseCode_Column = tk.Label(window, width=7,height=3, font=("normal",10), text="開課代碼",compound="center")
    CourseCode_Column.pack()
    CourseCode_Column.place(x=170, y=270,anchor=CENTER)

    #================================================================================================================
    #ReviseArea
    #ReviseTitle
    Revise_Column = tk.Label(window, width=20, height=3, font=("normal", 10), text="調整", compound="center")
    Revise_Column.pack()
    Revise_Column.place(x=300, y=270, anchor=CENTER)

    #ReviseFirst_#
    Revise_ExchangeFirst = tk.Label(window, width=2, height=1, font=("normal", 10), text="#", compound="center")
    Revise_ExchangeFirst.pack()
    Revise_ExchangeFirst.place(x=220, y=300, anchor=CENTER)

    #ReviseFirst_TextBox
    global Revise_ExchangeFirst_Box
    Revise_ExchangeFirst_Box = tk.Entry(window, width=3)
    Revise_ExchangeFirst_Box.pack()
    Revise_ExchangeFirst_Box.place(x=240, y=300, anchor=CENTER)

    #ReviseSecond_#
    Revise_ExchangeSecond = tk.Label(window, width=2, height=1, font=("normal", 10), text="#", compound="center")
    Revise_ExchangeSecond.pack()
    Revise_ExchangeSecond.place(x=270, y=300, anchor=CENTER)

    #ReviseSecond_TextBox
    global Revise_ExchangeSecond_Box
    Revise_ExchangeSecond_Box = tk.Entry(window, width=3)
    Revise_ExchangeSecond_Box.pack()
    Revise_ExchangeSecond_Box.place(x=290, y=300, anchor=CENTER)

    #ExchangeButton
    ExchangeButton = tk.Button(text="交換", command=Exchange)
    ExchangeButton.place(x=340, y=300, anchor=CENTER)

    #Remove_#
    Revise_Remove = tk.Label(window, width=2, height=1, font=("normal", 10), text="#", compound="center")
    Revise_Remove.pack()
    Revise_Remove.place(x=250, y=330, anchor=CENTER)

    #Remove_TextBox
    global Revise_Remove_Box
    Revise_Remove_Box = tk.Entry(window, width=3)
    Revise_Remove_Box.pack()
    Revise_Remove_Box.place(x=275, y=330, anchor=CENTER)

    #Remove_Button
    Remove_Button = tk.Button(text=U"刪除", command=Drop)
    Remove_Button.place(x=330, y=330, anchor=CENTER)

    #================================================================================================================
    #Saving Area
    #SavingTitle
    Saving_Column = tk.Label(window, width=20, height=2, font=("normal", 10), text=U"儲存", compound="center")
    Saving_Column.pack()
    Saving_Column.place(x=300, y=370, anchor=CENTER)

    #SavingButton
    SavingButton = tk.Button(text=U"儲存加退選清單", command=SelectiveSaving)
    SavingButton.place(x=300, y=390, anchor=CENTER)

    # ================================================================================================================
    # Execution Area
    # ExecutionTitle
    Execution_Column = tk.Label(window, width=20, height=2, font=("normal", 10), text=U"搶課", compound="center")
    Execution_Column.pack()
    Execution_Column.place(x=300, y=420, anchor=CENTER)

    # ExecutionButton
    global Execution_Mode
    Execution_Mode = ttk.Combobox(window, state="readonly", width=15, values=["UC模式(推薦)","ChromeDriver"])
    Execution_Mode.pack()
    Execution_Mode.place(x=300, y=450, anchor=CENTER)
    Execution_Mode.current(0)
    ExecutionButton = tk.Button(text=U"執行搶課主程式", command=ExecutionMainFunction)
    ExecutionButton.place(x=300, y=480, anchor=CENTER)

def AddToList():
    if  Optional_Selective.get() == "加選" and OpenCourseBox.get() !="":
        AddToList_Action.append("Add")
        AddToList_OpenCourse.append(OpenCourseBox.get())
        OpenCourseBox.delete(0, END)
        showList()
    elif Optional_Selective.get() == "退選" and OpenCourseBox.get() !="":
        AddToList_Action.append("Remove")
        AddToList_OpenCourse.append(OpenCourseBox.get())
        OpenCourseBox.delete(0, END)
        showList()
    elif Optional_Selective.get() == "刷課" and OpenCourseBox.get() !="":
        AddToList_Action.append("Cycle")
        AddToList_OpenCourse.append(OpenCourseBox.get())
        OpenCourseBox.delete(0, END)
        showList()
    else:
        messagebox.showinfo("提示","開課代碼不能為空白")

def showList():
    y_axis = 270
    for i in range(len(AddToList_Action)):
        y_axis = y_axis + 30
        temp = tk.Label(window,width=2,height=3,text=i+1,font=("normal",10),compound="center")
        temp.pack()
        temp.place(x=55,y=y_axis,anchor=CENTER)

        temp_1 = tk.Label(window,width=7,height=3,text=AddToList_Action[i],font=("normal",10),compound="center")
        temp_1.pack()
        temp_1.place(x=100,y=y_axis,anchor=CENTER)

        temp_2 = tk.Label(window, width=7,height=3,text=AddToList_OpenCourse[i], font=("normal",10),compound="center")
        temp_2.pack()
        temp_2.place(x=170, y=y_axis,anchor=CENTER)

    #print(y_axis)
    if (y_axis>=480):
        wide = 380
        height = str(540+(len(AddToList_Action)-7)*30)
        mix = str(wide)+"x"+height
        window.geometry(mix)
    return

def LoginInformationCheck():
    CurrentAccount = Account_textbox.get()
    CurrentPassword = Password_textbox.get()
    global Login_Path

    with open(Login_Path, 'r') as f:
        global Login
        Login = f.read().splitlines()
        for i in range(len(Login)):
            if (i + 1) == 1 or (i + 1) == 3:
                pass
            elif (i + 1) == 2:
                global Account_Login_Record
                Account_Login_Record = str(Login[i])  # 解密
            else:
                global Password_Login_Record
                Password_Login_Record = str(Login[i])  # 解密
        try:
            if Account_Login_Record != CurrentAccount or Password_Login_Record != CurrentPassword :
                messagebox.showinfo("提示", "請儲存帳號密碼")
                return False
        except NameError:
            messagebox.showinfo("提示", "請設定帳號密碼")
            return False
        return True

def launch_MainFunction():
    try:
        subprocess.Popen(working_dir + "/Module_Addition/main", shell=True)
    except:
        subprocess.Popen(working_dir + "/Module_Addition/main.exe", shell=True)

def ExecutionMainFunction():
    if(LoginInformationCheck()):
        global working_dir,SelectionMode_Path
        if(Execution_Mode.get()=="UC模式(推薦)"):
            with open(SelectionMode_Path, 'w') as f:
                f.write('')
                f.write('UCMode')
        else:
            with open(SelectionMode_Path, 'w') as f:
                f.write('')
                f.write('ChromeDriverMode')
        if hasattr(sys, 'frozen'):
            threading.Thread(target=launch_MainFunction).start()
        else:
            try:
                s = subprocess.Popen(['python3', 'main' + '.py'], cwd=working_dir+'/Module_Addition')
            except:
                s = subprocess.Popen(['python', 'main' + '.py'], cwd=working_dir+'/Module_Addition')
    else:
        pass

#main function
if __name__ == '__main__':
    build_GUI()