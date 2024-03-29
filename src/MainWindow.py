from telnetlib import SE
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QApplication, QComboBox,
        QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, 
        QPushButton, QSpinBox, QTextEdit,QVBoxLayout,QDoubleSpinBox)
import ast

from Generator import *
from Representation import AdjacencyMatrix, IncidentMatrix
from Utils import components, valid_graph, cons_graph, random_k_regular, find_Hamiltion_cycle,prim,\
                    randomizeGraph, plot_graph,dijkstra,dijkstraDist, graphCenter,miniMaxCenter
from EulerGraph import EulerGraph
from Kosaraju import *
from ShortPaths import *
from PageRange import page_rank_random_wandering, page_rank_vector_iteration, di_graph
from travelingsalesmanalgorithm import *
from p5ex12 import *
graph_representation_list = ['Select Graph Representation','AdjacencyList','AdjacencyMatrix','IncidentMatrix']

data={'name': 'Representation.png','size': (3, 3),'directed_all': False,'node_size': 500,'graph': None,'nodes_description':{},'edges_description':{}}

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #create user interface
        self.initUI()
        self.layout0=None
        self.layout1=None
        self.layout2=None
        self.layout3=None
        self.layout4=None
        self.layout5=None
        self.layout6=None
        self.layout7=None
        self.layout8=None
        self.graph_3=None
        #connect functionality with methods
        self.setupQtConnections()
        #set geometry
        self.setGeometry(50, 50, 900, 600)
        #set window title
        self.setWindowTitle('Graphs Presentation')

    def initUI(self):
        #Tool Bar & EDI
        #basic
        self.originalPalette = QApplication.palette()

        self.LeftGroupBox = QGroupBox("Option")
        self.layoutLeftGroupBox = QVBoxLayout()
        self.LeftGroupBox.setLayout(self.layoutLeftGroupBox)

        self.RightGroupBox = QGroupBox("Display")
        self.layoutRightGroupBox = QVBoxLayout()
        self.RightGroupBox.setLayout(self.layoutRightGroupBox)

        topLayout = QHBoxLayout()
        topLayout = QHBoxLayout()
        self.project1Button = QPushButton('Project1', self)
        self.project2Button = QPushButton('Project2', self)
        self.project3Button = QPushButton('Project3', self)
        self.project4Button = QPushButton('Project4', self)
        self.project5Button = QPushButton('Project5', self)
        self.project6Button = QPushButton('Project6', self)
        topLayout.addWidget(self.project1Button)
        topLayout.addWidget(self.project2Button)
        topLayout.addWidget(self.project3Button)
        topLayout.addWidget(self.project4Button)
        topLayout.addWidget(self.project5Button)
        topLayout.addWidget(self.project6Button)
        topLayout.addStretch(1)

        #init main Layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0,1,2)
        mainLayout.addWidget(self.LeftGroupBox, 1, 0)
        mainLayout.addWidget(self.RightGroupBox, 1, 1)

        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def setupQtConnections(self):
        """
        A method that combines events with appropriate methods
        """
        self.project1Button.clicked.connect(self.initProject1)
        self.project2Button.clicked.connect(self.initProject2)
        self.project3Button.clicked.connect(self.initProject3)
        self.project4Button.clicked.connect(self.initProject4)
        self.project5Button.clicked.connect(self.initProject5)
        self.project6Button.clicked.connect(self.initProject6)

    def clear_right_layout(self):
        if self.layout3:
            for i in reversed(range(self.layout3.count())):
                try:
                    self.layout3.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout4:
            for i in reversed(range(self.layout4.count())):
                try:
                    self.layout4.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout7:
            for i in reversed(range(self.layout7.count())):
                try:
                    self.layout7.itemAt(i).widget().setParent(None)
                except:pass
        for i in reversed(range(self.layoutRightGroupBox.count())):
            try:
                self.layoutRightGroupBox.itemAt(i).widget().setParent(None)
            except: pass    

    def clear_left_layout(self):
        if self.layout0:
            for i in reversed(range(self.layout0.count())):
                try:
                    self.layout0.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout1:
            for i in reversed(range(self.layout1.count())):
                try:
                    self.layout1.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout2:
            for i in reversed(range(self.layout2.count())):
                try:
                    self.layout2.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout5:
            for i in reversed(range(self.layout5.count())):
                try:
                    self.layout5.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout6:
            for i in reversed(range(self.layout6.count())):
                try:
                    self.layout6.itemAt(i).widget().setParent(None)
                except:pass
        if self.layout8:
            for i in reversed(range(self.layout8.count())):
                try:
                    self.layout8.itemAt(i).widget().setParent(None)
                except:pass
        for i in reversed(range(self.layoutRightGroupBox.count())):
            try:
                self.layoutLeftGroupBox.itemAt(i).widget().setParent(None)
            except: pass
        for i in reversed(range(self.layoutRightGroupBox.count())):
            try:
                self.layoutLeftGroupBox.itemAt(i).widget().setParent(None)
            except: pass

    def enable_all(self):
        self.project1Button.setEnabled(True)
        self.project2Button.setEnabled(True)
        self.project3Button.setEnabled(True)
        self.project4Button.setEnabled(True)
        self.project5Button.setEnabled(True)
        self.project6Button.setEnabled(True)
