import os
import datetime
import os
import random
import ssl
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.constants import *
from tkinter import filedialog

import cryptocode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import chromedriver_autoinstaller
ssl._create_default_https_context = ssl._create_unverified_context

URL_Chinese = "https://www.ais.tku.edu.tw/EleCos/login.aspx?ReturnUrl=%2felecos%2f"
URL_English = "https://www.ais.tku.edu.tw/EleCos_English/loginE.aspx"

global ChineseScript
ChineseScript = "javascript: (function(){ var numHash={b6589fc6ab0dc82cf12099d1c2d40ab994e8410c:\"0\",\"356a192b7913b04c54574d18c28d46e6395428ab\":\"1\",da4b9237bacccdf19c0760cab7aec4a8359010b0:\"2\",\"77de68daecd823babbb58edb1c8e14d7106e83bb\":\"3\",\"1b6453892473a467d07372d45eb05abc2031647a\":\"4\",ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4:\"5\",c1dfd96eea8cc2b62785275bca38ac261256e278:\"6\",\"902ba3cda1883801594b6e1b452790cc53948fda\":\"7\",fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f:\"8\",\"0ade7c2cf97f75d009975f4d720d1fa6c19f4897\":\"9\"};$.ajax({url:\"https://www.ais.tku.edu.tw/EleCos/Handler1.ashx\",type:\"post\",async:false,success:function(voice){document.getElementById(\"txtCONFM\").value=numHash[voice[0]]+numHash[voice[1]]+numHash[voice[2]]+numHash[voice[3]]+numHash[voice[4]]+numHash[voice[5]];}}); })();"
global EnglishScript
EnglishScript = "javascript: (function(){ var numHash={b6589fc6ab0dc82cf12099d1c2d40ab994e8410c:\"0\",\"356a192b7913b04c54574d18c28d46e6395428ab\":\"1\",da4b9237bacccdf19c0760cab7aec4a8359010b0:\"2\",\"77de68daecd823babbb58edb1c8e14d7106e83bb\":\"3\",\"1b6453892473a467d07372d45eb05abc2031647a\":\"4\",ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4:\"5\",c1dfd96eea8cc2b62785275bca38ac261256e278:\"6\",\"902ba3cda1883801594b6e1b452790cc53948fda\":\"7\",fe5dbbcea5ce7e2988b8c69bcfdfde8904aabc1f:\"8\",\"0ade7c2cf97f75d009975f4d720d1fa6c19f4897\":\"9\"};$.ajax({url:\"https://www.ais.tku.edu.tw/EleCos_English/Handler1.ashx\",type:\"post\",async:false,success:function(voice){document.getElementById(\"txtCONFM\").value=numHash[voice[0]]+numHash[voice[1]]+numHash[voice[2]]+numHash[voice[3]]+numHash[voice[4]]+numHash[voice[5]];}}); })();"
global window
window = tk.Tk()

global AddToList_Action
AddToList_Action = []
global AddToList_OpenCourse
AddToList_OpenCourse = []
Account_Login_Record = 0
Password_Login_Record = 0
working_dir = os.path.dirname(os.path.realpath(__file__))
global Login_Path
Login_Path = working_dir+"/ProgramPlugin_1.info"
global Selective_Path
Selective_Path = working_dir+"/ProgramPlugin_2.info"
global SelectionMode_Path
SelectionMode_Path = working_dir+"/ProgramPlugin_3.info"
chromedriver_autoinstaller.install()
global SelectionMode
global driver

# Check select Mode
with open(SelectionMode_Path, 'r') as f:
    global SelectionMode
    SelectionMode = f.read().splitlines()
    SelectionMode = str(SelectionMode[0])

def OpenChrome():
    global driver,Driver_Path
    if (SelectionMode == "UCMode"):
        service = ChromeService()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service,options=options)
    else:
        messagebox.showinfo("提示", "請選取ChromeDriver檔案")
        ChromeDriver_path = filedialog.askopenfilename()  # 選擇檔案後回傳檔案路徑與名稱
        service = ChromeService(executable_path=ChromeDriver_path)
        # print(ChromeDriver_path)
        driver = webdriver.Chrome(service=service)


