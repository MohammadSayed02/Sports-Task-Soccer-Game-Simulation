'''
/**
 * Soccer Game Simulation
 *
 *  Created on: Thursday Apr 27 2023
 *  Author    : Mohammad Sayed Zaky
 */
 '''
# ________________________________________________Libraries______________________________________________!!
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
import numpy as np
import pyqtgraph as pg
import matplotlib.colors as mcolors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm
import sys
import logging
import os
import time
# ___________________________________________MainWindow__________________________________________________!!
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soccer Game Simulation")
        self.setWindowIcon(QIcon('imgs/football.png'))
        self.resize(1920, 1000)
        # self.setFixedSize(1920, 1000)
        self.pixmap = QPixmap("imgs/background.png")
        self.background = QLabel(self)
        self.background.setPixmap(self.pixmap)
        self.create_widgets()
        self.create_layout()
# ____________________________________________initialization_____________________________________________!!
        self.g = 9.81
        self.Distance_from_the_goal = 0
        self.Firing_angle = 0.0
        self.Firing_velocityag = 0
        self.current_path = None
        self.saved = False
        self.x = 0
        self.high_max = 0
        self.modeToggle = False
        # self.x, self.high_max= self.adding()
# _________________________________________resize to Full Screen_________________________________________!!
    def resizeEvent(self, event):
        pixmap = self.pixmap.scaled(self.size(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.background.setPixmap(pixmap)
        self.background.setGeometry(0, 0, self.width(), self.height())
# __________________________________________________Widgets______________________________________________!!
    def create_widgets(self):
        self.distance_slider = QSlider(Qt.Orientation.Horizontal)
        self.distance_slider.setRange(0, 200)
        self.distance_slider.setValue(10)
        self.distance_slider.setTickInterval(1)
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setRange(5, 90)
        self.angle_slider.setValue(9)
        self.angle_slider.setTickInterval(1)
        self.velocity_slider = QSlider(Qt.Orientation.Horizontal)
        self.velocity_slider.setRange(5, 150)
        self.velocity_slider.setValue(12)
        self.velocity_slider.setTickInterval(1)
        self.max_height_label = QLabel()
        self.max_height_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.goal_height_label = QLabel()
        self.goal_height_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
# ______________________________________________Layout___________________________________________________!!
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
        self.label2 = QLabel("Firing angle:          ")
        self.label2.setStyleSheet('color: black')
        self.label2.setFont(QFont("sanserif",12))
        self.label3 = QLabel("Firing velocity:       ")
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
        self.fig = Figure(figsize=(13, 7), dpi=100)        
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.canvas.setVisible(False)
        self.setMinimumSize(200, 200)
        self.axes.set_alpha(0.5)
        self.axes.set_facecolor((0, 0, 0, 0))
        self.axes.spines['bottom'].set_alpha(0.2)
        self.axes.spines['top'].set_alpha(0)
        self.axes.spines['right'].set_alpha(0)
        self.axes.spines['left'].set_alpha(0.2)
        self.axes.tick_params(axis='both', which='both', length=0, labelcolor='blue')
        font = QFont()
        font.setBold(True)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.Plot_Toggle = QPushButton()
        self.Plot_Toggle.setIcon(QIcon('imgs/ball-mode.png'))
        self.Plot_Toggle.setMinimumSize(40,40)
        self.Plot_Toggle.setMaximumSize(40,40)
        self.Plot_Toggle.setIconSize(QSize(40,40))
        self.Plot_Toggle.setStyleSheet("QPushButton { border-radius: 50px; }")
        self.Plot_Toggle.clicked.connect(self.update_plot_modeToggle)
        self.save_btn = QPushButton()
        self.save_btn.setIcon(QIcon('imgs/save'))
        self.save_btn.setMinimumSize(33,33)
        self.save_btn.setMaximumSize(33,33)
        self.save_btn.setIconSize(QSize(33,33))
        self.save_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
        self.save_btn.clicked.connect(self.save_asFile)
        self.show_hide_btn = QPushButton()
        self.show_hide_btn.setIcon(QIcon('imgs/hide'))
        self.show_hide_btn.setMinimumSize(40,40)
        self.show_hide_btn.setMaximumSize(40,40)
        self.show_hide_btn.setIconSize(QSize(40,40))
        self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
        self.show_hide_btn.clicked.connect(self.toggleCanvas)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)       
        self.spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hbox_plotWidget = QHBoxLayout()
        self.hbox_plotWidget.addItem(self.spacer)
        self.hbox_plotWidget.addWidget(self.canvas)
        self.hbox_plotWidget.addItem(self.spacer)
        layout.addLayout(self.hbox_plotWidget)
        layout.addWidget(self.Plot_Toggle)
        layout.addItem(spacer)       
        layout.addWidget(self.save_btn)
        layout.addItem(spacer)       
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
# ________________________________________________Functions______________________________________________!!

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
        # return self.x, self.high_max
# __________________________________________________Slots________________________________________________!!

    def show_slider_value1(self, value):
        self.label_slider1.setText(str(self.distance_slider.value()))
        self.adding()
        

    def show_slider_value2(self, value):
        self.label_slider2.setText(str(self.angle_slider.value()))
        self.adding()
        

    def show_slider_value3(self, value):
        self.label_slider3.setText(str(self.velocity_slider.value()))
        self.adding()
        
# _________________________________________________Plot__________________________________________________!!
   
    def update_plot_modeToggle(self):
        if (self.modeToggle == True):
            self.modeToggle = False
        else:
            self.modeToggle = True
            
    def update_plot(self):
        
        if(self.modeToggle):
            
            self.axes.clear()
            self.axes.plot(self.x, self.high_max, color='green')
            self.axes.set_xlabel('Distance from Goal')
            self.axes.set_ylabel('Height of the Ball')
            self.axes.set_title('Ball Tracking')
            # for i in range(0, len(self.x), 30000):
            #     # self.axes.plot(self.x[i], self.high_max[i])
            #     self.ballImg, = self.axes.plot([self.x[i]], [self.high_max[i]], 'o', color='green', markersize=30)
            self.canvas.draw()
            
            
            self.Plot_Toggle.setIcon(QIcon('imgs/curve-mode.png'))
            self.Plot_Toggle.setMinimumSize(40,40)
            self.Plot_Toggle.setMaximumSize(40,40)
            self.Plot_Toggle.setIconSize(QSize(40,40))
            self.Plot_Toggle.setStyleSheet("QPushButton { border-radius: 50px; }")
        
        
        else:
            colors = mcolors.LinearSegmentedColormap.from_list("", ["lightgreen", "darkgreen"])
            self.axes.clear()
            # self.axes.plot(self.x, self.high_max, color='green')
            self.axes.set_xlabel('Distance from Goal')
            self.axes.set_ylabel('Height of the Ball')
            self.axes.set_title('Ball Tracking')
            for i in range(0, len(self.x), 30000):
                
                    color = colors(i / len(self.x))
                    self.ballImg, = self.axes.plot([self.x[i]], [self.high_max[i]], 'o', color=color, markersize=32)
                
            self.canvas.draw()
            
            self.Plot_Toggle.setIcon(QIcon('imgs/ball-mode.png'))
            self.Plot_Toggle.setMinimumSize(40,40)
            self.Plot_Toggle.setMaximumSize(40,40)
            self.Plot_Toggle.setIconSize(QSize(40,40))
            self.Plot_Toggle.setStyleSheet("QPushButton { border-radius: 50px; }")
# __________________________________________________Save_________________________________________________!!
       
    def save_asFile(self):
        if self.maybe_save():
            pathname, _ = QFileDialog.getSaveFileName(self, 'Save file', 'save Log', 'Log Files (*.log)')
            logging.basicConfig(filename=pathname, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

            dir_name, file_name = os.path.split(pathname)

            with open(os.path.join(dir_name, file_name), 'w') as f:
                f.write("Distance From Goal: {}\n".format(self.distance_slider.value()))
                f.write("Firing Angle: {}\n".format(self.angle_slider.value()))
                f.write("Firing Velocity: {}\n".format(self.velocity_slider.value()))
                f.write("Maximum Ball Height: {}\n".format(max(self.high_max)))
                f.write("Ball Height at Goal Plane: {}\n".format(self.height_at_the_goal))

            fig_path = os.path.join(dir_name, "plot.png")
            self.fig.savefig(fig_path)

            QMessageBox.about(self, "Save", "Congratulations, Your Current Simulation Outputs have been saved successfully!!")
            self.current_path = pathname
            # self.saved = True
            self.setWindowTitle(pathname)
  
  


    def maybe_save(self):
        if (self.distance_slider.valueChanged.connect(lambda: True) or 
            self.angle_slider.valueChanged.connect(lambda: True) or 
            self.velocity_slider.valueChanged.connect(lambda: True)):
            return True
        else:
            return False


# ______________________________________________Exit-Saving______________________________________________!!

    def closeEvent(self, event):
        if not self.saved:
            reply = QMessageBox.question(self, 'Save', 'Do you want to save your changes?', 
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Save:
                self.save_asFile()
                # self.saved = True
            elif reply == QMessageBox.StandardButton.Discard:
                exit
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
# _____________________________________________Show/Hide Toggle__________________________________________!!

    def toggleCanvas(self):
        if self.canvas.isVisible():
            self.canvas.hide()
            self.show_hide_btn.setIcon(QIcon('imgs/hide'))
            self.show_hide_btn.setMinimumSize(40,40)
            self.show_hide_btn.setMaximumSize(40,40)
            self.show_hide_btn.setIconSize(QSize(40,40))
            self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
            
        else:
            self.canvas.show()
            self.show_hide_btn.setIcon(QIcon('imgs/visible'))
            self.show_hide_btn.setMinimumSize(40,40)
            self.show_hide_btn.setMaximumSize(40,40)
            self.show_hide_btn.setIconSize(QSize(25,25))
            self.show_hide_btn.setStyleSheet("QPushButton { border-radius: 50px; }")
            
# __________________________________________________Exec_________________________________________________!!
        

app = QApplication(sys.argv)
app.processEvents()
window = MainWindow()
window.show()
sys.exit(app.exec())
