import mysql.connector as sql

conn = sql.connect(host='localhost', user='root', password='dpsbn')
cur = conn.cursor()

password = [(1, 'qwerty'),
            (2, 'asdfghjkl'),
            (3, 'zxcvbnm'),
            (4, 'Bloodbank'),
            (5, 'Dyuthi'),
            (6, '1234567890'),
            (7, 'Ashwini'),
            (8, 'Arpitha'),
            (9, 'wqefrgtf'),
            (10, '1234r5t'),
            (11, 'Angie'),
            (12, 'wefcwef'),
            (13, '3e2rf4v'),
            (14, 'vebvaeb'),
            (15, 'wertvfa'),
            (16, 'apple'),
            (17, 'banana'),
            (18, 'carrot'),
            (19, 'dates'),
            (20, 'fruit')]

recs = [(1, 'Dyuthi Ramesh', '18', 'dyuthi.ramesh@gmail.com', '1234567890', 'AB+', 'F'),
        (2, 'Ashwini Ravindra Battu', '18', 'ashwinirbattu@gmail.com', '1234598760', 'A+', 'F'),
        (3, 'Arpitha Shivaswaroopa', '18', 'arpitha.shiva@outlook.com', '7896541230', 'O+', 'F'),
        (4, 'Selena Gomez', '29', 'selgomez@gmail.com', '9586543285', 'AB+', 'F'),
        (5, 'Frederic Chopin', '45', 'fredc@gmail.com', '6435148871', 'B+', 'M'),
        (6, 'Leonardo DiCaprio', '36', 'leodc@gmail.com', '1414803661', 'O+', 'M'),
        (7, 'Ludwig Van Beethoven', '55', 'beethoven@gmail.com', '8710637329', 'AB-', 'M'),
        (8, 'Jane Austen', '25', 'janeaus@gmail.com', '1000335726', 'A-', 'F'),
        (9, 'Arnold Schwarzanegger', '48', 'arnoldsch@gmail.com', '2448762536', 'B-', 'M'),
        (10, 'JK Rowling', '52', 'jkrowling@gmail.com', '4493139246', 'O-', 'F'),
        (11, 'Emma Watson', '31', 'emmawatson@gmail.com', '7659394129', 'AB+', 'F'),
        (12, 'Tom Cruise', '60', 'tomcruisemi@gmail.com', '6885525061', 'A-', 'M'),
        (13, 'Daniel Craig', '56', 'dancraig@gmail.com', '5045743753', 'AB-', 'M'),
        (14, 'Agatha Christie', '18', 'agathachristie@gmail.com', '4649848627', 'B+', 'F'),
        (15, 'Arthur Conan Doyle', '20', 'acdauthor@gmail.com', '8749789355', 'A+', 'M'),
        (16, 'Michael Phelps', '36', 'micphelp@gmail.com', '9807654321', 'A+', 'M'),
        (17, 'Charlotte Bronte', '63', 'charbroncb@gmail.com', '7586543285', 'A+', 'F'),
        (18, 'Jane Goodall', '55', 'janegoodall@gmail.com', '7586543210', 'B+', 'F'),
        (19, 'Roald Dahl', '64', 'rddalh@gmail.com', '9786054321', 'Other', 'M'),
        (20, 'Enid Blyton', '63', 'enidblyton@gmail.com', '9786054321', 'O-', 'M')]

cur.execute("DROP DATABASE BLOODBANKDB;")
cur.execute("CREATE DATABASE BLOODBANKDB;")
cur.execute("USE BLOODBANKDB;")

cur.execute('''CREATE TABLE LOGIN_CREDENTIALS(
DONOR_ID INT AUTO_INCREMENT,
PASSWORD VARCHAR(15),
PRIMARY KEY (DONOR_ID));''')
for j in password:
    cur.execute("INSERT INTO LOGIN_CREDENTIALS(PASSWORD) VALUES ('{}')".format(j[1]))
    conn.commit()
cur.execute("SELECT * FROM LOGIN_CREDENTIALS")
r = cur.fetchall()
print(r)

cur.execute('''CREATE TABLE DONOR_INFO(
            DONOR_ID INT,NAME VARCHAR(50), AGE CHAR(2), EMAIL_ID VARCHAR(50), PHONE_NO VARCHAR(10),BLOOD_GROUP VARCHAR(5), SEX VARCHAR(3),
            FOREIGN KEY(DONOR_ID) REFERENCES LOGIN_CREDENTIALS(DONOR_ID));''')

for i in recs:
    cur.execute('''INSERT INTO DONOR_INFO(DONOR_ID,NAME,AGE,EMAIL_ID,PHONE_NO,BLOOD_GROUP,SEX) 
    VALUES('{}','{}','{}','{}','{}','{}','{}')'''.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
    conn.commit()

cur.execute("SELECT * FROM DONOR_INFO")
s = cur.fetchall()
print(s)

conn.close()