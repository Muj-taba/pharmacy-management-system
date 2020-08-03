import sys


from PyQt5 import QtGui
import MySQLdb
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import xlsxwriter
from login import Ui_Form as login_window
from main import Ui_Form as main_window
from reports import Ui_Form as reports_window


#from PyQt5.uic import loadUiType
#from os import path
#FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))
#FORM_CLASS2, _ = loadUiType(path.join(path.dirname(__file__), "login.ui"))
#FORM_CLASS3, _ = loadUiType(path.join(path.dirname(__file__), "reports.ui"))



class Login(QMainWindow, login_window):
    def __init__(self, parent= None):
        super(Login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handle_login)
        self.window2 = None




###################### labe ###############################3
        i = QPixmap("icon.png")
        icon = i.scaled(190, 200)
        self.label_3.setPixmap(icon)




        # self.pushButton_2.setIcon(QIcon('images.jpg'))
        # self.pushButton_2.setIconSize(QSize(100, 100))

    def Handle_login(self):
        username = self.lineEdit.text()
        key = self.lineEdit_2.text()
        if username == "cullen" and key == "123":
            self.window2 = Main()
            self.close()
            self.window2.show()
        else:
            self.label.setText("Something goes wrong, Try again")




class Main(QMainWindow, main_window):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_DB_connections()
        self.Icons()
        self.window3 = reports()
        self.window = Login()
        self.Handle_Buttons()
        self.time()


############################# time

    def time(self):
        current_time = QDate.currentDate()
        self.dateEdit.setDate(current_time)



################################# Refresh sale table #################################################

        self.tableWidget.insertRow(0)
        self.cur.execute('''
                    SELECT m_id,customer_name,doctor_name,hospital_name,city,zip,cure_name,sale_price,quantity FROM sale
                ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

#########################################################################################

################################# Refresh purchase table #################################################

        self.tableWidget_2.insertRow(0)
        self.cur.execute('''
                    SELECT m_id,cure_name,quantity,purchase_price,sale_price,supplier,company FROM purchase
                ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)


