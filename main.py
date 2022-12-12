# This is the Main File that loads all the Other Modules

# Importing Required Modules
import PIL.Image
from PIL import ImageTk
import Checks as Check
from tkinter import *
import mysql.connector
import ctypes
import datetime
import random
from mysql.connector import DataError
from tkinter import messagebox
from time import sleep
import os

w1=Tk()
w1.overrideredirect(1)
user32=ctypes.windll.user32
sz_x=user32.GetSystemMetrics(0)
sz_y=user32.GetSystemMetrics(1)
w1_x=500
w1_y=272
ad_x=int((sz_x-w1_x)/2)
ad_y=int((sz_y-w1_y)/2)
size=str(w1_x)+'x'+str(w1_y)+'+'+str(ad_x)+'+'+str(ad_y)
w1.geometry(size)
ph=ImageTk.PhotoImage(PIL.Image.open('PHOTOS\welcome.png'))
l1=Label(w1,image=ph)
l1.pack()
w1.after(5000, lambda:w1.destroy())
w1.mainloop()
# Defining the per/km Charge of each Class
sleeper_charge = int(1.5)
third_ac_charge = int(2)
second_ac_charge = int(3)
first_ac_charge = int(4)

# Defining Some Initial Variables
current_date = datetime.date.today()

# A Ticket can be Booked 4 Months before the Actual Trip
max_date = current_date + datetime.timedelta(days=120)
# Initial Checks

# Checking the Connection to the MySQL Server
connection_status = Check.CheckConnection()
if connection_status is False:
    quit()
else:
    Check.CheckDatabase()  # Checking for the Requirements of the Project
    t=True

mn = mysql.connector.connect(host="localhost", user='root',password='Sarthak@123', database="railway")
cur = mn.cursor()
os.system("cls")

def back_button(master,slave=None):

        def back():
            master.destroy()
            if slave:
                slave.destroy()
            mainframe()
            
        btn=Button(master,text='BACK',height=1,width=7,command=lambda:back())
        btn.pack()

def CheckFare():
    frm1.destroy()
    global frm7
    frm7=Frame(root)
    frm7.pack()
    back_button(frm7)
    lb1=Label(frm7,text="Search by Entering the Station Code!")
    lb1.pack()
    lb2=Label(frm7,text="FROM")
    lb2.pack()
    start_opt = Entry(frm7)
    start_opt.pack()
    lb3=Label(frm7,text='TO')
    lb3.pack()
    final_opt = Entry(frm7)
    final_opt.pack()
    bt=Button(frm7,text='check fare',height=3,width=25,command=lambda :fare(start_opt,final_opt))
    bt.pack()

def fare(start_opt,final_opt):
    start_opt=str(start_opt.get())
    final_opt=str(final_opt.get())
    txt = "Train_No| Distance| Sleeper| Third AC| Second AC| First AC\n"
    cur.execute(
        'SELECT Train_No, Distance from train_info where Source_Station_Code="{}" AND Destination_Station_Code="{}";'.format(start_opt, final_opt))
    result_fare = cur.fetchall()
    if len(result_fare) == 0:
        messagebox.showerror('ERROR',"No Available Trains!")
    else:
        for x in result_fare:
            txt+=str(x[0])+'\t'+str(x[1])+"\tRs."+ str(int(x[1]) * sleeper_charge)+ "\tRs."+ str(int(x[1]) * third_ac_charge)+ "\tRs."+str(int(x[1]) * second_ac_charge)+ "\tRs."+ str(int(x[1]) * first_ac_charge)+'\n\n'
    txt=txt.replace('(','').replace(')','').replace('\'','')

    frm7.destroy()
    global frm8
    frm8=Frame(root)
    frm8.pack()
    back_button(frm8)
    lb=Label(frm8,text=txt)
    lb.pack()

