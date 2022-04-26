import csv
import webbrowser
from widgets import *
from Backtracking import Backtracking
from Dijkstra import Dijkstra
from graph import Graph, mrtList
from AStar import AStarMap

class window:

    #Widget Dimensions
    __winWidth = 1080
    __winHeight = 720
    __logoWidth = 400
    __logoHeight = 90
    __buttonWidth = 150
    __buttonHeight = 80
    __textWidth = 400
    __textHeight = 40
    __labelWidth = 150
    __labelHeight = 40
    __comboWidth = 400
    __comboHeight = 40
    __tableWidth = 300
    __tableHeight = 500
    __radioWidth = 150
    __radioHeight = 40

    #Widget Coordinates
    __logoX = (__winWidth - __logoWidth) / 2
    __logoY = (__winHeight - __logoHeight) / 4
    __comboX = __logoX
    __comboY = __logoY + 100
    __labelX = __comboX - 150
    __labelY = __comboY
    __buttonX = __comboX
    __buttonY = __comboY + 100
    __tableX = (__winWidth - __tableWidth) / 2
    __tableY = 100
    __radioX = __comboX
    __radioY = __comboY + 130

    tag = "MRTBUS"

    #Button functions
    def nextFunction(self):
        if self.mrtRadio.radio.isChecked():
            self.tag = "MRT"
        if self.busRadio.radio.isChecked():
            self.tag = "BUS"
        if self.mrtBusRadio.radio.isChecked():
            self.tag = "MRTBUS"
        conjested = self.conjestCombo.combo.currentText()
        self.graph1 = Graph("graph.csv",self.tag, conjested)
        self.mainWin()
        self.stackWidget.setCurrentPage(self.mainPage)

    def searchClicked(self):
        startLoc = self.startCombo.combo.currentText()
        destLoc = self.destCombo.combo.currentText()
        if startLoc and destLoc in self.locations:
            #Dijkstra
            temp = Dijkstra(self.graph1, startLoc)
            dijkPath = temp.find_path(destLoc)
            self.dijkCost = "Time taken: " + str(round(float(dijkPath[0]), 2)) + "mins", "Total Cost: $" + str(round(float(dijkPath[1]), 2))
            self.dijkCostLabel.setText(str(self.dijkCost))
            self.dijkTable.addRow(len(dijkPath[2:]))
            self.dijkTable.addCol(1)
            self.dijkTable.addData(dijkPath[2:], 0)

            #Backtracking
            back_tracker = Backtracking()
            pathShort = back_tracker.find_shortest_path(self.graph1.adjList, startLoc, destLoc, 0, 0)
            self.btCost = "Time taken: " + str(round(float(pathShort[0]), 2)) + "mins", "Total Cost: $" + str(round(float(pathShort[1]), 2))
            self.backTrackingLabel.setText(str(self.btCost))
            self.backTrackTable.addRow(len(pathShort[2:]))
            self.backTrackTable.addCol(1)
            self.backTrackTable.addData(pathShort[2:], 0)

            #Astar
            astar = AStarMap(self.graph1, startLoc)
            timePath = astar.FindPath(destLoc, True)
            self.astarCost = "Time taken: " + str(round(float(timePath[0]), 2)) + "mins", "Total Cost: $" + str(round(float(timePath[1]), 2))
            self.astarCostLabel.setText(str(self.astarCost))
            self.aStarTable.addRow(len(timePath[2:]))
            self.aStarTable.addCol(1)
            self.aStarTable.addData(timePath[2:], 0)
            self.stackWidget.setCurrentPage(self.resultPage)

        else:
            msgBox = newMessageBox("Error!", "Invalid input! Please check again!", "winIcon.PNG")

    def backClicked(self):
        self.stackWidget.setCurrentPage(self.mainPage)

    #Call function to setup UI
    def setupUI(self, window):
        window.setWindowIcon("winIcon.PNG")
        self.cenWidget = QtWidgets.QWidget(window.win)
        window.win.setCentralWidget(self.cenWidget)
        self.stackWidget = newStackWidget(self.cenWidget, 0, 0, self.__winWidth, self.__winHeight)
        self.firstWin()
        self.resultWin()
        self.stackWidget.setCurrentPage(self.firstPage)

    #Call function to setup main window
    def mainWin(self):
        self.mainPage = newWidgetPage()
        self.locations = self.graph1.adjList
        self.mainlogo = newLabel(self.mainPage.page, self.__logoX, self.__logoY, self.__logoWidth, self.__logoHeight, "", "mainLogo.PNG")
        self.startCombo = newComboBox(self.mainPage.page, self.__comboX, self.__comboY, self.__comboWidth, self.__comboHeight, "Ariel", 10)
        self.startCombo.combo.addItems(self.locations)
        self.destCombo = newComboBox(self.mainPage.page, self.__comboX, self.__comboY+50, self.__comboWidth, self.__comboHeight, "Ariel", 10)
        self.destCombo.combo.addItems(self.locations)
        self.startLabel = newLabel(self.mainPage.page, self.__labelX-10, self.__labelY, self.__labelWidth+100, self.__labelHeight, "Select Starting Point:", "", "Ariel", 10)
        self.destLabel = newLabel(self.mainPage.page, self.__labelX+4, self.__labelY+50, self.__labelWidth, self.__labelHeight, "Select Destination:", "", "Ariel", 10)
        self.searchButton = newPushButton(self.mainPage.page, self.__buttonX+105, self.__buttonY, self.__buttonWidth, self.__buttonHeight, self.searchClicked, "Search", "Ariel", 10)
        self.stackWidget.addPage(self.mainPage.page)

    def resultWin(self):
        self.resultPage = newWidgetPage()
        self.dijkTable = newTable(self.resultPage.page, self.__tableX, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.aStarTable = newTable(self.resultPage.page, self.__tableX+340, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.backTrackTable = newTable(self.resultPage.page, self.__tableX-340, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.backButton = newPushButton(self.resultPage.page, self.__buttonX+358, self.__buttonY+250, self.__buttonWidth, self.__buttonHeight, self.backClicked, "Back", "Ariel", 10)
        self.backTrackingImage = newLabel(self.resultPage.page, self.__labelX-135, self.__labelY-220, self.__labelWidth+100, self.__labelHeight, "", "backTracking.png")
        self.dijkPathImage = newLabel(self.resultPage.page, self.__labelX+205, self.__labelY-220, self.__labelWidth+100, self.__labelHeight, "", "dijkPath.png")
        self.aStarPathImage = newLabel(self.resultPage.page, self.__labelX+545, self.__labelY-220, self.__labelWidth+100, self.__labelHeight, "", "astarDirection.png")
        self.backTrackingLabel = newLabel(self.resultPage.page, self.__labelX-135, self.__labelY-190, self.__labelWidth+150, self.__labelHeight, " ")
        self.astarCostLabel = newLabel(self.resultPage.page, self.__labelX+545, self.__labelY-190, self.__labelWidth+150, self.__labelHeight, " ")
        self.dijkCostLabel = newLabel(self.resultPage.page, self.__labelX+205, self.__labelY-190, self.__labelWidth+150, self.__labelHeight, " ")
        self.stackWidget.addPage(self.resultPage.page)

    def firstWin(self):
        self.firstPage = newWidgetPage()
        self.firstWinLogo = newLabel(self.firstPage.page, self.__logoX, self.__logoY, self.__logoWidth, self.__logoHeight, "", "mainLogo.PNG")
        self.mrtBusRadio = newRadioButton(self.firstPage.page, self.__radioX, self.__radioY-90, self.__radioWidth, self.__radioHeight, "MRT && Bus", "Ariel", 10)
        self.mrtRadio = newRadioButton(self.firstPage.page, self.__radioX+120, self.__radioY-90, self.__radioWidth, self.__radioHeight, "MRT Only", "Ariel", 10)
        self.busRadio = newRadioButton(self.firstPage.page, self.__radioX+230, self.__radioY-90, self.__radioWidth, self.__radioHeight, "Bus Only", "Ariel", 10)
        self.mrtBusRadio.radio.setChecked(True)
        self.conjestLabel = newLabel(self.firstPage.page, self.__labelX+30, self.__labelY, self.__labelWidth, self.__labelHeight, "Conjested MRT:", "", "Ariel", 10)
        self.locations = mrtList("graph.csv")
        self.locations2 = self.filterMRT(self.locations.dropdown)
        self.conjestCombo = newComboBox(self.firstPage.page, self.__comboX, self.__comboY, self.__comboWidth, self.__comboHeight, "Ariel", 10)
        self.conjestCombo.combo.addItems(self.locations2)
        self.nextButton = newPushButton(self.firstPage.page, self.__buttonX+250, self.__buttonY, self.__buttonWidth, self.__buttonHeight, self.nextFunction, "Next", "Ariel", 10)
        self.traffcLinkButton = newPushButton(self.firstPage.page, self.__buttonX, self.__buttonY, self.__buttonWidth, self.__buttonHeight, self.openLink, "Check Traffic", "Ariel", 10)
        self.stackWidget.addPage(self.firstPage.page)

    def filterMRT(self, locations):
        a = []
        for x in locations:
            if x not in a:
                a.append(x)
        return a

    def openLink(self):
        webbrowser.open_new("https://mrt.sg/news")