#########################################################################################




    def Handle_Buttons(self):
        self.pushButton_8.clicked.connect(self.Add_sale)
        self.pushButton_7.clicked.connect(self.Search_sale)
        self.pushButton_6.clicked.connect(self.Delete_sale)
        self.pushButton_5.clicked.connect(self.Clear_all)
        #################################
        self.pushButton_10.clicked.connect(self.open_reports)
        self.pushButton_11.clicked.connect(self.Handle_logout)
        self.pushButton_12.clicked.connect(self.update_sale)
        #################################
        self.pushButton_3.clicked.connect(self.Add_purchase)
        self.pushButton_4.clicked.connect(self.clear_purchase)
        self.pushButton_14.clicked.connect(self.search_purchase)
        self.pushButton.clicked.connect(self.Update_purchase)
        self.pushButton_2.clicked.connect(self.Delete_purchase)
        #################################
        self.pushButton_9.clicked.connect(self.excel_choise)
        self.pushButton_13.clicked.connect(self.refresh_sale)
        self.pushButton_13.clicked.connect(self.refresh_purchase)

    def Handle_DB_connections(self):
        self.db = MySQLdb.connect(host="localhost", user="root" ,passwd="greenvip111", db="mydb")
        self.cur = self.db.cursor()



    def Handle_logout(self):
        self.close()
        self.window.show()

    def open_reports(self):
        self.window3.show()



    def Icons(self):
        i = QPixmap("icon.png")
        icon = i.scaled(74, 74)
        self.label1.setPixmap(icon)



    def Add_sale(self):
        m_id = self.lineEdit_17.text()
        customer_name = self.lineEdit_3.text()
        doctor_name = self.lineEdit_4.text()
        hospital = self.lineEdit_14.text()
        city = self.lineEdit_13.text()
        zip = self.lineEdit_16.text()
        cure_name = self.lineEdit_15.text()
        sale_price = self.lineEdit_11.text()
        quantity = self.lineEdit_12.text()

        self.cur.execute('''INSERT INTO sale(m_id,customer_name,doctor_name,hospital_name,city,zip,cure_name,sale_price,quantity)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                         (m_id,customer_name, doctor_name,hospital,city,zip,cure_name, sale_price, quantity))
        self.db.commit()

        self.lineEdit_17.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Inserting Data has been done successfuly...')

######################fetch all sale data auto #############################

        self.tableWidget.clearContents()
        self.tableWidget.insertRow(0)
        self.cur.execute('''
                    SELECT customer_name,doctor_name,sale_price,quantity FROM sale
                ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
######################################################################

######################### redresh sale table #######################

    def refresh_sale(self):

        self.tableWidget.clearContents()
        self.tableWidget.setVisible(False)
        self.tableWidget.setVisible(True)
        self.tableWidget.clearContents()

        self.tableWidget.insertRow(0)
        self.cur.execute('''
                    SELECT m_id,customer_name,doctor_name,hospital_name,city,zip,cure_name,sale_price,quantity FROM sale
                ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    def refresh_purchase(self):

        self.tableWidget_2.clearContents()
        self.tableWidget_2.setVisible(False)
        self.tableWidget_2.setVisible(True)

        self.tableWidget_2.insertRow(0)
        self.cur.execute('''
                     SELECT m_id,cure_name,quantity,purchase_price,sale_price,supplier,company FROM purchase
                 ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
    def Search_sale(self):
        search = self.lineEdit_18.text()

        query = "SELECT * FROM sale where m_id = %s"

        self.cur.execute(query, ([search]))
        data = self.cur.fetchall()
        for row in data:
            self.lineEdit_17.setText(str(row[0]))
            self.lineEdit_3.setText(row[1])
            self.lineEdit_4.setText(row[2])
            self.lineEdit_14.setText(row[3])
            self.lineEdit_13.setText(row[4])
            self.lineEdit_16.setText(str(row[5]))
            self.lineEdit_15.setText(row[6])
            self.lineEdit_11.setText(str(row[7]))
            self.lineEdit_12.setText(str(row[8]))


    def update_sale(self):
        m_id = self.lineEdit_17.text()
        customer_name = self.lineEdit_3.text()
        doctor_name = self.lineEdit_4.text()
        hospital = self.lineEdit_14.text()
        city = self.lineEdit_13.text()
        zip = self.lineEdit_16.text()
        cure_name = self.lineEdit_15.text()
        sale_price = self.lineEdit_11.text()
        quantity = self.lineEdit_12.text()

        self.cur.execute('''UPDATE
        sale SET customer_name =%s,doctor_name=%s,hospital_name =%s,city =%s,zip =%s,cure_name =%s,sale_price =%s,quantity =%s WHERE m_id =%s''',
                         (customer_name,doctor_name, hospital,city,zip,cure_name, sale_price, quantity,m_id))

        self.db.commit()
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('update has been done successfuly...')

        self.lineEdit_17.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")


    def Delete_sale(self):
        m_id = self.lineEdit_17.text()

        del_statmt = "DELETE FROM sale WHERE m_id =%s"

        self.cur.execute(del_statmt, (m_id,))
        self.db.commit()

        self.lineEdit_17.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Data Delete has been successfuly...')


    def Clear_all(self):
        self.lineEdit_17.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")

##################### EX TO EXCEL ###################################

    def excel_choise(self):
        current_value = self.comboBox.currentIndex()
        if current_value == 0:
            self.send_sale_excel()
        if current_value ==1:
            self.send_purchase_excel()


    def send_sale_excel(self):
        save_place = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter='All file(*.xlsx)')
        save_loc = str(save_place).split(',')[0][2:-1]

        query = "SELECT * FROM sale"
        self.cur.execute(query)
        result = self.cur.fetchall()


        wb = xlsxwriter.Workbook(save_loc)
        sheet1 = wb.add_worksheet()
        sheet1.write(0,0,"m_id")
        sheet1.write(0,1,"customer_name")
        sheet1.write(0,2,"doctor_name")
        sheet1.write(0,3,"hospital_name")
        sheet1.write(0,4,"city")
        sheet1.write(0,5,"zip")
        sheet1.write(0,6,"cure_name")
        sheet1.write(0,7,"sale_price")
        sheet1.write(0,8,"quantity")

        row_number = 1
        for row in result:
            column = 0
            for item in row:
                sheet1.write(row_number , column , str(item))
                column += 1
            row_number +=1
        wb.close()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Data Eported successfuly...')



    def send_purchase_excel(self):
        pass





    def Add_purchase(self):
        m_id = self.lineEdit_6.text()
        cure_name = self.lineEdit_2.text()
        quantity = self.lineEdit.text()
        purchase_price = self.lineEdit_7.text()
        sale_price = self.lineEdit_8.text()
        supplier = self.lineEdit_9.text()
        company = self.lineEdit_10.text()

        self.cur.execute('''INSERT INTO purchase(m_id,cure_name,quantity,purchase_price,sale_price,supplier,company)
                VALUES(%s,%s,%s,%s,%s,%s,%s)''',
                         (m_id,cure_name,quantity,purchase_price,sale_price,supplier,company))
        self.db.commit()

        self.lineEdit_6.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")


        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Adding purchase data has been done successfuly...')


    def search_purchase(self):
        search = self.lineEdit_19.text()

        query = "SELECT * FROM purchase where m_id = %s"

        self.cur.execute(query, ([search]))
        data = self.cur.fetchall()
        for row in data:
            self.lineEdit_6.setText(str(row[0]))
            self.lineEdit_2.setText(row[1])
            self.lineEdit.setText(str(row[2]))
            self.lineEdit_7.setText(str(row[3]))
            self.lineEdit_8.setText(str(row[4]))
            self.lineEdit_9.setText(row[5])
            self.lineEdit_10.setText(row[6])

    def clear_purchase(self):
        self.lineEdit_6.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")



    def Update_purchase(self):
        m_id = self.lineEdit_6.text()
        cure_name = self.lineEdit_2.text()
        quantity = self.lineEdit.text()
        purchase_price = self.lineEdit_7.text()
        sale_price = self.lineEdit_8.text()
        supplier = self.lineEdit_9.text()
        company = self.lineEdit_10.text()

        self.cur.execute('''UPDATE
        purchase SET cure_name=%s,quantity=%s,purchase_price=%s,sale_price=%s,supplier=%s,company=%s WHERE m_id = %s''',
                         (cure_name, quantity, purchase_price, sale_price, supplier, company,m_id))
        self.db.commit()

        self.lineEdit_6.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Update purchase date has been done successfuly...')

    def Delete_purchase(self):
        m_id = self.lineEdit_17.text()

        del_statmt = "DELETE FROM purchase WHERE m_id =%s"

        self.cur.execute(del_statmt, (m_id,))
        self.db.commit()

        self.lineEdit_6.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Data Delete has been successfuly...')

    def send_purchase_excel(self):
        save_place = QFileDialog.getSaveFileName(self, caption='Save as', directory='.', filter='All file(*.xlsx)')
        save_loc = str(save_place).split(',')[0][2:-1]

        query = "SELECT * FROM purchase"
        self.cur.execute(query)
        data = self.cur.fetchall()

        workbook = xlsxwriter.Workbook(save_loc)
        sheet1 = workbook.add_worksheet()
        sheet1.write(0,0, "m_id")
        sheet1.write(0, 1, "cure name")
        sheet1.write(0, 2, "quantity")
        sheet1.write(0, 3, "purchase price")
        sheet1.write(0, 4, "sale price")
        sheet1.write(0, 5, "supplier")
        sheet1.write(0, 6, "company")
        row_number = 1

        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number , column_number , str(item))
                column_number += 1
            row_number += 1
        workbook.close()

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Data Eported successfuly...')



