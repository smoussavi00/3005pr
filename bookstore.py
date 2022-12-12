import psycopg2
import getpass
import datetime
from datetime import date


#ADMIN password = admin
#Sample user: firstusr (username) pass (password)

#prints out instructions
def instructions(who):
    if who == 0:
        print("\n\tYou are now accessing the bookstore as the owner")
        print("\n\tUse 'add-book' to add a book")
        print("\tUse 'add-pub' to add a publisher to the record")
        print("\tUse 'exit' to leave the bookstore program")
        print("\tUse 'delete-book' to remove a book")
        print("\tUse 'reports' to show reports and stats")
        print("\tUse 'delete-pub' to remove a publisher from record\n")
        print("\tUse 'help' any time to see these instructions again\n")
    else:
        print("\n\tYou are now accessing the bookstore as a user")
        print("\n\tUse 'register' or 'login' at any time")
        print("\tUse 'exit' to leave the bookstore program")
        print("\tUse 'search' to search for a book")
        print("\tUse 'track' to see all orders and their status")
        print("\tUse 'cart' to see cart and checkout\n")
        print("\tUse 'help' any time to see these instructions again\n")    

#displays report to administrator
def reports(cursor):
    sql = "SELECT price,amount FROM book,purchase WHERE book.isbn = purchase.book_id AND user_id = 'admin'"
    cursor.execute(sql)
    results = cursor.fetchall()

    expenditures = 0
    for stock in results:
        expenditures += float(stock[0])*0.5*stock[1]

    sql = "SELECT price,pubcut,amount FROM book,purchase WHERE book.isbn = purchase.book_id AND NOT user_id = 'admin'"
    cursor.execute(sql)
    results = cursor.fetchall()

    sales = 0
    for purch in results:
        sales += float(purch[0])*0.01*(100-float(purch[1]))*purch[2]

    print()
    print("\tSales: {0}, Expenditures {1}, Profit {2}".format(sales, expenditures,sales-expenditures))
    print()

    sql = "SELECT sum(price*amount*0.01*(100-pubcut)), genre FROM book, genre, purchase WHERE book.isbn = genre.book_id AND book.isbn = purchase.book_id AND NOT purchase.user_id = 'admin' GROUP BY genre"
    cursor.execute(sql)
    results = cursor.fetchall()

    for genre in results:
        print("\tSales in {0}: {1}".format(genre[1], genre[0]))
    print()

    sql = "SELECT sum(price*amount*0.01*(100-pubcut)), author FROM book, author, purchase WHERE book.isbn = author.book_id AND book.isbn = purchase.book_id AND NOT purchase.user_id = 'admin' GROUP BY author"
    cursor.execute(sql)
    results = cursor.fetchall()

    for auth in results:
        print("\tSales by {0}: {1}".format(auth[1], auth[0]))
    print()
        
 #checks if there are publishers in record
def has_pub(cursor):
    sql = "SELECT * FROM publisher"
    cursor.execute(sql)
    return len(cursor.fetchall() ) > 0

#search the basket for a specified book
def list_search(basket,isbn):
    for book in basket:
        if book[0] == isbn:
            return basket.index(book)      
    return -1

#Creates a new account to login into the system
def register(cursor,user):
    #Ask the user for a username and password
    print("\n\tAccount registry - provide details")
    print("\tIn brackets - max character size, do not exceed\n")

    while True:
        usr = input("Username (20): ")
        pswd = getpass.getpass('Password (20):')
        add = input("Address (20): ")
        c = input("City (20): ")
        pr = input("Province, full name (30): ")
        post = input("Postal Code (10): ")

        #Check for empty fields
        has_exceeded = not(len(usr)<21 and len(pswd)<21 and len(add)<21 and len(c)<21 and len(pr)<31 and len(post)<31)
        has_empty = not(len(usr)>0 and len(pswd)>0 and len(add)>0 and len(c)>0 and len(pr)>0 and len(post)>0)
        
        if(has_empty ):
            print("\n\tYou have left empty responses in 1 or more fields")
        if(has_exceeded):
            print("\n\tYou have exceeded character limits in 1 or more fields")
        if(has_empty or has_exceeded):
            retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
            if(retry != 'Y'):
                print()
                break
        else:
            #Check if username already exists
            sql = "SELECT * FROM client WHERE username = '{0}'".format(usr)
            cursor.execute(sql)
            if (len(cursor.fetchall()) == 1 or usr == 'guest' or usr == 'admin'):
                ans = input("\nUsername already exists. Retry (R), exit (other): ")
                print()
                if(ans != 'R'):
                    break
            else:
                #We are good to go
                sql = "INSERT INTO client VALUES('{0}','{1}','{2}','{3}','{4}','{5}');".format(usr,pswd,add,c,pr,post)
                cursor.execute(sql)
                print("\n\tRegistered - You are now logged in\n")
                return usr
    return user

