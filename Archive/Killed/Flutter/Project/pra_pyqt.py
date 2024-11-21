import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDateTime.currentDateTime()
        self.initUI()

    def initUI(self):

        

        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel('Second Label', self)
        label2.setAlignment(Qt.AlignVCenter)

        font1 = label1.font()
        font1.setPointSize(20)

        font2 = label2.font()
        font2.setFamily('Times New Roman')
        font2.setBold(True)

        label1.setFont(font1)
        label2.setFont(font2)

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        btn1 = QPushButton('&Button1', self)
        btn1.setCheckable(True)
        btn1.toggle()

        btn2 = QPushButton(self)
        btn2.setText('Button&2')

        btn3 = QPushButton('Button3', self)
        btn3.setEnabled(False)

        

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

        label1 = QLabel('Label1', self)
        label1.move(40, 70)
        label2 = QLabel('Label2', self)
        label2.move(40, 110)

        btn11 = QPushButton('Button1', self)
        btn11.move(100, 70)
        btn22 = QPushButton('Button2', self)
        btn22.move(100, 110)

        lbl_red = QLabel('Red')
        lbl_green = QLabel('Green')
        lbl_blue = QLabel('Blue')

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
        
        # lbl_red.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # lbl_green.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # lbl_blue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # lbl_red.setFixedSize(180, 80)
        # lbl_green.setFixedSize(180, 80)
        # lbl_blue.setFixedSize(180, 80)

        lbl_red.setFixedHeight(80)
        lbl_red.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lbl_green.setFixedHeight(80)
        lbl_green.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        lbl_blue.setFixedHeight(80)
        lbl_blue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        
        vbox.addWidget(lbl_blue)
        vbox.addLayout(hbox)
        vbox.addLayout(grid)
        vbox.addLayout(layout)

        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        central_widget
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

        rbtn1 = QRadioButton('First Button', self)
        rbtn1.move(300, 165)
        rbtn1.setChecked(True)

        rbtn2 = QRadioButton(self)
        rbtn2.move(300, 185)
        rbtn2.setText('Second Button')

        self.lbl1 = QLabel('Option1', self)
        self.lbl1.move(80, 240)

        cb = QComboBox(self)
        cb.addItem('Option1')
        cb.addItem('Option2')
        cb.addItem('Option3')
        cb.addItem('Option4')
        cb.move(160, 240)

        cb.activated[str].connect(self.onActivated)

        self.setWindowTitle('Project')
        # self.move(300, 300)
        # self.resize(400, 200)
        self.setWindowIcon(QIcon('C:/Users/Edward/Desktop/PythonWorkspace/project/logo.png'))
        self.setGeometry(300, 300, 500, 350)
        
        cb = QCheckBox('Show title', self)
        cb.move(80, 175)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        self.lbl2 = QLabel(self)
        self.lbl2.move(80, 280)

        qle = QLineEdit(self)
        qle.move(160, 280)
        qle.textChanged[str].connect(self.onChanged)

        self.center()

        self.show() 
        
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('Project')
        else:
            self.setWindowTitle(' ')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onActivated(self, text):
        self.lbl1.setText(text)

    def onChanged(self, text):
        self.lbl2.setText(text)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   ex.show()
   sys.exit(app.exec_())

'''
여기서 self는 MyApp 객체를 말합니다.
setWindowTitle() 메서드는 타이틀바에 나타나는 창의 제목을 설정합니다.
move() 메서드는 위젯을 스크린의 x=300px, y=300px의 위치로 이동시킵니다.
resize() 메서드는 위젯의 크기를 너비 400px, 높이 200px로 조절합니다.
setWindowIcon() 메서드는 어플리케이션 아이콘을 설정하도록 합니다.
이를 위해서 QIcon 객체를 생성하였습니다. QIcon()에 보여질 이미지('logo.png')를 입력합니다.
이미지 파일을 다른 폴더에 따로 저장해 둔 경우에는 경로까지 함께 입력해주면 됩니다.
setGeometry() 메서드는 창의 위치와 크기를 설정합니다.
앞의 두 매개변수는 창의 x, y 위치를 결정하고, 뒤의 두 매개변수는 각각 창의 너비와 높이를 결정합니다.
이 메서드는 예제에서 사용했던 move()와 resize() 메서드를 하나로 합쳐놓은 것과 같습니다.
show() 메서드는 위젯을 스크린에 보여줍니다.
'__name__'은 현재 모듈의 이름이 저장되는 내장 변수입니다.
만약 'moduleA.py'라는 코드를 import해서 예제 코드를 수행하면 
__name__ 은 'moduleA'가 됩니다. 
그렇지 않고 코드를 직접 실행한다면 __name__ 은 __main__ 이 됩니다. 
따라서 이 한 줄의 코드를 통해 프로그램이 직접 실행되는지 
혹은 모듈을 통해 실행되는지를 확인합니다.
'''
