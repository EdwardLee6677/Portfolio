import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class DataPreprocessingDialog(QDialog):
    def __init__(self, parent=None):
        super(DataPreprocessingDialog, self).__init__(parent)

        self.df = None
        self.delimiter = ','

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.delimiter_label = QLabel('Delimiter:', self)
        self.delimiter_input = QComboBox(self)
        self.delimiter_input.addItems([',', ';', '\t', '|'])  # Predefined delimiter options
        vbox.addWidget(self.delimiter_label)
        vbox.addWidget(self.delimiter_input)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.applyPreprocessing)
        vbox.addWidget(self.ok_button)

        self.setLayout(vbox)
        self.setWindowTitle('Data Preprocessing')

    def applyPreprocessing(self):
        self.delimiter = self.delimiter_input.currentText()
        self.loadAndPreprocessData()
        self.accept()

    def loadAndPreprocessData(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            try:
                self.df = pd.read_csv(file_path, delimiter=self.delimiter)
            except Exception as e:
                print("Error while loading the file:", e)


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super(DataAnalysisApp, self).__init__()

        self.df = None

        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        main_widget.setFixedSize(1024, 768)  # Set the fixed size for the main window
        self.setCentralWidget(main_widget)

        vbox = QVBoxLayout()

        self.table_widget = QTableWidget(self)
        vbox.addWidget(self.table_widget)

        self.result_label = QLabel('Analysis Result:', self)
        vbox.addWidget(self.result_label)

        self.result_text_widget = QTextEdit(self)  # Use QTextEdit for displaying text results
        vbox.addWidget(self.result_text_widget)

        hbox = QHBoxLayout()
        load_button = QPushButton('Load', self)
        load_button.clicked.connect(self.loadData)
        hbox.addWidget(load_button)

        vbox.addLayout(hbox)
        main_widget.setLayout(vbox)

        self.setWindowTitle('Data Analysis App')

    def loadData(self):
        dialog = DataPreprocessingDialog(self)
        if dialog.exec_():
            self.df = dialog.df
            self.displayData()

    def displayData(self):
        if self.df is not None:
            self.table_widget.clear()
            self.table_widget.setColumnCount(len(self.df.columns))
            self.table_widget.setRowCount(3)

            for col_idx, col_name in enumerate(self.df.columns):
                for row_idx, data in enumerate(['attribute', str(self.df.dtypes[col_name]), 'true']):
                    item = QTableWidgetItem(data)
                    self.table_widget.setItem(row_idx, col_idx, item)

            self.table_widget.setVerticalHeaderLabels(['Role', 'Type', 'Usage'])
            self.table_widget.setHorizontalHeaderLabels(self.df.columns)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataAnalysisApp()
    mainWindow.show()
    sys.exit(app.exec_())
