# 3005pr

First install psycopg2 python library using pip

### In one terminal tab run (this will be the interface you will interact with):
  python3.8 bookstore.py
 
### In another run:
  python3.8 track.py 

This periodically updates shipment tracking statuses. By running track.py, you will input the number of seconds it will take to update a shipment's status
If you chose 5, for example, it will take 5 seconds for the status 'Order Recieved' to convert to 'Shipped', and so on. 

However, the main program will be bookstore.py. Just have track.py open in another tab while you use the application.

Another note, password for admin is admin.
