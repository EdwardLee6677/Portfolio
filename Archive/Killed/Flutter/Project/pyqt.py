import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QFileDialog, QDialog, QLabel, QComboBox, QTextEdit, QFormLayout


class MetaDataDialog(QDialog):
    def __init__(self, df, parent=None):
        super(MetaDataDialog, self).__init__(parent)

        self.df = df.copy()

        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.role_input = QComboBox(self)
        self.role_input.addItems(['attribute', 'label'])
        layout.addWidget('Role:', self.role_input)

        self.data_type_input = QComboBox(self)
        self.data_type_input.addItems(['float', 'int', 'str', 'date', 'datetime'])
        layout.addWidget('Data Type:', self.data_type_input)

        self.usage_input = QComboBox(self)
        self.usage_input.addItems(['true', 'false'])
        layout.addWidget('Usage:', self.usage_input)

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.clicked.connect(self.applyMetaData)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)
        self.setWindowTitle('Metadata Configuration')

    def applyMetaData(self):
        selected_role = self.role_input.currentText()
        selected_data_type = self.data_type_input.currentText()
        selected_usage = self.usage_input.currentText()

        for col_name in self.df.columns:
            if selected_role == 'label' and self.df[col_name].nunique() > 1:
                error_dialog = QDialog(self)
                error_dialog.setWindowTitle('Error')
                error_dialog.setLayout(QVBoxLayout())
                error_dialog.layout().addWidget(QLabel('Error: Multiple labels are not allowed.'))
                error_dialog.exec_()
                return

            self.df[col_name] = self.df[col_name].astype(selected_data_type)

        self.df['Usage'] = (self.df['Usage'] == 'true')

        self.accept()


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super(DataAnalysisApp, self).__init__()

        self.df = None

        self.initUI()

    def initUI(self):
        main_widget = QWidget(self)
        main_widget.setFixedSize(1024, 768)
        self.setCentralWidget(main_widget)

        vbox = QVBoxLayout()

        self.table_widget = QTableWidget(self)
        vbox.addWidget(self.table_widget)

        self.result_label = QLabel('Analysis Result:', self)
        vbox.addWidget(self.result_label)

        self.result_text_widget = QTextEdit(self)
        vbox.addWidget(self.result_text_widget)

        hbox = QHBoxLayout()

        load_button = QPushButton('Load', self)
        load_button.clicked.connect(self.showLoadDialog)
        hbox.addWidget(load_button)

        metadata_button = QPushButton('Metadata', self)
        metadata_button.clicked.connect(self.showMetaDataDialog)
        hbox.addWidget(metadata_button)

        run_button = QPushButton('Run', self)
        run_button.clicked.connect(self.runAnalysis)
        hbox.addWidget(run_button)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.saveAnalysis)
        hbox.addWidget(save_button)

        vbox.addLayout(hbox)
        main_widget.setLayout(vbox)

        self.setWindowTitle('Data Analysis App')

    def showLoadDialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_path:
            try:
                delimiter_dialog = QDialog(self)
                delimiter_dialog.setWindowTitle('Delimiter Selection')
                delimiter_dialog.setLayout(QFormLayout())
                
                delimiter_input = QComboBox(delimiter_dialog)
                delimiter_input.addItems([',', ';', '\t'])
                delimiter_dialog.addWidget('Delimiter:', delimiter_input)
                
                encoding_input = QComboBox(delimiter_dialog)
                encoding_input.addItems(['utf-8', 'latin1'])
                delimiter_dialog.addWidget('Encoding:', encoding_input)
                
                apply_button = QPushButton('Apply', delimiter_dialog)
                apply_button.clicked.connect(lambda: self.loadCSV(file_path, delimiter_input.currentText(),
                                                                  encoding_input.currentText()))
                delimiter_dialog.addWidget(apply_button)
                delimiter_dialog.exec_()
            except Exception as e:
                print("Error while loading the file:", e)

    def loadCSV(self, file_path, delimiter, encoding):
        try:
            self.df = pd.read_csv(file_path, nrows=10, delimiter=delimiter, encoding=encoding)
            self.displayData()
        except Exception as e:
            print("Error while loading the file:", e)

    def showMetaDataDialog(self):
        if self.df is not None:
            dialog = MetaDataDialog(self.df, self)
            if dialog.exec_():
                self.df = dialog.df
                self.displayData()

    def displayData(self):
        if self.df is not None:
            self.table_widget.clear()
            self.table_widget.setColumnCount(self.df.shape[1])
            self.table_widget.setRowCount(self.df.shape[0])

            for row_idx in range(self.df.shape[0]):
                for col_idx in range(self.df.shape[1]):
                    data = str(self.df.iloc[row_idx, col_idx])
                    item = QTableWidgetItem(data)
                    self.table_widget.setItem(row_idx, col_idx, item)

            self.table_widget.setHorizontalHeaderLabels(self.df.columns)

    def runAnalysis(self):
        # Implement the data analysis logic here
        if self.df is not None:
            result_text = "Analysis result will be displayed here."
            self.result_text_widget.setPlainText(result_text)

    def saveAnalysis(self):
        # Implement the code to save the analysis result
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataAnalysisApp()
    mainWindow.show()
    sys.exit(app.exec_())
