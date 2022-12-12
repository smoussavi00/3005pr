SELECT price,amount FROM book,purchase WHERE book.isbn = purchase.book_id AND user_id = 'admin';

SELECT price,pubcut,amount FROM book,purchase WHERE book.isbn = purchase.book_id AND NOT user_id = 'admin';

SELECT sum(price*amount*0.01*(100-pubcut)), genre FROM book, genre, purchase WHERE book.isbn = genre.book_id AND book.isbn = purchase.book_id AND NOT purchase.user_id = 'admin' GROUP BY genre

SELECT sum(price*amount*0.01*(100-pubcut)), author FROM book, author, purchase WHERE book.isbn = author.book_id AND book.isbn = purchase.book_id AND NOT purchase.user_id = 'admin' GROUP BY author

SELECT * FROM publisher;

SELECT * FROM client WHERE username = 'firstusr';

INSERT INTO client VALUES('secondusr','passwrd5','123 Main Street','Ottawa','Ontario','R2M 4T4');

SELECT * FROM client where username='firstusr' AND passwd='pass';

SELECT * FROM purchase WHERE user_id = 'firstusr';

INSERT INTO purchase VALUES('firstusr','1238-0921-3849',TO_DATE('2022/12/14', 'YYYY/MM/DD'),'Order Received','123 Lane, Ottawa, Ontario, 1238jk','17491837498, 32/12',1)

UPDATE book SET stock = stock - 1 WHERE isbn = '1238-0921-3849';

UPDATE book SET stock = 15 WHERE isbn = '1238-0921-3849';

INSERT INTO purchase VALUES('admin','1238-0921-3849',TO_DATE('2022/12/14', 'YYYY/MM/DD'),'Stocking Up','Online Bookstore Shipping','Online Bookstore Billing',12)

SELECT book.pub, book.pages, book.price, book.stock, STRING_AGG(genre.genre, ', ') AS genres FROM book, genre WHERE genre.book_id = book.isbn AND isbn = '1238-0921-3849' GROUP BY book.pub, book.pages, book.price, book.stock;

DELETE FROM phone WHERE pub ='3804 Publishing';

DELETE FROM publisher WHERE pub_name ='3804 Publishing';

DELETE FROM book where pub ='3804 Publishing';

DELETE FROM author WHERE book_id ='1238-0921-3849';

DELETE FROM genre WHERE book_id ='1238-0921-3849';

DELETE FROM book WHERE isbn ='1238-0921-3849';

SELECT * FROM publisher where lower(pub_name) LIKE '%3804%'

SELECT * FROM

(SELECT * FROM book WHERE isbn = 'Graph' 
UNION 
SELECT * FROM book WHERE lower(title) LIKE '%Graph%'
UNION
SELECT title,isbn,pub,pages,price,pubcut,stock FROM book,genre WHERE book.isbn = genre.book_id AND (lower(genre) LIKE '%Graph%')
UNION
SELECT title,isbn,pub,pages,price,pubcut,stock FROM book,author WHERE book.isbn = author.book_id AND (lower(author) LIKE '%Graph%') AS subq

INNER JOIN author ON subq.isbn = author.book_id;

SELECT * FROM publisher WHERE pub_name = '3804 Publishing';

INSERT INTO publisher VALUES ('2402 Publishing','2402 Stack Lane','2402pub@mail.com','12841-12803-959','Ontario','Ottawa');

INSERT INTO phone VALUES ('2402 Publishing','519-007-0952');

SELECT * FROM book WHERE isbn = '87837-4891-19';

SELECT * FROM publisher WHERE pub_name = '2402 Publishing';

INSERT INTO book VALUES ('Open Data Structures','87837-4891-19','2402 Publishing',100,19.99,5.00,20);

INSERT INTO purchase VALUES('admin','87837-4891-19',TO_DATE('2022/12/14', 'YYYY/MM/DD'),'Stocking Up','Online Bookstore Shipping','Online Bookstore Billing',20);

INSERT INTO author VALUES ('87837-4891-19','Algo Man');

INSERT INTO genre VALUES ('87837-4891-19','Data Structures');

UPDATE purchase SET status = 'Delivered' WHERE status = 'Out For Delivery';
UPDATE purchase SET status = 'Out For Delivery' WHERE status = 'Shipped';
UPDATE purchase SET status = 'Shipped' WHERE status = 'Order Received';