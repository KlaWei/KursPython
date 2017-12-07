import os
import sqlite3
import datetime
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk

current_dir_path = os.path.dirname(os.path.abspath(__file__))


class ContactsDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY,
                                                fname TEXT, lname TEXT, mail TEXT,
                                                pnumber INTEGER, last_view TEXT)
        ''')
        self.conn.commit()

    def add_to_database(self, fname, lname, mail, num):
        self.cursor.execute('''INSERT INTO contacts(fname, lname, mail, pnumber, last_view)
                               VALUES(?,?,?,?,?)''', (fname, lname, mail, num, '-'))
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_from_database(self, entry_id):
        self.conn.execute('''DELETE FROM contacts WHERE id = ?''', (entry_id,))
        self.conn.commit()

    def update_database_entry(self, entry_id, fname, lname, mail, num):
        self.cursor.execute('''UPDATE contacts SET fname = ?, lname = ?, mail = ?,
                               pnumber = ? WHERE id = ? ''', (fname, lname, mail, num, entry_id))
        self.conn.commit()

    def update_last_viewed(self, entry_id):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute('''UPDATE contacts SET last_view = ? WHERE id = ?''', (now, entry_id))
        self.conn.commit()
        return now

    def get_entries(self):
        self.cursor.execute('''SELECT * FROM contacts''')
        return self.cursor.fetchall()

    def search_for_name(self, name):
        self.cursor.execute('''SELECT * FROM contacts WHERE fname = ? OR lname = ?''', (name, name))
        return self.cursor.fetchall()


class Contacts(Gtk.Window):
    def __init__(self):
        self.editEntry = False
        self.editId = -1
        self.editIter = None
        self.database = ContactsDatabase()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(current_dir_path, 'contacts.glade'))
        self.window = self.builder.get_object('window1')
        self.treeview = self.builder.get_object('treeview1')
        self.liststore = self.builder.get_object('liststore1')
        self.window.connect("destroy", Gtk.main_quit)

        rows = self.database.get_entries()
        self.append_to_liststore_from_database(rows)

        self.entryFirstName = self.builder.get_object('first_name_entry')
        self.entryLastName = self.builder.get_object('last_name_entry')
        self.entryNumber = self.builder.get_object('phone_entry')
        self.entryMail = self.builder.get_object('email_entry')

        self.builder.connect_signals(self)
        self.window.show_all()

    def append_to_liststore_from_database(self, rows):
        if rows is not None:
            for row in rows:
                self.liststore.append([row[1], row[3], row[0], row[4], row[5], row[2]])

    def save_button_clicked(self, button):
        fname = self.entryFirstName.get_text()
        lname = self.entryLastName.get_text()
        mail = self.entryMail.get_text()
        number = int(self.entryNumber.get_text())

        if self.editEntry is False:
            entry_id = self.database.add_to_database(fname, lname, mail, number)
            self.liststore.append([fname, mail, entry_id, number, '-', lname])
        else:
            self.database.update_database_entry(self.editId, fname, lname, mail, number)
            self.liststore.set_value(self.editIter, 0, fname)
            self.liststore.set_value(self.editIter, 1, mail)
            self.liststore.set_value(self.editIter, 3, number)
            self.liststore.set_value(self.editIter, 5, lname)

    def clear_entries(self):
        self.editEntry = False
        self.entryFirstName.set_text("")
        self.entryLastName.set_text("")
        self.entryMail.set_text("")
        self.entryNumber.set_text("")

    def clear_button_clicked(self, button):
        self.clear_entries()

    def delete_button_clicked(self, button):
        self.database.delete_from_database(self.editId)
        self.clear_entries()
        self.liststore.clear()
        self.append_to_liststore_from_database(self.database.get_entries())

    def move_info_to_text_entries(self, treeview, path, col):
        self.editEntry = True
        selection = treeview.get_selection()
        (model, t_iter) = selection.get_selected()
        self.editId = model.get_value(t_iter, 2)
        self.editIter = t_iter
        now = self.database.update_last_viewed(self.editId)
        self.liststore.set_value(t_iter, 4, now)

        self.entryFirstName.set_text(model.get_value(t_iter, 0))
        self.entryLastName.set_text(model.get_value(t_iter, 5))
        self.entryMail.set_text(model.get_value(t_iter, 1))
        self.entryNumber.set_text(str(model.get_value(t_iter, 3)))

    def search_changed(self, search_entry):
        names = self.database.search_for_name(search_entry.get_text())
        self.liststore.clear()
        self.append_to_liststore_from_database(names)
        if search_entry.get_text() == "":
            self.append_to_liststore_from_database(self.database.get_entries())


if __name__ == "__main__":
    app = Contacts()
    Gtk.main()