#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 1
#
#------------------------------------------------------------------------------------------------------------------

    def initProject1(self):
        self.enable_all()
        self.project1Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        self.layout0 = QVBoxLayout()
        self.graph_representation_combo = QComboBox()
        self.graph_representation_combo.addItems(graph_representation_list)
        self.layout0.addWidget(self.graph_representation_combo)

        self.rand_graph_edge_number_button = QPushButton('Generate Model G(n,l)',self)
        self.rand_graph_edge_number_spin1_n = QSpinBox()
        self.rand_graph_edge_number_spin1_n.setValue(10)
        self.rand_graph_edge_number_spin1_l = QSpinBox()
        self.rand_graph_edge_number_spin1_l.setValue(5)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.rand_graph_edge_number_button)
        self.layout1.addWidget(self.rand_graph_edge_number_spin1_n)
        self.layout1.addWidget(self.rand_graph_edge_number_spin1_l)

        self.rand_graph_edge_probability_button = QPushButton('Generate Model G(n,p)',self)
        self.rand_graph_edge_number_spin2_n = QSpinBox()
        self.rand_graph_edge_number_spin2_n.setValue(10)
        self.rand_graph_edge_number_spin2_p = QDoubleSpinBox()
        self.rand_graph_edge_number_spin2_p.setSingleStep(0.1)
        self.rand_graph_edge_number_spin2_p.setValue(0.5)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.rand_graph_edge_probability_button)
        self.layout2.addWidget(self.rand_graph_edge_number_spin2_n)
        self.layout2.addWidget(self.rand_graph_edge_number_spin2_p)

        self.layout0.addLayout(self.layout1)
        self.layout0.addLayout(self.layout2)
        self.layoutLeftGroupBox.addLayout(self.layout0)
        # self.layoutLeftGroupBox.addStretch(0)

        #setup connection
        self.rand_graph_edge_number_button.clicked.connect(self.on_rand_graph_edge_number)
        self.rand_graph_edge_probability_button.clicked.connect(self.on_rand_graph_edge_probability)
        self.graph_representation_combo.currentTextChanged.connect(self.on_graph_representation_combo)


    def on_rand_graph_edge_number(self):
        self.clear_right_layout()
        Generator.rand_graph_edge_number(self.rand_graph_edge_number_spin1_n.value(), self.rand_graph_edge_number_spin1_l.value()).graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomGraphEdgeNumber.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)

    def on_rand_graph_edge_probability(self):
        self.clear_right_layout()
        Generator.rand_graph_edge_probability(self.rand_graph_edge_number_spin2_n.value(), self.rand_graph_edge_number_spin2_p.value()).graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomGraphEdgeProbability.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)

    def on_graph_representation_combo(self):
        self.clear_right_layout()

        self.inputTextEdit = QTextEdit()
        if self.graph_representation_combo.currentText() == graph_representation_list[1]:
            self.inputTextEdit.setText("""{ 1:  [2,5,6],
2:  [1,3,6],
3:  [2,4,5,12],
4:  [3,8,9,11],
5:  [1,3,7,9],
6:  [1,2,7],
7:  [5,6,8],
8:  [4,7,9,12],
9:  [4,5,8,10],
10: [9],
11: [4],
12: [3,8]}""")
        if self.graph_representation_combo.currentText() == graph_representation_list[2]:
            self.inputTextEdit.setText("""[[0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
[1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0],
[1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
[1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
[0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]""")
        if self.graph_representation_combo.currentText() == graph_representation_list[3]:
            self.inputTextEdit.setText("""[[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]""")
        label = QLabel("Select the representation you want to convert to!")
        self.representationBox = QComboBox()
        self.representationBox.addItems(graph_representation_list)

        self.layout3 = QHBoxLayout()
        self.returnTextEdit = QTextEdit()
        self.returnTextEdit.setReadOnly(True)
        self.returnTextEdit.setMaximumWidth(250)
        self.labelImage = QLabel()

        self.layout3.addWidget(self.returnTextEdit)
        self.layout3.addWidget(self.labelImage)

        self.layoutRightGroupBox.addWidget(self.inputTextEdit)
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(self.representationBox)
        self.layoutRightGroupBox.addLayout(self.layout3)
        self.representationBox.currentTextChanged.connect(self.on_graph_representation)

    def on_graph_representation(self):
        data['graph']=ast.literal_eval(self.inputTextEdit.toPlainText())
        tmp = None
        if self.graph_representation_combo.currentText() == graph_representation_list[1]: tmp = AdjacencyList(data)
        if self.graph_representation_combo.currentText() == graph_representation_list[2]: tmp = AdjacencyMatrix(data)
        if self.graph_representation_combo.currentText() == graph_representation_list[3]: 
            tmp = IncidentMatrix(data)
        self.graph_representation_helper(tmp)

    def graph_representation_helper(self,tmp):
        if self.representationBox.currentText() == graph_representation_list[1]: 
            self.returnTextEdit.setText(tmp.toAdjacencyList().printGraph())
            tmp.toAdjacencyList().graphVisualization()
        if self.representationBox.currentText() == graph_representation_list[2]: 
            self.returnTextEdit.setText(tmp.toAdjacencyMatrix().printGraph())
            tmp.toAdjacencyMatrix().graphVisualization()
        if self.representationBox.currentText() == graph_representation_list[3]: 
            self.returnTextEdit.setText(tmp.toIncidentMatrix().printGraph())
            tmp.toIncidentMatrix().graphVisualization()

        pixmap = QPixmap('src/__imgcache__/Representation.png')
        self.labelImage.setPixmap(pixmap)

