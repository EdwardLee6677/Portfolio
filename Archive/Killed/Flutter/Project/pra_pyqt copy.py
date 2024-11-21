import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMainWindow, QAction, qApp, QDesktopWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QTextEdit, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, QDateTime, QDate, Qt

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDateTime.currentDateTime()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        grid.addWidget(QLabel('Title:'), 0, 0)
        grid.addWidget(QLabel('Author:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        lbl_red = QLabel('Red')
        lbl_red.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 세로로 늘어남
        lbl_green = QLabel('Green')
        lbl_green.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 세로로 늘어남
        lbl_blue = QLabel('Blue')
        lbl_blue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 세로로 늘어남

        lbl_red.setStyleSheet("color: red;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: #FA8072;"
                             "border-radius: 3px")
        lbl_green.setStyleSheet("color: green;"
                               "background-color: #7FFFD4")
        lbl_blue.setStyleSheet("color: blue;"
                              "background-color: #87CEFA;"
                              "border-style: dashed;"
                              "border-width: 3px;"
                              "border-color: #1E90FF")

        grid.addWidget(lbl_red, 3, 0)  # 라벨 위젯을 원하는 위치에 배치
        grid.addWidget(lbl_green, 4, 0)  # 라벨 위젯을 원하는 위치에 배치
        grid.addWidget(lbl_blue, 5, 0)  # 라벨 위젯을 원하는 위치에 배치

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch(1)  # 상하로 늘어나도록 추가
        vbox.addLayout(hbox)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        exitAction = QAction(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(qApp.quit)

        saveAction = QAction(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save File')

        editAction = QAction(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/edit.png'), 'Edit', self)
        editAction.setShortcut('Ctrl+E')
        editAction.setStatusTip('Edit File')

        printAction = QAction(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/print.png'), 'Print', self)
        printAction.setShortcut('Ctrl+P')
        printAction.setStatusTip('Print File')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        filemenu.addAction(saveAction)
        editmenu = menubar.addMenu('&Edit')
        editmenu.addAction(editAction)
        viewmenu = menubar.addMenu('&View')
        toolmenu = menubar.addMenu('&Tools')
        toolmenu.addAction(printAction)
        helpmenu = menubar.addMenu('&Help')

        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(saveAction)

        self.toolbar = self.addToolBar('Edit')
        self.toolbar.addAction(editAction)

        self.toolbar = self.addToolBar('Print')
        self.toolbar.addAction(printAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(300, 90)
        btn.resize(btn.sizeHint())
    
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>Quit</b> widget')
        btn.move(400, 90)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        self.setWindowTitle('Project')
        # self.move(300, 300)
        # self.resize(400, 200)
        self.setWindowIcon(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/logo.png'))
        self.setGeometry(300, 300, 500, 350)

        self.center()

        self.show()

        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.show()
   sys.exit(app.exec_())