def LoadTheLoginInformation():
    global Login_Path
    try:
        with open(Login_Path, 'r') as f:
            global Login
            Login = f.read().splitlines()
            for i in range(len(Login)):
                if (i+1)==1 or (i+1)==3:
                    pass
                elif (i+1)==2:
                    global Account_Login_Record
                    Account_Login_Record = str(Login[i])
                    #print("Account: "+Account_Login_Record,type(Account))
                    #print(line[i],type(line[i]))
                else:
                    global Password_Login_Record
                    Password_Login_Record = str(Login[i])
                    #print("Password: "+Password_Login_Record)
    except FileNotFoundError:
        messagebox.showinfo("提示", "無法載入登入資訊"+"\n"+"請先執行setting設定加退選資訊")
    if len(Login)==0:
        messagebox.showinfo("提示","沒有登入資訊"+"\n"+"請先執行setting設定登入資訊")
    return
def LoadTheSelectionInformation():
    global Selective_Path
    try:
        with open(Selective_Path, 'r') as f:
            global Selection
            Selection = f.read().splitlines()
            for i in range(len(Selection)):
                if (i+1)%2==1:
                    if str(Selection[i]) =="Add" or str(Selection[i]) =="Remove":
                        AddToList_Action.append(str(Selection[i]))
                    elif str(Selection[i]) =="Cycle":
                        pass
                elif (i+1)%2==0:
                    AddToList_OpenCourse.append(str(Selection[i]))
                else:
                    pass

    except FileNotFoundError:
        messagebox.showinfo("提示", "無法載入加退選清單"+"\n"+"請先執行setting設定加退選資訊")
        os._exit()
    if len(Selection)==0:
        messagebox.showinfo("提示","加退選清單為空白"+"\n"+"請先執行setting設定加退選資訊")
        os._exit()
    return
def build_GUI():
    #Build A GUI Window
    LoadTheLoginInformation()
    LoadTheSelectionInformation()
    window.title("搶課程式")
    window.geometry('380x440')
    window.resizable(False, True)

    #LanguageTitle
    LanguageTitle = tk.Label(window,width=30,text="語言選擇",font=("normal",15),compound="center")
    LanguageTitle.place(x=190,y=20,anchor=CENTER)
    LanguageSelect()

    #TimeTitle
    SelectiveTitle = tk.Label(window,width=30,text="搶課排程",font=("normal",15),compound="center")
    SelectiveTitle.place(x=190, y=80, anchor=CENTER)
    TimeMode()
    initial()

    #Execution Button
    ExecutionButton = tk.Button(window,text="開始搶課", command=Execution)
    ExecutionButton.place(x=190, y=320, anchor=CENTER)

    #AboutMe
    AboutMeTitle = tk.Label(window, text="~本機器人由淡江大學 資汛工程學系 WYSH 開發製作~", font=("normal", 10), compound="center")
    AboutMeTitle.place(x=190, y=350, anchor=CENTER)
    CompilerTitle = tk.Label(window, text="使用Python3.11.4開發製作，2023/08/28編譯", font=("normal", 10),compound="center")
    CompilerTitle.place(x=190, y=370, anchor=CENTER)
    SloganTitle = tk.Label(window, text="電腦怪傑，實力不容小覷，不服來戰", font=("normal", 10),compound="center")
    SloganTitle.place(x=190, y=390, anchor=CENTER)
    SloganTitle_2 = tk.Label(window, text="只有不想搶的課，沒有搶不到的課", font=("normal", 10), compound="center")
    SloganTitle_2.place(x=190, y=410, anchor=CENTER)
    window.mainloop()

def LanguageSelect():
    global var_1
    var_1 = tk.StringVar()
    global Language_Chinese, Language_English
    Language_Chinese = tk.Radiobutton(window,text='中文', command=LaguageSet,var=var_1, value=1)
    Language_English = tk.Radiobutton(window,text='English', command=LaguageSet,var=var_1, value=2)
    Language_Chinese.place(x=100, y=30)
    Language_English.place(x=220, y=30)
def LaguageSet():
    global SelectionMode
    global Language_Set
    global driver
    Language_Set = var_1.get()
    if Language_Set=="1":
        driver.get(URL_Chinese)
    else:
        driver.get(URL_English)
    return