#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 2
#
#------------------------------------------------------------------------------------------------------------------
    def initProject2(self):
        self.enable_all()
        self.project2Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        self.layout0 = QVBoxLayout()
        self.validGraphButton = QPushButton('Valid Graph',self)
        self.edgeRandomizationButton = QPushButton('Edge Randomize',self)
        self.findEulerCycleButton = QPushButton('Euler Cycle',self)
        self.findHamiltionCycleButton = QPushButton('Find Hamiltion Cycle',self)

        self.kRegularGraphsButton = QPushButton('K-Regular Graphs',self)
        self.layout0.addWidget(self.validGraphButton)
        self.layout0.addWidget(self.edgeRandomizationButton)
        self.layout0.addWidget(self.findEulerCycleButton)
        self.layout0.addWidget(self.kRegularGraphsButton)
        self.layout0.addWidget(self.findHamiltionCycleButton)
        self.validGraphButton.clicked.connect(self.on_valid_graph)
        self.edgeRandomizationButton.clicked.connect(self.on_edge_randomize)
        self.findEulerCycleButton.clicked.connect(self.on_find_euler_cycle)
        self.findHamiltionCycleButton.clicked.connect(self.on_find_hamiltion_cycle)
        self.kRegularGraphsButton.clicked.connect(self.on_k_regular_graphs)
        self.layoutLeftGroupBox.addLayout(self.layout0)

    def on_valid_graph(self):
        self.clear_right_layout()

        self.inputTextEdit = QTextEdit()
        self.inputTextEdit.setText("""[4, 2, 2, 3, 2, 1, 4, 2, 2, 2, 2]""")
        self.inputTextEdit.setMaximumHeight(250)
        valid = QPushButton('Valid Graph',self)
        self.labelImage1 = QLabel()
        labelImage2 = QLabel('------------------------------------------>')
        self.labelImage3 = QLabel()
        self.labelImage2 = QLabel()
        self.layout4=QVBoxLayout()
        self.labelImage4 = QLabel()
        self.layout4.addWidget(valid)
        self.layout4.addWidget(self.labelImage4)
        self.layout3=QHBoxLayout()
        self.layout3.addWidget(self.labelImage1)
        self.layout3.addWidget(labelImage2)
        self.layout3.addWidget(self.labelImage3)

        self.layoutRightGroupBox.addWidget(self.inputTextEdit)
        self.layoutRightGroupBox.addLayout(self.layout4)
        self.layoutRightGroupBox.addLayout(self.layout3)
        valid.clicked.connect(self.on_click_valid)

    def on_click_valid(self):
        if valid_graph(ast.literal_eval(self.inputTextEdit.toPlainText())):
            self.labelImage4.setText("The graph is graphical")
            cons_graph(ast.literal_eval(self.inputTextEdit.toPlainText())).graphVisualization()  #ex1
            pixmap = QPixmap('src/__imgcache__/CoherentComponent.png')
            self.labelImage1.setPixmap(pixmap)
            tmpStr = components(cons_graph(ast.literal_eval(self.inputTextEdit.toPlainText())).graph)     #ex3
            self.labelImage3.setText(tmpStr)
        else:
            self.labelImage4.setText("The graph is not graphical")

    def on_edge_randomize(self):
        self.clear_right_layout()

        self.inputTextEdit = QTextEdit()
        self.inputTextEdit.setText("""{ 1:  [2,5,6],
2:  [1,3,6],
3:  [2,4,5,12],
4:  [3,8,9,11],
5:  [1,3,7,9],
6:  [1,2,7],
7:  [5,6,8],
8:  [4,7,9,12],
9:  [4,5,8,10],
10: [9],
11: [4],
12: [3,8]}""")
        self.inputTextEdit.setMaximumHeight(250)
        randomize = QPushButton('Randomize',self)
        self.labelImage1 = QLabel()
        labelImage2 = QLabel('------------------------------------------>')
        self.labelImage3 = QLabel()
        self.labelImage2 = QLabel()
        self.layout4=QHBoxLayout()
        self.spin = QSpinBox()
        self.spin.setValue(10)
        self.layout4.addWidget(randomize)
        self.layout4.addWidget(self.spin)
        self.layout3=QHBoxLayout()
        self.layout3.addWidget(self.labelImage1)
        self.layout3.addWidget(labelImage2)
        self.layout3.addWidget(self.labelImage3)

        self.layoutRightGroupBox.addWidget(self.inputTextEdit)
        self.layoutRightGroupBox.addLayout(self.layout4)
        self.layoutRightGroupBox.addLayout(self.layout3)
        randomize.clicked.connect(self.on_click_randomize)

    def on_click_randomize(self):
        data['graph']=ast.literal_eval(self.inputTextEdit.toPlainText())
        tmp = AdjacencyList(data)
        tmp.graphVisualization()
        pixmap = QPixmap('src/__imgcache__/Representation.png')
        self.labelImage1.setPixmap(pixmap)
        randomizeGraph(tmp,self.spin.value()).graphVisualization()
        pixmap = QPixmap('src/__imgcache__/RandomizeGraph.png')
        self.labelImage3.setPixmap(pixmap)

    def on_find_euler_cycle(self):
        self.clear_right_layout()
        self.layout3=QVBoxLayout()
        self.layout4=QHBoxLayout()
        cycle = QPushButton('Find Euler Cycle(n)',self)
        self.spin = QSpinBox()
        self.spin.setValue(5)
        self.layout4.addWidget(cycle)
        self.layout4.addWidget(self.spin)
        self.labelImage1 = QLabel()
        self.labelImage2 = QLabel()
        self.labelImage3 = QLabel()
        self.layout3.addWidget(self.labelImage1)
        self.layout3.addWidget(self.labelImage2)
        self.layout3.addWidget(self.labelImage3)
        self.layoutRightGroupBox.addLayout(self.layout4)
        self.layoutRightGroupBox.addLayout(self.layout3)
        cycle.clicked.connect(self.on_click_cycle)

    def on_click_cycle(self):
        val = str(EulerGraph(self.spin.value()))
        pixmap = QPixmap('src/__imgcache__/CoherentComponent.png')
        self.labelImage1.setPixmap(pixmap)
        self.labelImage2.setText("The euler cycle found is:")
        print(val)
        self.labelImage3.setText(val)

    def on_k_regular_graphs(self):
        self.clear_right_layout()
        self.layout4=QHBoxLayout()
        random_k_regular_button = QPushButton('Random k-Regular Graphs',self)
        self.spin = QSpinBox()
        self.spin.setValue(2)
        self.spin1 = QSpinBox()
        self.spin1.setValue(8)
        self.layout4.addWidget(random_k_regular_button)
        self.layout4.addWidget(self.spin)
        self.layout4.addWidget(self.spin1)
        self.layout3=QHBoxLayout()
        self.labelImage1 = QLabel()
        self.layout3.addWidget(self.labelImage1)
        self.layoutRightGroupBox.addLayout(self.layout4)
        self.layoutRightGroupBox.addLayout(self.layout3)
        random_k_regular_button.clicked.connect(self.on_click_random_k)

    def on_click_random_k(self):
        random_k_regular(self.spin.value(),self.spin1.value())
        pixmap = QPixmap('src/__imgcache__/RandomizeGraph.png')
        self.labelImage1.setPixmap(pixmap)

    def on_find_hamiltion_cycle(self):
        self.clear_right_layout()

        self.inputTextEdit = QTextEdit()
        self.inputTextEdit.setText("""{1: [2,4,5],
2:  [1,3,5,6],
3:  [2,4,7],
4:  [1,3,6,7],
5:  [1,2,8],
6:  [2,4,8],
7:  [3,4,8],
8:  [5,6,7]}""")
        self.inputTextEdit.setMaximumHeight(250)
        self.layout4=QVBoxLayout()
        find_cycle = QPushButton('Find Hamiltion Cycle',self)
        self.layout4.addWidget(self.inputTextEdit)
        self.layout4.addWidget(find_cycle)
        self.labelImage1 = QLabel()
        self.labelImage3 = QLabel()

        labelImage2 = QLabel('------------------------------------------>')
        self.layout3=QHBoxLayout()
        self.layout3.addWidget(self.labelImage1)
        self.layout3.addWidget(labelImage2)
        self.layout3.addWidget(self.labelImage3)

        self.layoutRightGroupBox.addLayout(self.layout4)
        self.layoutRightGroupBox.addLayout(self.layout3)
        find_cycle.clicked.connect(self.on_click_find_cycle)

    def on_click_find_cycle(self):
        # find_Hamiltion_cycle
        data['graph']=ast.literal_eval(self.inputTextEdit.toPlainText())
        AdjacencyList(data).graphVisualization()
        pixmap = QPixmap('src/__imgcache__/Representation.png')
        self.labelImage1.setPixmap(pixmap)
        self.labelImage3.setText(str(find_Hamiltion_cycle(AdjacencyList(data).graph,1,[])))

