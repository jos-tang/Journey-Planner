import sys
from PyQt5 import QtCore, QtGui, QtWidgets #pip3 install pyqt5
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#Class to create a new window
#Main window that holds the other widgets
class newWindow:
    def __init__(self, name, width, height):
        #Initialize new instance of window
        self.win = QMainWindow()
        #Set Window Title
        self.win.setWindowTitle(name)
        #Set Window Size
        self.win.resize(width,height)
        
    #Set Window Icon
    def setWindowIcon(self, image):
        self.win.setWindowIcon(QtGui.QIcon(image))

class newApp:
    #Class to initialize a new instance of QApplication module which is required to run PyQt5
    def __init__(self):
        self.app = QApplication(sys.argv)

#Class to create a stack widget
#Stack widget holds widget pages
#Simulate changing of window by switching pages
class newStackWidget:
    def __init__(self, window, x, y, width, height):
        #Attach the stack widget to a window
        self.stackW = QtWidgets.QStackedWidget(window)
        #Set the position and size of the stack widget, x & y are coordinates
        self.stackW.setGeometry(x, y, width, height)
        #Set the stack widget index to point to the first widget page
        self.stackW.setCurrentIndex(0)
    
    def addPage(self, page):
        #Add a page to stack widget
        self.stackW.addWidget(page)
    
    def setCurrentPage(self, page):
        #Set a specific page as the current page
        self.stackW.setCurrentWidget(page.page)

#Class to create a new widget page
#Widget page contains a group of widgets
class newWidgetPage:
    def __init__(self):
        #Creates a new page
        self.page = QtWidgets.QWidget()

#Create new label widget
#Label can display text and images
class newLabel:
    def __init__(self, page, x, y, width, height, text="", image="", fontStyle="", fontSize=""):
        #Initialize new instance of Label UI
        self.label = QLabel(page)
        #Set Label x & y position and size
        #self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.label.setGeometry(QtCore.QRect(x, y, width, height))
        #Set alignment of label text to the left
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        #Set alignment of label text to be in the middle
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        #Allows word warpping of text
        self.label.setWordWrap(True)
        #Set lable background to transparent and background color to none
        self.label.setStyleSheet("background: transparent; background-color: none;")
        if text:
            self.setText(text)
        if image:
            self.setImage(image)
        if fontStyle and fontSize:
            self.setFont(fontStyle, fontSize)

    def setText(self, text):
        #Set the label text
        self.label.setText(text)
        #Automatically update the length of label to fit text
        self.label.update()

    def setFont(self, fontStyle, fontSize):
        #Set font style and font size of text
        self.label.setFont(QFont(fontStyle, fontSize))
    
    def setImage(self, image):
        #Set display image in Label
        self.label.setPixmap(QtGui.QPixmap(image))
        #Enable image scaling to fit Label size
        self.label.setScaledContents(True)

#Class to create a new button widget
class newPushButton:
    def __init__(self, page, x, y, width, height, clickedfunction, text="", fontStyle="", fontSize=""):
        #Initialize new instance of PushButton UI
        self.pushButton = QPushButton(page)
        #Set PushButton x & y position and size
        self.pushButton.setGeometry(QtCore.QRect(x, y, width, height))
        #Calls function when PushButton is clicked
        self.pushButton.clicked.connect(clickedfunction)
        if text:
            self.setText(text)
        if fontStyle and fontSize:
            self.setFont(fontStyle, fontSize)
    
    def setText(self, text):
        #Set PushButton text
        self.pushButton.setText(text)
    
    def setFont(self, fontStyle, fontSize):
        #Set font style and font size of text
        self.pushButton.setFont(QFont(fontStyle,int(fontSize)))

#Class to create new combobox object
class newComboBox:
    def __init__(self, page, x, y, width, height, fontStyle="", fontSize=""):
        #Initialize new instance of ComboBox UI
        self.combo = QComboBox(page)
        #Set ComboBox x & y position and size
        self.combo.setGeometry(x, y, width, height)
        #Allows user to key values into ComboBox
        self.combo.setEditable(True)
        #Prevent user input from being added into ComboBox
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        #Make ComboBox empty
        self.combo.setPlaceholderText(" ")
        #Filter combobox options
        self.filter = QSortFilterProxyModel(self.combo)
        #Set filter case sensitivity to accept both upper and lower case
        self.filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        #Used to display recommendation as users starts typing
        self.filter.setSourceModel(self.combo.model())
        #Auto complete user input
        self.completer = QCompleter(self.filter, self.combo)
        #Set auto complete case sensitivity to accept both upper and lower case
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.combo.setCompleter(self.completer)
        #Start filtering if text in ComboBox is edited
        self.combo.lineEdit().textEdited.connect(self.filter.setFilterFixedString)
        #Call auto complete function if user hits enter
        self.completer.activated.connect(self.autoComplete)
        if fontStyle and fontSize:
            self.setFont(fontStyle, fontSize)

    def autoComplete(self, text):
        if text:
            index = self.combo.findText(text)
            self.combo.setCurrentIndex(index)

    def setFont(self, fontStyle, fontSize):
        #Set font style and font size of text
        self.combo.setFont(QFont(fontStyle,int(fontSize)))

#Class to create new messagebox object
class newMessageBox:
    def __init__(self, winTitle, text, winIcon="" , msgIcon="Critical"):
        #Initialized a new instance of message box UI
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle(winTitle)
        self.msgBox.setText(text)
        if winIcon:
            self.msgBox.setWindowIcon(QtGui.QIcon(winIcon))
        if msgIcon == "Critical":
            self.msgBox.setIcon(QMessageBox.Critical)
        self.msgBox.exec_()

    def show(self):
        """! set the messagebox to be visible
        """
        msgBox = self.msgBox
        msgBox.exec_()

#Class to create new table object
class newTable:
    def __init__(self, page, x, y, width, height):
        self.table = QTableWidget(page)
        self.table.setGeometry(x, y, width, height)
        self.table.verticalHeader().setDefaultSectionSize(20)
        self.table.horizontalHeader().setDefaultSectionSize(273)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def addData(self, data, col):
        rowCount = 0
        colCount = col
        for x in data:
            self.table.setItem(rowCount, colCount, QTableWidgetItem(str(x)))
            self.table.item(rowCount, colCount).setTextAlignment(Qt.AlignCenter)
            rowCount += 1
    
    def addRow(self, numRow):
        self.table.setRowCount(numRow)
    
    def addCol(self, numCol):
        self.table.setColumnCount(numCol)

class newRadioButton:
    def __init__(self, page, x, y, width, height, text, fontStyle="", fontSize=""):
        self.radio = QRadioButton(text, page)
        self.radio.setGeometry(x, y, width, height)
        if fontStyle and fontSize:
            self.setFont(fontStyle, fontSize)

    def setFont(self, fontStyle, fontSize):
        #Set font style and font size of radiobutton
        self.radio.setFont(QFont(fontStyle, fontSize))