import sqlite3


def initialize():
    con=sqlite3.connect('../library.db')
    # con = sqlite3.connect('library.db')
    cur = con.cursor()

    cur.execute('create table if not exists books(book_id integer primary key autoincrement,'
                                                 'book_name text,'
                                                 'book_author text,'
                                                 'book_page text,'
                                                 'book_language text,'
                                                 'book_link text,'
                                                 'book_status integer default 0)')