#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 3
#
#------------------------------------------------------------------------------------------------------------------
    def initProject3(self):
        self.enable_all()
        self.project3Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        self.random_undirected_consistent_graph_button = QPushButton('Random undirected consistent graph',self)
        self.random_undirected_consistent_graph_spin1_n = QSpinBox()
        self.random_undirected_consistent_graph_spin1_n.setValue(6)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.random_undirected_consistent_graph_button)
        self.layout1.addWidget(self.random_undirected_consistent_graph_spin1_n)
        self.random_undirected_consistent_graph_button.clicked.connect(self.on_random_undirected_consistent_graph)
                
        self.random_s03e02_button = QPushButton('Algortih Dijkstra For \nRandom undirected consistent graph',self)
        self.random_s03e02_spin2_n = QSpinBox()
        self.random_s03e02_spin2_n.setValue(0)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.random_s03e02_button)
        self.layout2.addWidget(self.random_s03e02_spin2_n)
        self.random_s03e02_button.clicked.connect(self.on_s03e02_graph)

        self.random_s03e03_button = QPushButton('Adjacency Matrix',self)

        self.layout5 = QHBoxLayout()
        self.layout5.addWidget(self.random_s03e03_button)
        self.random_s03e03_button.clicked.connect(self.on_s03e03_graph)

        self.random_s03e04_button = QPushButton('Center/Minimax Center',self)

        self.layout6 = QHBoxLayout()
        self.layout6.addWidget(self.random_s03e04_button)
        self.random_s03e04_button.clicked.connect(self.on_s03e04_graph)

        self.random_s03e05_button = QPushButton('Minimal spanning tree',self)

        self.layout8 = QHBoxLayout()
        self.layout8.addWidget(self.random_s03e05_button)
        self.random_s03e05_button.clicked.connect(self.on_s03e05_graph)

        self.layout0=QVBoxLayout()
        self.layout0.addLayout(self.layout1)
        self.layout0.addLayout(self.layout2)
        self.layout0.addLayout(self.layout5)
        self.layout0.addLayout(self.layout6)
        self.layout0.addLayout(self.layout8)
        self.layoutLeftGroupBox.addLayout(self.layout0)

    def on_random_undirected_consistent_graph(self):
        self.clear_right_layout()
        self.graph_3=Generator.rand_undirected_consistent_graph(self.random_undirected_consistent_graph_spin1_n.value()).toAdjacencyList()
        self.graph_3.graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomUndirectedConsistentGraph.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)

    def on_s03e02_graph(self):
        self.clear_right_layout()

        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomUndirectedConsistentGraph.png')
        label.setPixmap(pixmap)
        label_result=QLabel(str(dijkstra(self.random_s03e02_spin2_n.value(),self.graph_3)))
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(label_result)

    def on_s03e03_graph(self):
        self.clear_right_layout()

        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomUndirectedConsistentGraph.png')
        label.setPixmap(pixmap)
        label_result=QLabel("\n".join(str(i) for i in dijkstraDist(self.graph_3)))
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(label_result)

    def on_s03e04_graph(self):
        self.clear_right_layout()

        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomUndirectedConsistentGraph.png')
        label.setPixmap(pixmap)
        label_result=QLabel(f'Center: {graphCenter(self.graph_3)}\nMinimax Center: {miniMaxCenter(self.graph_3)}')
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(label_result)

    def on_s03e05_graph(self):
        self.clear_right_layout()

        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomUndirectedConsistentGraph.png')
        label.setPixmap(pixmap)
        MST , weights, len_data = prim(self.graph_3)
        label_result=QLabel(f'Minimal spanning tree:\n'+'\n'.join(f'{MST[i]} - {i}    {weights[i][MST[i]]}' for i in range(1, len_data)))
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(label_result)

