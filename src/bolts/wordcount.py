from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extensions



class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()

        #unicode schenanigans
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

        # connect to the generic database
        self.conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")
        # does the Tcount database exist?
        cur = self.conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datname LIKE (%s);",("tcount",))
        results = cur.fetchall()
        self.conn.commit()

        print("hello world")
        #Create the Database
        try:
            # first check if database exists
            if len(results) == 0:
                print("I am here")
                # CREATE DATABASE can't run inside a transaction
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur.execute("CREATE DATABASE tcount")
                cur.close()
                self.conn.close()
            else:
                print("Database tcount exists already")
        except:
            print("Could not create tcount")

        #Connecting to Tcount
        self.conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")

        #Check if the Table exists already
        cur = self.conn.cursor()
        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)",
                    ('tweetwordcount',))
        table_exists = cur.fetchone()[0]
        if not(table_exists):
            #Create a Table
            #The first step is to create a cursor.
            cur.execute("CREATE TABLE tweetwordcount \
                (word TEXT PRIMARY KEY     NOT NULL, \
                count INT     NOT NULL);")
            self.conn.commit()
        else:
            print("Table tweetwordcount exists")

    def process(self, tup):
        word = tup.values[0]

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        cur = self.conn.cursor()
        cur.execute("UPDATE tweetwordcount SET count=%s WHERE word=%s", (self.counts[word],word))
        print("update rows {0:d}".format(cur.rowcount))
        if cur.rowcount == 0:
            #Insert
            cur.execute("INSERT INTO tweetwordcount (word,count) VALUES (%s, 1)",(word,));
        self.conn.commit()

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
