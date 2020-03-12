import sys
from PyQt5.QtWidgets import QLabel, QWidget, QMessageBox, QFileDialog, QStatusBar, QComboBox, QApplication, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QMainWindow, QTableWidgetItem, QDialog, QTabWidget, QDialogButtonBox, QTableWidget, QAction
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
		self.data = {}

	def validate(self, table):
		count = 0
		e = {}
		d = {}
		for i in range(table.rowCount()):
			e[i] = {}
			d[i] = {}
			for j in range(table.rowCount()):
				if table.item(i,0) is None or table.item(j,0) is None or i == j:
					continue
				try:
					if table.item(i,0).text() == table.item(j,0).text():
						count = count + 1
						e[i][0] = 'id of '+str(i+1)+' data similar to '+str(j+1)+' data'
				except ValueError:
					continue
			for j in range(table.columnCount()):
				value = table.item(i,j)
				if value is None or value.text() == '':
					e[i][j] = 'No value in the cell '+str(i+1)+', '+str(j+1)
					count = count + 1
					d[i][table.horizontalHeaderItem(j).text()] = None
				else:
					try:
						d[i][table.horizontalHeaderItem(j).text()] = int(value.text())
					except ValueError:
						e[i][j] = 'Value is not Int in the cell '+str(i+1)+', '+str(j+1)
						d[i][table.horizontalHeaderItem(j).text()] = value.text()
						count = count + 1
		self.errors[id(table)] = e
		self.count_errors[id(table)] = count
		self.data[id(table)] = d

	def setMessageBox(self):
		self.detailedError = ""
		for id in self.errors:
			if self.count_errors[id]:
				self.detailedError = self.detailedError + "Errors in tab "+self.tabs.id[id]+":\n"
				for row in self.errors[id]:
					for col in self.errors[id][row]:
						self.detailedError = self.detailedError+self.errors[id][row][col]+'\n'
		self.infotmativeError = ""
		count = 0
		for id in self.count_errors:
			if self.count_errors[id]:
				count = count + self.count_errors[id]
				self.infotmativeError = self.infotmativeError + str(self.count_errors[id]) + " error found in tab "+self.tabs.id[id]+'\n'
		self.textError = "Total "+str(count)+" errors found"
		self.msg.msg.setText(self.textError)
		self.msg.msg.setInformativeText(self.infotmativeError)
		self.msg.msg.setDetailedText(self.detailedError)
		self.msg.msg.setIcon(QMessageBox.Warning)

	def submit(self):
		directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		for id in self.data:
			for d in self.data[id].values():
				if d['ID'] == None: continue
				print(directory + '/' + self.tabs.id[id] + '_' + str(d['ID']) + '.txt')
				with open(directory+'/'+self.tabs.id[id]+'_'+str(d['ID'])+'.txt', 'w') as file:
					file.write(str(d))
					print(d)




class MessageBox(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.label = QLabel('Error Status:')
		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)

		self.msg.setText("No error")
		self.msg.setInformativeText("Everything all right")
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
		self.submit.clicked.connect(self.submit_action)
		self.validateall = QPushButton('Validate All')
		self.validateall.clicked.connect(self.validateall_action)
		self.submitall = QPushButton('Submit All')
		self.submitall.clicked.connect(self.submitall_action)
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
		App.errors = {}
		App.count_errors = {}
		App.data = {}
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
		print(App.count_errors)
		print(App.errors)
		print(App.data)

	@pyqtSlot()
	def validateall_action(self):
		App.errors = {}
		App.count_errors = {}
		App.data = {}
		App.validate(App.tabs.finplate.form_widget)
		App.validate(App.tabs.tensionmember.form_widget)
		App.validate(App.tabs.bcendplate.form_widget)
		App.validate(App.tabs.cheatangle.form_widget)
		App.setMessageBox()
		print(App.count_errors)
		print(App.errors)
		print(App.data)

	@pyqtSlot()
	def submit_action(self):
		self.validate_action()
		App.submit()

	@pyqtSlot()
	def submitall_action(self):
		self.validateall_action()
		App.submit()

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

		self.form_widget = MyTable(2, 7)
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
