import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import statsmodels.api as sm
import bardapi
import os

class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super(LoadDialog, self).__init__(parent)

        self.delimiter = ","
        self.encoding = "utf-8"

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.delimiter_label = QLabel('Delimiter:', self)
        self.delimiter_input = QComboBox(self)
        self.delimiter_input.addItems([',', ';', '\t'])
        vbox.addWidget(self.delimiter_label)
        vbox.addWidget(self.delimiter_input)

        self.encoding_label = QLabel('Encoding:', self)
        self.encoding_input = QComboBox(self)
        self.encoding_input.addItems(['cp949', 'utf-8'])
        vbox.addWidget(self.encoding_label)
        vbox.addWidget(self.encoding_input)

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.clicked.connect(self.applySettings)
        vbox.addWidget(self.apply_button)

        self.setLayout(vbox)
        self.setWindowTitle('Load Settings')

    def applySettings(self):
        self.delimiter = self.delimiter_input.currentText()
        self.encoding = self.encoding_input.currentText()
        self.accept()

class ModifyDataDialog(QDialog):
    def __init__(self, data_frame, parent=None):
        super(ModifyDataDialog, self).__init__(parent)
        self.data_frame = data_frame
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.data_table_widget = QTableWidget(self)
        self.data_table_widget.setRowCount(self.data_frame.shape[0])
        self.data_table_widget.setColumnCount(self.data_frame.shape[1])
        self.data_table_widget.setHorizontalHeaderLabels(self.data_frame.columns)
        vbox.addWidget(self.data_table_widget)

        hbox = QHBoxLayout()

        remove_column_button = QPushButton('Remove Column', self)
        remove_column_button.clicked.connect(self.removeColumn)
        hbox.addWidget(remove_column_button)

        remove_missing_columns_button = QPushButton('Remove Missing Columns', self)
        remove_missing_columns_button.clicked.connect(self.removeMissingColumns)
        hbox.addWidget(remove_missing_columns_button)

        remove_missing_rows_button = QPushButton('Remove Missing Rows', self)
        remove_missing_rows_button.clicked.connect(self.removeMissingRows)
        hbox.addWidget(remove_missing_rows_button)

        apply_button = QPushButton('Apply', self)
        apply_button.clicked.connect(self.applyChanges)
        hbox.addWidget(apply_button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.resize(1024, 600)
        self.setWindowTitle('Modify Data')

        self.displayData()

    def removeColumn(self):
        selected_items = self.data_table_widget.selectedItems()
        if selected_items:
            column_name = selected_items[0].column()
            self.data_frame.drop(self.data_frame.columns[column_name], axis=1, inplace=True)
            self.displayData()

    def removeMissingColumns(self):
        self.data_frame.dropna(axis=1, how='any', inplace=True)
        self.displayData()

    def removeMissingRows(self):
        self.data_frame.dropna(axis=0, how='any', inplace=True)
        self.displayData()

    def applyChanges(self):
        self.accept()

    def displayData(self):
        self.data_table_widget.clear()
        self.data_table_widget.setRowCount(self.data_frame.shape[0])
        self.data_table_widget.setColumnCount(self.data_frame.shape[1])
        self.data_table_widget.setHorizontalHeaderLabels(self.data_frame.columns)

        for row_idx in range(self.data_frame.shape[0]):
            for col_idx in range(self.data_frame.shape[1]):
                data = str(self.data_frame.iloc[row_idx, col_idx])
                item = QTableWidgetItem(data)
                self.data_table_widget.setItem(row_idx, col_idx, item)

class ModelDialog(QDialog):
    def __init__(self, parent=None):
        super(ModelDialog, self).__init__(parent)

        self.selected_model = ""

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.model_label = QLabel('Select Model:', self)
        self.model_input = QComboBox(self)
        self.model_input.addItems(['Linear Regression', 'Logistic Regression', 'Causal Impact', 'Causal Discovery', 'Causal Inference'])
        vbox.addWidget(self.model_label)
        vbox.addWidget(self.model_input)

        self.apply_button = QPushButton('Apply', self)
        self.apply_button.clicked.connect(self.applyModel)
        vbox.addWidget(self.apply_button)

        self.setLayout(vbox)
        self.setWindowTitle('Model Selection')

    def applyModel(self):
        self.selected_model = self.model_input.currentText()
        self.accept()

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super(DataAnalysisApp, self).__init__()
        self.df = None
        self.target_column = None
        self.model = None
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

        self.report_text_widget = QTextEdit(self)
        vbox.addWidget(self.report_text_widget)

        hbox = QHBoxLayout()

        load_button = QPushButton('Load', self)
        load_button.clicked.connect(self.showLoadDialog)
        hbox.addWidget(load_button)

        edit_button = QPushButton('Edit', self)
        edit_button.clicked.connect(self.showModifyDataDialog)
        hbox.addWidget(edit_button)

        target_button = QPushButton('Target', self)
        target_button.clicked.connect(self.selectTargetColumn)
        hbox.addWidget(target_button)

        model_button = QPushButton('Model', self)
        model_button.clicked.connect(self.showModelDialog)
        hbox.addWidget(model_button)

        vbox.addLayout(hbox)
        main_widget.setLayout(vbox)

        self.setWindowTitle('Data Analysis App')

    def showLoadDialog(self):
        dialog = LoadDialog(self)
        if dialog.exec_():
            delimiter = dialog.delimiter
            encoding = dialog.encoding
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                       options=options)
            if file_path:
                try:
                    self.df = pd.read_csv(file_path, encoding=encoding, sep=delimiter)
                    self.displayData()
                except Exception as e:
                    print("Error while loading the file:", e)

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

    def showModifyDataDialog(self):
        if self.df is not None:
            dialog = ModifyDataDialog(self.df, self)
            if dialog.exec_():
                self.df = dialog.data_frame
                self.displayData()

    def selectTargetColumn(self):
        if self.df is not None:
            column_items = self.df.columns.tolist()
            target_column, ok = QInputDialog.getItem(self, "Select Target Column", "Columns:", column_items, 0, False)
            if ok and target_column:
                self.target_column = target_column

    def showModelDialog(self):
        dialog = ModelDialog(self)
        if dialog.exec_():
            self.selected_model = dialog.selected_model
            self.runAnalysis()

    def runAnalysis(self):
        if self.df is not None and self.target_column is not None and self.selected_model:
            X = self.df.drop(columns=[self.target_column])
            y = self.df[self.target_column]

            # 전처리: 결측치와 무한대 값을 제거합니다.
            X = X.replace([np.inf, -np.inf], np.nan).dropna()

            # 프로그레스 다이얼로그를 생성하고 설정합니다.
            progress_dialog = QProgressDialog("Running Analysis...", "Cancel", 0, 100, self)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setWindowTitle("Progress")
            progress_dialog.setAutoClose(True)

            def perform_analysis():
                nonlocal X
                if self.selected_model == "Linear Regression":
                    result = perform_linear_regression(X, y)
                elif self.selected_model == "Logistic Regression":
                    result = perform_logistic_regression(X, y)
                return result

            # 선형 회귀 분석을 실행합니다.
            def perform_linear_regression(X, y):
                X = sm.add_constant(X)
                model = sm.OLS(y, X).fit()
                summary = model.summary()  # 분석 결과 요약 정보를 얻습니다.
                summary_str = str(summary)  # 요약 정보를 문자열로 변환
                return summary_str

            # 로지스틱 회귀 분석을 실행합니다.
            def perform_logistic_regression(X, y):
                X = sm.add_constant(X)
                model = sm.Logit(y, X).fit()
                summary = model.summary()  # 분석 결과 요약 정보를 얻습니다.
                summary_str = str(summary)  # 요약 정보를 문자열로 변환
                return summary_str

            def update_progress(progress):
                progress_dialog.setValue(progress)
                QApplication.processEvents()

            def analysis_complete(result):
                import bardapi
                import os                
                self.result_text_widget.setPlainText(result)
                bard_api_key = "aAg-FMfUz_N8GTUvAXqxBwYvNuXbnc_t5KFM5XYAFFYMzoZuSs0itzN7l_lC4535CfaOSg."
                os.environ['_BARD_API_KEY'] = bard_api_key
                input_text = result
                response = bardapi.core.Bard(bard_api_key).get_answer(input_text)
                result = response['choices'][0]['content'][0]
                response = bardapi.core.Bard(bard_api_key).get_answer(str(result))['content']
                self.report_text_widget.setPlainText(result)
                progress_dialog.setValue(100)

            # 분석 작업을 백그라운드 스레드에서 실행하고, 진행 상황을 프로그레스 바로 업데이트합니다.
            class AnalysisThread(QThread):
                update_signal = pyqtSignal(int)
                complete_signal = pyqtSignal(str)

                def run(self):
                    result = perform_analysis()
                    self.complete_signal.emit(result)

            thread = AnalysisThread()
            thread.update_signal.connect(update_progress)
            thread.complete_signal.connect(analysis_complete)
            thread.start()

            # 프로그레스 다이얼로그를 표시하고 실행합니다.
            progress_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = DataAnalysisApp()
    mainWindow.show()
    sys.exit(app.exec_())