class reports(QMainWindow, reports_window):
    def __init__(self, parent=None):
        super(reports, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_reports_buttons()
        self.Handle_db()
        self.tableWidget.setVisible(False)
        self.tableWidget_2.setVisible(False)


    def Handle_reports_buttons(self):
        self.pushButton.clicked.connect(self.search_report_choice)


    def Handle_db(self):
        self.datab = MySQLdb.connect(host="localhost", user="root", passwd="greenvip111", db="mydb")
        self.curse = self.datab.cursor()

    def search_report_choice(self):
        current_choise = self.comboBox.currentIndex()
        if current_choise == 0:
            self.tableWidget.setVisible(False)
            self.tableWidget_2.setVisible(True)
            self.search_re_sale()
        if current_choise == 1:
            self.tableWidget_2.setVisible(False)
            self.tableWidget.setVisible(True)
            self.serarch_re_purchase()



    def search_re_sale(self):

        self.tableWidget_2.clearContents()
        search = self.lineEdit.text()
        self.tableWidget_2.insertRow(0)
        query = "SELECT * FROM sale where m_id = %s"
        self.curse.execute(query,([search]))
        data = self.curse.fetchall()
        #str(data)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                self.tableWidget_2.item(row, column).setBackground(QtGui.QColor(127, 136, 150))

                column += 1


            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
            self.lineEdit.setText("")





    def serarch_re_purchase(self):

        self.tableWidget.clearContents()

        search = self.lineEdit.text()
        self.tableWidget.insertRow(0)
        query = "SELECT * FROM purchase where m_id = %s"
        self.curse.execute(query, ([search]))
        data = self.curse.fetchall()
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                self.tableWidget.item(row, column).setBackground(QtGui.QColor(158, 170, 188))


                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.lineEdit.setText("")










def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
