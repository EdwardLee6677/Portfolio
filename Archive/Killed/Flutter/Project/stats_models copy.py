import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic


class CSVTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

    def rowCount(self, parent=QModelIndex()):
        return self.data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return str(self.data.iloc[index.row(), index.column()])
        elif role == Qt.EditRole:
            return str(self.data.iloc[index.row(), index.column()])

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return str(self.data.columns[section])

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame()
        self.dataset_metadata = pd.DataFrame()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        '''Blank Table Widget'''
        table_widget = QTableWidget()

        textedit_widget = QTextEdit()


        '''PushButton for Load CSV file'''
        button_load = QPushButton("Load")
        button_load.clicked.connect(lambda state, widget = table_widget: self.slot_button_load(state, widget))

        '''PushButton for Load CSV file'''
        button_run = QPushButton("Run")
        button_run.clicked.connect(lambda state, widget=textedit_widget: self.slot_button_run(state, widget))

        '''PushButton for Save modified CSV'''
        button_save = QPushButton("Save")
        button_save.clicked.connect(lambda state, widget = table_widget: self.slot_button_save(state, widget))

        layout.addWidget(table_widget)
        layout.addWidget(textedit_widget)
        layout.addWidget(button_load)
        layout.addWidget(button_run)
        layout.addWidget(button_save)

        self.setLayout(layout)
        self.resize(1024, 768)
        self.show()

    def slot_button_load(self, state, widget):
        filename,_ = QFileDialog.getOpenFileName(self, 'Open file', './', "CSV Files (*.csv)")

        if filename:
            sep,_= QInputDialog.getText(self, "Separator", "Enter the separator for CSV file (e.g., ',' or ';'):", QLineEdit.Normal, ",")
            if sep and len(sep) == 1:
                df = pd.read_csv(filename, sep=sep)
                self.data = df
                self.create_table_widget(widget, df)


    def create_table_widget(self, widget, df):
        widget.setRowCount(len(df.index))
        widget.setColumnCount(len(df.columns))
        widget.setHorizontalHeaderLabels(df.columns)
        widget.setVerticalHeaderLabels(df.index.map(str))

        for row_index, row in enumerate(df.index):
            for col_index, column in enumerate(df.columns):
                value = df.loc[row][column]
                item = QTableWidgetItem(str(value))
                widget.setItem(row_index, col_index, item)

    def slot_button_run(self, state, widget):
        self.build_model(widget)

    def build_model(self, widget):
        from statsmodels.formula.api import ols
        # str_formula = self.build_formula()
        # model = ols(formula=str_formula, data=self.data).fit()
        model = ols(formula='quality ~ alcohol', data=self.data).fit()
        report = str(model.summary())
        widget.setText(report)

    # def build_formula():
    #     str_formula = ""
    #     self.dataset_metadata

    #     return str_formula

    def slot_button_save(self, state, widget):
        for row_index in range(widget.rowCount()):
            for col_index in range(widget.columnCount()):
                item = widget.item(row_index, col_index)
                content = item.text()
                print(content)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())