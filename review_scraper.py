# LIBRARIES
import requests
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import sqlite3
from pandas import DataFrame
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# FUNCTIONS

def clear():
    url.set("")
    tablename.set("")


def FetchData():
    
    global totalrecords
    global count
    global link
    global table 
    
    link = str(url.get())
    table = str(tablename.get())
    
    # WEB SCRAPING
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    try:
    
        driver = webdriver.Chrome('C:\Drivers\chromedriver.exe', chrome_options = options)
        driver.get(link)
        content = driver.page_source

        review_list = []
        star_list = []
        title_list = []
        soup = BeautifulSoup(content,"html.parser")

        for ids in soup.find_all("div",{"class":"reviewText"}):
            reviewText = ids.text.replace("\n","").strip().encode('ascii', 'ignore').decode('ascii')
            review_list.append(reviewText)

        for title in soup.find_all("a",{"class":"review-title"}):
            reviewTitle = title.text.replace("\n","").strip().encode('ascii', 'ignore').decode('ascii')
            title_list.append(reviewTitle)

        for rating in soup.select('div.reviews-content a[title]'):
            reviewRating = rating.get('title')
            star_list.append(reviewRating)
    
        totalrecords = len(star_list)
    
        conn = sqlite3.connect('AMAZON_REVIEWS')
        curs = conn.cursor()
        try:
            curs.execute("CREATE TABLE "+table+" (Rating char(50), Review_Title char(1000), Review_Content char(999999999))")
            for i in range(0,totalrecords):
                curs.execute('insert into '+table+' values(?,?,?)',(star_list[i],title_list[i],review_list[i]))
            l1.configure(text = table+" added successfully")
        
        except:
            l1.configure(text = "Table Name Error")
        
    except:
        l1.configure(text = "Invalid URL")
    
    conn.commit()
    conn.close()
    
    
def db_init():
    
    global count
    global prod
    global tot_rec
    
    prod = str(product.get())
    
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    
    try:
        curs.execute("select * from "+prod)
        rec = curs.fetchall()
        tot_rec = len(rec)
        conn.commit()
        conn.close()
        if(tot_rec > 0):
            count = 1
        firstRec()
    
        l2.configure(text=str(count)+"/"+str(tot_rec))
    
    except:
        messagebox.showerror("SQL ERROR", "Table Not Found")
    
    

def firstRec():
    global count
    global prod
    global tot_rec
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+prod)
    first = curs.fetchone()
    stars.set(first[0])
    title.set(first[1])
    text.set(first[2])
    conn.close()
    count = 1
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def preRec():
    global count
    global tot_rec
    global prod
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return        
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    ins_rec=curs.execute('select * from '+prod)
    if(count==1):
        first = curs.fetchone()
    else:
        for i in range(1,count):
            first = curs.fetchone()
        count -= 1
    stars.set(first[0])
    title.set(first[1])
    text.set(first[2])
    conn.close()
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def nextRec():
    global count
    global tot_rec
    global prod
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    ins_rec=curs.execute('select * from '+prod)
    if(tot_rec == 1):
        first = curs.fetchone()
    else:
        for i in range(1,count+1):
            first = curs.fetchone()
    if(count<tot_rec):
        first = curs.fetchone()
    else:
        count -= 1
    stars.set(first[0])
    title.set(first[1])
    text.set(first[2])
    conn.close()
    count += 1
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def lastRec():
    global count
    global prod
    global tot_rec
    if(count==0):
        messagebox.showerror("SQL ERROR", "No Records...")
        return
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    ins_rec = curs.execute("select * from "+prod)
    if(tot_rec == 1):
        first = curs.fetchone()
    else:
        count = 0
        for i in range(1,tot_rec+1):
            first = curs.fetchone()
            count += 1
    stars.set(first[0])
    title.set(first[1])
    text.set(first[2])
    conn.close()
    l2.configure(text=str(count)+"/"+str(tot_rec))
    
def addRec():
    global tot_rec
    global count
    global prod
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('insert into '+prod+' values (?, ?, ?)', (stars.get(), title.get(), text.get(),))
        conn.commit()
        conn.close()
        tot_rec += 1
        count = tot_rec
        l2.configure(text=str(count)+"/"+str(tot_rec))
        
    except:
        messagebox.showerror("SQL ERROR", "Value Error")
    
def delRec():
    global count
    global tot_rec
    global prod
    if(count==0):
        messagebox.showerror("DELETE ERROR", "No Records...")
        return
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('delete from '+prod+' where Review_Title=?',(title.get(),))
        conn.commit()
        conn.close()
        count = 1
        tot_rec -= 1
        firstRec()
    
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")
    
def updateRec():
    global prod
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('update '+prod+' set Rating=?,Review_Title=?,Review_Content=? where Review_Title=?',(stars.get(),title.get(),text.get(),title.get()))
        conn.commit()
        conn.close()
        count = 1
        firstRec()
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")

def searchRec():
    global prod
    conn = sqlite3.connect('AMAZON_REVIEWS')
    curs = conn.cursor()
    try:
        ins_rec=curs.execute('select * from '+prod+' where Review_Title like ?',(title.get(),))
        first = curs.fetchone()
        stars.set(first[0])
        title.set(first[1])
        text.set(first[2])
        conn.close()
    except:
        messagebox.showerror("SQL ERROR", "Value Not Found")
    
def plot():
    
    tabname = str(name.get())
    
    figure1 = plt.Figure(figsize=(5,4),dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, tab3)
    bar1.get_tk_widget().grid(row=4,column=2)
    
    conn = sqlite3.connect('AMAZON_REVIEWS')
    try:
        df = pd.read_sql_query("select * from "+tabname, conn)
        conn.commit()
        conn.close()
        df['Rating'].value_counts().plot(kind='bar', ax = ax1)
        ax1.set_title('Ratings Vs Frequency')
        ax1.tick_params(axis='x', rotation=10)
        
    except:
        messagebox.showerror("SQL ERROR", "Table Not Found")

