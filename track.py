import psycopg2
import threading

#Connects you to bookstore database server
#This file updates tracking statuses

def connection():
    conn = psycopg2.connect(
    database="bookstore", user='postgres', password='postgres', host='bookstore.chbafd9rzbbl.us-east-2.rds.amazonaws.com', port= '5432'
    )
    conn.autocommit = True
    return conn.cursor()

sql = '''
    UPDATE purchase SET status = 'Delivered' WHERE status = 'Out For Delivery';
    UPDATE purchase SET status = 'Out For Delivery' WHERE status = 'Shipped';
    UPDATE purchase SET status = 'Shipped' WHERE status = 'Order Received';
'''

def tracking_update():
    threading.Timer(ans, tracking_update).start()
    cursor = connection()
    cursor.execute(sql)

ans = int(input("Enter delivery time interval (in seconds): "))
tracking_update()