def exebook(train_no, Name, Mobile, adhaar, Class):
    Time_of_Booking = datetime.datetime.now()
    date = Time_of_Booking.date()
    date = date.strftime("%d-%m-%y")

    # Creating Unique ID for each Booking
    id = random.randint(1, 10000)
    cur.execute("SELECT Booking_ID FROM BOOKINGS")
    result = cur.fetchall()
    Used_ID = []
    for x in result:
        for y in x:
            Used_ID.append(y)
    while True:
        if id in Used_ID:
            id = random.randint(1, 10000)
        else:
            break
    try:
        query = "INSERT INTO bookings values({}, '{}', '{}', '{}', '{}', {}, '{}')".format(
            train_no, Name, Mobile, adhaar, date, id, Class)
        cur.execute(query)
    except DataError:
        messagebox.showerror('ERROR',"Error in Booking!")
    else:
        messagebox.showinfo('SUCCESS',"Successfully Booked!")
        mn.commit()

def book():
    frm1.destroy()
    global frm2
    frm2=Frame(root)
    frm2.pack()
    back_button(frm2)
    lb1=Label(frm2,text='\nTrain number')
    lb1.pack()
    train_no=Entry(frm2)
    train_no.pack()
    lb2=Label(frm2,text='\nEnter your name')
    lb2.pack()
    Name=Entry(frm2)
    Name.pack()
    lb3=Label(frm2,text='\nEnter your phone number')
    lb3.pack()
    Mobile=Entry(frm2)
    Mobile.pack()
    lb4=Label(frm2,text='\nEnter your adhaar number')
    lb4.pack()
    adhaar=Entry(frm2)
    adhaar.pack()
    lb5=Label(frm2,text='\n"Enter class from these options Sleeper", "AC-1", "AC-2", "AC-3"')
    lb5.pack()
    Class=Entry(frm2)
    Class.pack()
    bt=Button(frm2,text='Book',height=3,width=25,command=lambda :cbook(train_no, Name, Mobile, adhaar, Class))
    bt.pack()
    frm2.mainloop()

def cbook(train_no, Name, Mobile, adhaar, Class):
    try:
        train_no=int(train_no.get())
        adhaar=str(adhaar.get())
        Name=str(Name.get())
        Mobile=str(Mobile.get())
        Class=str(Class.get())
        print('here')

        cond=True
        if type(train_no)!=int:
            messagebox.showerror('ERROR','Please enter a valid train number!')
            cond=False
        if len(Name)>30:
            messagebox.showerror('ERROR','name too long!')
            cond=False
        if len(Mobile)<10 or len(Mobile)>10 or Mobile==0000000000:
            messagebox.showerror('ERROR','Please enter a valid Mobile number!')
            cond=False
        if len(adhaar)!=12:
            messagebox.showerror('ERROR','Please enter a valid Adhaar number!')
            cond=False
        if Class not in ["Sleeper", "AC-1", "AC-2", "AC-3"]:
            messagebox.showerror('ERROR','Please enter a valid class!')
            cond=False

    except Exception as e:
        print(e)
        messagebox.showerror('ERROR',e)
    global frm2
    frm2.destroy()
    if cond:
        exebook(train_no, Name, Mobile, adhaar, Class)
        mainframe()
    else:
        book()

def ShowBookings():
    frm1.destroy()
    global frm3
    frm3=Frame(root)
    frm3.pack()
    back_button(frm3)
    lb=Label(frm3,text="\nEnter Your 10 Digit Mobile Number")
    lb.pack()
    number=Entry(frm3)
    number.pack()
    bt=Button(frm3,text='show',height=3,width=25,command=lambda :show(number))
    bt.pack()
    frm3.mainloop()

def show(number):
    number=number.get()
    cur.execute('SELECT * FROM bookings where Mobile_No="{}"'.format(number))
    result = cur.fetchall()
    txt=""
    if len(result) == 0:
        txt="No Records Found!"
    else:
        booking_no = 1
        txt='Booking No |  Train No | passanger |   Mobile  |  Adhaar number |  Time Of Booking |  Booking ID |  Class\n\n'
        for x in result:
            txt+='\t  '+str(booking_no)+'\t  ' + str(x[0])+'\t'+str(x[1])+'\t   '+str(x[2])+'\t'+str(x[3])+'\t'+str(x[4])+'\t\t'+str(x[5])+'\t'+str(x[6])+'\t'
            booking_no += 1
    txt=txt.replace('(','').replace(')','').replace('\'','')+ "\n\n"
    frm3.destroy()
    global frm4
    frm4=Frame(root)
    frm4.pack()
    lb=Label(frm4,text=txt)
    lb.pack()
    back_button(frm4)
    frm4.mainloop()

