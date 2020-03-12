import sys
from PyQt5.QtWidgets import QLabel, QWidget, QMessageBox, QStatusBar, QComboBox, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QMainWindow, QTableWidgetItem, QDialog, QTabWidget, QDialogButtonBox, QTableWidget, QAction
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


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

		self.errors = {}
		self.count_errors = {}

	def validate(self, table):
		count = 0
		e = {}
		for i in range(table.rowCount()):
			e[i] = {}
			e2 = e[i]
			for j in range(table.columnCount()):
				value = table.item(i,j)
				if value == None:
					e2[j] = 'None'
					count = count + 1
				else:
					try:
						int(value.text())
					except ValueError:
						e2[j] = 'not Int'
						count = count + 1
		self.errors[id(table)] = e
		self.count_errors[id(table)] = count

	def setMessageBox(self):
		print(self.errors)
		print(self.count_errors)
		detail = ""
		for id in self.errors:
			if self.count_errors[id]:
				form = self.errors[id]
				detail = detail + "Errors in tab "+self.tabs.id[id]+":\n"
				for row in form:
					row_errors = form[row]
					for col in row_errors:
						col_errors = row_errors[col]
						detail = detail+'('+str(row)+','+str(col)+') '+col_errors+'\n'
		text = ""
		for id in self.count_errors:
			if self.count_errors[id]:
				text = text + str(self.count_errors[id]) + " error found in tab "+self.tabs.id[id]+'\n'
		self.msg.msg.setText(text)
		self.msg.msg.setDetailedText(detail)
		self.msg.msg.setIcon(QMessageBox.Warning)


class MessageBox(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.label = QLabel('Error Status:')
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)

		self.msg.setText("No error")
#		self.msg.setInformativeText("Everything all right")
		self.msg.setStandardButtons(QMessageBox.Ignore)

		self.box = QVBoxLayout(self)
		self.box.addWidget(self.label)
		self.box.addWidget(self.msg)
		self.box.addStretch()
		self.setLayout(self.box)


class Buttons(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.dropdown = QComboBox()
		self.load = QPushButton('Load')
		self.validate = QPushButton('Validate')
		self.validate.clicked.connect(self.validate_action)
		self.submit = QPushButton('Submit')
		self.validateall = QPushButton('Validate All')
		self.validateall.clicked.connect(self.validateall_action)
		self.submitall = QPushButton('Submit All')
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

	@pyqtSlot()
	def validate_action(self):
		index = self.dropdown.currentIndex()
		if index == 0:
			App.validate(App.tabs.finplate.form_widget)
		elif index == 1:
			App.validate(App.tabs.tensionmember.form_widget)
		elif index == 2:
			App.validate(App.tabs.bcendplate.form_widget)
		else:
			App.validate(App.tabs.cheatangle.form_widget)
		App.setMessageBox()

	@pyqtSlot()
	def validateall_action(self):
		App.validate(App.tabs.finplate.form_widget)
		App.validate(App.tabs.tensionmember.form_widget)
		App.validate(App.tabs.bcendplate.form_widget)
		App.validate(App.tabs.cheatangle.form_widget)
		App.setMessageBox()


class Tab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.vbox = QVBoxLayout(self)

		self.tabs = QTabWidget()
		self.finplate = FinPlate()
		self.tensionmember = TensionMember()
		self.bcendplate = BCEndPlate()
		self.cheatangle = CheatAngle()
		self.id = {id(self.finplate.form_widget): 'Fin Plate', id(self.tensionmember.form_widget): 'Tension Member', id(self.cheatangle.form_widget): 'Cheat Angle', id(self.bcendplate.form_widget): 'BC End Plate'}
		self.tabs.addTab(self.finplate, "Fin Plate")
		self.tabs.addTab(self.tensionmember, "Tension Member")
		self.tabs.addTab(self.bcendplate, "BC End Plate")
		self.tabs.addTab(self.cheatangle, "Cheat Angle")

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

		self.form_widget = MyTable(1, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Connection type', 'Axial load', 'Sher load', 'Bolt diameter', 'Bolt grade', 'Plate Thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class TensionMember(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(1, 5)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Member length', 'Tensile load', 'Support condition at End 1', 'Support condition at End 2']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class BCEndPlate(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(1, 8)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'End plate type', 'Sher load', 'Axial load', 'Maximum Load', 'Bolt diameter', 'Bolt grade', 'Plate thickness']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


class CheatAngle(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = MyTable(1, 7)
		self.setCentralWidget(self.form_widget)
		col_headers = ['ID', 'Angle leg 1', 'Angle leg 2', 'Angle thickness', 'Sher load', 'Bolt diameter', 'Bolt grade']
		self.form_widget.setHorizontalHeaderLabels(col_headers)
		self.form_widget.resizeColumnsToContents()
		self.form_widget.resizeRowsToContents()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	App = App()
	sys.exit(app.exec_())