#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 4
#
#------------------------------------------------------------------------------------------------------------------
    def initProject4(self):
        self.enable_all()
        self.project4Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        #1.1
        self.random_digraph_edge_number_button = QPushButton('Random digraph edge(n,v)',self)
        self.random_digraph_edge_number_spin1_n = QSpinBox()
        self.random_digraph_edge_number_spin1_n.setValue(10)
        self.random_digraph_edge_number_spin1_l = QSpinBox()
        self.random_digraph_edge_number_spin1_l.setValue(5)

        self.layout0 = QHBoxLayout()
        self.layout0.addWidget(self.random_digraph_edge_number_button)
        self.layout0.addWidget(self.random_digraph_edge_number_spin1_n)
        self.layout0.addWidget(self.random_digraph_edge_number_spin1_l)
        self.random_digraph_edge_number_button.clicked.connect(self.on_random_digraph_edge_number)
        #1.2
        self.random_digraph_edge_prob_button = QPushButton('Random digraph edge(n,p)',self)
        self.random_digraph_edge_prob_spin1_n = QSpinBox()
        self.random_digraph_edge_prob_spin1_n.setValue(10)
        self.random_digraph_edge_prob_spin1_l = QDoubleSpinBox()
        self.random_digraph_edge_prob_spin1_l.setSingleStep(0.1)
        self.random_digraph_edge_prob_spin1_l.setValue(0.5)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.random_digraph_edge_prob_button)
        self.layout1.addWidget(self.random_digraph_edge_prob_spin1_n)
        self.layout1.addWidget(self.random_digraph_edge_prob_spin1_l)
        self.random_digraph_edge_prob_button.clicked.connect(self.on_random_digraph_edge_prob)

        #2
        self.kosaraju_button = QPushButton('Kosaraju Algorithm (Random(n,p))',self)
        self.kosaraju_spin1_n = QSpinBox()
        self.kosaraju_spin1_n.setValue(10)
        self.kosaraju_spin1_l = QDoubleSpinBox()
        self.kosaraju_spin1_l.setSingleStep(0.1)
        self.kosaraju_spin1_l.setValue(0.5)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.kosaraju_button)
        self.layout2.addWidget(self.kosaraju_spin1_n)
        self.layout2.addWidget(self.kosaraju_spin1_l)
        self.kosaraju_button.clicked.connect(self.on_kosaraju)

        self.bellman_ford_button = QPushButton('Bellma Ford Algorithm (Random(n,p))',self)
        self.bellman_ford_spin1_n = QSpinBox()
        self.bellman_ford_spin1_n.setValue(10)
        self.bellman_ford_spin1_l = QDoubleSpinBox()
        self.bellman_ford_spin1_l.setSingleStep(0.1)
        self.bellman_ford_spin1_l.setValue(0.5)

        self.layout5 = QHBoxLayout()
        self.layout5.addWidget(self.bellman_ford_button)
        self.layout5.addWidget(self.bellman_ford_spin1_n)
        self.layout5.addWidget(self.bellman_ford_spin1_l)
        self.bellman_ford_button.clicked.connect(self.on_bellman_ford)

        #5
        self.johnson_button = QPushButton('Johnson Algorithm (Random(n,p))',self)
        self.johnson_spin1_n = QSpinBox()
        self.johnson_spin1_n.setValue(10)
        self.johnson_spin1_l = QDoubleSpinBox()
        self.johnson_spin1_l.setSingleStep(0.1)
        self.johnson_spin1_l.setValue(0.5)

        self.layout6 = QHBoxLayout()
        self.layout6.addWidget(self.johnson_button)
        self.layout6.addWidget(self.johnson_spin1_n)
        self.layout6.addWidget(self.johnson_spin1_l)
        self.johnson_button.clicked.connect(self.on_johnson)

        self.layoutLeftGroupBox.addLayout(self.layout0)
        self.layoutLeftGroupBox.addLayout(self.layout1)
        self.layoutLeftGroupBox.addLayout(self.layout2)
        self.layoutLeftGroupBox.addLayout(self.layout5)
        self.layoutLeftGroupBox.addLayout(self.layout6)

    def on_random_digraph_edge_number(self):
        self.clear_right_layout()
        Generator.rand_digraph_edge_number(self.random_digraph_edge_number_spin1_n.value(),self.random_digraph_edge_number_spin1_l.value()).graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomDigraphEdgeNumber.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)

    def on_random_digraph_edge_prob(self):
        self.clear_right_layout()
        Generator.rand_digraph_edge_probability(self.random_digraph_edge_prob_spin1_n.value(),self.random_digraph_edge_prob_spin1_l.value()).graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomDigraphEdgeProbability.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)
    
    def on_kosaraju(self):
        self.clear_right_layout()
        tmp = Kosaraju(self.kosaraju_spin1_n.value(),self.kosaraju_spin1_l.value(),True)
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomDigraphEdgeProbability.png')
        label.setPixmap(pixmap)
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(QLabel("Result:"))
        self.layoutRightGroupBox.addWidget(QLabel(str(tmp)))

    def on_bellman_ford(self):
        self.clear_right_layout()
        repres = Generator.rand_digraph_edge_probability(self.bellman_ford_spin1_n.value(),self.bellman_ford_spin1_l.value())
        repres.graphVisualization()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomDigraphEdgeProbability.png')
        label.setPixmap(pixmap)
        graph=[]

        for i in repres.graph.keys():
            for j in repres.graph[i]:
                graph.append([i,j,repres.edges_description[(i,j)]['weight']])
        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(QLabel("Result:"))
        self.layoutRightGroupBox.addWidget(QLabel(str(ShortPaths.bellman_ford(0,graph,self.bellman_ford_spin1_n.value()))))

    def on_johnson(self):
        self.clear_right_layout()
        tmp=Generator.rand_digraph_edge_probability(self.johnson_spin1_n.value(),self.johnson_spin1_l.value()).toAdjacencyList()
        tmp.graphVisualization()
        # ShortPaths.johnson(tmp)
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/randomDigraphEdgeProbability.png')
        label.setPixmap(pixmap)

        self.layoutRightGroupBox.addWidget(label)
        self.layoutRightGroupBox.addWidget(QLabel("Result:"))
        self.layoutRightGroupBox.addWidget(QLabel(ShortPaths.johnson(tmp)))

