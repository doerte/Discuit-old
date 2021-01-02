import sys
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QComboBox

from interface.MainWindow import Ui_MainWindow

class TableModel(QtCore.QAbstractTableModel): 
	def __init__(self, data):
		super().__init__()
		self._data = data
		
	def data(self, index, role): 
		if role == Qt.DisplayRole:
		# See below for the nested-list data structure. # .row() indexes into the outer list,
		# .column() indexes into the sub-list
			value = self._data.iloc[index.row(), index.column()]
			return str(value)

	def rowCount(self, index):
		# The length of the outer list.
		return self._data.shape[0]

	def columnCount(self, index):
		# The following takes the first sub-list, and returns
		# the length (only works if all rows are an equal length) 
		return self._data.shape[1]

	def headerData(self, section, orientation, role):
		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return str(self._data.columns[section])
			if orientation == Qt.Vertical:
				return str(self._data.index[section])


	def isValid( self, fileName ):
		try: 
			file = open( fileName, 'r' )
			file.close()
			return True
		except:
			return False

	def readFile( self, fileName ):
		'''
		sets the member fileName to the value of the argument
		if the file exists.  Otherwise resets both the filename
		and file contents members.
		'''
		if self.isValid( fileName ):
			if fileName.endswith('.csv'):
				self.fileContents = pd.read_csv(fileName)
			else:
				self.fileContents = pd.read_excel(fileName)
		else:
			self.fileContents = ""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow): 
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		data = pd.DataFrame()
		self.model = TableModel(data)

		self.pushButton.clicked.connect(self.browse)
		self.label_2.hide()

	def refreshAll(self, data, variables):
		#remove old labels ComboBoxes
		for i in reversed(range(self.gridLayout.count())): 
			self.gridLayout.itemAt(i).widget().setParent(None)

		#display top 5 (.head()) rows of data file
		self.model= TableModel(data.head())
		self.tableView.setModel(self.model)
		self.label_2.show()
		for variable in variables:
				widget = QLabel(str(variable))
				selector = QComboBox()
				selector.addItem("ignore")  
				selector.addItem("categorical") 
				selector.addItem("continuous")
				self.gridLayout.addWidget(widget,0, variables.index(variable))
				self.gridLayout.addWidget(selector, 1, variables.index(variable))

	def browse(self):
		
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
						None,
						"Choose File", "",
						"Spreadsheet (*.xlsx *.xls *.csv)")
		if fileName:
			self.model.readFile(fileName)
			data = self.model.fileContents
			variables = list(self.model.fileContents.columns)

			self.refreshAll(data, variables)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()