#login for users
def login(cursor, user):
    print("\n\t Login form - enter correct details")
    while True:
        print()
        usr = input("Enter your username: ")
        pswd = getpass.getpass('Enter your password: ')

        sql = "SELECT * FROM client where username='{0}' AND passwd='{1}';".format(usr,pswd)
        cursor.execute(sql)

        if(len(cursor.fetchall()) == 0 or usr == 'guest' or usr == 'admin'):
            ans = input("\nInvalid credentials - retry (R) or exit (other): ")
            if(ans != 'R'):
                print()
                return user       
        else:
            print("\n\tYou are logged in as {0}\n".format(usr))
            return usr

#Sees the location of orders
def track(cursor,user):
    print("\n\tTracking Orders\n")
    sql = "SELECT * FROM purchase WHERE user_id = '{0}';".format(user)
    cursor.execute(sql)
    orders = cursor.fetchall()

    if(len(orders) == 0):
        print("\tNo orders to show")
    else:
        for ordr in orders:
            print("\tTracking Id: {0}, Status: {1}, Date: {2}, Count: {3}".format(ordr[7],ordr[3],ordr[2],ordr[6]))

    print()

#Checks the items in the cart
def cart(cursor,user,basket,c_date):
    if(len(basket) == 0):
        print("\n\tYour cart is empty\n")
    else:
        print("\n\tCart Items - {0}\n".format(len(basket)))
        sum = 0
        for i in range(len(basket)):
            print("\t{0} - {1} (Count: {2})".format(i+1,basket[i][1], basket[i][4]))
            sum += basket[i][4]*basket[i][2]
        print("\n\tSubtotal: ${0}\n".format(sum))
        act = input("Would you like to checkout? Yes (Y), remove item (Use #), exit (other): ")
        print()
        if(act == 'Y'):
            a = input("Address (20): ")
            c = input("City (20): ")
            pr = input("Province, full name (30): ")
            post = input("Postal Code (10): ")
            shipping = ", ".join([a,c,pr,post])

            cn = input("\nCard Number: ")
            exp = input("Expiry - MM/YY: ")
            print()
            billing = ", ".join([cn,exp])

            for book in basket:
                sql = "INSERT INTO purchase VALUES('{0}','{1}',TO_DATE('{2}', 'YYYY/MM/DD'),'Order Received','{3}','{4}',{5})".format(user,book[0],"/".join(str(c_date).split("-")),shipping,billing,book[4])
                cursor.execute(sql)
                if book[3] > 4:
                    sql = "UPDATE book SET stock = stock - {0} WHERE isbn = '{1}'".format(book[4],book[0])
                    cursor.execute(sql)
                else:
                    sql = "UPDATE book SET stock = 15 WHERE isbn = '{0}'".format(book[0])
                    cursor.execute(sql)
                    sql = "INSERT INTO purchase VALUES('admin','{0}',TO_DATE('{1}', 'YYYY/MM/DD'),'Stocking Up','Online Bookstore Shipping','Online Bookstore Billing',{2})".format(book[0],"/".join(str(c_date).split("-")),15-book[4])
                    cursor.execute(sql)
            
            print("\tOrder placed! Use 'track' to see status of orders.\n")

        elif act.isnumeric():
            num = int(input("Copies to remove: "))
            if num > basket[int(act)-1][4]:
                print("\n\tInvalid entry\n")
                return
            
            elif num == basket[int(act)-1]:
                basket.remove(basket[int(act)-1])           
            else:
                basket[int(act)-1][4] -=1 

            print("\n\tItem removed")
            

