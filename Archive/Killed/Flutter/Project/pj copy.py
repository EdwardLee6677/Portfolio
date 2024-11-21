import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Data Analysis")
        self.setGeometry(100, 100, 800, 600)

        # Load data button
        self.load_data_button = QPushButton("Load Data", self)
        self.load_data_button.setGeometry(10, 10, 100, 30)
        self.load_data_button.clicked.connect(self.load_data)

        # Role, Data Type, Use Column settings
        self.role_label = QLabel("Role:", self)
        self.role_combo = QComboBox(self)
        self.role_combo.addItem("Attribute")
        self.role_combo.addItem("Label")
        self.role_label.setGeometry(10, 50, 60, 30)
        self.role_combo.setGeometry(80, 50, 100, 30)

        self.data_type_label = QLabel("Data Type:", self)
        self.data_type_combo = QComboBox(self)
        self.data_type_combo.addItem("float")
        self.data_type_combo.addItem("int")
        self.data_type_combo.addItem("str")
        self.data_type_combo.addItem("date")
        self.data_type_combo.addItem("datetime")
        self.data_type_label.setGeometry(200, 50, 80, 30)
        self.data_type_combo.setGeometry(280, 50, 100, 30)

        self.use_column_label = QLabel("Use Column:", self)
        self.use_column_combo = QComboBox(self)
        self.use_column_combo.addItem("True")
        self.use_column_combo.addItem("False")
        self.use_column_label.setGeometry(400, 50, 80, 30)
        self.use_column_combo.setGeometry(480, 50, 100, 30)

        # Apply settings button
        self.apply_button = QPushButton("Apply Settings", self)
        self.apply_button.setGeometry(600, 50, 150, 30)
        self.apply_button.clicked.connect(self.apply_settings)

        # Table widget to display data
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(10, 100, 780, 490)

        self.show()

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.df = pd.read_csv(file_name, sep=str(self.get_separator_dialog()))
            self.display_table()

    def get_separator_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Separator Settings")
        layout = QVBoxLayout(dialog)

        separator_label = QLabel("Enter the separator for CSV file:", dialog)
        layout.addWidget(separator_label)

        separator_edit = QLineEdit(dialog)
        layout.addWidget(separator_edit)

        ok_button = QPushButton("OK", dialog)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        dialog.exec_()
        return separator_edit.text()

    def apply_settings(self):
        role = self.role_combo.currentText()
        data_type = self.data_type_combo.currentText()
        use_column = self.use_column_combo.currentText() == "True"

        if role == "Label":
            if self.df.filter(like="Label", axis=1).shape[1] >= 2:
                QMessageBox.warning(self, "Error", "Cannot have more than one Label.")
                return

        column_name = self.table_widget.horizontalHeaderItem(self.table_widget.currentColumn()).text()
        self.df[column_name] = self.df[column_name].astype(data_type)
        if not use_column:
            self.df.drop(column_name, axis=1, inplace=True)

        self.display_table()

    def display_table(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)

        if hasattr(self, "df"):
            self.table_widget.setRowCount(len(self.df))
            self.table_widget.setColumnCount(len(self.df.columns))
            self.table_widget.setHorizontalHeaderLabels(self.df.columns)

            for i, row in self.df.iterrows():
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(i, j, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    sys.exit(app.exec_())
