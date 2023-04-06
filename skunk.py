from systemVariables import systemVariables
from documentProcessor import *

from os import listdir, startfile
from os.path import basename, dirname, realpath
from re import match
from sys import exit, argv
from time import sleep
from tkinter import Tk, filedialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *





class mainApplication(QMainWindow):
    
    def __init__(self):
        
        
        super().__init__()
        
        self.createCommonVariables()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setFixedSize(systemVariables.appDimension[0], systemVariables.appDimension[1])
        
        self.styleSheet = systemVariables.stylesheet
        self.setStyleSheet(self.styleSheet)
        
        
        self.createMainUserInterface()
    
    
    
    
    
    def createCommonVariables(self):
        
        self.currentDirectory = dirname(realpath(__file__))
        
        self.listOfFiles = []
        self.filesPresent = False
        self.payload = []
        self.currentQueryIndex = 0
        self.changeQueryIndex = False
        
        self.holdTimer = QTimer()
        self.holdTimer.setInterval(2500)
    
    
    
    
    
    def clickSelectFromDirectoryButton(self):
        
        directory = filedialog.askdirectory()
        stringDirectory = str(directory)
        self.listOfFiles = []
        if directory:
            directory = listdir(directory)
        for file in directory:
            if file.endswith('.txt'):
                self.listOfFiles.append(stringDirectory + '\\' + file)
        if len(self.listOfFiles) == 0:
            self.filesPresent = False
            self.selectDirectory.setChecked(False)
        else:
            self.filesPresent = True
            self.selectDirectory.setChecked(True)
            self.selectFiles.setChecked(False)
    
    
    
    def clickSelectFromFilesButton(self):
        
        directory = filedialog.askopenfilenames()
        self.listOfFiles = []
        for file in directory:
            if file.endswith('.txt'):
                self.listOfFiles.append(file)
            print(file)
        if len(self.listOfFiles) == 0:
            self.filesPresent = False
            self.selectFiles.setChecked(False)
        else:
            self.filesPresent = True
            self.selectFiles.setChecked(True)
            self.selectDirectory.setChecked(False)
    
    
    
    def clickSelectDynamicIndexButton(self):
        self.dynamicIndexButton.setChecked(True)
        self.termPartitionedIndexButton.setChecked(False)
    
    
    
    def clickSelectTPIndexButton(self):
        self.termPartitionedIndexButton.setChecked(True)
        self.dynamicIndexButton.setChecked(False)
    
    
    
    def clickExecuteButton(self):
        
        if not self.filesPresent:
            return
        
        self.payload = []
        for path in self.listOfFiles:
            currentDocument = [path]
            with open(path, 'r', encoding = 'utf--8', errors = 'ignore') as document:
                currentDocument.append(document.read())
            self.payload.append(currentDocument)
        
        self.termsScrollableWidget = QScrollArea(self.mainStackedWidget)
        self.termsScrollableWidget.setObjectName('emptyContainerWidget')
        self.termsScrollableWidget.setFixedSize(self.mainStackedWidget.width(), self.mainStackedWidget.height())
        self.termsContainerWidget = QWidget(self.mainStackedWidget)
        self.termsContainerWidget.setObjectName('emptyContainerWidget')
        self.termsContainerWidget.setFixedWidth(self.termsScrollableWidget.width())
        self.termsContainerLayout = QVBoxLayout()
        self.termsContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.termsContainerLayout.setSpacing(20)
        
        if self.termPartitionedIndexButton.isChecked():
            indexer = termPartitionedIndex(self.payload)
            for term, totalCount, documentCount in indexer.termIndex:
                
                termContainerWidget = QWidget(self.termsContainerWidget)
                termContainerWidget.setObjectName('containerWidget')
                termContainerWidget.setFixedSize(self.termsContainerWidget.width(), 30 + 20 + (35 * len(documentCount)))
                termLabel = QLabel(termContainerWidget)
                termLabel.setObjectName('termLabel')
                termLabel.setFixedHeight(20)
                termLabel.move(10, 10)
                termLabel.setText(term)
                termCountLabel = QLabel(termContainerWidget)
                termCountLabel.setObjectName('termCountLabel')
                termCountLabel.setFixedSize(100, 20)
                termCountLabel.move(termContainerWidget.width() - 10 - 100, 10)
                termCountLabel.setText("Count: " + str(len(documentCount)))
                termCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                for currentIndex, index in enumerate(documentCount):
                    fileContainer = QWidget(termContainerWidget)
                    fileContainer.setObjectName('fileContainerWidget')
                    fileContainer.setFixedSize(termContainerWidget.width() - 20, 30)
                    fileContainer.move(10, 50 + 35 * currentIndex)
                    fileName = QLabel(fileContainer)
                    fileName.setObjectName('fileNameLabel')
                    fileName.setMaximumWidth(fileContainer.width() - 100)
                    fileName.setFixedHeight(20)
                    fileName.move(0, 5)
                    fileName.setText(str(basename(indexer.documentLocation[index[0]])))
                    fileName.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    openFileButton = QPushButton(fileContainer)
                    openFileButton.setObjectName('tealButton')
                    openFileButton.setFixedSize(80, 20)
                    openFileButton.setText('OPEN FILE')
                    openFileButton.move(fileContainer.width() - 10 - 80, 5)
                    openFileButton.clicked.connect(lambda checked, argument = indexer.documentLocation[index[0]]: startfile(argument))
                
                self.termsContainerLayout.addWidget(termContainerWidget)
        else:
            indexer = dynamicIndex(self.payload)
            for term, documents in indexer.termIndex:
                
                documents = documents.split(', ')
                termContainerWidget = QWidget(self.termsContainerWidget)
                termContainerWidget.setObjectName('containerWidget')
                termContainerWidget.setFixedSize(self.termsContainerWidget.width(), 30 + 20 + (35 * len(documents)))
                termLabel = QLabel(termContainerWidget)
                termLabel.setObjectName('termLabel')
                termLabel.setFixedHeight(20)
                termLabel.move(10, 10)
                termLabel.setText(term)
                termCountLabel = QLabel(termContainerWidget)
                termCountLabel.setObjectName('termCountLabel')
                termCountLabel.setFixedSize(100, 20)
                termCountLabel.move(termContainerWidget.width() - 10 - 100, 10)
                termCountLabel.setText("Count: " + str(len(documents)))
                termCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                for currentIndex, index in enumerate(documents):
                    fileContainer = QWidget(termContainerWidget)
                    fileContainer.setObjectName('fileContainerWidget')
                    fileContainer.setFixedSize(termContainerWidget.width() - 20, 30)
                    fileContainer.move(10, 50 + 35 * currentIndex)
                    fileName = QLabel(fileContainer)
                    fileName.setObjectName('fileNameLabel')
                    fileName.setMaximumWidth(fileContainer.width() - 100)
                    fileName.setFixedHeight(20)
                    fileName.move(0, 5)
                    fileName.setText(str(basename(indexer.documentLocation[int(index)])))
                    fileName.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    openFileButton = QPushButton(fileContainer)
                    openFileButton.setObjectName('tealButton')
                    openFileButton.setFixedSize(80, 20)
                    openFileButton.setText('OPEN FILE')
                    openFileButton.move(fileContainer.width() - 10 - 80, 5)
                    openFileButton.clicked.connect(lambda checked, argument = indexer.documentLocation[int(index)]: startfile(argument))
                
                self.termsContainerLayout.addWidget(termContainerWidget)
        self.termsContainerWidget.setLayout(self.termsContainerLayout)
        self.termsScrollableWidget.setWidget(self.termsContainerWidget)
        self.termsScrollableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.termsScrollableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.mainStackedWidget.addWidget(self.termsScrollableWidget)
        self.mainStackedWidget.setCurrentWidget(self.termsScrollableWidget)
    
    
    
    
    def createMainUserInterface(self):
        
        sidePanelWidget = QWidget(self)
        sidePanelWidget.setObjectName('containerWidget')
        sidePanelWidget.setFixedSize(200, self.height() - 40)
        sidePanelWidget.move(20, 20)
        
        logoPixmap = QPixmap(self.currentDirectory + r'\Images\Logo.png')
        logoLabel = QLabel(sidePanelWidget)
        logoLabel.setPixmap(logoPixmap)
        logoLabel.resize(logoPixmap.width(), logoPixmap.height())
        logoLabel.move((200 - logoPixmap.width()) // 2, 40)
        
        fileUploadWidget = QWidget(sidePanelWidget)
        fileUploadWidget.setObjectName('emptyContainerWidget')
        fileUploadWidget.setFixedWidth(sidePanelWidget.width() - 20)
        fileUploadWidget.move(10, 40 + logoPixmap.height() + 70)
        fileUploadLabel = QLabel(fileUploadWidget)
        fileUploadLabel.setObjectName('mainLabel')
        fileUploadLabel.setText('Search from...')
        self.selectDirectory = QPushButton(fileUploadWidget)
        self.selectDirectory.setObjectName('defaultButton')
        self.selectDirectory.setFixedHeight(20)
        self.selectDirectory.setText('DIRECTORY')
        self.selectDirectory.setCheckable(True)
        self.selectDirectory.move(0, fileUploadLabel.height() - 0)
        self.selectDirectory.clicked.connect(self.clickSelectFromDirectoryButton)
        self.selectFiles = QPushButton(fileUploadWidget)
        self.selectFiles.setObjectName('defaultButton')
        self.selectFiles.setFixedHeight(20)
        self.selectFiles.setText('FILES')
        self.selectFiles.setCheckable(True)
        self.selectFiles.move(90, fileUploadLabel.height() - 0)
        self.selectFiles.clicked.connect(self.clickSelectFromFilesButton)
        
        indexTypeWidget = QWidget(sidePanelWidget)
        indexTypeWidget.setObjectName('emptyContainerWidget')
        indexTypeWidget.setFixedWidth(sidePanelWidget.width() - 20)
        indexTypeWidget.move(10, 40 + logoPixmap.height() + 70 + fileUploadWidget.height() + 50)
        indexTypeLabel = QLabel(indexTypeWidget)
        indexTypeLabel.setObjectName('mainLabel')
        indexTypeLabel.setText('Select an indexing type')
        self.dynamicIndexButton = QPushButton(indexTypeWidget)
        self.dynamicIndexButton.setObjectName('defaultButton')
        self.dynamicIndexButton.setFixedHeight(20)
        self.dynamicIndexButton.setText('DYNAMIC')
        self.dynamicIndexButton.setCheckable(True)
        self.dynamicIndexButton.move(0, indexTypeLabel.height() - 0)
        self.dynamicIndexButton.setChecked(True)
        self.dynamicIndexButton.clicked.connect(self.clickSelectDynamicIndexButton)
        self.termPartitionedIndexButton = QPushButton(indexTypeWidget)
        self.termPartitionedIndexButton.setObjectName('defaultButton')
        self.termPartitionedIndexButton.setFixedHeight(20)
        self.termPartitionedIndexButton.setText('T-PARTITIONED')
        self.termPartitionedIndexButton.setCheckable(True)
        self.termPartitionedIndexButton.move(75, indexTypeLabel.height() - 0)
        self.termPartitionedIndexButton.clicked.connect(self.clickSelectTPIndexButton)
        
        self.executeButton = QPushButton(sidePanelWidget)
        self.executeButton.setObjectName('tealButton')
        self.executeButton.setFixedSize(sidePanelWidget.width() - 20, 20)
        self.executeButton.setText('EXECUTE')
        # self.executeButton.move(10, 40 + logoPixmap.height() + 70 + fileUploadWidget.height() + 50 + indexTypeWidget.height() + 70)
        self.executeButton.move(10, sidePanelWidget.height() - 10 - 20)
        self.executeButton.clicked.connect(self.clickExecuteButton)
        
        self.mainStackedWidget = QStackedWidget(self)
        self.mainStackedWidget.setObjectName('emptyContainerWindow')
        self.mainStackedWidget.setFixedSize(self.width() - 20 - 20 - 200 - 20, self.height() - 40)
        self.mainStackedWidget.move(240, 20)
        self.noContentWidget = QWidget(self.mainStackedWidget)
        self.noContentWidget.setObjectName('emptyContainerWindow')
        self.noContentWidget.setFixedSize(self.mainStackedWidget.width(), self.mainStackedWidget.height())
        noContentLabel = QLabel(self.noContentWidget)
        noContentLabel.setObjectName('subLabel')
        noContentLabel.setMaximumWidth(300)
        noContentLabel.setText('Wow, such empty!\nAdd a few documents to view their term indices...')
        noContentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        noContentLabel.setWordWrap(True)
        noContentLabel.move((self.noContentWidget.width() - noContentLabel.width()) // 2, (self.noContentWidget.height() - noContentLabel.height()) // 2)
        self.mainStackedWidget.addWidget(self.noContentWidget)
        self.mainStackedWidget.setCurrentWidget(self.noContentWidget)
        
        





def startUp():
    
    application = QApplication(argv)
    applicationInitializer = mainApplication()
    applicationInitializer.show()
    exit(application.exec())
        
        
        


if __name__ == '__main__':
    
    try:
        startUp()
    
    except Exception as errorCode:
        print(f"An error has occured!\n{errorCode}")
        sleep(5)
        exit()