warnings.filterwarnings("ignore")
    
# GUI
    

win = tk.Tk()
win.title("Review Analysis System")
win.geometry("700x600")

tab_parent = ttk.Notebook(win)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text="Add a New Product")
tab_parent.add(tab2, text="Modify Products")
tab_parent.add(tab3, text="Product Analysis")


# TAB 1

l1a = Label(tab1,text = "Add a New Product",font=("cambria",15,"bold"), width=50, anchor="c")
l1a.grid(row=1,column=1,columnspan=4)

urllabel = Label(tab1,text="Enter URL: ",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
urllabel.grid(row=2,column=1)
url = StringVar()
urlentry = Entry(tab1,textvariable = url,width = 45,font=("cambria",15,"bold"),bg="orange")
urlentry.grid(row=2,column=2,columnspan=3)

tablelabel = Label(tab1,text="Product:",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
tablelabel.grid(row=3,column=1)
tablename = StringVar()
tableentry = Entry(tab1,textvariable = tablename,width = 45,font=("cambria",15,"bold"),bg="orange")
tableentry.grid(row=3,column=2,columnspan=3)

b1 = Button(tab1, width="8", text="Enter", command=FetchData,font=("cambria",15,"bold"))
b1.grid(row=4, column=2,padx=10,pady=10)

b10 = Button(tab1, width="8", text="Clear", command=clear,font=("cambria",15,"bold"))
b10.grid(row=4, column=3,padx=10,pady=10)

l1 = Label(tab1,font=("cambria",15,"bold"), width=50, anchor="c")
l1.grid(row=5,column=1,columnspan=4)




# TAB 2

l1b = Label(tab2,text = "Read/Update Product Reviews",font=("cambria",15,"bold"), width=50, anchor="c")
l1b.grid(row=1,column=1,columnspan=4)

tablelabel = Label(tab2,text="Product:",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
tablelabel.grid(row=2,column=1)
product = StringVar()
tableentry = Entry(tab2,textvariable = product,width = 45,font=("cambria",15,"bold"),bg="orange")
tableentry.grid(row=2,column=2,columnspan=3)

b1 = Button(tab2, width="8", text="Modify", command=db_init,font=("cambria",15,"bold"))
b1.grid(row=3, column=3,padx=10,pady=10)


starlabel = Label(tab2,text="Rating: ",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
starlabel.grid(row=5,column=1)
stars = StringVar()
starentry = Entry(tab2,textvariable = stars,width = 45,font=("cambria",15,"bold"),bg="orange")
starentry.grid(row=5,column=2,columnspan=3)

titlelabel = Label(tab2,text="Title: ",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
titlelabel.grid(row=6,column=1)
title = StringVar()
titleentry = Entry(tab2,textvariable = title,width = 45,font=("cambria",15,"bold"),bg="orange")
titleentry.grid(row=6,column=2,columnspan=3)

textlabel = Label(tab2,text="Review: ",font=("cambria",15,"bold"),bg="grey",fg="black", width=8, anchor="w")
textlabel.grid(row=7,column=1)
text = StringVar()
textentry = Entry(tab2,textvariable = text,width = 45,font=("cambria",15,"bold"),bg="orange")
textentry.grid(row=7,column=2,columnspan=3)

l2 = Label(tab2,font=("cambria",15,"bold"),bg="white", width=8, anchor="c")
l2.grid(row=8,column=1,columnspan=4)

b2 = Button(tab2, width="8", text="|<", command=firstRec,font=("cambria",15,"bold"))
b2.grid(row=9, column=1,padx=10,pady=10)
b3 = Button(tab2, width="8", text="<", command=preRec,font=("cambria",15,"bold"))
b3.grid(row=9, column=2)
b4 = Button(tab2, width="8", text=">", command=nextRec,font=("cambria",15,"bold"))
b4.grid(row=9, column=3)
b5 = Button(tab2, width="8", text=">|", command=lastRec,font=("cambria",15,"bold"))
b5.grid(row=9, column=4)

b6 = Button(tab2,width="10",text="ADD", command=addRec,font=("cambria",15,"bold"))
b6.grid(row=10,column=1,padx=10,pady=10)
b7 = Button(tab2,width="10",text="DELETE", command=delRec,font=("cambria",15,"bold"))
b7.grid(row=10,column=2)
b8 = Button(tab2,width="10",text="UPDATE", command=updateRec,font=("cambria",15,"bold"))
b8.grid(row=10,column=3)
b9 = Button(tab2,width="15",text="SEARCH TITLE", command=searchRec,font=("cambria",15,"bold"))
b9.grid(row=10,column=4)



# TAB 3

l1c = Label(tab3,text = "Product Analysis",font=("cambria",15,"bold"), width=50, anchor="c")
l1c.grid(row=1,column=1,columnspan=4)

namelabel = Label(tab3,text="Product:",font=("cambria",18,"bold"),bg="grey",fg="black", width=8, anchor="w")
namelabel.grid(row=2,column=1)
name = StringVar()
nameentry = Entry(tab3,textvariable = name,width = 45,font=("cambria",15,"bold"),bg="orange")
nameentry.grid(row=2,column=2,columnspan=3)

b10 = Button(tab3, width="8", text="Analyze", command=plot,font=("cambria",15,"bold"))
b10.grid(row=3, column=2,padx=10,pady=10)






tab_parent.pack(expand=1, fill='both')
win.mainloop()