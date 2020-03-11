import sys
from PyQt5.QtWidgets import QLabel, QWidget, QMessageBox, QStatusBar, QComboBox, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, \
	QPushButton, QApplication, QMainWindow, QTableWidgetItem, QDialog, QTabWidget, QDialogButtonBox, QTableWidget, \
	QAction
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Application")
		self.tabs = Tab(self)
		self.btns = Buttons(self)
		self.msg = MessageBox(self)
		self.grid = QGridLayout(self)
		self.grid.addWidget(self.tabs, 0, 0, 10, 7)
		self.grid.addWidget(self.btns, 0, 7, 1, 3)
		self.grid.addWidget(self.msg, 2, 7, 7, 3)
		self.grid.setContentsMargins(7, 7, 7, 7)
		self.setLayout(self.grid)

		self.show()


class MessageBox(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		label = QLabel('Error Status:')
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setText("No error")
		msg.setInformativeText("Everything all right")
		msg.setDetailedText("This is detailed text")
		msg.setStandardButtons(QMessageBox.Ignore)

		self.box = QVBoxLayout(self)
		self.box.addWidget(label)
		self.box.addWidget(msg)
		self.box.addStretch()
		self.setLayout(self.box)


class Buttons(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.load = QPushButton('Load')
		self.validate = QPushButton('Validate')
		self.submit = QPushButton('Submit')
		self.validateall = QPushButton('Validate All')
		self.submitall = QPushButton('Submit All')
		self.dropdown = QComboBox()
		self.dropdown.addItems(["FinPlate", "TensionMember", "BCEndPlate", "CheatAngle"])

		self.vbox = QVBoxLayout(self)
		self.hbox = QHBoxLayout(self)
		self.hbox.addWidget(self.load)
		self.hbox.addWidget(self.validate)
		self.hbox.addWidget(self.submit)

		self.hbox2 = QHBoxLayout(self)
		self.hbox2.addWidget(self.validateall)
		self.hbox2.addWidget(self.submitall)

		self.vbox.addSpacing(40)
		self.vbox.addWidget(self.dropdown)
		self.vbox.addLayout(self.hbox)
		self.vbox.addSpacing(50)
		self.vbox.addLayout(self.hbox2)
		self.setLayout(self.vbox)


class Tab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.vbox = QVBoxLayout(self)

		self.tabs = QTabWidget()

		self.tabs.addTab(FinPlate(), "Fin Plate")
		self.tabs.addTab(TensionMember(), "Tension Member")
		self.tabs.addTab(BCEndPlate(), "BC End Plate")
		self.tabs.addTab(CheatAngle(), "Cheat Angle")

		self.vbox.addWidget(self.tabs)
		self.setLayout(self.vbox)


class MyTable(QTableWidget):
	def __init__(self, r, c):
		super().__init__(r, c)
		self.cellChanged.connect(self.c_current)
		self.setMinimumSize(1300, 600)

	def c_current(self):
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		row = self.currentRow()
		col = self.currentColumn()
		value = self.item(row, col)
		value = value.text()
		print("The current cell is", row, ",", col)
		print("In this cell we have:", value)


class FinPlate(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Connection type', 'Axial load', 'Sher load', 'Bolt diameter', 'Bolt grade',
		               'Plate Thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class TensionMember(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 5)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Member length', 'Tensile load', 'Support condition at End 1',
		               'Support condition at End 2']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class BCEndPlate(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 8)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'End plate type', 'Sher load', 'Axial load', 'Maximum Load', 'Bolt diameter', 'Bolt grade',
		               'Plate thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class CheatAngle(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(10, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Angle leg 1', 'Angle leg 2', 'Angle thickness', 'Sher load', 'Bolt diameter',
		               'Bolt grade']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	App = App()
	sys.exit(app.exec_())