def TimeMode():
    global var_2
    var_2 = tk.StringVar()
    global TimeMode_Immediately, TimeMode_Schedule
    TimeMode_Immediately = tk.Radiobutton(window,text='立即',command=TimeModeSet, var=var_2,value=3)
    TimeMode_Schedule = tk.Radiobutton(window,text='預約搶課',command=TimeModeSet, var=var_2,value=4)
    TimeMode_Immediately.place(x=100, y=100)
    TimeMode_Schedule.place(x=220, y=100)
def TimeModeSet():
    global TimeMode_Set
    TimeMode_Set = var_2.get()
    if TimeMode_Set =="3":
        initial()
    else:
        TimeSetArea()
    return
def initial():
    # TimeAreaTitle
    TimeAreaTitle = tk.Label(window,width=30, state="disable",text="時間設定", font=("normal", 15), compound="center")
    TimeAreaTitle.place(x=190, y=150, anchor=CENTER)

    # YearTitle
    YearTitle = tk.Label(window,width=3, state="disable", text="年份", font=("normal", 10), compound="center")
    YearTitle.place(x=80, y=180, anchor=CENTER)

    # YearSelectionBox
    global YearSelection
    YearSelection = ttk.Combobox(window, state="disable", width=4,
                                 values=["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"])
    YearSelection.pack()
    YearSelection.place(x=75, y=200, anchor=CENTER)
    YearSelection.current(0)

    # MonthTitle
    MonthTitle = tk.Label(window,width=3, state="disable", text="月份", font=("normal", 10), compound="center")
    MonthTitle.place(x=125, y=180, anchor=CENTER)

    # MonthSelectionBox
    global MonthSelection
    MonthSelection = ttk.Combobox(window, state="disable", width=2,
                                  values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
    MonthSelection.pack()
    MonthSelection.place(x=125, y=200, anchor=CENTER)
    MonthSelection.current(0)

    # DateTitle
    DateTitle = tk.Label(window,width=3, state="disable", text="日期", font=("normal", 10), compound="center")
    DateTitle.place(x=170, y=180, anchor=CENTER)

    # DateSelectionBox
    global DateSelection
    DateSelection = ttk.Combobox(window, state="disable", width=2,
                                 values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                         "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26",
                                         "27", "28", "29", "30", "31"])
    DateSelection.pack()
    DateSelection.place(x=170, y=200, anchor=CENTER)
    DateSelection.current(10)

    # HourTitle
    HourTitle = tk.Label(window,width=3, state="disable", text="小時", font=("normal", 10), compound="center")
    HourTitle.place(x=225, y=180, anchor=CENTER)

    # HourSelectionBox
    global HourSelection
    HourSelection = ttk.Combobox(window, state="disable", width=2,
                                 values=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
                                         "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
    HourSelection.pack()
    HourSelection.place(x=225, y=200, anchor=CENTER)
    HourSelection.current(12)

    # MinutesTitle
    MinutesTitle = tk.Label(window,width=3, state="disable", text="分", font=("normal", 10), compound="center")
    MinutesTitle.place(x=270, y=180, anchor=CENTER)

    # MinutesSelectionBox
    global MinutesSelection
    MinutesSelection = ttk.Combobox(window, state="disable", width=2,
                                    values=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                            "12", "13",
                                            "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                                            "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                                            "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                                            "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"])
    MinutesSelection.pack()
    MinutesSelection.place(x=270, y=200, anchor=CENTER)
    MinutesSelection.current(30)

    # SecondTitle
    SecondTitle = tk.Label(window,width=3, state="disable", text="秒", font=("normal", 10), compound="center")
    SecondTitle.place(x=315, y=180, anchor=CENTER)

    # SecondSelectionBox
    global SecondSelection
    SecondSelection = ttk.Combobox(window, state="disable", width=2,
                                   values=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                           "12", "13",
                                           "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                                           "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                                           "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                                           "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"])
    SecondSelection.pack()
    SecondSelection.place(x=315, y=200, anchor=CENTER)
    SecondSelection.current(0)
    return
def TimeSetArea():
    # TimeAreaTitle
    TimeAreaTitle = tk.Label(window,width=30, state="normal",text="時間設定", font=("normal", 15), compound="center")
    TimeAreaTitle.place(x=190, y=150, anchor=CENTER)

    #YearTitle
    YearTitle = tk.Label(window,width=3, state="normal", text="年份", font=("normal", 10), compound="center")
    YearTitle.place(x=80, y=180, anchor=CENTER)

    #YearSelectionBox
    global YearSelection
    YearSelection = ttk.Combobox(window, state="readonly",width=4,values=["2023","2024","2025","2026","2027","2028","2029","2030"])
    YearSelection.pack()
    YearSelection.place(x=75, y=200, anchor=CENTER)
    YearSelection.current(0)

    #MonthTitle
    MonthTitle = tk.Label(window,width=3, state="normal", text="月份", font=("normal", 10), compound="center")
    MonthTitle.place(x=125, y=180, anchor=CENTER)

    #MonthSelectionBox
    global MonthSelection
    MonthSelection = ttk.Combobox(window, state="readonly", width=2,values=["01", "02", "03", "04", "05", "06", "07", "08","09","10","11","12"])
    MonthSelection.pack()
    MonthSelection.place(x=125, y=200, anchor=CENTER)
    MonthSelection.current(0)

    #DateTitle
    DateTitle = tk.Label(window,width=3, state="normal", text="日期", font=("normal", 10), compound="center")
    DateTitle.place(x=170, y=180, anchor=CENTER)

    #DateSelectionBox
    global DateSelection
    DateSelection = ttk.Combobox(window, state="readonly", width=2, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"])
    DateSelection.pack()
    DateSelection.place(x=170, y=200, anchor=CENTER)
    DateSelection.current(10)

    #HourTitle
    HourTitle = tk.Label(window,width=3, state="normal", text="小時", font=("normal", 10), compound="center")
    HourTitle.place(x=225, y=180, anchor=CENTER)

    #HourSelectionBox
    global HourSelection
    HourSelection = ttk.Combobox(window, state="readonly", width=2,values=["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13","14", "15", "16", "17", "18", "19", "20", "21", "22", "23"])
    HourSelection.pack()
    HourSelection.place(x=225, y=200, anchor=CENTER)
    HourSelection.current(12)

    #MinutesTitle
    MinutesTitle = tk.Label(window,width=3, state="normal", text="分", font=("normal", 10), compound="center")
    MinutesTitle.place(x=270, y=180, anchor=CENTER)

    #MinutesSelectionBox
    global MinutesSelection
    MinutesSelection = ttk.Combobox(window, state="readonly", width=2,
                                 values=["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13",
                                         "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59"])
    MinutesSelection.pack()
    MinutesSelection.place(x=270, y=200, anchor=CENTER)
    MinutesSelection.current(30)

    # SecondTitle
    SecondTitle = tk.Label(window,width=3, state="normal", text="秒", font=("normal", 10), compound="center")
    SecondTitle.place(x=315, y=180, anchor=CENTER)

    #SecondSelectionBox
    global SecondSelection
    SecondSelection = ttk.Combobox(window, state="readonly", width=2,
                                    values=["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
                                            "12", "13",
                                            "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
                                            "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
                                            "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                                            "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"])
    SecondSelection.pack()
    SecondSelection.place(x=315, y=200, anchor=CENTER)
    SecondSelection.current(0)
    return
def Execution():
    global driver
    try:
        Account(Account_Login_Record)
        Password(Password_Login_Record)
        ConfirmNumber()
        if TimeMode_Set=="3":
            driver.find_element("xpath", "//*[@id=\"btnLogin\"]").click()  # 時間到了會自動幫你按登入
            Selection_Main()
        else:
            TimeSet = YearSelection.get()+"-"+MonthSelection.get()+"-"+DateSelection.get()+" "+HourSelection.get()+":"+MinutesSelection.get()+":"+SecondSelection.get()#str(int(SecondSelection.get())+1)
            TimeCheck(TimeSet)
            Selection_Main()
    except:
        pass
    return
def Selection_Main():
    for i in range(len(AddToList_Action)):
        if AddToList_Action[i]=="Add":
            AddCourse(AddToList_OpenCourse[i])
        elif AddToList_Action[i]=="Remove":
            RemoveCourse(AddToList_OpenCourse[i])
        else:
            pass

#Login information
#StudentID
def Account(Account_Number):
    global driver
    try:
        account = driver.find_element("xpath","//*[@id=\"txtStuNo\"]")
        account.clear()
        account.send_keys(Account_Number)#學號
    except:
        print("系統尚未開放")
    return
#StudentPassword
def Password(Password_Value):
    global driver
    try:
        password = driver.find_element("xpath","//*[@id=\"txtPSWD\"]")
        password.clear()
        password.send_keys(Password_Value)#密碼
    except:
        print("系統尚未開放")
    return
def ConfirmNumber():
    global driver
    #ConfirmNumber
    #try:
    ConfirmNumber = driver.find_element("xpath","//*[@id=\"txtCONFM\"]")
    ConfirmNumber.clear()
    try:
        if Language_Set=="1":
            driver.execute_script(ChineseScript)
        else:
            driver.execute_script(EnglishScript)
    except:
        ConfirmNumber.send_keys("")
    return

def TimeCheck(TIME_SET):
    global driver
    #Check the time
    #格式'2023-01-11 12:29:59'
    #確認加選時間，但拜託格式不要改，空格不要刪除
    try:
        localtime = time.localtime()
        global result
        result = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
        year_check = result[0]+result[1]+result[2]+result[3]
        month_check = result[5]+result[6]
        date_check = result[8]+result[9]
        hour_check = result[11]+result[12]
        minutes_check = result[14]+result[15]
        seconds_check = result[17]+result[18]
        RandomNumber = random.randrange(11)
        current = datetime.datetime(int(year_check),int(month_check),int(date_check),int(hour_check),int(minutes_check),int(seconds_check))
        selection_time_set = datetime.datetime(int(YearSelection.get()),int(MonthSelection.get()),int(DateSelection.get()),int(HourSelection.get()),int(MinutesSelection.get()),int(SecondSelection.get())+RandomNumber)

        #print(current<selection_time_set)
        while current<=selection_time_set:
            localtime = time.localtime()
            result = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            year_check = result[0] + result[1] + result[2] + result[3]
            month_check = result[5] + result[6]
            date_check = result[8] + result[9]
            hour_check = result[11] + result[12]
            minutes_check = result[14] + result[15]
            seconds_check = result[17] + result[18]
            current = datetime.datetime(int(year_check), int(month_check), int(date_check), int(hour_check),int(minutes_check), int(seconds_check))
            print(result)
            time.sleep(1)
            driver.refresh()
            Account(Account_Login_Record)
            Password(Password_Login_Record)
            ConfirmNumber()

        #Login
        driver.find_element("xpath", "//*[@id=\"btnLogin\"]").click()  # 時間到了會自動幫你按登入
        print("LoginTime: "+result)
    except:
        driver.find_element("xpath", "//*[@id=\"btnLogin\"]").click()  # 時間到了會自動幫你按登入
        print("已經嘗試登入")
    return

def RemoveCourse(OpenCode):
    global driver
    #Remove
    #要刪除的課程
    try:
        Remove_Number = driver.find_element("xpath","//*[@id=\"txtCosEleSeq\"]")
        Remove_Number.clear()
        Remove_Number.send_keys(OpenCode) #""不要刪掉
        driver.find_element("xpath","//*[@id=\"btnDel\"]").click()
    except:
        #messagebox.showinfo("提示","系統尚未開放，請耐心等學校開放")
        print("系統尚未開放，退選失敗")
    return
def AddCourse(OpenCode):
    global driver
    #Add
    RandomNumber = random.randrange(3)
    time.sleep(RandomNumber)
    #要加的課程
    try:
        Add_Number = driver.find_element("xpath","//*[@id=\"txtCosEleSeq\"]")
        Add_Number.clear()
        Add_Number.send_keys(OpenCode) #""不要刪掉
        driver.find_element("xpath","//*[@id=\"btnAdd\"]").click()
    except:
        #messagebox.showinfo("提示", "系統尚未開放，請耐心等學校開放")
        try:
            driver.find_element("xpath", "//*[@id=\"btnReLogin\"]").click()  # 按下重新登入
            Account(Account_Login_Record)
            Password(Password_Login_Record)
            ConfirmNumber()
            driver.find_element("xpath", "//*[@id=\"btnLogin\"]").click()  #按下登入
        except:
            pass
    return

def ShowCurrentTable():
    global driver
    #Show the all Class that you have selected
    driver.find_element("xpath","//*[@id=\"btnEleCos\"]").click()
#============================================================================================
#main function
#messagebox.showinfo("提示",working_dir)
if __name__ == '__main__':
    OpenChrome()
    build_GUI()