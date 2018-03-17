import sqlite3
import cv2
from PIL import Image
import os
import qrcode as qrenc
from  pyzbar.pyzbar import decode
import datetime
import mysql.connector

def qrcode_regno():
    cam = cv2.VideoCapture(0)

    decoded = None
    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gaus = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)



        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        decoded = decode(gaus)

        if len(decoded)>0:
            break



    cam.release()

    cv2.destroyAllWindows()

    qrcode_string = str(decoded[0][0])


    qrcode_list = qrcode_string.split(',')

    reg_no = str(qrcode_list[1])
    reg_no = reg_no.lstrip()
    name = str(qrcode_list[0])
    name = name.lstrip()
    name = name[2:]
    return reg_no,name


def choose_subject():
    subject = int(input("Choose a subject \n 1. Physics \n 2. Chemistry \n 3. Maths"))
    if (subject == 1):
        sub = 'physics'
        return sub
    elif (subject == 2):
        sub = 'chemistry'
        return sub
    elif (subject == 3):
        sub = 'maths'
        return sub
    else:
        print("choose wisely")


def main():
    option = int(input("Choose any of the following \n 1. Mark Attendance \n 2. Check Attendance \n 3. Quit"))
    if (option==1):

        subject = choose_subject()
        reg_no,name = qrcode_regno()
        date = datetime.date.today()



        cnx = mysql.connector.connect(host = 'localhost', user = 'root', database = 'attendance', passwd = '')
        cursor = cnx.cursor()
        try:
            cursor.execute("""INSERT INTO attendance VALUES (%s,%s,%s,%s)""",(name,reg_no,date,subject))
            cnx.commit()
        except:
            cnx.rollback()
        cnx.close()



    elif (option==2):


        reg_no,name = qrcode_regno()
        physics = 'physics'
        chemistry = 'chemistry'
        maths = 'maths'
        list = [('name','reg_no','physics','chemistry','maths')]

        cnx = mysql.connector.connect(host = 'localhost', user = 'root', database = 'attendance', passwd = '')
        cursor =  cnx.cursor()
        print(reg_no)
        query = "SELECT count(reg_no),name, reg_no FROM attendance where reg_no=" +str(reg_no) + " GROUP BY subject"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(list)
        print(rows)

        cnx.close()


    elif (option==3):
        return False
    else:
        print("Choose wisely")
    return True



while main():
    pass

