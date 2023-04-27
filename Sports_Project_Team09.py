'''
/**
 * Soccer Game Simulation
 *
 *  Created on: Thursday Apr 27 2023
 *  Author    : Mohammad Sayed Zaky
 */'''
# ________________________________________________Libraries______________________________________________!!
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm
import sys
# ____________________________________________global-variables___________________________________________!!
Distance_from_the_goal = 0
Firing_angle = 0.0
Firing_velocityag = 0
g = 9.81
font = QFont()
font.setBold(True)
# ________________________________________________Canvas_________________________________________________!!

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)        
        self.axes = fig.add_subplot(111)
        super().__init__(fig)        
        self.setVisible(True)
        self.double_click_enabled = True
        self.setParent(parent)
        self.setMinimumSize(200, 200)
        self.axes.set_alpha(0.5)
        self.axes.set_facecolor((0, 0, 0, 0))
        self.axes.spines['bottom'].set_alpha(0.2)
        self.axes.spines['top'].set_alpha(0)
        self.axes.spines['right'].set_alpha(0)
        self.axes.spines['left'].set_alpha(0.2)
        self.axes.tick_params(axis='both', which='both', length=0, labelcolor='blue')
        
        

    def mouseDoubleClickEvent(self, event):
        if self.double_click_enabled:
            self.setVisible(False)
            self.double_click_enabled = False
        else:
            self.setVisible(True)
            self.double_click_enabled = True