#Searches for a book to buy
def search_buy(cursor,user,basket):
    print("\n\tBook search - make selection to see details")
    while True:
        to_checkout = search_book(cursor)
        if(to_checkout != None):
            sql = "SELECT book.pub, book.pages, book.price, book.stock, STRING_AGG(genre.genre, ', ') AS genres FROM book, genre WHERE genre.book_id = book.isbn AND isbn = '{0}' GROUP BY book.pub, book.pages, book.price, book.stock;".format(to_checkout[0])
            cursor.execute(sql)
            results = cursor.fetchall()

            #Now we display the book details
            print("\n\tTitle: {0}".format(to_checkout[1][0]))
            print("\tIBSN: {0}".format(to_checkout[0]))
            print("\tAuthor(s): {0}".format(", ".join(to_checkout[1][1])))
            print("\tPublisher: {0}".format(results[0][0]))
            print("\tPages: {0}".format(results[0][1]))
            print("\tPrice: ${0}".format(results[0][2]))
            print("\tStock: {0}".format(results[0][3]))
            print("\tGenre(s): {0}".format(results[0][4]))

            print()
            

            ans = input("Add {0} to Cart? Yes (Y), find another (F), exit (other): ".format(to_checkout[1][0]))
            
            if(ans == 'Y'):
                if(user == 'guest'):
                    print("\n\tPlease login or register to add to cart\n")
                    break
                elif(results[0][3] == 0):

                    ans_2 = input("\nInsufficient stock - Look for another book (B), exit (other): ")
                    if(ans_2 != 'B'):
                        break
                else: 

                    if(list_search(basket,to_checkout[0]) == -1):
                        ans_3 = int(input("\nHow many copies?: "))
                        print()

                        if ans_3 <= results[0][3]:
                            basket.append([to_checkout[0],to_checkout[1][0],results[0][2],results[0][3],ans_3])
                            ans_2 = input("\nAdded to cart - Look for another book (B), exit (other): ")
                            print()
                            if(ans_2 != 'B'):
                                break
                        else:
                            ans_7 = input("Not enough in stock - Look for another book (B), exit (other): ")
                            print()
                            if(ans_7 != 'B'):
                                break
                    else:
                        book = list_search(basket,to_checkout[0])
                        ans_5 = int(input("\nHow many more copies? You have {0}: ".format(basket[book][4])))
                        if ans_5 + basket[book][4] > results[0][3]:
                            ans_6 = input("Not enough in stock - Look for another book (B), exit (other): ")
                            print()
                            if(ans_6 != 'B'):
                                break
                        else: 
                            basket[book][4] += ans_5
                            break

            elif(ans != 'F'):
                break
        else:
            break

#Deletes a publisher
def delete_pub(cursor):
    print("\n\tDelete publisher - search for the publisher\n")
    print("\n\tNote: All associated books will be removed")

    while True:
        to_delete = search_pub(cursor)
        if(to_delete != None):
            print()
            ans = input("Delete {0}? Yes (Y), find another (F), exit (other): ".format(to_delete[0]))
            if(ans == 'Y'):
                    sql = '''
                        
                        DELETE FROM phone WHERE pub ='{0}';
                        DELETE FROM publisher WHERE pub_name ='{0}';
                        DELETE FROM book where pub ='{0}';

                    '''.format(to_delete[0])
                    cursor.execute(sql)
                    print("\n\Publisher deleted\n")
                    break
            elif(ans != 'F'):
                break
        else:
            print()
            ans_2 = input("Nothing to delete, try again? Yes (Y), exit (other): ")
            if(ans_2 != 'Y'):
                print()
                break

#Deletes a book
def delete_book(cursor):
    print("\n\tDelete book - first search for the book\n")
    while True:
        to_delete = search_book(cursor)
        if(to_delete != None):
            print()
            ans = input("Delete {0}? Yes (Y), find another (F), exit (other): ".format(to_delete[1][0]))
            if(ans == 'Y'):
                    sql = '''
                        
                        DELETE FROM author WHERE book_id ='{0}';
                        DElETE FROM genre WHERE book_id ='{0}';
                        DELETE FROM book WHERE isbn ='{0}';
                    
                    '''.format(to_delete[0])
                    cursor.execute(sql)
                    print("\n\tBook deleted\n")
                    break
            elif(ans != 'F'):
                break
        else:
            print()
            ans_2 = input("Nothing to delete, try again? Yes (Y), exit (other): ")
            if(ans_2 != 'Y'):
                print()
                break

