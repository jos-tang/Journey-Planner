import csv
import webbrowser
from widgets import *
from Backtracking import Backtracking
from Dijkstra import Dijkstra
from graph import Graph
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
    __tableWidth = 290
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
        self.graph1 = Graph("graph.csv",self.tag,"")
        self.mainWin()
        self.stackWidget.setCurrentPage(self.mainPage)

    def searchClicked(self):
        startLoc = self.startCombo.combo.currentText()
        destLoc = self.destCombo.combo.currentText()
        if startLoc and destLoc in self.locations:
            #Dijkstra
            temp = Dijkstra(self.graph1, startLoc)
            dijkPath = temp.find_path(destLoc)
            self.dijkTable.addRow(len(dijkPath[2:]))
            self.dijkTable.addCol(1)
            self.dijkTable.addData(dijkPath[2:], 0)

            #Backtracking
            back_tracker = Backtracking()
            pathShort = back_tracker.find_shortest_path(self.graph1.adjList, startLoc, destLoc, 0, 0)
            self.backTrackTable.addRow(len(pathShort[2:]))
            self.backTrackTable.addCol(1)
            self.backTrackTable.addData(pathShort[2:], 0)
            self.stackWidget.setCurrentPage(self.resultPage)

            #Astar
            astar = AStarMap(self.graph1, startLoc)
            timePath = astar.FindPath(destLoc, True)
            print("Astar Path")
            print (timePath)
            # self.aStarTable.addRow(len(timePath[2:]))
            # self.aStarTable.addCol(1)
            # self.aStarTable.addData(timePath[2:], 0)

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
        # self.locations = self.getLocation("graph.csv", self.tag)
        self.locations = self.graph1.adjList
        self.mainlogo = newLabel(self.mainPage.page, self.__logoX, self.__logoY, self.__logoWidth, self.__logoHeight, "", "mainLogo.PNG")
        self.startCombo = newComboBox(self.mainPage.page, self.__comboX, self.__comboY, self.__comboWidth, self.__comboHeight, "Ariel", 12)
        self.startCombo.combo.addItems(self.locations)
        self.destCombo = newComboBox(self.mainPage.page, self.__comboX, self.__comboY+50, self.__comboWidth, self.__comboHeight, "Ariel", 12)
        self.destCombo.combo.addItems(self.locations)
        self.startLabel = newLabel(self.mainPage.page, self.__labelX, self.__labelY, self.__labelWidth, self.__labelHeight, "Select Starting Point:", "", "Ariel", 12)
        self.destLabel = newLabel(self.mainPage.page, self.__labelX+16, self.__labelY+50, self.__labelWidth, self.__labelHeight, "Select Destination:", "", "Ariel", 12)
        self.searchButton = newPushButton(self.mainPage.page, self.__buttonX+250, self.__buttonY+100, self.__buttonWidth, self.__buttonHeight, self.searchClicked, "Search", "Ariel", 12)
        # self.mrtBusRadio.radio.setChecked(True)
        self.stackWidget.addPage(self.mainPage.page)

    def resultWin(self):
        self.resultPage = newWidgetPage()
        self.dijkTable = newTable(self.resultPage.page, self.__tableX, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.aStarTable = newTable(self.resultPage.page, self.__tableX+340, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.backTrackTable = newTable(self.resultPage.page, self.__tableX-340, self.__tableY, self.__tableWidth, self.__tableHeight)
        self.backButton = newPushButton(self.resultPage.page, self.__buttonX+358, self.__buttonY+250, self.__buttonWidth, self.__buttonHeight, self.backClicked, "Back", "Ariel", 12)
        self.btLinkButton = newPushButton(self.resultPage.page, self.__buttonX-107, self.__buttonY+250, self.__buttonWidth, self.__buttonHeight, self.openLink, "Check Traffic", "Ariel", 12)
        self.shortestPathImage = newLabel(self.resultPage.page, self.__labelX-135, self.__labelY-195, self.__labelWidth+50, self.__labelHeight-5, "", "shortestPath.png")
        self.dijkPathImage = newLabel(self.resultPage.page, self.__labelX+205, self.__labelY-200, self.__labelWidth+100, self.__labelHeight, "", "dijkPath.png")
        self.stackWidget.addPage(self.resultPage.page)

    def firstWin(self):
        self.firstPage = newWidgetPage()
        self.mrtBusRadio = newRadioButton(self.firstPage.page, self.__radioX, self.__radioY, self.__radioWidth, self.__radioHeight, "MRT && Bus", "Ariel", 12)
        self.mrtRadio = newRadioButton(self.firstPage.page, self.__radioX+110, self.__radioY, self.__radioWidth, self.__radioHeight, "MRT Only", "Ariel", 12)
        self.busRadio = newRadioButton(self.firstPage.page, self.__radioX+210, self.__radioY, self.__radioWidth, self.__radioHeight, "Bus Only", "Ariel", 12)
        self.conjestLabel = newLabel(self.firstPage.page, self.__labelX+34, self.__labelY+100, self.__labelWidth, self.__labelHeight, "Conjested MRT:", "", "Ariel", 12)
        # self.locations2 = self.filterBus(self.locations)
        # self.conjestCombo = newComboBox(self.firstPage.page, self.__comboX, self.__comboY+100, self.__comboWidth, self.__comboHeight, "Ariel", 12)
        # self.conjestCombo.combo.addItems(self.locations2)
        self.nextButton = newPushButton(self.firstPage.page, self.__buttonX, self.__buttonY+300, self.__buttonWidth, self.__buttonHeight, self.nextFunction, "Next", "Ariel", 12)
        self.stackWidget.addPage(self.firstPage.page)

    def getLocation(self, file, tag):
        # filename = open("graph.csv", "r")
        # file = csv.DictReader(filename)
        # tempArr = []
        # locArr = []
        # for col in file:
        #     tempArr.append(col["Pasir ris"])
        # locArr.append("Pasir ris")
        # for x in tempArr:
        #     if x not in locArr:
        #         locArr.append(x)
        # return locArr
        # g = Graph("graph.csv", tag,"")
        # return g.adjList
        pass

    def filterBus(self, locations):
        temp = [x for x in locations if "Bus" in x]
        for y in temp:
            del locations[y]
        return locations

    def openLink(self):
        webbrowser.open_new("https://www.tomtom.com/en_gb/traffic-index/singapore-traffic/")
