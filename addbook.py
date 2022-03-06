from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import sqlite3

con=sqlite3.connect('../library.db')
# con=sqlite3.connect('library.db')
cur=con.cursor()


class AddBook(Toplevel):
    def save_file(self):
        path=filedialog.askdirectory()
        self.ent_link.delete(0, 'end')
        self.ent_link.insert(0, path)
        print(type(path))
    def click_name(self,*args):
        self.ent_name.delete(0, 'end')
    def click_author(self,*args):
        self.ent_author.delete(0, 'end')
    def click_page(self,*args):
        self.ent_page.delete(0, 'end')
    def click_language(self,*args):
        self.ent_language.delete(0, 'end')
    def click_link(self,*args):
        self.ent_link.delete(0, 'end')

    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False,False)

        #######################Frames#######################

        #Top Frame
        self.topFrame= Frame(self,height=150,bg='white')
        self.topFrame.pack(fill=X)
        #Bottom Frame
        self.bottomFrame= Frame(self,height=600,bg='#fcc324')
        self.bottomFrame.pack(fill=X)
        #heading, image
        self.top_image= PhotoImage(file='../icons/addbook.png')
        # self.top_image= PhotoImage(file='icons/addbook.png')
        top_image_lbl=Label(self.topFrame,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=10)
        heading=Label(self.topFrame, text='  Add Book ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

        ###########################################Entries and Labels########################3

        #name
        self.lbl_name=Label(self.bottomFrame,text='Name :',font='arial 15 bold',fg='white',bg='#fcc324')
        self.lbl_name.place(x=40,y=40)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.insert(0,'Please enter a book name')
        self.ent_name.bind("<Button-1>", self.click_name)
        self.ent_name.place(x=185,y=45)
        # author
        self.lbl_author = Label(self.bottomFrame, text='Author :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_author.insert(0, 'Please enter an author name')
        self.ent_author.bind("<Button-1>", self.click_author)
        self.ent_author.place(x=185, y=85)
        # page
        self.lbl_page = Label(self.bottomFrame, text='Page :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_page.place(x=40, y=120)
        self.ent_page = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_page.insert(0, 'Please enter number of pages')
        self.ent_page.bind("<Button-1>", self.click_page)
        self.ent_page.place(x=185, y=125)
        # language
        self.lbl_language = Label(self.bottomFrame, text='Language :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_language.place(x=40, y=160)
        self.ent_language = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_language.insert(0, 'Please enter book language')
        self.ent_language.bind("<Button-1>", self.click_language)
        self.ent_language.place(x=185, y=165)
        #link
        self.lbl_link = Label(self.bottomFrame, text='Link to folder :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_link.place(x=40, y=200)
        self.ent_link = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_link.insert(0, 'Please enter a link to this book')
        # self.ent_link.bind("<Button-1>", self.click_link)
        self.ent_link.place(x=185, y=200)
        self.ent_select = Button(self.bottomFrame, text='Select Folder', command=self.save_file)
        self.ent_select.place(x=385, y=200)
        #Button
        button=Button(self.bottomFrame,text='Add Book',command=self.addBook)
        button.place(x=305,y=245)



    def addBook(self):
        name = self.ent_name.get()
        author=self.ent_author.get()
        page= self.ent_page.get()
        language=self.ent_language.get()
        link=self.ent_link.get()

        if (name and author and page and language !=""):
            try:
                query="INSERT INTO 'books' (book_name,book_author,book_page,book_language, book_link) VALUES(?,?,?,?,?)"
                cur.execute(query,(name,author,page,language,link))
                con.commit()
                messagebox.showinfo("Success","Successfully added to database",icon='info')

            except:
                messagebox.showerror("Error","Cant add to database",icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')
        self.click_name()
        self.click_author()
        self.click_page()
        self.click_language()
        self.click_link()
        # main.Main.doubleClick_update()