from tkinter import *
from tkinter import ttk
import sqlite3
import os
import addbook,addmember,givebook, database
from tkinter import messagebox

con=sqlite3.connect('../library.db')
# con=sqlite3.connect('library.db')
cur=con.cursor()


class Main(object):
    folder_path=''
    def __init__(self,master):
        self.master = master
        database.initialize()

        def displayStatistics(evt):
            count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
            # count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            # print(count_books)
            self.lbl_book_count.config(text='Total :'+ str(count_books[0][0])+' books in library')
            # self.lbl_member_count.config(text="Total member : "+str(count_members[0][0]))
            self.lbl_taken_count.config(text="Taken books :"+str(taken_books[0][0]))
            displayBooks(self)


        def displayBooks(evt):

            books=cur.execute("SELECT * FROM books").fetchall()
            count=0

            self.list_books.delete(0,END)
            for book in books:
                # print(book)
                self.list_books.insert(count,str(book[0])+ "-" +book[1])
                count +=1
            # self.master.after(100, self.displayBooks)

            def bookInfo(evt):
                global folder_path
                value=str(self.list_books.get(self.list_books.curselection()))
                id=value.split('-')[0]
                book =cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
                book_info=book.fetchall()
                print(book_info)
                self.list_details.delete(0,'end')
                self.list_details.insert(0,"Book Name : "+book_info[0][1])
                self.list_details.insert(1,"Author : "+book_info[0][2])
                self.list_details.insert(2,"Page : "+book_info[0][3])
                self.list_details.insert(3,"Language : "+book_info[0][4])
                self.list_details.insert(4,"Link : "+book_info[0][5])
                if book_info[0][6] == 0:
                    self.list_details.insert(5,"Status : Avaiable")
                else:
                    self.list_details.insert(5,"Status : Not Avaiable")
                folder_path = book_info[0][5]
                if folder_path is not None:
                    self.btn_folder['state'] = 'normal'


            def doubleClick():
                books = cur.execute("SELECT * FROM books").fetchall()
                count = 0

                self.list_books.delete(0, END)
                for book in books:
                    # print(book)
                    self.list_books.insert(count, str(book[0]) + "-" + book[1])
                    count += 1


            self.list_books.bind('<<ListboxSelect>>',bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>',displayStatistics)
            self.tabs.bind('<ButtonRelease-1>',displayBooks)
            self.list_books.bind('<Double-Button-1>',doubleClick)


        def open_folder():
            global folder_path

            folder_path1 = os.path.realpath(folder_path)
            os.startfile(folder_path1)
            # open(f"{folder_path}")

        #frames
        mainFrame=Frame(self.master)
        mainFrame.pack()
        #top frames
        topFrame= Frame(mainFrame,width=1050,height=70,bg='#f8f8f8',padx=20,relief=SUNKEN,borderwidth=2)
        topFrame.pack(side=TOP,fill=X)
        #center frame
        centerFrame = Frame(mainFrame,width=1100,relief=RIDGE,bg='#e0f0f0',height=680)
        centerFrame.pack(side=TOP)
        #Center Left Frame
        centerLeftFrame= Frame(centerFrame,width=750,height=700,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerLeftFrame.pack(side=LEFT)
        #center right frame
        centerRightFrame= Frame(centerFrame,width=650,height=500,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerRightFrame.pack()

        #search bar
        search_bar =LabelFrame(centerRightFrame,width=440,height=75,text='Search Box',bg='#9bc9ff')
        search_bar.pack(fill=BOTH)
        self.lbl_search=Label(search_bar,text='Search :', font='arial 12 bold',bg='#9bc9ff',fg='white')
        self.lbl_search.grid(row=0,column=0,padx=20,pady=10)
        self.ent_search=Entry(search_bar,width=30,bd=10)
        self.ent_search.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.btn_search=Button(search_bar,text='Search',font='arial 12',bg='#fcc324',fg='white',
                               command=self.searchBooks)
        self.btn_search.grid(row=0,column=4,padx=20,pady=10)


        #title and image
        image_bar=Frame(centerRightFrame,width=440,height=350)
        image_bar.pack(fill=BOTH)
        self.title_right=Label(image_bar,text='Welcome to our Library',font='arial 16 bold')
        self.title_right.grid(row=0)
        self.img_library=PhotoImage(file='../icons/library.png')
        # self.img_library = PhotoImage(file='icons/library.png')
        self.lblImg=Label(image_bar,image=self.img_library)
        self.lblImg.grid(row=1)
        self.lblCopy = Label(image_bar, text="Copyright© Sergey Kozyrev. All rights reserved.")
        self.lblCopy.grid(row=1, pady=(340,0),sticky=N)


############################################Tool Bar########################################
        #add book
        self.iconbook=PhotoImage(file='../icons/add_book.png')
        # self.iconbook=PhotoImage(file='icons/add_book.png')
        self.btnbook= Button(topFrame,text='Add Book',image=self.iconbook,compound=LEFT,
                             font='arial 12 bold',command=self.addBook)
        self.btnbook.pack(side=LEFT,padx=10)


######################################Tabs#########################################
            ###############tab1###############################
        self.tabs= ttk.Notebook(centerLeftFrame,width=780,height=660)
        self.tabs.pack()
        # self.tab1_icon=PhotoImage(file='icons/books.png')
        self.tab1_icon=PhotoImage(file='../icons/books.png')
        # self.tab2_icon=PhotoImage(file='icons/members.png')
        self.tab1=ttk.Frame(self.tabs)
        self.tab2=ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='Library Management',image=self.tab1_icon,compound=LEFT)
        # self.tabs.add(self.tab2,text='Statistics',image=self.tab2_icon,compound=LEFT)

        #list books
        self.list_books= Listbox(self.tab1,width=40,height=30,bd=5,font='times 12 bold')
        self.sb=Scrollbar(self.tab1,orient=VERTICAL)
        self.list_books.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        #list details
        self.list_details=Listbox(self.tab1,width=47,height=15,bd=5,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)
        self.btn_folder=Button(self.tab1, text='Open folder', command=open_folder,
                               font='times 12 bold', state='disabled')
        self.btn_folder.grid(row=0, column=1, pady=(340,0),  sticky=N)
        ##########################tab2####################################
        #statistics
        self.lbl_book_count= Label(self.tab2,text="adfafs",pady=20,font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count=Label(self.tab2,text="asdfadsf",pady=20,font='verdana 14 bold')
        self.lbl_member_count.grid(row=1,sticky=W)
        self.lbl_taken_count=Label(self.tab2,text="asdfdafd",pady=20,font='verdana 14 bold')
        self.lbl_taken_count.grid(row=2,sticky=W)

        #functions
        displayBooks(self)
        # displayStatistics(self)

    def doubleClick_update(self):
        books = cur.execute("SELECT * FROM books").fetchall()
        count = 0

        self.list_books.delete(0, END)
        for book in books:
            # print(book)
            self.list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1




    def addBook(self):
        add=addbook.AddBook()

    def addMember(self):
        member=addmember.AddMember()

    def searchBooks(self):
        value = self.ent_search.get()
        search= cur.execute("SELECT * FROM books WHERE book_name LIKE ?",('%'+value+'%',)).fetchall()
        print(search)
        self.list_books.delete(0,END)
        count=0
        for book in search:
            self.list_books.insert(count,str(book[0])+ "-"+book[1])
            count +=1
    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks= cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0,END)

            count=0
            for book in allbooks:
                self.list_books.insert(count,str(book[0]) + "-"+book[1])
                count +=1

        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status =?",(0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books= cur.execute("SELECT * FROM books WHERE book_status =?",(1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])

                count += 1
        self.master.update_idletasks()
        self.master.after(100, self.listBooks)

def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1250x750+350+200")
    root.iconbitmap('../icons/icon.ico')
    # root.iconbitmap('icons/icon.ico')
    root.mainloop()

if __name__ == '__main__':
    main()