def ccancel(unique_id):
    cur.execute( "DELETE FROM bookings WHERE Booking_ID={}".format(unique_id))
    messagebox.showinfo('MESSAGE',"Booking cancelled!")
    mn.commit()
    frm6.destroy()
    mainframe()

def cancel(unique_id):
    unique_id=int(unique_id.get())
    cond=True
    if len(str(unique_id)) == 0:
        cond=False
        messagebox.showerror('ERROR',"Invalid ID!")
    elif unique_id < 1:
        cond=False
        messagebox.showerror('ERROR',"ID Out of Range!")
    elif unique_id > 10000:
        cond=False
        messagebox.showerror('ERROR',"ID Out of Range!")
    elif len(str(unique_id)) != 0 and unique_id >= 1 and unique_id <= 10000:
        cur.execute(
            "SELECT * FROM bookings WHERE Booking_ID={}".format(unique_id))
        result = cur.fetchall()
        txt=''
        if len(result) == 0:
            txt="No Records Found!"
        txt+="Train_No, Passenger_Name, Mobile_No, Passenger_Adhaar, Time_Of_Booking, Booking_ID, Class\n\n"
        for x in result:
            txt += str(x).replace('(','').replace(')','').replace('\'','').replace(', ',',         ')+ "\n\n"
    if cond:
        frm5.destroy()
        global frm6
        frm6=Frame(root)
        frm6.pack()
        back_button(frm6)
        lb=Label(frm6,text=txt)
        lb.pack()
        bt=Button(frm6,text='Cancel',height=3,width=25,command=lambda :ccancel(unique_id))
        bt.pack()
    else:
        mainframe()

def CancelBooking():
    frm1.destroy()
    global frm5
    frm5=Frame(root)
    frm5.pack()
    back_button(frm5)
    lb1=Label(frm5,text='Please use the show my bookings option to get Booking ID\n')
    lb1.pack()
    lb2=Label(frm5,text='Enter Unique Booking ID\n')
    lb2.pack()
    id=Entry(frm5)
    id.pack()
    bt=Button(frm5,text='proceed',height=3,width=25,command=lambda :cancel(id))
    bt.pack()

def AvailableTrains():
    frm1.destroy()
    global frm9
    frm9=Frame(root)
    frm9.pack()
    back_button(frm9)
    lb1=Label(frm9,text="Search by Entering the Station Codes!")
    lb1.pack()
    lb2=Label(frm9,text='FROM')
    lb2.pack()
    start_opt = Entry(frm9)
    start_opt.pack()
    lb3=Label(frm9,text='TO')
    lb3.pack()
    final_opt = Entry(frm9)
    final_opt.pack()
    lb4=Label(frm9,text='DATE(YYYY-MM-DD)')
    lb4.pack()
    date = Entry(frm9)
    date.pack()
    bt=Button(frm9,text='Search',height=3,width=25,command=lambda :search(date,start_opt,final_opt))
    bt.pack()

def search(date, start_opt, final_opt):
    start_opt=str(start_opt.get())
    final_opt=str(final_opt.get())
    date = str(date.get())
    date_user = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    frm9.destroy()
    global frm10
    frm10=Frame(root)
    frm10.pack()
    back_button(frm10)
    if date_user < current_date or date_user > max_date:
        messagebox.showerror('ERROR',"Please enter a Valid Date!")
        AvailableTrains()
    else:
        cur.execute(
            'SELECT Train_No, Source_Station_Name, Destination_Station_Name, Arrival_Time, Departure_Time from train_info where Source_Station_Code="{}" AND Destination_Station_Code="{}";'.format(
                start_opt, final_opt))
        result = cur.fetchall()
        txt = "\tTrain No   |   Source Station   |   Destination Station   |   Arrival Time   |   Departure Time\n\n"
        if len(result) == 0:
            lb=Label(frm10,text="No Trains Available!")
            lb.pack()
        else:
            for x in result:
                txt+=x[0]+'\t'+x[1]+'\t'+x[2]+'\t     '+x[3]+'\t     '+x[4]+ "\n"
            lb=Label(frm10,text=txt)
            lb.pack()

