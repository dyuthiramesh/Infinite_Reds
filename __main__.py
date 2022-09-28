"""
Class 12 Computer Science Project 2021-22
Authors: Dyuthi Ramesh, Arpitha Shivaswaroopa, Ashwini Ravindra Battu
Class: XII A    School: Delhi Public School Bangalore North
"""

################# BLOOD BANK MANAGEMENT SYSTEM #################

import sys
import mysql.connector as sql

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, Qt

from PIL import Image, ImageDraw, ImageFont
import yagmail

donor_id, name, blood_grp, email, pdf_path = '', '', '', '', ''
var1, var2, var3, var4, var5, var6, = '', '', '', '', '', ''
var7, var8, var9, var10, var11, var12 = '', '', '', '', '', ''


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("UI Screens/welcomescreen.ui", self)
        self.adminlogin.clicked.connect(self.gotoadminlogin)
        self.donorlogin.clicked.connect(self.gotodonorlogin)

    def gotoadminlogin(self):
        adminlogin = AdminLoginScreen()
        widget.addWidget(adminlogin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotodonorlogin(self):
        donorlogin = DonorLoginScreen()
        widget.addWidget(donorlogin)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DonorSignUpScreen(QDialog):
    def __init__(self):
        super(DonorSignUpScreen, self).__init__()
        loadUi("UI Screens/donorsignup.ui", self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)

        conn = sql.connect(host='localhost', user='root', password='dpsbn')
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS BLOODBANKDB;")
        cur.execute("USE BLOODBANKDB;")
        cur.execute('''CREATE TABLE IF NOT EXISTS LOGIN_CREDENTIALS(
        DONOR_ID INT AUTO_INCREMENT,
        PASSWORD VARCHAR(15),
        PRIMARY KEY (DONOR_ID));''')
        cur.execute("SELECT * FROM LOGIN_CREDENTIALS;")
        recs = cur.fetchall()
        global donor_id
        if recs == []:
            donor_id = 1
        else:
            donor_id = (recs[-1][0]) + 1
        self.donorid.setText(str(donor_id))
        conn.close()
        self.createaccount.clicked.connect(self.createaccountfunction)

    def createaccountfunction(self):
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        if len(password) == 0 or len(confirmpassword) == 0:
            self.errormsg.setText("Please input all fields")
        elif len(password) > 15 or len(confirmpassword) > 15:
            self.errormsg.setText("Too long password. Please try again")
        elif password != confirmpassword:
            self.errormsg.setText("Passwords don't match. Please try again.")
        else:
            conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
            cur = conn.cursor()
            cur.execute("INSERT INTO LOGIN_CREDENTIALS(PASSWORD) VALUES ('{}');".format(password))
            conn.commit()
            conn.close()
            DonorSignUpScreen.gotodonorpersonalinfo()

    def gotodonorpersonalinfo():
        personalinfo = DonorPersonalInfo()
        widget.addWidget(personalinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DonorLoginScreen(QDialog):
    def __init__(self):
        super(DonorLoginScreen, self).__init__()
        loadUi("UI Screens/donorlogin.ui", self)
        self.donorpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupredirect.clicked.connect(self.gotodonorsignup)
        self.donorauthenticate.clicked.connect(self.donorloginfunction)

    def gotodonorsignup(self):
        donorsignup = DonorSignUpScreen()
        widget.addWidget(donorsignup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def donorloginfunction(self):
        global donor_id
        donor_id = self.donoridfield.text()
        password = self.donorpasswordfield.text()
        if len(donor_id) == 0 or len(password) == 0:
            self.errormsg.setText("Please input all fields")
        else:
            conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM LOGIN_CREDENTIALS WHERE DONOR_ID = '{}' AND PASSWORD = '{}';".format(donor_id, password))
            rec = cur.fetchone()
            if rec is None:
                self.errormsg.setText("Invalid Donor ID or password. Please try again.")
            else:
                DonorLoginScreen.gotodonorpersonalinfo(self)
            conn.close()

    def gotodonorpersonalinfo(self):
        personalinfo = DonorPersonalInfo()
        widget.addWidget(personalinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminLoginScreen(QDialog):
    def __init__(self):
        super(AdminLoginScreen, self).__init__()
        loadUi("UI Screens/adminlogin.ui", self)
        self.adminpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.adminauthenticate.clicked.connect(self.adminloginfunction)

    def adminloginfunction(self):
        admin_id = self.adminidfield.text()
        password = self.adminpasswordfield.text()
        if len(admin_id) == 0 or len(password) == 0:
            self.errormsg.setText("Please input all fields")
        elif admin_id != "A291622" or password != "1nfiniteRed$":
            self.errormsg.setText("Invalid ID or password. Please try again.")
        else:
            AdminLoginScreen.gotoadminmenu(self)

    def gotoadminmenu(self):
        search = Search()
        widget.addWidget(search)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Search(QDialog):
    def __init__(self):
        super(Search, self).__init__()
        loadUi("UI Screens/searchmenu.ui", self)
        self.homescreenredirect.clicked.connect(self.gotohomescreen)
        self.modifyredirect.clicked.connect(self.gotomodifyscreen)
        column_widths = [105, 285, 50, 285, 130, 135, 50]
        for i in range(7):
            self.tableWidget.setColumnWidth(i, column_widths[i])
        self.loaddata()
        self.searchbutton.clicked.connect(self.searchrecord)
        self.showallrecs.clicked.connect(self.loaddata)

    def loaddata(self):
        conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM DONOR_INFO;")
        recs = cur.fetchall()
        self.tableWidget.setRowCount(len(recs))
        for i in range(len(recs)):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem(str(recs[i][j]))
                self.tableWidget.setItem(i, j, item)
                item.setTextAlignment(Qt.AlignCenter)
        conn.close()

    def searchrecord(self):
        searchgroup = self.searchlist.currentText()
        searchvalue = self.searchfield.text()
        conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM DONOR_INFO WHERE {} LIKE '{}%';".format(searchgroup, searchvalue))
        recs = cur.fetchall()
        self.tableWidget.setRowCount(len(recs))
        for i in range(len(recs)):
            for j in range(7):
                item = QtWidgets.QTableWidgetItem(str(recs[i][j]))
                self.tableWidget.setItem(i, j, item)
                item.setTextAlignment(Qt.AlignCenter)
        conn.close()

    def gotomodifyscreen(self):
        modifyscreen = Modify()
        widget.addWidget(modifyscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotohomescreen(self):
        homescreen = WelcomeScreen()
        widget.addWidget(homescreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Modify(QDialog):
    def __init__(self):
        super(Modify, self).__init__()
        loadUi("UI Screens/modifymenu.ui", self)
        self.searchscreenredirect.clicked.connect(self.gotosearchscreen)
        column_widths = [100, 285, 50, 285, 130, 140, 60]
        for i in range(7):
            self.tableWidget.setColumnWidth(i, column_widths[i])
        Search.loaddata(self)
        self.modifybutton.clicked.connect(self.modifyrecord)

    def modifyrecord(self):
        donorid = self.donoridfield.text()
        modifywhat = self.comboBox.currentText()
        modifyto = self.modifyfield.text()
        if donorid.isdigit() == False:
            self.errormsg.setText("Invalid Donor ID")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif modifywhat == "AGE" and (int(modifyto) < 18 or int(modifyto) > 65):
            self.errormsg.setText("Invalid Age")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif modifywhat == "PHONE_NO" and len(modifyto) != 10:
            self.errormsg.setText("Invalid Phone Number")
            self.errormsg.setAlignment(Qt.AlignCenter)
        else:
            self.errormsg.setText("")
            conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
            cur = conn.cursor()
            cur.execute("UPDATE DONOR_INFO SET {} = '{}' WHERE DONOR_ID = {};".format(modifywhat, modifyto, donorid))
            conn.commit()
            conn.close()
            Search.loaddata(self)


    def gotosearchscreen(self):
        searchscreen = Search()
        widget.addWidget(searchscreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DonorPersonalInfo(QDialog):
    def __init__(self):
        super(DonorPersonalInfo, self).__init__()
        loadUi("UI Screens/donorpersonalinfo.ui", self)

        conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS DONOR_INFO(
                    DONOR_ID INT,NAME VARCHAR(50), AGE CHAR(2), EMAIL_ID VARCHAR(50), PHONE_NO VARCHAR(10),
                    BLOOD_GROUP VARCHAR(5), SEX VARCHAR(3),
                    FOREIGN KEY(DONOR_ID) REFERENCES LOGIN_CREDENTIALS(DONOR_ID));''')
        conn.commit()
        conn.close()

        self.proceed.clicked.connect(self.insertinfo)

    def insertinfo(self):
        global name, email, blood_grp
        name = self.namefield.text()
        age = self.agefield.text()
        phone_no = self.phonenofield.text()
        blood_grp = self.bloodgroupfield.currentText()
        email = self.emailIDfield.text()
        if self.sexfield.currentText() == "Male":
            sex = "M"
        else:
            sex = "F"

        if len(name) == 0 or len(age) == 0 or len(phone_no) == 0 or len(email) == 0:
            self.errormsg.setText("Please input all fields")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif int(age) < 18 or int(age) > 65:
            self.errormsg.setText("Not eligible age to donate")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif len(phone_no) != 10:
            self.errormsg.setText('Please enter a 10 digit number')
            self.errormsg.setAlignment(Qt.AlignCenter)
        else:
            conn = sql.connect(host='localhost', user='root', password='dpsbn', database='bloodbankdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM DONOR_INFO WHERE DONOR_ID = {};".format(donor_id))
            rec = cur.fetchone()
            if rec is None:
                cur.execute('''INSERT INTO DONOR_INFO(DONOR_ID,NAME,AGE,PHONE_NO,BLOOD_GROUP,EMAIL_ID,SEX)
                VALUES ('{}','{}','{}','{}','{}','{}','{}')'''.format(donor_id, name, age, phone_no, blood_grp, email, sex))
            else:
                cur.execute('''UPDATE DONOR_INFO SET NAME = '{}',AGE = '{}', PHONE_NO = '{}', BLOOD_GROUP = '{}', 
                EMAIL_ID = '{}',SEX = '{}' WHERE DONOR_ID = '{}';'''.format(name, age, phone_no, blood_grp, email, sex, donor_id))
            conn.commit()
            conn.close()
            DonorPersonalInfo.gotoconsentinfo(self)

    def gotoconsentinfo(self):
        consentinfo = ConsentInfo()
        widget.addWidget(consentinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ConsentInfo(QDialog):
    def __init__(self):
        super(ConsentInfo, self).__init__()
        loadUi("UI Screens/consentofdonor.ui", self)
        self.proceed.clicked.connect(self.cbstate)

    def cbstate(self):
        if self.checkBox.isChecked():
            ConsentInfo.gotoquestionnaireinfo(self)

    def gotoquestionnaireinfo(self):
        questionnaireinfo = QuestionnaireInfo1()
        widget.addWidget(questionnaireinfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class QuestionnaireInfo1(QDialog):
    def __init__(self):
        super(QuestionnaireInfo1, self).__init__()
        loadUi("UI Screens/questionnaireinfo1stpage.ui", self)
        self.yes1.toggled.connect(self.updatevar1)
        self.no1.toggled.connect(self.updatevar1)
        self.yes2.toggled.connect(self.updatevar2)
        self.no2.toggled.connect(self.updatevar2)
        self.yes3.toggled.connect(self.updatevar3)
        self.no3.toggled.connect(self.updatevar3)
        self.yes4.toggled.connect(self.updatevar4)
        self.no4.toggled.connect(self.updatevar4)
        self.proceed.clicked.connect(self.rbstate)

    def updatevar1(self):
        rbtn = self.sender()
        global var1
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var1 = True
            elif rbtn.text() == "NO":
                var1 = False

    def updatevar2(self):
        rbtn = self.sender()
        global var2
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var2 = True
            elif rbtn.text() == "NO":
                var2 = False

    def updatevar3(self):
        rbtn = self.sender()
        global var3
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var3 = True
            elif rbtn.text() == "NO":
                var3 = False

    def updatevar4(self):
        rbtn = self.sender()
        global var4
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var4 = True
            elif rbtn.text() == "NO":
                var4 = False

    def rbstate(self):
        options = [var1, var2, var3, var4]
        if options[0] == '' or options[1] == '' or options[2] == '' or options[3] == '':
            self.errormsg.setText("Please answer all questions")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif options[0] == options[1] == options[2] == options[3] == False:
            QuestionnaireInfo1.gotoquestionnaireinfo2(self)
        else:
            self.errormsg.setText("You are not eligible to donate blood")
            self.errormsg.setAlignment(Qt.AlignCenter)

    def gotoquestionnaireinfo2(self):
        questionnaireinfo2 = QuestionnaireInfo2()
        widget.addWidget(questionnaireinfo2)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class QuestionnaireInfo2(QDialog):
    def __init__(self):
        super(QuestionnaireInfo2, self).__init__()
        loadUi("UI Screens/questionnaireinfo2ndpage.ui", self)
        self.yes5.toggled.connect(self.updatevar5)
        self.no5.toggled.connect(self.updatevar5)
        self.yes6.toggled.connect(self.updatevar6)
        self.no6.toggled.connect(self.updatevar6)
        self.yes7.toggled.connect(self.updatevar7)
        self.no7.toggled.connect(self.updatevar7)
        self.yes8.toggled.connect(self.updatevar8)
        self.no8.toggled.connect(self.updatevar8)
        self.proceed.clicked.connect(self.rbstate)

    def updatevar5(self):
        rbtn = self.sender()
        global var5
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var5 = True
            elif rbtn.text() == "NO":
                var5 = False

    def updatevar6(self):
        rbtn = self.sender()
        global var6
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var6 = True
            elif rbtn.text() == "NO":
                var6 = False

    def updatevar7(self):
        rbtn = self.sender()
        global var7
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var7 = True
            elif rbtn.text() == "NO":
                var7 = False

    def updatevar8(self):
        rbtn = self.sender()
        global var8
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var8 = True
            elif rbtn.text() == "NO":
                var8 = False

    def rbstate(self):
        options = [var5, var6, var7, var8]
        if options[0] == '' or options[1] == '' or options[2] == '' or options[3] == '':
            self.errormsg.setText("Please answer all questions")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif options[0] == options[1] == options[2] == options[3] == False:
            QuestionnaireInfo2.gotoquestionnaireinfo3(self)
        else:
            self.errormsg.setText("You are not eligible to donate blood")
            self.errormsg.setAlignment(Qt.AlignCenter)

    def gotoquestionnaireinfo3(self):
        questionnaireinfo3 = QuestionnaireInfo3()
        widget.addWidget(questionnaireinfo3)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class QuestionnaireInfo3(QDialog):
    def __init__(self):
        super(QuestionnaireInfo3, self).__init__()
        loadUi("UI Screens/questionnaireinfo3rdpage.ui", self)
        self.yes9.toggled.connect(self.updatevar9)
        self.no9.toggled.connect(self.updatevar9)
        self.yes10.toggled.connect(self.updatevar10)
        self.no10.toggled.connect(self.updatevar10)
        self.yes11.toggled.connect(self.updatevar11)
        self.no11.toggled.connect(self.updatevar11)
        self.yes12.toggled.connect(self.updatevar12)
        self.no12.toggled.connect(self.updatevar12)
        self.proceed.clicked.connect(self.rbstate)

    def updatevar9(self):
        rbtn = self.sender()
        global var9
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var9 = True
            elif rbtn.text() == "NO":
                var9 = False

    def updatevar10(self):
        rbtn = self.sender()
        global var10
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var10 = True
            elif rbtn.text() == "NO":
                var10 = False

    def updatevar11(self):
        rbtn = self.sender()
        global var11
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var11 = True
            elif rbtn.text() == "NO":
                var11 = False

    def updatevar12(self):
        rbtn = self.sender()
        global var12
        if rbtn.isChecked() == True:
            if rbtn.text() == "YES":
                var12 = True
            elif rbtn.text() == "NO":
                var12 = False

    def rbstate(self):
        options = [var9, var10, var11, var12]
        if options[0] == '' or options[1] == '' or options[2] == '' or options[3] == '':
            self.errormsg.setText("Please answer all questions")
            self.errormsg.setAlignment(Qt.AlignCenter)
        elif options[3] == True and (options[0] == options[1] == options[2] == False):
            QuestionnaireInfo3.gotoemailcertificate(self)
        else:
            self.errormsg.setText("You are not eligible to donate blood")
            self.errormsg.setAlignment(Qt.AlignCenter)

    def gotoemailcertificate(self):
        emailcertificate = EmailCertificate()
        widget.addWidget(emailcertificate)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class EmailCertificate(QDialog):
    def __init__(self):
        super(EmailCertificate, self).__init__()
        loadUi("UI Screens/emailcertificate.ui", self)
        self.emailcertificate.clicked.connect(self.generate_certificate)
        self.homescreenredirect.clicked.connect(self.gotowelcomescreen)

    def generate_certificate(self):
        font_path = "C:\WINDOWS\FONTS\MTCORSVA.TTF"
        date = QDate.currentDate()
        with Image.open('Blood Donor Certificate.png') as img:  # opening image
            image_width = img.width
            draw = ImageDraw.Draw(img)
            text_width, _ = draw.textsize(name, font=ImageFont.truetype(font_path, 60))
            draw.text(xy=((image_width - text_width) / 2, 550), text='{}'.format(name), fill=(0, 0, 0),
                      font=ImageFont.truetype(font_path, 60))
            draw.text(xy=(505, 865), text='{}'.format(blood_grp), fill=(0, 0, 0),
                      font=ImageFont.truetype(font_path, 40))
            draw.text(xy=(505, 910), text=date.toString(Qt.DefaultLocaleLongDate), fill=(0, 0, 0),
                      font=ImageFont.truetype(font_path, 40))
            image = img.convert('RGB')
            global pdfpath
            pdfpath = 'Certificates/Certificate_{}_{}.pdf'.format(name, date.toString('dd-MM-yyyy'))
            image.save(pdfpath)
        EmailCertificate.automate_email(self)

    def automate_email(self):
        yag = yagmail.SMTP(user="redsinfinite@gmail.com",
                           password="rtumhtbarhfnrwfw")  # initiating connection with SMTP server
        yag.send(to=email, subject="Certificate of Appreciation",
                 contents='''
                 Dear {},
                 Thank you for donating blood.

                 Regards,
                 The Infinite Reds Team
                 '''.format(name.split()[0]), attachments=pdfpath)
        self.status.setText("Email Sent!")
        self.status.setAlignment(Qt.AlignCenter)

    def gotowelcomescreen(self):
        welcomescreen = WelcomeScreen()
        widget.addWidget(welcomescreen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowTitle("Infinite Reds Blood Bank")
widget.show()
sys.exit(app.exec_())