#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 5
#
#------------------------------------------------------------------------------------------------------------------
    def initProject5(self):
        self.enable_all()
        self.project5Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        self.proj5_button = QPushButton('Random flow network &\nFord-Fulkerson algorithm',self)
        self.spin = QSpinBox()
        self.spin.setValue(3)
        self.proj5_button.clicked.connect(self.on_proj5)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.proj5_button)
        self.layout1.addWidget(self.spin)

        self.layoutLeftGroupBox.addLayout(self.layout1)

    def on_proj5(self):
        self.clear_right_layout()
        self.layout3=QHBoxLayout()

        g, layers = random_flow_network(self.spin.value())
        Utils.plot_graph(g, layers, filename='random_flow_network')

        self.layout4=QVBoxLayout()
        label0 = QLabel("Random flow network")
        label1 = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/random_flow_network.png')
        label1.setPixmap(pixmap)
        label2 = QLabel(f'Layers: {layers}')
        self.layout4.addWidget(label0)
        self.layout4.addWidget(label1)
        self.layout4.addWidget(label2)
        
        f, fmax = Ford_Fulkerson(g)
        Utils.plot_graph(g, layers, filename='ford_fulkerson_algorithm', flow=f)
        self.layout7=QVBoxLayout()     
        label3 = QLabel("Ford-Fulkerson algorithm")
        label4 = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/ford_fulkerson_algorithm.png')
        label4.setPixmap(pixmap)
        label5 = QLabel(f"Maximum flow value |Fmax| = {fmax}")
        self.layout7.addWidget(label3)
        self.layout7.addWidget(label4)
        self.layout7.addWidget(label5)

        self.layout3.addLayout(self.layout4)
        self.layout3.addLayout(self.layout7)
        self.layoutRightGroupBox.addLayout(self.layout3)
        
