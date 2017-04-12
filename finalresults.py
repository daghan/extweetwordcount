
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

# Connect to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="pass", host="localhost", port="5432")


# does the database exist?
cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database WHERE datname LIKE (%s);",("tcount",))
results = cur.fetchall()
conn.commit()

if len(results) == 0:
    conn.close()
    sys.exit("Database tcount doesn't exist or can't connect to it")
else:
    conn = psycopg2.connect(database="tcount", user="postgres", password="pass", host="localhost", port="5432")
    #Check if the Table exists already
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)",
                ('tweetwordcount',))
    table_exists = cur.fetchone()[0]
    if not(table_exists):
        conn.close()
        sys.exit('Table tweetwordcount doesn\'t exist!')
    else:
        if len(sys.argv[1:]) == 0:
            cur.execute("SELECT word, count FROM tweetwordcount ORDER BY word ASC")
            records = cur.fetchall()
            for rec in records:
               print "word = ", rec[0]
               print "count = ", rec[1], "\n"
            conn.commit()
        else:
            word = sys.argv[1]
            cur.execute("SELECT count FROM tweetwordcount WHERE word like %s",(word,))
            count = cur.fetchone()[0]
            print("Total number of occurrences of \"{0:s}\": {1:d}".format(word,count))
            conn.commit()
    conn.close()