################# MAIN CANVAS###############
root = Tk()
root.title('Indian Railways')
user32=ctypes.windll.user32
sz_x=user32.GetSystemMetrics(0)
sz_y=user32.GetSystemMetrics(1)
root_x=650
root_y=650
ad_x=int((sz_x-root_x)/2)
ad_y=int((sz_y-root_y)/2)
size=str(root_x)+'x'+str(root_y)+'+'+str(ad_x)+'+'+str(ad_y)
root.geometry(size)
root.resizable(0,0)
root.withdraw()
################# MAIN CANVAS###############

##############LOGIN CANVAS##################
pwd=Tk()
pwd.title('Log IN')
pw=Frame(pwd)
user32=ctypes.windll.user32
sz_x=user32.GetSystemMetrics(0)
sz_y=user32.GetSystemMetrics(1)
pwd_x=210
pwd_y=170
ad_x=int((sz_x-pwd_x)/2)
ad_y=int((sz_y-pwd_y)/2)
size=str(pwd_x)+'x'+str(pwd_y)+'+'+str(ad_x)+'+'+str(ad_y)
pwd.geometry(size)
pwd.withdraw()
##############LOGIN CANVAS##################

##############login function################
def login():
    try:
        pwd.deiconify()
    except:pass
    pwd.title('Log IN')
    global frm
    frm = Frame(pwd)
    frm.pack()
    un=Label(frm,text='Username')
    un.pack()
    une=Entry(frm)
    une.pack()
    p=Label(frm,text='Password')
    p.pack()
    pe=Entry(frm,show='*')
    pe.pack()
    bl=Label(frm)
    bl.pack()
    btn=Button(frm,text='LOG IN',command=lambda a1=une,a2=pe:checkpass(a1,a2))
    btn.pack()
    btn=Button(frm,text='SIGN UP',command=lambda :register())
    btn.pack()
    frm.mainloop()

def checkpass(a1,a2):
    a1=a1.get()
    a2=a2.get()
    try:
        cur.execute("SELECT password FROM password WHERE username='{}';".format(a1))
        result = cur.fetchall()
        if result[0][0]==a2:
            root.deiconify()
            pwd.destroy()
            mainframe()
        else:
            messagebox.showerror('ERROR','invalid credentials')
            frm.destroy()
            login()
    except Exception as e:
        messagebox.showerror('ERROR','invalid credentials or {}'.format(e))
        messagebox.showinfo('MESSAGE','try signing up')
        frm.destroy()
        login()
##############login function################
#############register function##############
def register():
    pwd.title('SIGN UP')
    global frmr
    frm.destroy()
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

def exeregister(username,password,confirm):
    username=str(username.get())
    password=str(password.get())
    confirm = str(confirm.get())
    if password==confirm:
        cur.execute("INSERT INTO password VALUES('{}','{}')".format(username,password))
        mn.commit()
        frmr.destroy()
        login()
    else:
        messagebox.showerror('ERROR','password doesn\'t match')
        frmr.destroy()
        register()


def mainframe():
    global frm1
    frm1=Frame(root)
    frm1.pack()
    lb1=Label(frm1,text='\nWELCOME TO INDIAN RAILWAYS:\n\n',font=('Ariel','22'))
    lb1.pack()
    bt1=Button(frm1,text='Book a Train',height=3,width=25,command=lambda :book())
    bt1.pack()
    bt2=Button(frm1,text='Cancel a Booking',height=3,width=25,command=lambda:CancelBooking())
    bt2.pack()
    bt3=Button(frm1,text='Check Fares',height=3,width=25,command=lambda:CheckFare())
    bt3.pack()
    bt4=Button(frm1,text='Show My Bookings',height=3,width=25,command=lambda:ShowBookings())
    bt4.pack()
    bt5=Button(frm1,text='Show Available Trains',height=3,width=25,command=lambda:AvailableTrains())
    bt5.pack()
    bt6=Button(frm1,text='Exit',height=3,width=25,command=lambda:quit())
    bt6.pack()
    frm1.mainloop()

login()