#+-----------------------------------------------------------------------------------------------------------------
#
# PROJECT 6
#
#------------------------------------------------------------------------------------------------------------------
    def initProject6(self):
        self.enable_all()
        self.project6Button.setDisabled(True)
        self.clear_right_layout()
        self.clear_left_layout()
        #-------------------------
        #1.1print(page_rank_random_wandering(di_graph, 0.15,1000000))
        self.page_rank_random_wandering_button = QPushButton('Page rank random wandering',self)
        self.page_rank_random_wandering_spin1_l = QDoubleSpinBox()
        self.page_rank_random_wandering_spin1_l.setSingleStep(0.1)
        self.page_rank_random_wandering_spin1_l.setValue(0.15)
        self.page_rank_random_wandering_spin1_n = QSpinBox()
        self.page_rank_random_wandering_spin1_n.setMaximum(2000000)
        self.page_rank_random_wandering_spin1_n.setValue(1000000)
        self.page_rank_random_wandering_button.clicked.connect(self.on_page_rank_random_wandering)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.page_rank_random_wandering_button)
        self.layout1.addWidget(self.page_rank_random_wandering_spin1_l)
        self.layout1.addWidget(self.page_rank_random_wandering_spin1_n)

        #1.2
        self.page_rank_vector_iteration_button = QPushButton('Page rank vector iteration',self)
        self.page_rank_vector_iteration_spin1_l = QDoubleSpinBox()
        self.page_rank_vector_iteration_spin1_l.setSingleStep(0.1)
        self.page_rank_vector_iteration_spin1_l.setValue(0.15)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.page_rank_vector_iteration_button)
        self.layout2.addWidget(self.page_rank_vector_iteration_spin1_l)
        self.page_rank_vector_iteration_button.clicked.connect(self.on_page_rank_vector_iteration)
        #2
        self.traveling_salesman_algorithm_button = QPushButton('Traveling salesman algorithm',self)
        self.traveling_salesman_algorithm_spin = QSpinBox()
        self.traveling_salesman_algorithm_spin.setMaximum(2000000)
        self.traveling_salesman_algorithm_spin.setValue(1000)

        self.layout0 = QHBoxLayout()
        self.layout0.addWidget(self.traveling_salesman_algorithm_button)
        self.layout0.addWidget(self.traveling_salesman_algorithm_spin)
        self.traveling_salesman_algorithm_button.clicked.connect(self.on_traveling_salesman_algorithm)

        self.layoutLeftGroupBox.addLayout(self.layout1)
        self.layoutLeftGroupBox.addLayout(self.layout2)
        self.layoutLeftGroupBox.addLayout(self.layout0)

    def on_page_rank_random_wandering(self):
        self.clear_right_layout()
        self.layout3=QHBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/Rysunek.png')
        label.setPixmap(pixmap)
        tmp = page_rank_random_wandering(di_graph, self.page_rank_random_wandering_spin1_l.value(),self.page_rank_random_wandering_spin1_n.value())
        label1 = QLabel('\n'.join(str(i)+":"+str(j) for i,j in tmp.items()))
        self.layout3.addWidget(label)
        self.layout3.addWidget(label1)
        self.layoutRightGroupBox.addLayout(self.layout3)

    def on_page_rank_vector_iteration(self):
        self.clear_right_layout()
        self.layout3=QHBoxLayout()
        label = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/Rysunek.png')
        label.setPixmap(pixmap)
        tmp=page_rank_vector_iteration(di_graph, self.page_rank_vector_iteration_spin1_l.value())
        label1 = QLabel('\n'.join(str(i)+":"+str(j) for i,j in tmp.items()))
        self.layout3.addWidget(label)
        self.layout3.addWidget(label1)
        self.layoutRightGroupBox.addLayout(self.layout3)

    def on_traveling_salesman_algorithm(self):
        lista=read_data_from_file('src/data.dat')
        plt.plot([i[0] for i in lista],[i[1] for i in lista], linestyle='-', marker='o', color='red')
        plt.savefig('src/__imgcache__/traveling_1.png')
        plt.close()
        start_cycle_length=distance(lista)
        start = time.time()
        lista=algorith(lista, self.traveling_salesman_algorithm_spin.value()) 
        # MAX_IT: 500 000, TIME: 66s DISTANCE: 2072
        # MAX_IT: 1 000 000, TIME: 134s DISTANCE: 2006
        end = time.time()
        print(end - start)
        end_cycle_length=distance(lista)
        plt.plot([i[0] for i in lista],[i[1] for i in lista], linestyle='-', marker='o', color='red')
        plt.savefig('src/__imgcache__/traveling_2.png')
        plt.close()

        self.clear_right_layout()
        self.layout3=QHBoxLayout()

        self.layout4=QVBoxLayout()
        label0 = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/traveling_1.png')
        label0.setPixmap(pixmap)
        label1 = QLabel("Start Cycle Length")
        label2 = QLabel(str(start_cycle_length))
        self.layout4.addWidget(label0)
        self.layout4.addWidget(label1)
        self.layout4.addWidget(label2)
        
        self.layout7=QVBoxLayout()     
        label3 = QLabel(self)
        pixmap = QPixmap('src/__imgcache__/traveling_2.png')
        label3.setPixmap(pixmap)
        label4 = QLabel("End Cycle Length")
        label5 = QLabel(str(end_cycle_length))
        self.layout7.addWidget(label3)
        self.layout7.addWidget(label4)
        self.layout7.addWidget(label5)

        self.layout3.addLayout(self.layout4)
        self.layout3.addLayout(self.layout7)
        self.layoutRightGroupBox.addLayout(self.layout3)
