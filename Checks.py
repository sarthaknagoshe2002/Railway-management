# This Module has the Functions that Verify the Requirements of the Project

# Importing Required Modules
import mysql.connector as con
from mysql.connector.errors import ProgrammingError, Error
from zmq import NULL
import InsertData as Insert
from tkinter import *
from tkinter import messagebox
import ctypes

# Functions

def register():
    global pwd
    pwd=Tk()
    pwd.title('SIGN UP')
    user32=ctypes.windll.user32
    sz_x=user32.GetSystemMetrics(0)
    sz_y=user32.GetSystemMetrics(1)
    pwd_x=210
    pwd_y=170
    ad_x=int((sz_x-pwd_x)/2)
    ad_y=int((sz_y-pwd_y)/2)
    size=str(pwd_x)+'x'+str(pwd_y)+'+'+str(ad_x)+'+'+str(ad_y)
    pwd.geometry(size)
    global frmr
    frmr = Frame(pwd)
    frmr.pack()
    un=Label(frmr,text='Username')
    un.pack()
    une=Entry(frmr)
    une.pack()
    p=Label(frmr,text='Password')
    p.pack()
    pe=Entry(frmr,show='*')
    pe.pack()
    c=Label(frmr,text=' Confirm Password')
    c.pack()
    ce=Entry(frmr,show='*')
    ce.pack()
    bl=Label(frmr)
    bl.pack()
    btn=Button(frmr,text='REGISTER',command=lambda a1=une,a2=pe, a3=ce:exeregister(a1,a2,a3))
    btn.pack()
    pwd.mainloop()

def exeregister(username,password,confirm):
    username=str(username.get())
    password=str(password.get())
    confirm = str(confirm.get())
    mn = con.connect(host="localhost", user='root',
                     database="railway", password='Sarthak@123')
    cur = mn.cursor()
    if password==confirm:
        cur.execute("INSERT INTO password VALUES('{}','{}')".format(username,password))
        mn.commit()
        frmr.destroy()
        pwd.destroy()
    else:
        messagebox.showerror('ERROR','password doesn\'t match')
        frmr.destroy()
        pwd.destroy()
        register()

def CheckDatabase():
    """
    CheckDatabase() -> Checks if the Database required Exists or not

    Parameters -> None
    """

    print("Checking Database Requirements..")

    db = con.connect(host="localhost", user='root',
                     database="", password='Sarthak@123')
    cur = db.cursor()
    result = None

    try:
        cur.execute("use railway;")
    except ProgrammingError:
        print("Database does not Exist!")
        result = False
    else:
        result = True

    if result is True:
        print("Database exists!")
    else:
        print("Creating Database with the Required Tables..")
        print("Please be Patient!")
        cur.execute("create database railway;")
        cur.execute("use railway;")
        CreateTables()
        register()
        print('registered')
        print("Database and Tables Created!")

    cur.close()
    db.close()


def CreateTables():
    """
    CreateTables() -> Creates all the Required Tables

    Parameters -> None
    """

    db = con.connect(host="localhost", user='root',
                     database="railway", password='Sarthak@123')
    cur = db.cursor()

    cur.execute(
        "create table train_info (Train_No varchar(10) NOT NULL, Station_Code varchar(20) NOT NULL, Station_Name varchar(30) NOT NULL, Arrival_Time varchar(20) NOT NULL, Departure_Time varchar(20) NOT NULL, Distance varchar(10) NOT NULL, Source_Station_Code varchar(20) NOT NULL, Source_Station_Name varchar(70) NOT NULL, Destination_Station_Code varchar(20) NOT NULL, Destination_Station_Name varchar(60) NOT NULL);")

    cur.execute("create table bookings (Train_No int NOT NULL, Passenger_Name varchar(30) NOT NULL, Mobile_No varchar(10) NOT NULL, Passenger_Adhaar varchar(12) NOT NULL, Date_Of_Booking varchar(20) NOT NULL, Booking_ID int NOT NULL, Class varchar(20) NOT NULL);")
    cur.execute("create table password(username varchar(30) NOT NULL, Password varchar(30) NOT NULL);")
    Insert.InsertDataTrain()


    cur.close()
    db.close()


def CheckConnection():
    """
    CheckConnection() -> Tests the Connection with the Mysql Server

    Parameter -> None
    """

    try:
        print("Checking the Connection to the MySQL Server..")
        connection = con.connect(host='localhost',
                                 database='',
                                 user='root',
                                 password='Sarthak@123')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server Version", db_Info)

    except Error:

        print("Error connecting to MySQL Server, Make sure the MySQL Server is running and then try again!")
        print("Exiting!")
        return False

    else:
        return True