#Deletes a publisher
def search_pub(cursor):
    while True:
        search = input("\nSearch publisher (no advanced search for this): ")
        sql = "SELECT * FROM publisher where lower(pub_name) LIKE '%{0}%'".format(search.lower())
        cursor.execute(sql)
        results = cursor.fetchall()

        print()
        for i in range(len(results)):
            print("\t{0} - {1}".format(i+1,results[i][0]))

        print()
        if(len(results) != 0):
            ans = input("Make a selection (Use #) or retry (R) or exit (other): ")
            if(ans == 'R'):
                pass
            elif(ans.isnumeric()):
                if(int(ans) <= len(results) and int(ans) > 0):
                    return results[int(ans)-1]
                else:
                    ans_2 = input("\nInvalid entry. Retry (R) or exit (other)")
                    if(ans_2 != 'R'):
                        break
            else:
                break
        else:
            ans = input("No results - retry (R) or exit (other): ")
            print()
            if(ans != 'R'):
                break

#General search for a book
def search_book(cursor):
    while True:
        search = input("\nSearch with ISBN, title, author, or genre: ")

        split = search.split()
        advanced_genre = "lower(genre) LIKE '%{0}%'".format(split[0].lower()) 
        advanced_author = "lower(author) LIKE '%{0}%'".format(split[0].lower()) 
        advanced_title = "lower(title) LIKE '%{0}%'".format(split[0].lower()) 
        for i in range(len(split)-1):
            advanced_genre = advanced_genre + " OR lower(genre) LIKE '%{0}%'".format(split[i+1].lower())
            advanced_author = advanced_author + " OR lower(author) LIKE '%{0}%'".format(split[i+1].lower())
            advanced_title = advanced_title + " OR lower(title) LIKE '%{0}%'".format(split[i+1].lower())

        sql = '''

        SELECT * FROM

        (SELECT * FROM book WHERE isbn = '{0}' 
        UNION 
        SELECT * FROM book WHERE {1}
        UNION
        SELECT title,isbn,pub,pages,price,pubcut,stock FROM book,genre WHERE book.isbn = genre.book_id AND ({2})
        UNION
        SELECT title,isbn,pub,pages,price,pubcut,stock FROM book,author WHERE book.isbn = author.book_id AND ({3})) AS subq
        
        INNER JOIN author ON subq.isbn = author.book_id;
        
        '''.format(search,advanced_title,advanced_genre,advanced_author)

        cursor.execute(sql)
        results = cursor.fetchall()

        display={}
        for i in range(len(results)):
            if(display.get(results[i][1]) != None):
                display[results[i][1]][1].append(results[i][8])
            else:
                display[results[i][1]] = [results[i][0],[results[i][8]]]
        display = list(display.items())


        print()
        for i in range(len(display)):
            print("\t{0} - {1} by {2}".format(i+1,display[i][1][0],", ".join(display[i][1][1])))
        print()

        if(len(results) != 0):
            ans = input("Make a selection (Use #) or retry (R) or exit (other): ")
            if(ans == 'R'):
                pass
            elif(ans.isnumeric()):
                if(int(ans) <= len(display) and int(ans) > 0):
                    return display[int(ans)-1]
                else:
                    ans_2 = input("\nInvalid entry. Retry (R) or exit (other)")
                    if(ans_2 != 'R'):
                        break
            else:
                break
        else:
            ans = input("\nNo results - retry (R) or exit (other): ")
            if(ans != 'R'):
                break

