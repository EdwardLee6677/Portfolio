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

        self.delimiter_label = QLabel('Delimiter:')
        self.delimiter_input = QLineEdit(',')
        vbox.addWidget(self.delimiter_label)
        vbox.addWidget(self.delimiter_input)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.applyPreprocessing)
        vbox.addWidget(self.ok_button)

        self.setLayout(vbox)
        self.setWindowTitle('Data Preprocessing')

    def applyPreprocessing(self):
        self.delimiter = self.delimiter_input.text()
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
        self.data_roles = {}
        self.data_types = {}
        self.data_usage = {}

        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        vbox = QVBoxLayout()

        self.table_widget = QTableWidget(self)
        vbox.addWidget(self.table_widget)

        self.result_label = QLabel('Analysis Result:', self)
        vbox.addWidget(self.result_label)

        self.result_text_widget = QTableWidget(self)
        vbox.addWidget(self.result_text_widget)

        hbox = QHBoxLayout()
        load_button = QPushButton('Load', self)
        load_button.clicked.connect(self.loadData)
        hbox.addWidget(load_button)

        run_button = QPushButton('Run', self)
        run_button.clicked.connect(self.runAnalysis)
        hbox.addWidget(run_button)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.saveResult)
        hbox.addWidget(save_button)

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
            self.table_widget.setRowCount(len(self.df.index) + 3)  # Add 3 for Role, Type, Usage

            self.data_roles = {}
            self.data_types = {}
            self.data_usage = {}

            for col_idx, col_name in enumerate(self.df.columns):
                role_combo = QComboBox(self)
                role_combo.addItems(['label', 'attribute'])
                role_combo.setCurrentText('attribute')
                self.data_roles[col_idx] = role_combo

                type_combo = QComboBox(self)
                type_combo.addItems(['float', 'int', 'str', 'date', 'datetime'])
                type_combo.setCurrentText(str(self.df.dtypes[col_name]))
                self.data_types[col_idx] = type_combo

                usage_combo = QComboBox(self)
                usage_combo.addItems(['true', 'false'])
                usage_combo.setCurrentText('true')
                self.data_usage[col_idx] = usage_combo

                for row_idx in range(len(self.df.index)):
                    item = QTableWidgetItem(str(self.df.iat[row_idx, col_idx]))
                    self.table_widget.setItem(row_idx + 3, col_idx, item)

            self.table_widget.setVerticalHeaderLabels(['Role', 'Type', 'Usage'] + self.df.index.astype(str).tolist())
            self.table_widget.setHorizontalHeaderLabels(self.df.columns)


    def runAnalysis(self):
        if self.df is not None:
            # Implement data analysis algorithms (linear regression, logistic regression, etc.) here
            # Display the results in the 'self.result_text_widget'
            pass

    def saveResult(self):
        if self.df is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "Text Files (*.txt);;Docs Files (*.docs);;HWP Files (*.hwp);;PNG Files (*.png);;PDF Files (*.pdf);;All Files (*)", options=options)
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        f.write("Write your analysis result here.")
                    print("Result saved successfully.")
                except Exception as e:
                    print("Error while saving the file:", e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
