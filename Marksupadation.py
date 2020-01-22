from tkinter import *
from tkinter.ttk import *
import pandas as pd
import tkinter.messagebox
import math 
import mysql.connector

def execute():
    global avg
    fia=fria.get()  
    sia=seia.get()
    tia=thia.get()
    if((0<=fia<=30)and(0<=sia<=30)and(0<=tia<=30)):
        avg=(math.ceil((int(fia)+int(sia)+int(tia))/3))
        Label(root,text="Average :").place(x=80,y=263)
        l=Label(root,text=avg,font=('Bold',20))
        l.place(x=135,y=280)
        l.after(4000,lambda:l.destroy())
    else:
        l3=Label(root,text="Marks exceeds total marks(30)")
        l3.place(x=290,y=71)
        l3.after(2000,lambda:l3.destroy())
    assign=assig.get()
    if 0<=assign<=10:
        total=(avg+int(assign))
        Label(root,text="Total :").place(x=259,y=263)
        l2=Label(root,text=total,font=('Bold',20))
        l2.place(x=295,y=279)
        l2.after(4000,lambda:l2.destroy())
    else:
        lb=Label(root,text="*Maximum Assignment Marks is 10",font=('Bold',13))
        lb.place(x=205,y=197)
        lb.after(3000,lambda:lb.destroy())
        
def update(x):
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="test")
    mycursor=mydb.cursor()
    eusn=[]
    enter=usn.get()
    if (len(enter)!=0):
        a=enter.isupper()
        if a is True:
            eusn.append(enter)
        else:
            eusn.append(enter.swapcase())
    else:
        la=Label(root,text="**PLEASE FILL THE USN**",font=('Bold',13))
        la.place(x=290,y=21)
        la.after(3000,lambda:la.destroy())
        
    mycursor.execute('select usn from ia')
    b=[]
    rows =mycursor.fetchall()
    for row in rows:
        a=list(row)
        b.append(a)
    
    fia=fria.get()
    sia=seia.get()
    tia=thia.get()
    if((0<=fia<=30)and(0<=sia<=30)and(0<=tia<=30)):
        avg=(math.ceil((int(fia)+int(sia)+int(tia))/3))
    else:
        l3=Label(root,text="Marks exceeds total marks(30)")
        l3.place(x=290,y=71)
        l3.after(2000,lambda:l3.destroy())
    assign=assig.get()
    if 0<=assign<=10:
        total=(avg+int(assign))
    else:
        lb=Label(root,text="*Maximum Assignment Marks is 10",font=('Bold',13))
        lb.place(x=205,y=197)
        lb.after(3000,lambda:lb.destroy())
    if eusn in b:
        sql='update ia set fia=%s,sia=%s,tia=%s,avg=%s,assign=%s,total=%s,verified ="yes" where usn =%s '
        iputdata=(fia,sia,tia,avg,assign,total,enter)
        mycursor.execute (sql,iputdata)
        mydb.commit()
        e1.delete(0,END)
        fria.set(0)
        seia.set(0)
        thia.set(0)
        assig.set(0)
        x.place_forget()
        
        mycursor.execute('select verified from ia')
        c=[]
        rows=mycursor.fetchall()
        for row in rows:
            tmp=list(row)
            c.append(tmp)
        count=0 
        for i in range(0,(len(c))):
            if(c[i]==['yes']):
                count+=1
        Label(root,text="students' marks updated",font=('Times')).place(x=57,y=375)  
        Label(root,text=count,font=('Bold',19)).place(x=27,y=365)
        if count==(len(b)):
            try:
                df1 = pd.read_sql('SELECT * FROM `ia` ', con=mydb)
                data=df1.rename(columns={'usn':'USN','name':'Name','fia':'1st IA','sia':'2nd IA','tia':'3rd IA','avg':'Average','assign':'Assignment','total':'Total','verified':'Verified'})
                df1.to_excel('IAMarks.xlsx',index=False,startrow=1)
                yesno=tkinter.messagebox.showinfo("All Updates Completed","Please check the Excel sheet for print")
                if yesno=="ok":
                     root.destroy()
            except:
                tkinter.messagebox.showerror("ERROR!!!!","File exists please do delete it")
                
                
    else:
        tkinter.messagebox.showerror("ERROR!!!!","This USN doesn't exisits ")
    
    
    
    

root = Tk()
root.title("Government Engineering college,Devagiri,Haveri-581110")
root.geometry("515x420")

usn= StringVar()
l1=Label(root, text="USN").place(x=10,y=21)
e1 = Entry(root,textvariable=usn,width=20)
e1.place(x=140,y=21)

fria=IntVar()
Label(root, text="FIRST IA").place(x=10,y=70)
e2 = Entry(root,textvariable=fria,width=20)
e2.place(x=140,y=70)


seia=IntVar()
Label(root, text="SECOND IA").place(x=10,y=120)
e3 =Entry(root,textvariable=seia,width=20)
e3.place(x=140,y=120)

thia=IntVar()
Label(root, text="THRID IA").place(x=10,y=169)
e4 = Entry(root,textvariable=thia,width=20)
e4.place(x=140,y=168)

assig=IntVar()
Label(root, text="ASSIGNMENT ").place(x=250,y=225)
e5 = Entry(root,textvariable=assig,width=10)
e5.place(x=330,y=225)

Button(root, text='ENTER',command=execute).place(x=80,y=225)
def select():
    if((var.get())==1):
        b1=Button(root, text='SUBMIT')  
        b1.configure(command=lambda:update(b1))  
        b1.place(x=297,y=365)
        
var=IntVar()
chkex=Checkbutton(root,text='I agree,Marks are satisfacotry and above detailes are filled in my presence',variable=var,command=select)
chkex.place(x=10,y=329)
mainloop()