#Adds a publisher to record
def add_publisher(cursor):
    print("\n\tAdd publisher - please complete all fields")
    print("\tIn brackets - max character size, do not exceed\n")

    while True:
        ph = []
        n = input("Name (20): ")
        a = input("Address (20): ")
        c = input("City (20): ")
        pr = input("Province, full name (30): ")
        e = input("Email (30): ")
        b = input("Bank Account (30): ")

        num_phone = int(input("\nHow many phone numbers?: "))
        print("\n\tEnter phones numbers - no duplicates\n")

        all_phones_good = True
        all_phones_great = True

        for _ in range(num_phone):
            phone = input("Phone (16): ")
            all_phones_good = all_phones_good and len(phone) > 0 
            all_phones_great = all_phones_great and len(phone) < 17
            ph.append(phone)

        has_empty = not(len(n)>0 and len(a)>0 and len(c)>0 and len(pr)>0 and len(e)>0 and len(b)>0 and all_phones_good)
        has_exceeded = not(len(n)<21 and len(a)<21 and len(c)<21 and len(pr)<31 and len(e)<31 and len(b)<31 and all_phones_great)
        phones_duplicate = len(ph) != len(set(ph))

        if(has_empty or num_phone < 1):
            print("\n\tYou have left empty responses in 1 or more fields")
        if(has_exceeded):
            print("\n\tYou have exceeded character limits in 1 or more fields")
        if(phones_duplicate):
            print("\n\tYou have included duplicate phone numbers")
        if(has_exceeded or has_empty or phones_duplicate or num_phone < 1):
            retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
            if(retry != 'Y'):
                break
        else:
            #check if publisher already exists
            sql = "SELECT * FROM publisher WHERE pub_name = '{0}'".format(n)
            cursor.execute(sql)
            if(len(cursor.fetchall()) == 1):
                print("\nPublisher already exists with that given name.")
                retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
                if(retry != 'Y'):
                    break
            else:
                sql = "INSERT INTO publisher VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(n,a,e,b,pr,c)
                cursor.execute(sql)
                for i in range(num_phone):
                    sql = "INSERT INTO phone VALUES ('{0}','{1}')".format(n,ph[i])
                    cursor.execute(sql)
                print("\nAdded new publisher\n")
                break

#Adds a book to record    
def add_book(cursor,cdate):
    print("\n\tAdd book - please complete all fields")
    print("\tIn brackets - max character size, do not exceed\n")

    while True:
        auth = []
        gen = []
        t = input("Title (50): ")
        isbn = input("ISBN (20): ")
        pb = input("Publisher (20): ")
        pg = input("Page Num (Integer): ")
        pc = input("Price (Enter float, 2 decimal points): ")
        pbcut = input("Publishers % Cut (Enter float, 2 decimal points, 0.00 - 100.00): ")
        st = input("Stock (Integer): ")


        num_auth = int(input("\nHow many authors?: "))
        print("\n\tEnter author names - no duplicates\n")

        all_auth_good = True
        all_auth_great = True

        for _ in range(num_auth):
            author = input("Author (20): ")
            all_auth_good = all_auth_good and len(author) > 0 
            all_auth_great = all_auth_great and len(author) < 21
            auth.append(author)
        
        num_gen = int(input("\nHow many genres?: "))
        print("\n\tEnter genre tags - no duplicates\n")

        all_gen_good = True
        all_gen_great = True

        for _ in range(num_gen):
            genre = input("Genre (10): ")
            all_gen_good = all_gen_good and len(genre) > 0 
            all_gen_great = all_gen_great and len(genre) < 11
            gen.append(genre)

        has_empty = not(len(t)>0 and len(isbn)>0 and len(pb)>0 and all_auth_good and all_gen_good)
        has_exceeded = not(len(t)<51 and len(isbn)<21 and len(pb)<21 and all_auth_great and all_gen_great)
        auth_gen_duplicate = len(auth) != len(set(auth)) or len(gen) != len(set(gen))

        if(has_empty or num_gen < 1 or num_auth < 1):
            print("\n\tYou have left empty responses in 1 or more fields")
        if(has_exceeded):
            print("\n\tYou have exceeded character limits in 1 or more fields")
        if(auth_gen_duplicate):
            print("\n\tYou have included duplicate authors or genres")
        if(has_exceeded or has_empty or auth_gen_duplicate or num_gen < 1 or num_auth < 1):
            retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
            if(retry != 'Y'):
                break
        else:
            #check if ISBN already exists
            sql = "SELECT * FROM book WHERE isbn = '{0}'".format(isbn)
            cursor.execute(sql)

            if(len(cursor.fetchall()) == 1):
                print("\nBook already exists with given ISBN")
                retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
                if(retry != 'Y'):
                    break
            else:
                #check is publisher actually exists, if not reject the book addition
                sql = "SELECT * FROM publisher WHERE pub_name = '{0}'".format(pb)
                cursor.execute(sql)

                if(len(cursor.fetchall()) == 0):
                    print("\nPublisher does not exist")
                    retry = input("\nWould you like to retry? Yes (Y), No (Other) : ")
                    if(retry != 'Y'):
                        break
                else:
                    sql = "INSERT INTO book VALUES ('{0}','{1}','{2}',{3},{4},{5},{6})".format(t,isbn,pb,pg,pc,pbcut,st)
                    cursor.execute(sql)

                    sql = "INSERT INTO purchase VALUES('admin','{0}',TO_DATE('{1}', 'YYYY/MM/DD'),'Stocking Up','Online Bookstore Shipping','Online Bookstore Billing',{2})".format(isbn,"/".join(str(cdate).split("-")),st)
                    cursor.execute(sql)
                    
                    for i in range(num_auth):
                        sql = "INSERT INTO author VALUES ('{0}','{1}')".format(isbn,auth[i])
                        cursor.execute(sql)

                    for i in range(num_gen):
                        sql = "INSERT INTO genre VALUES ('{0}','{1}')".format(isbn,gen[i])
                        cursor.execute(sql)                    
                    
                    print("\nAdded new book\n")
                    break
                                
