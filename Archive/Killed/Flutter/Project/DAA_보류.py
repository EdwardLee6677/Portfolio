import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


# 데이터 로드 및 전처리 다이얼로그
class DataPreprocessingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("데이터 로드 및 전처리")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.file_path = ""
        self.delimiter = ","
        self.column_roles = {}
        self.column_data_types = {}
        self.column_usage = {}

        self.file_path_label = QLabel("파일 경로:")
        self.file_path_edit = QLineEdit()
        self.file_path_btn = QPushButton("찾아보기")
        self.file_path_btn.clicked.connect(self.browse_file)

        self.delimiter_label = QLabel("구분자:")
        self.delimiter_edit = QLineEdit()
        self.delimiter_edit.setText(self.delimiter)
        self.delimiter_edit.textChanged.connect(self.set_delimiter)

        self.column_table = QTableWidget(self)
        self.column_table.setColumnCount(5)
        self.column_table.setHorizontalHeaderLabels(["열", "역할", "데이터 타입", "사용 여부", "독립변수로 사용"])
        self.column_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ok_btn = QPushButton("적용")
        self.ok_btn.clicked.connect(self.apply_preprocessing)

        layout.addWidget(self.file_path_label)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.file_path_btn)
        layout.addWidget(self.delimiter_label)
        layout.addWidget(self.delimiter_edit)
        layout.addWidget(self.column_table)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def browse_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "CSV 파일 열기", "", "CSV 파일 (*.csv);;모든 파일 (*)", options=options)
        if file_path:
            self.file_path = file_path
            self.file_path_edit.setText(self.file_path)
            self.load_csv()

    def load_csv(self):
        try:
            df = pd.read_csv(self.file_path, delimiter=self.delimiter)
            self.column_table.setRowCount(len(df.columns))
            for row, col_name in enumerate(df.columns):
                self.column_roles[col_name] = "attribute"
                self.column_data_types[col_name] = "str"
                self.column_usage[col_name] = True

                col_name_item = QTableWidgetItem(col_name)
                col_role_item = QTableWidgetItem(self.column_roles[col_name])
                col_data_type_item = QTableWidgetItem(self.column_data_types[col_name])
                col_usage_item = QTableWidgetItem(str(self.column_usage[col_name]))

                self.column_table.setItem(row, 0, col_name_item)
                self.column_table.setItem(row, 1, col_role_item)
                self.column_table.setItem(row, 2, col_data_type_item)
                self.column_table.setItem(row, 3, col_usage_item)

        except Exception as e:
            QMessageBox.warning(self, "오류", f"파일을 로드하는 도중 오류가 발생했습니다: {e}")

    def set_delimiter(self):
        self.delimiter = self.delimiter_edit.text()

    def apply_preprocessing(self):
        for row in range(self.column_table.rowCount()):
            col_name = self.column_table.item(row, 0).text()
            self.column_roles[col_name] = self.column_table.item(row, 1).text()
            self.column_data_types[col_name] = self.column_table.item(row, 2).text()
            self.column_usage[col_name] = bool(int(self.column_table.item(row, 3).text()))

        # 데이터 전처리를 수행하고 그 결과를 메인 윈도우의 테이블 위젯에 적용합니다.
        # 전처리가 완료되면 다이얼로그를 닫습니다.
        self.accept()

# 메인 윈도우

class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis App")
        self.setGeometry(200, 200, 800, 600)

        self.table_widget = QTableWidget(self)
        self.analysis_result_label = QLabel("Analysis Result:", self)
        self.analysis_result_text = QLabel(self)

        load_btn = QPushButton("Load", self)
        load_btn.clicked.connect(self.load_data)

        run_btn = QPushButton("Run", self)
        run_btn.clicked.connect(self.run_analysis)

        save_btn = QPushButton("Save", self)
        save_btn.clicked.connect(self.save_result)

        button_layout = QHBoxLayout()
        button_layout.addWidget(load_btn)
        button_layout.addWidget(run_btn)
        button_layout.addWidget(save_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.analysis_result_label)
        main_layout.addWidget(self.analysis_result_text)
        main_layout.addLayout(button_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_data(self):
        dialog = DataPreprocessingDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Load the preprocessed data from the dialog to the main window's table widget.
            pass

    def run_analysis(self):
        # Perform data analysis using the selected algorithm and show results in the analysis_result_text.
        pass

    def save_result(self):
        # Save analysis results to txt, docs, hwp, png, pdf format.
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec_())
