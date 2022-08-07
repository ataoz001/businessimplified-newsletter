import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from email.message import EmailMessage
import ssl
import smtplib



class Notepad(QWidget):
    def __init__(self):
        super().__init__()
    
        self.init_ui()

    def init_ui(self):
        self.yazi_alani = QTextEdit()

        self.owners = QLabel('Programmer: Atahan Ozdogan \n Writer: Mustafa Alp Yalcin')

        self.subject_text = QLabel('Subject:')
        
        self.body_text = QLabel('Body:')

        self.mail_success = QLabel('')

        self.subject = QLineEdit()

        self.clear = QPushButton('temizle')

        self.ac = QPushButton('ac')

        self.kaydet = QPushButton('kaydet')

        self.gonder = QPushButton('Send')

        self.subject_clear = QPushButton('clear')

        etiket2 = QLabel(self)
        etiket2.setPixmap(QtGui.QPixmap("bslogo4"))

        h_box = QHBoxLayout()
        h_box.addWidget(self.clear)
        h_box.addWidget(self.ac)
        h_box.addWidget(self.kaydet)
        # this v box is for the body and subjects place
        v_box3 = QVBoxLayout()
        v_box3.addWidget(self.subject_text)
        v_box3.addStretch()
        v_box3.addWidget(self.body_text)
        v_box3.addStretch()
        v_box = QVBoxLayout()
        v_box.addWidget(self.subject)
        v_box.addWidget(self.yazi_alani)
        v_box.addLayout(h_box)
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.subject_clear)
        v_box2.addStretch()
        v_box2.addWidget(etiket2)
        v_box2.addStretch()
        v_box2.addWidget(self.owners)
        v_box2.addStretch()
        v_box2.addWidget(self.gonder)
        v_box2.addStretch()
        v_box2.addWidget(self.mail_success)
        h_box2 = QHBoxLayout()
        h_box2.addLayout(v_box3)
        h_box2.addLayout(v_box)
        h_box2.addLayout(v_box2)

        self.setLayout(h_box2)

        self.clear.clicked.connect(self.yaziyi_temizle)
        self.ac.clicked.connect(self.dosya_ac)
        self.kaydet.clicked.connect(self.dosya_kaydet)
        self.gonder.clicked.connect(self.email_at)
        self.subject_clear.clicked.connect(self.yaziyi_temizle)
        
    def yaziyi_temizle(self):
        sender = self.sender()

        if sender.text() == "temizle":
            self.yazi_alani.clear()
        else:
            self.subject.clear()

    def dosya_ac(self):
        dosya_ismi = QFileDialog.getOpenFileName(self, 'Dosya Ac', os.getenv('HOME'))

        with open(dosya_ismi[0], 'r') as file: 
            self.yazi_alani.setText(file.read())


    def dosya_kaydet(self):
        dosya_ismi = QFileDialog.getSaveFileName(self, 'Dosya Kaydet', os.getenv('HOME'))

        with open(dosya_ismi[0], 'w' ) as file:
            file.write(self.yazi_alani.toPlainText())

    def email_at(self):
        email_sender = 'businessimplifiednewsletter@gmail.com'
        email_password = '#email app password from gmail'
        subject =  self.subject.text()
        body = self.yazi_alani.toPlainText()
        with open('mailing_list.txt', 'r') as file:
            file_context = file.readlines()
            mailing_list = []
            for i in file_context: 
                i = i[:-1]
                mailing_list.append(i)
        for i in mailing_list:
            print(i)
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = i
            em['Subject'] = subject

            em.set_content(body)

            context = ssl.create_default_context()
            try: 
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender ,i , em.as_string())
                    self.mail_success.setText('mail has been sent succesfully')
            except:
                    self.mail_success.setText('your password or mail is incorrect')



class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pencere = Notepad()
        self.setCentralWidget(self.pencere)
        self.menuleri_olustur()
        self.setWindowTitle('newsletter mailing process')
        self.setGeometry(700,750,800,700)
        self.show()

    def menuleri_olustur(self):
        menubar = self.menuBar()

        dosya = menubar.addMenu('Dosya')
        dosya_ac = QAction('Dosya Ac', self)
        dosya_ac.setShortcut('⌘ + O')

        dosya_ac = QAction('Dosya Ac', self)
        dosya_ac.setShortcut('⌘ + O ')

        dosya_kaydet = QAction('Dosya kaydet', self)
        dosya_kaydet.setShortcut('⌘ + D')

        cikis = QAction('Cikis', self)
        cikis.setShortcut('⌘ + Q')
        
        temizle = QAction('Temizle', self)
        temizle.setShortcut('⌘ + C')

        dosya.addAction(dosya_ac)
        dosya.addAction(dosya_kaydet)
        dosya.addAction(cikis)
        dosya.addAction(temizle)


        dosya.triggered.connect(self.response)
        

    
    def response(self, action):
        if action.text() == 'Dosya Ac':
            self.pencere.dosya_ac()
        elif action.text() == 'Dosya Kaydet':
            self.pencere.dosya_kaydet()
        elif action.text() == 'Temizle':
            self.pencere.yaziyi_temizle()
        else:
            qApp



app = QApplication(sys.argv)
menu = Menu()
sys.exit(app.exec_())
