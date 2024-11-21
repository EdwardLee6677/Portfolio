import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget, QFileDialog, QComboBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QModelIndex


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.roles = {
            Qt.UserRole + 1: 'id',
            Qt.UserRole + 2: 'label',
            Qt.UserRole + 3: 'attribute',
            Qt.UserRole + 4: 'datatype',
            Qt.UserRole + 5: 'enabled'
        }

    def rowCount(self, parent=QModelIndex()):
        return self.data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            return str(self.data.iloc[row, col])
        elif role in self.roles:
            role_name = self.roles[role]
            return self.data.at[row, role_name]

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role in self.roles:
            row = index.row()
            col = index.column()
            role_name = self.roles[role]
            self.data.at[row, role_name] = value
            self.dataChanged.emit(index, index, [role])
            return True

        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return str(self.data.columns[section])

        return QVariant()

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        # Load CSV data
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "CSV Files (*.csv)"
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './', file_filter, options=options)

        if filename:
            df = pd.read_csv(filename)

            # Initialize column roles and data types
            col_roles = ['label'] * len(df.columns)
            col_datatypes = ['float'] * len(df.columns)
            col_enabled = [True] * len(df.columns)

            model_data = {
                'id': list(range(len(df.columns))),
                'label': df.columns.tolist(),
                'attribute': col_roles,
                'datatype': col_datatypes,
                'enabled': col_enabled
            }

            roles_df = pd.DataFrame(model_data)
            df.insert(0, 'id', list(range(len(df))))

            model = CustomTableModel(df)
            self.table_view.setModel(model)

            for i in range(len(df.columns)):
                attribute_combobox = QComboBox()
                attribute_combobox.addItems(col_roles)
                self.table_view.setIndexWidget(model.index(0, i+1), attribute_combobox)

                datatype_combobox = QComboBox()
                datatype_combobox.addItems(['float', 'int', 'nominal'])
                self.table_view.setIndexWidget(model.index(1, i+1), datatype_combobox)

                enabled_combobox = QComboBox()
                enabled_combobox.addItems(['True', 'False'])
                self.table_view.setIndexWidget(model.index(2, i+1), enabled_combobox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
