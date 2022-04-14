import sqlite3
from datetime import datetime
from lcd import LCD

DB_NAME = 'data.db'


class Mailbox:
    def __init__(self):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute('create table if not exists events (timestamp text, event_type text)')
            con.commit()

        self.mail_count = self._get_count()
        self._lcd = LCD()
        self._update_lcd()

    def receive_mail(self):
        self.mail_count += 1
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("insert into events values (datetime('now', 'localtime'), 'new_mail')")
            con.commit()
        self._update_lcd()

    def clear(self):
        self.mail_count = 0
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("insert into events values (datetime('now', 'localtime'), 'clean')")
            con.commit()
        self._update_lcd()

    def history(self):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("select * from events where datetime(timestamp) > datetime('now', '-7 days')")
            return cur.fetchall()

    def _update_lcd(self):
        self._lcd.text('Mails:', 1, align='center')
        self._lcd.text(str(self.mail_count), 2, align='center')

    def _update_lcd(self):
        self._lcd.text('Mails:', 1, align='center')
        self._lcd.text(str(self.mail_count), 2, align='center')

    def _get_count(self):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("select * from events where event_type == 'clean' order by timestamp desc")
            last_clean = cur.fetchone()
            if not last_clean:
                last_clean = (datetime.min.isoformat(), )

            cur.execute("select count(*) from events where datetime(timestamp) > datetime(?)", (last_clean[0] , ))
            return cur.fetchone()[0]