#Main program
current_date = date.today()

#Connection to the database
conn = psycopg2.connect(
   database="bookstore", user='postgres', password='postgres', host='bookstore.chbafd9rzbbl.us-east-2.rds.amazonaws.com', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()

#Main interface
while True:
    print("\nWelcome to Bookstore 3005\n")
    admin_or_user = input("Continue as user (U), admin (A) or exit (other):  ")
    if(admin_or_user == 'A'):
        while True:
            print()
            admin_pass = getpass.getpass('Please enter admin password: ')
            if(admin_pass != 'admin'):
                retry = input("Incorrect - retry (R), continue as user (U) or exit (other): ")
                if(retry == 'R'):
                    pass
                elif(retry == 'U'):
                    admin_or_user = 'U'
                    break
                else:
                    break
            else:
                
                instructions(0)

                while True:
                    cmd = input("[admin] ")
                    if(cmd == 'exit'):
                        break
                    elif(cmd == 'add-pub'):
                        add_publisher(cursor)
                    elif(cmd == 'add-book'):
                        if(not has_pub(cursor)):
                            print("\n\tThere are no publishers on record. Use 'add-pub'\n")
                        else:
                            add_book(cursor,current_date)
                    elif(cmd == 'delete-book'):
                        delete_book(cursor)
                    elif(cmd == 'delete-pub'):
                        delete_pub(cursor)
                    elif(cmd == 'help'):
                        instructions(0)
                    elif(cmd == 'reports'):
                        reports(cursor)
                    else:
                        print("\n\t" + cmd +  " - not recognized\n")
                break

    if(admin_or_user == 'U'):
        user = 'guest'
        instructions(1)
        while True:
            cmd = input("[{0}] ".format(user))
            if(cmd == 'exit'):
                break
            elif(cmd == 'register'):
                bask = []
                user = register(cursor,user)
            elif(cmd == 'help'):
                instructions(1)
            elif(cmd == 'login'):
                bask = []
                user = login(cursor,user)
            elif(cmd == 'search'):
                if(user == 'guest'):
                    search_buy(cursor,user,[])
                else:
                    search_buy(cursor,user,bask)
            elif(cmd == 'cart'):
                if(user == 'guest'):
                    print("\n\tRegister or lLogin to view cart\n")
                else:
                    cart(cursor,user,bask,current_date)
            elif(cmd == 'track'):
                if user == 'guest':
                    print("\n\tRegister or login to see orders\n")
                else:
                    track(cursor,user)
            else:
                print("\n\t" + cmd +  " - not recognized.\n")
    print("\nThank you for visiting Bookstore 3005\n")
    break

conn.close()
