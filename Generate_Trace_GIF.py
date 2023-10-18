#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 09:15:06 2023

@author: Evan Telford (ejt2133@columbia.edu)
"""
#%%
#load pertinent packages
import pandas as pan
import glob
import numpy as np
import os
from pathlib import Path
from tqdm import tqdm
from PIL import Image
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QFileDialog,
    QWidget,
    QGroupBox,
    QColorDialog
)
import re
#%%
#sets the default font style for matplotlib plots
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 4}
matplotlib.rc('font', **font)
matplotlib.use('Qt5Agg')
#%%
#define a function for natural sorting globbed files.
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
#%%
#canvas class for making the data plot
class MplCanvas(FigureCanvasQTAgg):
    #Initialization function for the canvas
    def __init__(self, parent=None, width=7, height=7, dpi=600):
        super().__init__()
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        for axis in ['top','bottom','left','right']:
            self.axes.spines[axis].set_color('k')
            self.axes.spines[axis].set_linewidth(0.5)
        self.axes.tick_params(width=0.5,length=2.0)
        super(MplCanvas, self).__init__(self.fig)
#%%
#this is the main GUI window class
class MainWindow(QMainWindow):
    #Initialization for the main gui window
    def __init__(self):
        #initialize gui parameters
        super().__init__()
        self.custom_font = QFont('Arial',10)
        app.setFont(self.custom_font, "QLabel")
        self.setFixedSize(1400,900)
        self.main_layout = QGridLayout()
        self.setWindowTitle("Generate Trace Plots")
        self.filename=[] 
        #define gui areas
        self.load_GUI()
        self.available_data()
        self.plot_data()
        self.generate_trace()
        #create plot
        self.dataplot=MplCanvas(self)
        self.toolbar1=NavigationToolbar(self.dataplot,self)
        #update default layout size
        self.plot_x.setText(str(1400))
        self.plot_y.setText(str(900))
        #Add all widgets to the overall layout
        self.main_layout.addWidget(self.LoadGUI,0,0,1,1)
        self.main_layout.addWidget(self.AvailableData,1,0,1,1)
        self.main_layout.addWidget(self.Plot,2,0,3,1)
        self.main_layout.addWidget(self.Trace,5,0,2,1)
        self.main_layout.addWidget(self.dataplot,1,1,6,1)
        self.main_layout.addWidget(self.toolbar1,0,1,1,1)
        #create the main layout
        self.widget=QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        
#GUI generators##################################################################################################################################################################################################################################     
    
    #GUI for loading data files
    def load_GUI(self):
        #define layout
        layout = QGridLayout()
        #define group box
        self.LoadGUI = QGroupBox('Load Data') 
        #create widgets
        self.filename = QLineEdit()
        l2_button=QPushButton('Load Data')
        l2_button.clicked.connect(self.getfile)
        l2_button.clicked.connect(lambda: self.load_data(self.filename.text()))
        #adds widgets to layout
        layout.addWidget(self.filename, 0,1) 
        layout.addWidget(l2_button, 0,0)
        #set the layout
        self.LoadGUI.setLayout(layout)
     
    #GUI for listing the available data columns
    def available_data(self):
        #define layout
        layout = QGridLayout()
        #define group box
        self.AvailableData = QGroupBox('Available Data')
        #create widgets
        self.xlabel= QLabel("x-axis")
        self.ylabel= QLabel("y-axis")
        self.xaxis=QComboBox()
        self.yaxis=QComboBox()
        self.xaxis.currentIndexChanged.connect(lambda: self.clear_plot_parameters())
        self.yaxis.currentIndexChanged.connect(lambda: self.clear_plot_parameters())
        #center labels:
        self.xlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ylabel.setAlignment(QtCore.Qt.AlignCenter)
        #adds widgets to layout
        layout.addWidget(self.xlabel, 0,0) 
        layout.addWidget(self.ylabel, 0,1)
        layout.addWidget(self.xaxis,1,0)
        layout.addWidget(self.yaxis,1,1) 
        #set the layout
        self.AvailableData.setLayout(layout)

    #GUI for plotting data in the canvas and setting plot parameters
    def plot_data(self):
        #define layout
        layout = QGridLayout()
        #create widgets
        self.Plot = QGroupBox('Plot Data') 
        #create widgets
        self.xlim_lower_label=QLabel("Lower x-axis")
        self.xlim_upper_label=QLabel("Upper x-axis")
        self.ylim_lower_label=QLabel("Lower y-axis")
        self.ylim_upper_label=QLabel("Upper y-axis")
        self.xlim_lower=QLineEdit()
        self.xlim_upper=QLineEdit()
        self.ylim_lower=QLineEdit()
        self.ylim_upper=QLineEdit()
        #changing labels
        self.y_label_label=QLabel("y-axis label")
        self.x_label_label=QLabel("x-axis label")
        self.y_label=QLineEdit()
        self.x_label=QLineEdit()
        #changing font size
        self.font_label=QLabel("Font size")
        self.font_size=QLineEdit()
        #line styles, colors, marker size
        self.axis_width_label=QLabel("Axis width")
        self.axis_width=QLineEdit()
        self.data_plot_style_label=QLabel("Plot style")
        self.data_plot_style=QLineEdit()
        self.data_markersize_label=QLabel("Marker size")
        self.data_markersize=QLineEdit()
        self.data_linewidth_label=QLabel("Line width")
        self.data_linewidth=QLineEdit()
        self.data_color_label=QLabel("Plot color")
        self.data_color=QLineEdit()
        #change dimension of the plot
        self.plot_x_label=QLabel("x-dimension")
        self.plot_y_label=QLabel("y-dimension")
        self.plot_x=QLineEdit()
        self.plot_y=QLineEdit()
        adjust_plot_button=QPushButton('Adjust plot size')
        adjust_plot_button.clicked.connect(lambda: self.update_plot_size())
        #add button to choose plot color
        self.color_button=QPushButton("Pick color")
        self.color_button.clicked.connect(lambda: self.update_color(self.data_color))
        #part for plotting the data
        l3_button=QPushButton('Plot Data')
        l3_button.clicked.connect(lambda: self.dataplot.axes.cla())
        l3_button.clicked.connect(lambda: self.update_plot(self.data[self.xaxis.currentText()].to_numpy(),self.data[self.yaxis.currentText()].to_numpy())) 
        #center labels:
        self.xlim_lower_label.setAlignment(QtCore.Qt.AlignCenter)
        self.xlim_upper_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ylim_lower_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ylim_upper_label.setAlignment(QtCore.Qt.AlignCenter)
        self.y_label_label.setAlignment(QtCore.Qt.AlignCenter)
        self.x_label_label.setAlignment(QtCore.Qt.AlignCenter)
        self.font_label.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_width_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_plot_style_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_markersize_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_linewidth_label.setAlignment(QtCore.Qt.AlignCenter)
        self.data_color_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_x_label.setAlignment(QtCore.Qt.AlignCenter)
        self.plot_y_label.setAlignment(QtCore.Qt.AlignCenter)
        #adds widgets to layout
        layout.addWidget(self.xlim_lower_label,0,0,1,1)
        layout.addWidget(self.xlim_upper_label,0,1,1,1)
        layout.addWidget(self.ylim_lower_label,0,2,1,1)
        layout.addWidget(self.ylim_upper_label,0,3,1,1)
        layout.addWidget(self.xlim_lower,1,0,1,1)
        layout.addWidget(self.xlim_upper,1,1,1,1)
        layout.addWidget(self.ylim_lower,1,2,1,1)
        layout.addWidget(self.ylim_upper,1,3,1,1)
        layout.addWidget(self.x_label_label,2,0,1,2)
        layout.addWidget(self.y_label_label,2,2,1,2)
        layout.addWidget(self.x_label,3,0,1,2)
        layout.addWidget(self.y_label,3,2,1,2)
        layout.addWidget(self.font_label,4,0,1,1)
        layout.addWidget(self.font_size,5,0,1,1)
        layout.addWidget(self.axis_width_label,4,1,1,1)
        layout.addWidget(self.axis_width,5,1,1,1)
        layout.addWidget(self.data_plot_style_label,4,2,1,1)
        layout.addWidget(self.data_plot_style,5,2,1,1)
        layout.addWidget(self.data_markersize_label,4,3,1,1)
        layout.addWidget(self.data_markersize,5,3,1,1)
        layout.addWidget(self.data_color_label,6,0,1,2)
        layout.addWidget(self.data_color,6,2,1,2)
        layout.addWidget(self.color_button,7,0,1,4)
        layout.addWidget(l3_button, 8,0,1,4) 
        layout.addWidget(self.plot_x_label,9,0,1,2)
        layout.addWidget(self.plot_y_label,9,2,1,2)
        layout.addWidget(self.plot_x,10,0,1,2)
        layout.addWidget(self.plot_y,10,2,1,2)
        layout.addWidget(adjust_plot_button,11,0,1,4) 
        #set the layout
        self.Plot.setLayout(layout) 
    
    #GUI for generating individual plots for the trace GIF
    def generate_trace(self):
        layout = QGridLayout()
        #define layout
        self.Trace = QGroupBox('Trace Data') 
        #create widgets
        self.trace_color_1_label=QLabel("Color before")
        self.trace_color_2_label=QLabel("Color marker")
        self.trace_color_3_label=QLabel("Color after")
        self.bg_color_1_label=QLabel("Background before")
        self.bg_color_2_label=QLabel("Marker line color")
        self.bg_color_3_label=QLabel("Background after")
        self.trace_marker_label=QLabel("Marker Type")
        self.trace_marker=QLineEdit()
        self.trace_number_label=QLabel("Number of traces")
        self.trace_number=QLineEdit()
        self.trace_gif_time_label=QLabel("Frame separation (ms)")
        self.trace_gif_time=QLineEdit()
        l3_button=QPushButton('Trace Data')
        l3_button.clicked.connect(lambda: self.dataplot.axes.cla())
        l3_button.clicked.connect(lambda: self.trace_data(self.data[self.xaxis.currentText()].to_numpy(),self.data[self.yaxis.currentText()].to_numpy()))
        self.color_1_button=QPushButton("Pick color")
        self.color_2_button=QPushButton("Pick color")
        self.color_3_button=QPushButton("Pick color")
        self.bg_color_1_button=QPushButton("Pick color")
        self.bg_color_2_button=QPushButton("Pick color")
        self.bg_color_3_button=QPushButton("Pick color")
        self.color_1_button.clicked.connect(lambda: self.update_color(self.color_1_identifier))
        self.color_2_button.clicked.connect(lambda: self.update_color(self.color_2_identifier))
        self.color_3_button.clicked.connect(lambda: self.update_color(self.color_3_identifier))
        self.bg_color_1_button.clicked.connect(lambda: self.update_color(self.bg_color_1_identifier))
        self.bg_color_2_button.clicked.connect(lambda: self.update_color(self.bg_color_2_identifier))
        self.bg_color_3_button.clicked.connect(lambda: self.update_color(self.bg_color_3_identifier))
        self.color_1_identifier=QLineEdit()
        self.color_2_identifier=QLineEdit()
        self.color_3_identifier=QLineEdit()
        self.bg_color_1_identifier=QLineEdit()
        self.bg_color_2_identifier=QLineEdit()
        self.bg_color_3_identifier=QLineEdit()
        #center labels:
        self.trace_color_1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trace_color_2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trace_color_3_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bg_color_1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bg_color_2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bg_color_3_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trace_marker_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trace_number_label.setAlignment(QtCore.Qt.AlignCenter)
        self.trace_gif_time_label.setAlignment(QtCore.Qt.AlignCenter)
        #adds widgets to layout
        layout.addWidget(self.trace_color_1_label,0,0,1,1)
        layout.addWidget(self.color_1_button,2,0,1,1)
        layout.addWidget(self.color_1_identifier,1,0,1,1)
        layout.addWidget(self.trace_color_2_label,0,1,1,1)
        layout.addWidget(self.color_2_button,2,1,1,1)
        layout.addWidget(self.color_2_identifier,1,1,1,1)
        layout.addWidget(self.trace_color_3_label,0,2,1,1)
        layout.addWidget(self.color_3_button,2,2,1,1)
        layout.addWidget(self.color_3_identifier,1,2,1,1)
        #########
        layout.addWidget(self.bg_color_1_label,3,0,1,1)
        layout.addWidget(self.bg_color_1_button,5,0,1,1)
        layout.addWidget(self.bg_color_1_identifier,4,0,1,1)
        layout.addWidget(self.bg_color_2_label,3,1,1,1)
        layout.addWidget(self.bg_color_2_button,5,1,1,1)
        layout.addWidget(self.bg_color_2_identifier,4,1,1,1)
        layout.addWidget(self.bg_color_3_label,3,2,1,1)
        layout.addWidget(self.bg_color_3_button,5,2,1,1)
        layout.addWidget(self.bg_color_3_identifier,4,2,1,1)
        #########
        layout.addWidget(self.trace_marker_label,6,0,1,1)
        layout.addWidget(self.trace_marker,7,0,1,1)
        layout.addWidget(self.trace_number_label,6,1,1,1)
        layout.addWidget(self.trace_number,7,1,1,1)
        layout.addWidget(self.trace_gif_time_label,6,2,1,1)
        layout.addWidget(self.trace_gif_time,7,2,1,1)
        layout.addWidget(l3_button, 8,0,1,3) 
        #set the layout
        self.Trace.setLayout(layout) 
        
#Functions##################################################################################################################################################################################################################################
    #function that asks user for color and sets the desired QLineEdit text with the corresponding hex code
    def update_color(self, text_object): 
        color=QColorDialog.getColor()
        text_object.setText(color.name())

    #opens window to find and select files
    def getfile(self): 
        fname=QFileDialog.getOpenFileName(self, 'Open file')
        self.filename.setText(fname[0])
        
    #loads any quantum design data file (or in general comma delimited files with [Data] right before the beginning of the dataset)
    def load_data(self,name): 
        self.xaxis.clear()
        self.yaxis.clear()
        word='[Data]'
        with open(name,encoding='latin1') as fp:
            lines=fp.readlines()
            for line in lines:
                if line.find(word) != -1:
                    start_line=lines.index(line)
                    break
        file=pan.read_csv(name, header=start_line+1,sep=',',encoding='latin1',skip_blank_lines=False)
        headers=list(file.columns.values)
        self.xaxis.addItems(headers)
        self.yaxis.addItems(headers)
        self.data=pan.DataFrame(file)
        
    #updates the canvas plot with the input data parameters
    def update_plot(self,x,y): 
        temp_x=np.array(x)
        temp_y=np.array(y)
        temp_x = temp_x[~np.isnan(temp_y)]
        temp_y = temp_y[~np.isnan(temp_y)]
        self.update_font_size()
        self.update_data_style(temp_x,temp_y)
        self.dataplot.axes.set_xlabel(self.xaxis.currentText(),labelpad=1)
        self.dataplot.axes.set_ylabel(self.yaxis.currentText(),labelpad=1)
        self.dataplot.axes.tick_params(direction="in")
        self.dataplot.axes.yaxis.set_ticks_position('both')
        self.dataplot.axes.xaxis.set_ticks_position('both')
        self.update_axes_style()
        self.update_axes()
        self.dataplot.axes.margins(0.1)
        self.dataplot.axes.tick_params(axis='x', pad=1)
        self.dataplot.axes.tick_params(axis='y', pad=1)
        self.update_axes_label()
        self.dataplot.fig.tight_layout()
        self.dataplot.draw()
        
    #updates the canvas for generating the trace gif. This is different from update_plot since the traces require additional control parameters
    def trace_plot_update(self,x,y,data_style,colors,ms,lw): 
        temp_x=np.array(x)
        temp_y=np.array(y)
        temp_x = temp_x[~np.isnan(temp_y)]
        temp_y = temp_y[~np.isnan(temp_y)]
        self.update_font_size()
        self.dataplot.axes.set_xlabel(self.xaxis.currentText(),labelpad=1)
        self.dataplot.axes.set_ylabel(self.yaxis.currentText(),labelpad=1)
        self.dataplot.axes.plot(temp_x,temp_y,data_style,markersize=ms,linewidth=lw,color=colors)
        self.dataplot.axes.tick_params(direction="in")
        self.dataplot.axes.yaxis.set_ticks_position('both')
        self.dataplot.axes.xaxis.set_ticks_position('both')
        self.update_axes_style()
        self.update_axes()
        self.dataplot.axes.margins(0.1)
        self.dataplot.axes.tick_params(axis='x', pad=1)
        self.dataplot.axes.tick_params(axis='y', pad=1)
        self.update_axes_label()
        self.dataplot.fig.tight_layout()
        self.dataplot.draw()
        
    #update axis limits
    def update_axes(self): 
        if len(self.xlim_lower.text())>0 and len(self.xlim_upper.text())>0:   
            xl=float(self.xlim_lower.text())
            xu=float(self.xlim_upper.text())
            self.dataplot.axes.set_xlim([xl,xu])
        else:
            pass
        if len(self.ylim_lower.text())>0 and len(self.ylim_upper.text())>0:   
            yl=float(self.ylim_lower.text())
            yu=float(self.ylim_upper.text())
            self.dataplot.axes.set_ylim([yl,yu])
        else:
            pass
        xmin, xmax = self.dataplot.axes.get_xlim()
        ymin, ymax = self.dataplot.axes.get_ylim()
        self.ylim_lower.setText(str(ymin))
        self.ylim_upper.setText(str(ymax))
        self.xlim_lower.setText(str(xmin))
        self.xlim_upper.setText(str(xmax))
        
    #updates the axis labels
    def update_axes_label(self): 
        temp_fs=matplotlib.pyplot.rcParams['font.size']
        if len(self.x_label.text())>0:
            temp_xl=self.x_label.text()
        else:
            temp_xl=self.xaxis.currentText()
        if len(self.y_label.text())>0:
            temp_yl=self.y_label.text()
        else:
            temp_yl=self.yaxis.currentText()
        self.dataplot.axes.set_xlabel(temp_xl,fontsize=temp_fs,labelpad=1)
        self.dataplot.axes.set_ylabel(temp_yl,fontsize=temp_fs,labelpad=1)
        self.x_label.setText(self.dataplot.axes.get_xlabel())
        self.y_label.setText(self.dataplot.axes.get_ylabel())
        self.font_size.setText(str(temp_fs))
        
    #updates the font size for the canvas plot
    def update_font_size(self):
        if len(self.font_size.text())>0:
            matplotlib.pyplot.rcParams.update({'font.size': float(self.font_size.text())})
        else:
            pass
        self.font_size.setText(str(matplotlib.pyplot.rcParams['font.size']))
        
    #updates the axis border and tick width
    def update_axes_style(self):
        if len(self.axis_width.text())>0:
            for axis in ['top','bottom','left','right']:
                self.dataplot.axes.spines[axis].set_linewidth(float(self.axis_width.text()))
                self.dataplot.axes.tick_params(width=float(self.axis_width.text()),length=float(self.axis_width.text())*4)
        else:
            pass
        self.axis_width.setText(str(self.dataplot.axes.spines['top'].get_linewidth()))
        
    #updates the data marker and line style of the plot
    def update_data_style(self,x,y):
        self.dataplot.axes.cla()
        if len(self.data_plot_style.text())>0:
            temp_plot_style=self.data_plot_style.text()
        else:
            temp_plot_style='o-'
        if len(self.data_markersize.text())>0:
            temp_marker_size=float(self.data_markersize.text())
        else:
            temp_marker_size=2
        if len(self.data_color.text())>0:
            temp_data_color=self.data_color.text()
        else:
            temp_data_color='k'
        self.dataplot.axes.plot(x,y,temp_plot_style,markersize=temp_marker_size,color=temp_data_color,linewidth=0.5)
        self.data_color.setText(str(temp_data_color))
        self.data_plot_style.setText(str(temp_plot_style))
        self.data_markersize.setText(str(temp_marker_size))
    
    #function for clearing all plot parameters when switching data columns
    def clear_plot_parameters(self):
        self.xlim_lower.clear()
        self.ylim_lower.clear()
        self.xlim_upper.clear()
        self.ylim_upper.clear()
        self.x_label.clear()
        self.y_label.clear()
        self.font_size.clear()
        self.axis_width.clear()
        self.data_plot_style.clear()
        self.data_markersize.clear()
        self.data_color.clear()
        
    #main function for generating and saving plots for the trace GUI
    def trace_data(self,x,y):
        if len(self.color_1_identifier.text())>0:
            temp_color_1=self.color_1_identifier.text()
        else:
            temp_color_1='grey'
        if len(self.color_2_identifier.text())>0:
            temp_color_2=self.color_2_identifier.text()
        else:
            temp_color_2='red'
        if len(self.color_3_identifier.text())>0:
            temp_color_3=self.color_3_identifier.text()
        else:
            temp_color_3='black'
        if len(self.trace_marker.text())>0:
            temp_marker=self.trace_marker.text()
        else:
            temp_marker='o'  
        if len(self.data_markersize.text())>0:
            temp_marker_size=float(self.data_markersize.text())
        else:
            temp_marker_size=1     
        if len(self.data_plot_style.text())>0:
            temp_marker_style=self.data_plot_style.text()
        else:
            temp_marker_style='-' 
        if len(self.trace_number.text())>0:
            N=int(self.trace_number.text())
        else:
            N=51   
        if len(self.bg_color_1_identifier.text())>0:
            bg_color_1=self.bg_color_1_identifier.text()
        else:
            bg_color_1='w'   
        if len(self.bg_color_2_identifier.text())>0:
            bg_color_2=self.bg_color_2_identifier.text()
        else:
            bg_color_2='w'   
        
        if len(self.bg_color_3_identifier.text())>0:
            bg_color_3=self.bg_color_3_identifier.text()
        else:
            bg_color_3='w'   
        self.color_1_identifier.setText(temp_color_1)
        self.color_2_identifier.setText(temp_color_2)
        self.color_3_identifier.setText(temp_color_3)
        self.trace_marker.setText(temp_marker)
        self.data_markersize.setText(str(temp_marker_size))
        self.data_plot_style.setText(temp_marker_style)
        self.trace_number.setText(str(N))
        self.bg_color_1_identifier.setText(bg_color_1)
        self.bg_color_2_identifier.setText(bg_color_2)
        self.bg_color_3_identifier.setText(bg_color_3)
        folder_name="Frames"
        x_temp=x
        y_temp=y
        N_range=np.linspace(0,len(x_temp)-2,N)
        pbar=tqdm(total=len(N_range))
        for i,f in enumerate(N_range):
            self.dataplot.axes.cla()
            temp_index=int(f)
            x_data_before=x_temp[:temp_index]
            y_data_before=y_temp[:temp_index]
            x_data_after=x_temp[temp_index:]
            y_data_after=y_temp[temp_index:]
            x_data_current=x_temp[temp_index]
            y_data_current=y_temp[temp_index]
            if len(x_data_before)>0:
                if bg_color_1=='w':
                    pass
                else:
                    temp=np.array([x_data_before[0],x_data_before[len(x_data_before)-1]])
                    print(temp)
                    self.dataplot.axes.axvspan(temp.min(),temp.max(),facecolor=bg_color_1,alpha=0.5)
            else:
                pass
            if len(x_data_after)>0:
                if bg_color_3=='w':
                    pass
                else:
                    temp2=np.array([x_data_after[0],x_data_after[len(x_data_after)-1]])
                    print(temp2)
                    self.dataplot.axes.axvspan(temp2.min(),temp2.max(),facecolor=bg_color_3,alpha=0.5)
            else:
                pass
            self.trace_plot_update(x=x_data_before, y=y_data_before, data_style=temp_marker_style, colors=temp_color_1, ms=temp_marker_size, lw=0.5)
            self.trace_plot_update(x=x_data_after, y=y_data_after, data_style=temp_marker_style,colors=temp_color_3, ms=temp_marker_size, lw=0.5)
            if bg_color_2=='w':
                pass
            else:
                self.dataplot.axes.axvline(x=x_data_current,color=bg_color_2,linewidth=1,alpha=1)
            self.trace_plot_update(x=x_data_current, y=y_data_current, data_style=temp_marker, colors=temp_color_2, ms=temp_marker_size*2, lw=0.5)
            self.save_plot(folder_name,'Frame_'+str(temp_index)+'.png')
            pbar.update(i)
        pbar.close()     
        
        self.create_gif(folder_name)
    
    #function for saving the trace plots
    def save_plot(self, folder_name, name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path=Path(dir_path)
        name_path=Path(dir_path)/folder_name
        if not os.path.exists(name_path):
           os.makedirs(name_path)
        os.chdir(name_path)
        self.dataplot.fig.savefig(name, bbox_inches='tight',dpi=600)
   
    #function for generating a GIF from the individual trace plots
    def create_gif(self, folder_name):
        if len(self.trace_gif_time.text())>0:
            temp_gif_time=int(self.trace_gif_time.text())
        else:
            temp_gif_time=100 
        self.trace_gif_time.setText(str(temp_gif_time))
        #sets up the basic directory
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path=Path(dir_path)
        name_path=Path(dir_path)/folder_name
        os.chdir(name_path)
        names=sorted(glob.glob('*Frame_*'),key=natural_keys)
        # Take list of paths for images
        image_path_list = names
        image_list = [Image.open(file) for file in image_path_list] 
        image_list[0].save(
            'animation.gif',
            save_all=True,
            append_images=image_list[1:], # append rest of the images
            duration=temp_gif_time, # in milliseconds
            loop=0)
        
    #function for updating the pixel size of the GUI. This is intended to help the user adjust the plot aspect ratio.
    def update_plot_size(self):
        if len(self.plot_x.text())>0:
            xd=int(self.plot_x.text())
        else:
            xd=1400
        if len(self.plot_y.text())>0:
            yd=int(self.plot_y.text())
        else:
            yd=900
        if xd<500:
            xd=500
        if yd<500:
            yd=500
        if xd>2000:
            xd=2000
        if yd>2000:
            yd=2000
        self.plot_x.setText(str(xd))
        self.plot_y.setText(str(yd))
        self.setFixedSize(xd,yd) #fix window size
#%%
#This is the code to run the main GUI   
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()