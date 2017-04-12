#Sample code snippets for working with psycopg


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


# does the database exist?
cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database WHERE datname LIKE (%s);",("tcount",))
results = cur.fetchall()
conn.commit()

#Create the Database

try:
    # first check if database exists
    if len(results) == 0:
        print("I am here")
        # CREATE DATABASE can't run inside a transaction
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("CREATE DATABASE tcount")
        cur.close()
        conn.close()
    else:
        print("Database tcount exists already")
except:
    print "Could not create tcount"

#Connecting to tcount

conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
print(conn.encoding)


#Check if the Table exists already
cur = conn.cursor()
cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)",
            ('tweetwordcount',))
table_exists = cur.fetchone()[0]
if not(table_exists):
    #Create a Table
    #The first step is to create a cursor.
    cur.execute("CREATE TABLE tweetwordcount \
        (word TEXT PRIMARY KEY     NOT NULL, \
        count INT     NOT NULL);")
    conn.commit()
else:
    print("Table tweetwordcount exists")

#Running sample SQL statements
#Inserting/Selecting/Updating

#Rather than executing a whole query at once, it is better to set up a cursor that encapsulates the query,
#and then read the query result a few rows at a time. One reason for doing this is
#to avoid memory overrun when the result contains a large number of rows.

cur = conn.cursor()
cur.execute("UPDATE tweetwordcount SET count=count+1 WHERE word=%s", ('test',))
print("update rows {0:d}".format(cur.rowcount))
if cur.rowcount == 0:
    #Insert
    cur.execute("INSERT INTO tweetwordcount (word,count) VALUES ('test', 1)");
conn.commit()

#Using variables to update
# uCount=5
# uWord="test"
# cur.execute("UPDATE tweetwordcount SET count=%s WHERE word=%s", (uCount, uWord))
# conn.commit()

#Select
cur.execute("SELECT word, count from tweetwordcount")
records = cur.fetchall()
for rec in records:
   print "word = ", rec[0]
   print "count = ", rec[1], "\n"
conn.commit()

conn.close()
