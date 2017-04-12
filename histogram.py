
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
        if len(sys.argv[1:]) != 1:
            print(sys.argv)
            sys.exit('Histogram feature requires 2 numbers as arguments')
        else :
            args = sys.argv[1].split(',')
            if len(args) != 2:
                sys.exit('Histogram feature requires 2 numbers as arguments')
            try:
                k1 = int(args[0])
                k2 = int(args[1])
                cur = conn.cursor()
                cur.execute('''SELECT word, count FROM tweetwordcount \
                             WHERE count >= %s AND count <= %s \
                             ORDER BY count DESC''',(k1,k2))
                records = cur.fetchall()
                for rec in records:
                   print("{0:s}: {1:d}".format(rec[0],rec[1]))
                conn.commit()
                conn.close()
            except ValueError:
                sys.exit("One of the arguments is not a number")