# class PlotCanvas(FigureCanvas):
#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         super().__init__(fig)
        
        
# ______________________________________________MainWindow_______________________________________________!!
        
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Soccer Game Simulation")
        self.setWindowIcon(QIcon('imgs/icon.jpg'))
        self.setFixedSize(1920, 1000)
        self.pixmap = QPixmap("imgs/background.png")
        self.background = QLabel(self)
        self.background.setPixmap(self.pixmap)
        self.high_max=0
                
    def resizeEvent(self, event):
        pixmap = self.pixmap.scaled(self.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())
        self.create_widgets()
        self.create_layout()
        
    def create_widgets(self):
        self.distance_slider = QSlider(Qt.Orientation.Horizontal)
        self.distance_slider.setRange(0, 200)
        self.distance_slider.setValue(10)
        self.distance_slider.setTickInterval(1)
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setRange(5, 90)
        self.angle_slider.setValue(10)
        self.angle_slider.setTickInterval(1)
        self.velocity_slider = QSlider(Qt.Orientation.Horizontal)
        self.velocity_slider.setRange(5, 150)
        self.velocity_slider.setValue(10)
        self.velocity_slider.setTickInterval(1)
        self.max_height_label = QLabel()
        self.max_height_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.goal_height_label = QLabel()
        self.goal_height_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


    def create_layout(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.label_slider1 = QLabel(self)
        self.label_slider2 = QLabel(self)
        self.label_slider3 = QLabel(self)
        self.label_slider1.setFont(QFont("sanserif",15))
        self.label_slider2.setFont(QFont("sanserif",15))
        self.label_slider3.setFont(QFont("sanserif",15))
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.label1 = QLabel("Distance from goal:")
        self.label1.setStyleSheet('color: black')
        self.label1.setFont(QFont("sanserif",12))
        self.label2 = QLabel("Firing angle:")
        self.label2.setStyleSheet('color: black')
        self.label2.setFont(QFont("sanserif",12))
        self.label3 = QLabel("Firing velocity:")
        self.label3.setStyleSheet('color: black')
        self.label3.setFont(QFont("sanserif",12))
        self.hbox1.addWidget(self.label1)
        self.hbox1.addWidget(self.distance_slider)
        self.hbox1.addWidget(self.label_slider1)
        self.hbox2.addWidget(self.label2)
        self.hbox2.addWidget(self.angle_slider)
        self.hbox2.addWidget(self.label_slider2)
        self.hbox3.addWidget(self.label3)
        self.hbox3.addWidget(self.velocity_slider)
        self.hbox3.addWidget(self.label_slider3)        
        self.label_slider1.setText(str(self.distance_slider.value()))
        self.label_slider2.setText(str(self.angle_slider.value()))
        self.label_slider3.setText(str(self.velocity_slider.value()))     
        self.label4 = QLabel("Maximum ball height:")
        self.label4.setStyleSheet('color: green')
        self.label4.setFont(QFont("sanserif",20))
        self.label5 = QLabel("Ball height at goal plane:")
        self.label5.setStyleSheet('color: green')
        self.label5.setFont(QFont("sanserif",20))        
        self.max_height_label = QLabel()
        self.max_height_label.setStyleSheet('color:green')
        self.max_height_label.setFont(QFont("sanserif",20))
        self.max_height_label.setAlignment(Qt.AlignRight) 
        self.goal_height_label = QLabel()
        self.goal_height_label.setStyleSheet('color:green')
        self.goal_height_label.setFont(QFont("sanserif",20))
        self.goal_height_label.setAlignment(Qt.AlignRight)
        self.hbox4.addWidget(self.label4)
        self.hbox4.addWidget(self.max_height_label)
        self.hbox5.addWidget(self.label5)
        self.hbox5.addWidget(self.goal_height_label)
        form_layout.addRow(self.hbox1)
        form_layout.addRow(self.hbox2)
        form_layout.addRow(self.hbox3)
        form_layout.addRow(self.hbox4)
        form_layout.addRow(self.hbox5)
        layout.addLayout(form_layout)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.plot_widget = PlotCanvas(self, width=13, height=7, dpi=100)
        # self.fig = Figure(figsize=(50, 40), dpi=100)
        # self.ax = self.fig.add_subplot(111)
        self.show_hide_btn = QPushButton()
        self.show_hide_btn.setIcon(QIcon('imgs/visible'))
        self.show_hide_btn.setMinimumSize(40,40)
        self.show_hide_btn.setMaximumSize(40,40)
        self.show_hide_btn.setIconSize(QSize(25,25))
        self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
        self.show_hide_btn.clicked.connect(self.toggleCanvas)
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)       
        self.spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hbox_plotWidget = QHBoxLayout()
        self.hbox_plotWidget.addItem(self.spacer)
        self.hbox_plotWidget.addWidget(self.plot_widget)
        self.hbox_plotWidget.addItem(self.spacer)
        layout.addLayout(self.hbox_plotWidget)        
        layout.addWidget(self.show_hide_btn)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100) # Update every 100 milliseconds    
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.distance_slider.valueChanged.connect(self.show_slider_value1)
        self.angle_slider.valueChanged.connect(self.show_slider_value2)
        self.velocity_slider.valueChanged.connect(self.show_slider_value3)
        

    def adding(self):
        pi = 22 / 7
        self.max_height_label.clear()
        self.goal_height_label.clear()        
        self.Distance_from_the_goal = (self.distance_slider.value())
        self.Firing_angle = ((self.angle_slider.value())) * (pi / 180)
        self.Firing_velocityag = (self.velocity_slider.value())
        self.time = (self.Firing_velocityag * np.sin(self.Firing_angle)) / 9.8
        self.high = (self.Firing_velocityag * self.time * np.sin(self.Firing_angle)) - (
                    0.5 * 9.8 * self.time * self.time)
        self.s = self.Firing_velocityag * self.time * np.cos(self.Firing_angle)
        self.y = self.Distance_from_the_goal - self.s
        self.timing = self.y / (self.Firing_velocityag * np.cos(self.Firing_angle))
        self.t1 = self.time + self.timing
        self.t = np.arange(0, self.t1, .00001)
        self.height_at_the_goal = self.high - 0.5 * 9.8 * self.timing * self.timing
        self.high_max = (self.Firing_velocityag * self.t * np.sin(self.Firing_angle)) - (0.5 * 9.8 * self.t * self.t)
        self.x = ((self.Firing_velocityag * self.t) * np.cos(self.Firing_angle))
        self.max_height_label.setText(str(self.high))
        self.goal_height_label.setText(str(self.height_at_the_goal))

           

    def show_slider_value1(self, value):
        self.label_slider1.setText(str(self.distance_slider.value()))
        self.adding()

    def show_slider_value2(self, value):
        self.label_slider2.setText(str(self.angle_slider.value()))
        self.adding()

        
    def show_slider_value3(self, value):
        self.label_slider3.setText(str(self.velocity_slider.value()))
        self.adding()
     
    def update_plot(self):
        self.plot_widget.axes.clear()
        self.plot_widget.axes.plot(self.x, self.high_max)
        self.plot_widget.axes.set_xlabel('Distance from Goal')
        self.plot_widget.axes.set_ylabel('Height of the Ball')
        self.plot_widget.axes.set_title('Ball Tracking')        
        self.plot_widget.draw()
          
            
    def toggleCanvas(self):
        if self.plot_widget.isVisible():
            self.plot_widget.hide()
            self.show_hide_btn.setIcon(QIcon('imgs/hide'))
            self.show_hide_btn.setMinimumSize(40,40)
            self.show_hide_btn.setMaximumSize(40,40)
            self.show_hide_btn.setIconSize(QSize(40,40))
            self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
            
        else:
            self.plot_widget.show()
            self.show_hide_btn.setIcon(QIcon('imgs/visible'))
            self.show_hide_btn.setMinimumSize(40,40)
            self.show_hide_btn.setMaximumSize(40,40)
            self.show_hide_btn.setIconSize(QSize(25,25))
            self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
            
# __________________________________________________Exec_________________________________________________!!
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())



