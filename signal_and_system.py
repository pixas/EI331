import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
from numpy.core.einsumfunc import _parse_possible_contraction
from functools import partial
import typical_signals_wvfm
import fourier_series_and_transformation
import typical_signal_fs
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
import DT_convolution
import Amplitude_Modulation
import Sampling
import Through_LPF
import First_Order_Hold_Convertion

class MyFigure(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        super(MyFigure,self).__init__(self.fig)

class signal(QDialog):
    def __init__(self):
        super(signal,self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('信号与系统模拟')
        self.resize(400,600)
        layout=QVBoxLayout()
        self.setLayout(layout)
        layout.setSpacing(10)

        self.button1=QPushButton(self)
        self.button1.setText('典型信号波形')
        self.button1.clicked.connect(self.showDialog1)
        self.button2=QPushButton(self)
        self.button2.setText('卷积和、卷积积分')
        self.button2.clicked.connect(self.showDialog2)
        self.button3=QPushButton(self)
        self.button3.setText('傅里叶级数、傅里叶变换')
        self.button3.clicked.connect(self.showDialog3)
        self.button4=QPushButton(self)
        self.button4.setText('数模、模数转换')
        self.button4.clicked.connect(self.showDialog4)
        

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)


    def showDialog1(self):
        dialog=QDialog()
        dialog.setWindowTitle('典型信号波形')
        button1=QPushButton(dialog)
        button1.setText('连续时间单位冲激信号')
        button1.clicked.connect(self.showDialog11)
        button2=QPushButton(dialog)
        button2.setText('连续时间单位阶跃信号')
        button2.clicked.connect(self.showDialog12)
        button3=QPushButton(dialog)
        button3.setText('连续时间实指数信号')
        button3.clicked.connect(self.showDialog13)
        button4=QPushButton(dialog)
        button4.setText('连续时间复指数信号')
        button4.clicked.connect(self.showDialog14)
        button5=QPushButton(dialog)
        button5.setText('方波信号')
        button5.clicked.connect(self.showDialog15)
        button6=QPushButton(dialog)
        button6.setText('抽样信号')
        button6.clicked.connect(self.showDialog16)
        
        layout=QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(button6)
        dialog.setLayout(layout)

        dialog.exec()
        
    def showDialog2(self):
        dialog=QDialog()
        dialog.setWindowTitle('离散时间卷积和')
        label1=QLabel('待卷积信号1:')
        label2=QLabel('待卷积信号2:')
        cb1=QComboBox()
        cb2=QComboBox()
        cb1.addItems(['DT unit impulse function',
                        'DT unit step function',
                        'DT Real exponential',
                        'DT complex exponential',
                        'DT Sampling function',
                        'DT Rectangle waveform'])
        cb2.addItems(['DT unit impulse function',
                        'DT unit step function',
                        'DT Real exponential',
                        'DT complex exponential',
                        'DT Sampling function',
                        'DT Rectangle waveform'])
        button1=QPushButton('确认')
        button1.clicked.connect(lambda:self.select(cb1,cb2))
        layout=QGridLayout()
        layout.addWidget(label1,0,0,1,1)
        layout.addWidget(cb1,0,1,1,2)
        layout.addWidget(label2,1,0,1,1)
        layout.addWidget(cb2,1,1,1,2)
        layout.addWidget(button1)
        dialog.setLayout(layout)

        dialog.exec()

    def showDialog3(self):
        dialog=QDialog()
        dialog.setWindowTitle('傅里叶级数、傅里叶变换')
        button1=QPushButton(dialog)
        button1.setText('非周期方波信号的傅里叶变换')
        button1.clicked.connect(self.showDialog31)
        button2=QPushButton(dialog)
        button2.setText('周期单位冲激信号频谱')
        button2.clicked.connect(self.showDialog32)
        button3=QPushButton(dialog)
        button3.setText('非周期单位冲激信号频谱')
        button3.clicked.connect(self.showDialog33)
        button4=QPushButton(dialog)
        button4.setText('单位阶跃信号频谱')
        button4.clicked.connect(self.showDialog34)
        button5=QPushButton(dialog)
        button5.setText('离散时间指数信号频谱')
        button5.clicked.connect(self.showDialog35)
        button6=QPushButton(dialog)
        button6.setText('离散时间抽样信号频谱')
        button6.clicked.connect(self.showDialog36)
        button7=QPushButton(dialog)
        button7.setText('CT nth partial sum')
        button7.clicked.connect(self.showDialog37)
        
        layout=QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(button6)
        layout.addWidget(button7)
        
        dialog.setLayout(layout)

        dialog.exec()

    def showDialog4(self):
        dialog=QDialog()
        dialog.setWindowTitle('数模、模数转换')
        button1=QPushButton('Amplitude Modulation',dialog)
        button1.clicked.connect(self.showDialog41)
        button2=QPushButton('Sampling',dialog)
        button2.clicked.connect(self.showDialog42)
        button3=QPushButton('Through LPF',dialog)
        button3.clicked.connect(self.showDialog43)
        button4=QPushButton('First Order Hold Convertion',dialog)
        button4.clicked.connect(self.showDialog44)
        
        layout=QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        dialog.setLayout(layout)

        dialog.exec()

    def showDialog11(self):
        dialog=QDialog()
        dialog.setWindowTitle('连续时间单位冲激信号')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        layout=QVBoxLayout()
        layout.setSpacing(10)
        layout1=QFormLayout()
        layout1.addRow('振幅:',edit1)
        layout1.addRow('时移:',edit2)
        layout1wg=QWidget()
        layout1wg.setLayout(layout1)
        layout.addWidget(layout1wg)
        layout.addWidget(button1)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')

        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot11():
            dialog1=QDialog()
            dialog1.setWindowTitle('连续时间单位冲激信号图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                typical_signals_wvfm.plot_ct_unit_impulse(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            apt=QLabel('振幅:'+edit1.text(),dialog1)
            sft=QLabel('时移:'+edit2.text(),dialog1)
           
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(sft,10,3,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot11)
        dialog.exec()
        

    def showDialog12(self):
        dialog=QDialog()
        dialog.setWindowTitle('连续时间单位阶跃信号')
        label1=QLabel(dialog)
        label1.setText('振幅:')
        label2=QLabel(dialog)
        label2.setText('时移:')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        Rbutton=QRadioButton('逆向')
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(Rbutton,2,0,1,2)
        layout.addWidget(button1,3,0,1,2)
        
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot12():
            dialog1=QDialog()
            dialog1.setWindowTitle('连续时间单位阶跃信号图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                typical_signals_wvfm.plot_ct_unit_step(float(edit1.text()),float(edit2.text()),Rbutton.isChecked())
            except:
                self.empty()
                return
            apt=QLabel('振幅:'+edit1.text(),dialog1)
            sft=QLabel('时移:'+edit2.text(),dialog1)
            re=QLabel('逆向:'+str(Rbutton.isChecked()),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(sft,10,3,1,2)
            layout1.addWidget(re,10,6,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot12)
        dialog.exec()

    def showDialog13(self):
        dialog=QDialog()
        dialog.setWindowTitle('连续时间实指数信号')
        label1=QLabel(dialog)
        label1.setText('C:')
        label2=QLabel(dialog)
        label2.setText('a:')
        label3=QLabel('x(t) = Ce^(at)')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label3,0,0,1,2)
        layout.addWidget(label1,1,0,1,2)
        layout.addWidget(edit1,1,2,1,2)
        layout.addWidget(label2,2,0,1,2)
        layout.addWidget(edit2,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot13():
            dialog1=QDialog()
            dialog1.setWindowTitle('连续时间实指数信号图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                typical_signals_wvfm.plot_ct_real_exponential(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            apt=QLabel('C:'+edit1.text(),dialog1)
            a=QLabel('a:'+edit2.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(a,10,3,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot13)
        dialog.exec()

    def showDialog14(self):
        dialog=QDialog()
        dialog.setWindowTitle('连续时间复指数信号')
        label1=QLabel(dialog)
        label1.setText('C:')
        label2=QLabel(dialog)
        label2.setText('a:')
        label3=QLabel('x(t) = Ce^(at)')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        
        edit1.setToolTip('complex:a+bj')
        edit2.setToolTip('complex:a+bj')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label3,0,0,1,2)
        layout.addWidget(label1,1,0,1,2)
        layout.addWidget(edit1,1,2,1,2)
        layout.addWidget(label2,2,0,1,2)
        layout.addWidget(edit2,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)

        def plot14():
            dialog1=QDialog()
            dialog1.setWindowTitle('连续时间复指数信号图像')
            
            try:
                F=typical_signals_wvfm.plot_ct_complex_exponential(edit1.text(),edit2.text())
            except NameError:
                self.errorinput()
                return
            except ValueError:
                self.empty()
                return

            apt=QLabel('C:'+edit1.text(),dialog1)
            a=QLabel('a:'+edit2.text(),dialog1)
           
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(a,10,3,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot14)
        dialog.exec()

    def showDialog15(self):
        dialog=QDialog()
        dialog.setWindowTitle('方波信号')
        label1=QLabel(dialog)
        label1.setText('振幅:')
        label2=QLabel(dialog)
        label2.setText('时移:')
        label3=QLabel(dialog)
        label3.setText('周期:')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot15():
            dialog1=QDialog()
            dialog1.setWindowTitle('方波信号图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                typical_signals_wvfm.plot_rectangle_waveform(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            apt=QLabel('振幅:'+edit1.text(),dialog1)
            sft=QLabel('时移:'+edit2.text(),dialog1)
            t=QLabel('周期:'+edit3.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(sft,10,3,1,2)
            layout1.addWidget(t,10,6,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot15)
        dialog.exec()

    def showDialog16(self):
        dialog=QDialog()
        dialog.setWindowTitle('抽样信号')
        label3=QLabel('x(t) = Asin(at)/(at)')
        label1=QLabel(dialog)
        label1.setText('A:')
        label2=QLabel(dialog)
        label2.setText('a:')
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label3,0,0,1,2)
        layout.addWidget(label1,1,0,1,2)
        layout.addWidget(edit1,1,2,1,2)
        layout.addWidget(label2,2,0,1,2)
        layout.addWidget(edit2,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot16():
            dialog1=QDialog()
            dialog1.setWindowTitle('抽样信号图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                typical_signals_wvfm.plot_sampling_function(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            mgt=QLabel('A:'+edit1.text(),dialog1)
            sca=QLabel('a:'+edit2.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(mgt,10,0,1,2)
            layout1.addWidget(sca,10,3,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot16)
        dialog.exec()

    def select(self,cb1,cb2):
        #
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT unit impulse function':
            self.dialog_impulse_impulse()
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT unit step function':
            self.dialog_impulse_step()
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT Real exponential':
            self.dialog_real_impulse()
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_complex()
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT Sampling function':
            self.dialog_sample_impulse()
        if cb1.currentText()=='DT unit impulse function' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_rectangle_impulse()
        #
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT unit impulse function':
            self.dialog_impulse_step()
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT unit step function':
            self.dialog_step_step()
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT Real exponential':
            self.dialog_real_step()
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_step()
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT Sampling function':
            self.dialog_sample_step()
        if cb1.currentText()=='DT unit step function' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_rectangle_step()
        #
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT unit impulse function':
            self.dialog_real_impulse()
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT unit step function':
            self.dialog_real_step()
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT Real exponential':
            self.dialog_real_real()
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_real()
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT Sampling function':
            self.dialog_real_sample()
        if cb1.currentText()=='DT Real exponential' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_real_rectangle()
        #
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT unit impulse function':
            self.dialog_complex_impulse()
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT unit step function':
            self.dialog_complex_step()
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT Real exponential':
            self.dialog_complex_real()
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_complex()
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT Sampling function':
            self.dialog_complex_sample()
        if cb1.currentText()=='DT complex exponential' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_complex_rectangle()
        #
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT unit impulse function':
            self.dialog_sample_impulse()
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT unit step function':
            self.dialog_sample_step()
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT Real exponential':
            self.dialog_real_sample()
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_sample()
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT Sampling function':
            self.dialog_sample_sample()
        if cb1.currentText()=='DT Sampling function' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_sample_rectangle()
        #
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT unit impulse function':
            self.dialog_rectangle_impulse()
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT unit step function':
            self.dialog_rectangle_step()
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT Real exponential':
            self.dialog_real_rectangle()
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT complex exponential':
            self.dialog_complex_rectangle()
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT Sampling function':
            self.dialog_sample_rectangle()
        if cb1.currentText()=='DT Rectangle waveform' and cb2.currentText()=='DT Rectangle waveform':
            self.dialog_rectangle_rectangle()
    #1
    def dialog_impulse_impulse(self):
        dialog=QDialog()
        dialog.setWindowTitle('impulse*impulse')
        label1=QLabel("time shift of impulse function1:",dialog)
        label2=QLabel("amplitude of impulse function1:",dialog)
        label3=QLabel('time shift of impulse function2:',dialog)
        label4=QLabel('amplitude of impulse function2:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit1.setToolTip('int')
        edit2.setToolTip('float')
        edit3.setToolTip('int')
        edit4.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        
        def plot_impulse_impulse():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot impulse*impulse')
            try:
                F=DT_convolution.plotconv_impulse_impulse(int(edit1.text()),float(edit2.text()),int(edit3.text()),float(edit4.text()))
            except:
                self.empty()
                return
            x1=QLabel('time shift of impulse function1:'+edit1.text(),dialog1)
            x2=QLabel('amplitude of impulse function1:'+edit2.text(),dialog1)
            x3=QLabel('time shift of impulse function2:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of impulse function2:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_impulse_impulse)
        dialog.exec()
    #2
    def dialog_impulse_step(self):
        dialog=QDialog()
        dialog.setWindowTitle('impulse*step')
        label1=QLabel("time shift of impulse function:",dialog)
        label2=QLabel("amplitude of impulse function:",dialog)
        label3=QLabel('time shift of step function:',dialog)
        label4=QLabel('amplitude of step function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit1.setToolTip('int')
        edit2.setToolTip('float')
        edit3.setToolTip('int')
        edit4.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        
        def plot_impulse_step():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot impulse*step')
            try:
                F=DT_convolution.plotconv_impulse_step(int(edit1.text()),float(edit2.text()),int(edit3.text()),float(edit4.text()))
            except:
                self.empty()
                return
            imts=QLabel('time shift of impulse function:'+edit1.text(),dialog1)
            ima=QLabel('amplitude of impulse function:'+edit2.text(),dialog1)
            stts=QLabel('time shift of step function:'+edit3.text(),dialog1)
            sta=QLabel('amplitude of step function:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(imts,10,0,1,2)
            layout1.addWidget(ima,10,5,1,2)
            layout1.addWidget(stts,11,0,1,2)
            layout1.addWidget(sta,11,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_impulse_step)
        dialog.exec()
    #3
    def dialog_step_step(self):
        dialog=QDialog()
        dialog.setWindowTitle('step*step')
        label1=QLabel("time shift of step function1:",dialog)
        label2=QLabel("amplitude of step function1:",dialog)
        label3=QLabel('time shift of step function2:',dialog)
        label4=QLabel('amplitude of step function2:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit1.setToolTip('int')
        edit2.setToolTip('float')
        edit3.setToolTip('int')
        edit4.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        
        def plot_step_step():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot step*step')
            try:
                F=DT_convolution.plotconv_step_step(int(edit1.text()),float(edit2.text()),int(edit3.text()),float(edit4.text()))
            except:
                self.empty()
                return
            x1=QLabel('time shift of step function1:'+edit1.text(),dialog1)
            x2=QLabel('amplitude of step function1:'+edit2.text(),dialog1)
            x3=QLabel('time shift of step function2:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of step function2:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()
        button1.clicked.connect(plot_step_step)
        dialog.exec()
    #4
    def dialog_real_impulse(self):
        dialog=QDialog()
        dialog.setWindowTitle('real*impulse')
        label1=QLabel("a of real exponential:",dialog)
        label2=QLabel("time shift of real exponential:",dialog)
        label3=QLabel('amplitude of real exponential:',dialog)
        label4=QLabel('time shift of impulse function:',dialog)
        label5=QLabel('amplitude of impulse function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(doublevalidator)
        
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('float,not equal to 0')
        edit4.setToolTip('int')
        edit5.setToolTip('float,not equal to 0')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        
        def plot_real_impulse():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot real*impulse')
            try:
                F=DT_convolution.plotconv_real_exp_impulse(float(edit1.text()),int(edit2.text()),float(edit3.text()),int(edit4.text()),float(edit5.text()))
            except:
                self.empty()
                return
            x1=QLabel('a of real exponential:'+edit1.text(),dialog1)
            x2=QLabel('time shift of real exponential:'+edit2.text(),dialog1)
            x3=QLabel('amplitude of real exponential:'+edit3.text(),dialog1)
            x4=QLabel('time shift of impulse function:'+edit4.text(),dialog1)
            x5=QLabel('amplitude of impulse function:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_real_impulse)
        dialog.exec()
    #5
    def dialog_real_step(self):
        dialog=QDialog()
        dialog.setWindowTitle('real*step')
        label1=QLabel("a of real exponential:",dialog)
        label2=QLabel("time shift of real exponential:",dialog)
        label3=QLabel('amplitude of real exponential:',dialog)
        label4=QLabel('time shift of step function:',dialog)
        label5=QLabel('amplitude of step function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(doublevalidator)
        
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('float,not equal to 0')
        edit4.setToolTip('int')
        edit5.setToolTip('float,not equal to 0')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        
        def plot_real_step():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot real*step')
            try:
                F=DT_convolution.plotconv_real_exp_step(float(edit1.text()),int(edit2.text()),float(edit3.text()),int(edit4.text()),float(edit5.text()))
            except ValueError:
                self.empty()
                return
            except OverflowError:
                self.overflow()
                return

            x1=QLabel('a of real exponential:'+edit1.text(),dialog1)
            x2=QLabel('time shift of real exponential:'+edit2.text(),dialog1)
            x3=QLabel('amplitude of real exponential:'+edit3.text(),dialog1)
            x4=QLabel('time shift of step function:'+edit4.text(),dialog1)
            x5=QLabel('amplitude of step function:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_real_step)
        dialog.exec()
    #6
    def dialog_real_real(self):
        self.overflow()
    #7
    def dialog_real_sample(self):
        self.overflow()
    #8
    def dialog_real_rectangle(self):
        self.overflow()
    #9
    def dialog_complex_impulse(self):
        dialog=QDialog()
        dialog.setWindowTitle('complex*impulse')
        label1=QLabel("a of complex exponential:",dialog)
        label2=QLabel("time shift of complex exponential:",dialog)
        label3=QLabel('amplitude of complex exponential:',dialog)
        label4=QLabel('time shift of impulse function:',dialog)
        label5=QLabel('amplitude of impulse function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit2.setValidator(intvalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(doublevalidator)
        
        edit1.setToolTip('complex:a+bj')
        edit2.setToolTip('int')
        edit3.setToolTip('complex:a+bj')
        edit4.setToolTip('int')
        edit5.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        
        
        def plot_complex_impulse():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot complex*impulse')
            try:
                F=DT_convolution.plotconv_complex_exp_impulse(edit1.text(),int(edit2.text()),edit3.text(),int(edit4.text()),float(edit5.text()))
            except:
                self.empty()
                return
            x1=QLabel('a of complex exponential:'+edit1.text(),dialog1)
            x2=QLabel('time shift of complex exponential:'+edit2.text(),dialog1)
            x3=QLabel('amplitude of complex exponential:'+edit3.text(),dialog1)
            x4=QLabel('time shift of impulse function:'+edit4.text(),dialog1)
            x5=QLabel('amplitude of impulse function:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_complex_impulse)
        dialog.exec()
    #10
    def dialog_complex_step(self):
        self.overflow()
    #11
    def dialog_complex_real(self):
        self.overflow()
    #12
    def dialog_complex_complex(self):
        self.overflow()
    #13
    def dialog_complex_sample(self):
        self.overflow()
    #14
    def dialog_complex_rectangle(self):
        self.overflow()
    #15
    def dialog_sample_impulse(self):
        dialog=QDialog()
        dialog.setWindowTitle('sample*impulse')
        label1=QLabel("w of sampling function:",dialog)
        label2=QLabel("time shift of sampling function:",dialog)
        label3=QLabel('amplitude of sampling function:',dialog)
        label4=QLabel('time shift of impulse function:',dialog)
        label5=QLabel('amplitude of impulse function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(doublevalidator)
        
        edit1.setToolTip('float,must be in (0,pi)')
        edit2.setToolTip('int')
        edit3.setToolTip('float,not equal to 0')
        edit4.setToolTip('int')
        edit5.setToolTip('float,not equal to 0')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        
        
        def plot_sample_impulse():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot sample*impulse')
            try:
                F=DT_convolution.plotconv_sample_impulse(float(edit1.text()),int(edit2.text()),float(edit3.text()),int(edit4.text()),float(edit5.text()))
            except:
                self.empty()
                return
            x1=QLabel('w of sampling function:'+edit1.text(),dialog1)
            x2=QLabel('time shift of sampling function:'+edit2.text(),dialog1)
            x3=QLabel('amplitude of sampling function:'+edit3.text(),dialog1)
            x4=QLabel('time shift of impulse function:'+edit4.text(),dialog1)
            x5=QLabel('amplitude of impulse function:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_sample_impulse)
        dialog.exec()
    #16
    def dialog_sample_step(self):
        dialog=QDialog()
        dialog.setWindowTitle('sample*step')
        label1=QLabel("the value of time index n:",dialog)
        label2=QLabel("the corresponding accuracy:",dialog)
        label3=QLabel('w of sampling function:',dialog)
        label4=QLabel('time shift of sampling function:',dialog)
        label5=QLabel('amplitude of sampling function:',dialog)
        label6=QLabel('time shift of step function:',dialog)
        label7=QLabel('amplitude of step function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        edit7=QLineEdit(dialog)
        button1=QPushButton('计算',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(doublevalidator)
        edit6.setValidator(intvalidator)
        edit7.setValidator(doublevalidator)
        edit1.setToolTip('int')
        edit2.setToolTip('float,larger than 0')
        edit3.setToolTip('float,must be in (0,pi)')
        edit4.setToolTip('int')
        edit5.setToolTip('float,not equal to 0')
        edit6.setToolTip('int')
        edit7.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(label7,6,0,1,2)
        layout.addWidget(edit7,6,2,1,2)
        layout.addWidget(button1,7,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 and len(edit6.text())>0 and len(edit7.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        edit7.textChanged.connect(en_dis)
        def plot_sample_step():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot sample*step')
            try:
                F=DT_convolution.plotconv_sample_step(int(edit1.text()),float(edit2.text()),float(edit3.text()),int(edit4.text()),float(edit5.text()),int(edit6.text()),float(edit7.text()))
            except:
                self.empty()
                return
            x1=QLabel(F,dialog1)
            x2=QLabel('the value of time index n:'+edit1.text(),dialog1)
            x3=QLabel('the corresponding accuracy:'+edit2.text(),dialog1)
            x4=QLabel('w of sampling function:'+edit3.text(),dialog1)
            x5=QLabel('time shift of sampling function:'+edit4.text(),dialog1)
            x6=QLabel('amplitude of sampling function:'+edit5.text(),dialog1)
            x7=QLabel('time shift of step function:'+edit6.text(),dialog1)
            x8=QLabel('amplitude of step function:'+edit7.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(x1,0,0,1,2)
            layout1.addWidget(x2,0,5,1,2)
            layout1.addWidget(x3,1,0,1,2)
            layout1.addWidget(x4,1,5,1,2)
            layout1.addWidget(x5,2,0,1,2)
            layout1.addWidget(x6,2,5,1,2)
            layout1.addWidget(x7,3,0,1,2)
            layout1.addWidget(x8,3,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_sample_step)
        dialog.exec()
    #17
    def dialog_sample_sample(self):
        self.overflow()
    #18
    def dialog_sample_rectangle(self):
        dialog=QDialog()
        dialog.setWindowTitle('sample*rectangle')
        label1=QLabel("T1 of rectangle waveform:",dialog)
        label2=QLabel("T2 of rectangle waveform:",dialog)
        label3=QLabel('time shift of rectangle waveform:',dialog)
        label4=QLabel('amplitude of  rectangle waveform:',dialog)
        label5=QLabel("w of sampling function:",dialog)
        label6=QLabel('time shift of sampling function:',dialog)
        label7=QLabel('amplitude of sampling function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        edit7=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(doublevalidator)
        edit6.setValidator(intvalidator)
        edit7.setValidator(doublevalidator)
        edit1.setToolTip('int,T1<T2/2')
        edit2.setToolTip('int,T1<T2/2')
        edit3.setToolTip('int')
        edit4.setToolTip('float,not equal to 0')
        edit5.setToolTip('float,must be in (0,pi)')
        edit6.setToolTip('int')
        edit7.setToolTip('float,not equal to 0')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(label7,6,0,1,2)
        layout.addWidget(edit7,6,2,1,2)
        layout.addWidget(button1,8,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 and len(edit6.text())>0 and len(edit7.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        edit7.textChanged.connect(en_dis)
        def plot_sample_reactangle():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot sample*rectangle')
            try:
                F=DT_convolution.plotconv_rectangle_sample(int(edit1.text()),int(edit2.text()),int(edit3.text()),float(edit4.text()),float(edit5.text()),int(edit6.text()),float(edit7.text()))
            except ValueError:
                self.empty()
                return
            except OverflowError:
                self.overflow()
                return
            x1=QLabel('T1 of rectangle waveform:'+edit1.text(),dialog1)
            x2=QLabel('T2 of rectangle waveform:'+edit2.text(),dialog1)
            x3=QLabel('time shift of rectangle waveform:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of  rectangle waveform:'+edit4.text(),dialog1)
            x5=QLabel('w of sampling function:'+edit5.text(),dialog1)
            x6=QLabel('time shift of sampling function:'+edit6.text(),dialog1)
            x7=QLabel('amplitude of sampling function:'+edit7.text(),dialog1)
    
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            layout1.addWidget(x7,13,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_sample_reactangle)
        dialog.exec()
    #19
    def dialog_rectangle_impulse(self):
        dialog=QDialog()
        dialog.setWindowTitle('rectangle*impulse')
        label1=QLabel("T1 of rectangle waveform:",dialog)
        label2=QLabel("T2 of rectangle waveform:",dialog)
        label3=QLabel('time shift of rectangle waveform:',dialog)
        label4=QLabel('amplitude of  rectangle waveform:',dialog)
        label5=QLabel('time shift of impulse function:',dialog)
        label6=QLabel('amplitude of impulse function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(intvalidator)
        edit6.setValidator(doublevalidator)
        edit1.setToolTip('int,T1<T2/2')
        edit2.setToolTip('int,T1<T2/2')
        edit3.setToolTip('int')
        edit4.setToolTip('float,not equal to 0')
        edit5.setToolTip('int')
        edit6.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(button1,6,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 and len(edit6.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        
        def plot_rectangle_impulse():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot rectangle*impulse')
            try:
                F=DT_convolution.plotconv_rectangle_impulse(int(edit1.text()),int(edit2.text()),int(edit3.text()),float(edit4.text()),int(edit5.text()),float(edit6.text()))
            except:
                self.empty()
                return
            x1=QLabel('T1 of rectangle waveform:'+edit1.text(),dialog1)
            x2=QLabel('T2 of rectangle waveform:'+edit2.text(),dialog1)
            x3=QLabel('time shift of rectangle waveform:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of  rectangle waveform:'+edit4.text(),dialog1)
            x5=QLabel('time shift of impulse function:'+edit5.text(),dialog1)
            x6=QLabel('amplitude of impulse function:'+edit6.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_rectangle_impulse)
        dialog.exec()
    #20
    def dialog_rectangle_step(self):
        dialog=QDialog()
        dialog.setWindowTitle('rectangle*step')
        label1=QLabel("T1 of rectangle waveform:",dialog)
        label2=QLabel("T2 of rectangle waveform:",dialog)
        label3=QLabel('time shift of rectangle waveform:',dialog)
        label4=QLabel('amplitude of  rectangle waveform:',dialog)
        label5=QLabel('time shift of step function:',dialog)
        label6=QLabel('amplitude of step function:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(intvalidator)
        edit6.setValidator(doublevalidator)
        edit1.setToolTip('int,T1<T2/2')
        edit2.setToolTip('int,T1<T2/2')
        edit3.setToolTip('int')
        edit4.setToolTip('float,not equal to 0')
        edit5.setToolTip('int')
        edit6.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(button1,6,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 and len(edit6.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        
        def plot_rectangle_step():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot rectangle*step')
            try:
                F=DT_convolution.plotconv_rectangle_step(int(edit1.text()),int(edit2.text()),int(edit3.text()),float(edit4.text()),int(edit5.text()),float(edit6.text()))
            except ValueError:
                self.empty()
                return
            except OverflowError:
                self.overflow()
                return
            x1=QLabel('T1 of rectangle waveform:'+edit1.text(),dialog1)
            x2=QLabel('T2 of rectangle waveform:'+edit2.text(),dialog1)
            x3=QLabel('time shift of rectangle waveform:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of  rectangle waveform:'+edit4.text(),dialog1)
            x5=QLabel('time shift of step function:'+edit5.text(),dialog1)
            x6=QLabel('amplitude of step function:'+edit6.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_rectangle_step)
        dialog.exec()
    #21
    def dialog_rectangle_rectangle(self):
        dialog=QDialog()
        dialog.setWindowTitle('rectangle*rectangle')
        label1=QLabel("T1 of rectangle waveform1:",dialog)
        label2=QLabel("T2 of rectangle waveform1:",dialog)
        label3=QLabel('time shift of rectangle waveform1:',dialog)
        label4=QLabel('amplitude of  rectangle waveform1:',dialog)
        label5=QLabel("T1 of rectangle waveform2:",dialog)
        label6=QLabel("T2 of rectangle waveform2:",dialog)
        label7=QLabel('time shift of rectangle waveform2:',dialog)
        label8=QLabel('amplitude of  rectangle waveform2:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        edit7=QLineEdit(dialog)
        edit8=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(intvalidator)
        edit6.setValidator(intvalidator)
        edit7.setValidator(intvalidator)
        edit8.setValidator(doublevalidator)
        edit1.setToolTip('int,T1<T2/2')
        edit2.setToolTip('int,T1<T2/2')
        edit3.setToolTip('int')
        edit4.setToolTip('float,not equal to 0')
        edit5.setToolTip('int,T1<T2/2')
        edit6.setToolTip('int,T1<T2/2')
        edit7.setToolTip('int')
        edit8.setToolTip('float,not equal to 0')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(label7,6,0,1,2)
        layout.addWidget(edit7,6,2,1,2)
        layout.addWidget(label8,7,0,1,2)
        layout.addWidget(edit8,7,2,1,2)
        layout.addWidget(button1,8,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text()) > 0 and len(edit6.text())>0 and len(edit7.text()) > 0 and len(edit8.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        edit7.textChanged.connect(en_dis)
        edit8.textChanged.connect(en_dis)
        def plot_rectangle_reactangle():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot rectangle*rectangle')
            try:
                F=DT_convolution.plotconv_rectangle_rectangle(int(edit1.text()),int(edit2.text()),int(edit5.text()),int(edit6.text()),int(edit3.text()),float(edit4.text()),int(edit7.text()),float(edit8.text()))
            except ValueError:
                self.empty()
                return
            except OverflowError:
                self.overflow()
                return
            x1=QLabel('T1 of rectangle waveform1:'+edit1.text(),dialog1)
            x2=QLabel('T2 of rectangle waveform1:'+edit2.text(),dialog1)
            x3=QLabel('time shift of rectangle waveform1:'+edit3.text(),dialog1)
            x4=QLabel('amplitude of  rectangle waveform1:'+edit4.text(),dialog1)
            x5=QLabel('T1 of rectangle waveform2:'+edit5.text(),dialog1)
            x6=QLabel('T2 of rectangle waveform2:'+edit6.text(),dialog1)
            x7=QLabel('time shift of rectangle waveform2:'+edit7.text(),dialog1)
            x8=QLabel('amplitude of  rectangle waveform2:'+edit8.text(),dialog1)
    
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            layout1.addWidget(x7,13,0,1,2)
            layout1.addWidget(x8,13,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_rectangle_reactangle)
        dialog.exec()
    
    def showDialog31(self):
        dialog=QDialog()
        dialog.setWindowTitle('非周期方波信号的傅里叶变换')
        #T1=2, amplitude=1, omega_begin=-30, omega_end = 30, omega_number
        label1=QLabel('T1:',dialog)
        label2=QLabel('振幅:',dialog)
        label3=QLabel('起始ω:',dialog)
        label4=QLabel('终止ω:',dialog)
        label5=QLabel('ω_number:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        edit5.setToolTip('int')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 and len(edit5.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)

        def plot31():
            dialog1=QDialog()
            dialog1.setWindowTitle('非周期方波信号的傅里叶变换图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.fourier_transform_aperiodic_rectangle_waveform(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()),int(edit5.text()))
            except:
                self.empty()
                return 
            T1=QLabel('T1:'+edit1.text(),dialog1)
            apt=QLabel('振幅:'+edit2.text(),dialog1)
            ob=QLabel('起始ω:'+edit3.text(),dialog1)
            oe=QLabel('终止ω:'+edit4.text(),dialog1)
            on=QLabel('ω_number:'+edit5.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(T1,10,0,1,2)
            layout1.addWidget(apt,10,3,1,2)
            layout1.addWidget(ob,10,6,1,2)
            layout1.addWidget(oe,11,0,1,2)
            layout1.addWidget(on,11,3,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot31)
        dialog.exec()

    def showDialog32(self):
        dialog=QDialog()
        dialog.setWindowTitle('周期单位冲激信号频谱')
        #N=1, amplitude=1, cycles=5
        label1=QLabel('N:',dialog)
        label2=QLabel('amplitude:',dialog)
        label3=QLabel('cycles:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(intvalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(intvalidator)
        edit1.setToolTip('int')
        edit2.setToolTip('float')
        edit3.setToolTip('int')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot32():
            dialog1=QDialog()
            dialog1.setWindowTitle('周期单位冲激信号频谱图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.plot_periodic_unit_impulse_spectrum(int(edit1.text()),float(edit2.text()),int(edit3.text()))
            except:
                self.empty()
                return
            N=QLabel('N:'+edit1.text(),dialog1)
            apt=QLabel('amplitude:'+edit2.text(),dialog1)
            cy=QLabel('cycles:'+edit3.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(N,10,0,1,2)
            layout1.addWidget(apt,10,3,1,2)
            layout1.addWidget(cy,10,6,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot32)
        dialog.exec()

    def showDialog33(self):
        dialog=QDialog()
        dialog.setWindowTitle('非周期单位冲激信号频谱')
        #amplitude=1, omega_begin=-30, omega_end = 30
        label1=QLabel('amplitude:',dialog)
        label2=QLabel('omega_begin:',dialog)
        label3=QLabel('omega_end:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot33():
            dialog1=QDialog()
            dialog1.setWindowTitle('非周期单位冲激信号频谱图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.plot_aperiodic_unit_impulse_spectrum(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            apt=QLabel('amplitude:'+edit1.text(),dialog1)
            ob=QLabel('omega_begin:'+edit2.text(),dialog1)
            oe=QLabel('omega_end:'+edit3.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(ob,10,3,1,2)
            layout1.addWidget(oe,10,6,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot33)
        dialog.exec()

    def showDialog34(self):
        dialog=QDialog()
        dialog.setWindowTitle('单位阶跃信号频谱')
        #amplitude=1, time_begin=-35, time_end=36
        label1=QLabel('amplitude:',dialog)
        label2=QLabel('time_begin:',dialog)
        label3=QLabel('time_end:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('int')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot34():
            dialog1=QDialog()
            dialog1.setWindowTitle('单位阶跃信号频谱图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.plot_unit_step_spectrum(float(edit1.text()),int(edit2.text()),int(edit3.text()))
            except:
                self.empty()
                return
            apt=QLabel('amplitude:'+edit1.text(),dialog1)
            tb=QLabel('time_begin:'+edit2.text(),dialog1)
            te=QLabel('time_end:'+edit3.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(tb,10,3,1,2)
            layout1.addWidget(te,10,6,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot34)
        dialog.exec()

    def showDialog35(self):
        dialog=QDialog()
        dialog.setWindowTitle('离散时间指数信号频谱')
        #amplitude=1, omega0=1, l_begin=-10, l_end=11
        label1=QLabel('amplitude:',dialog)
        label2=QLabel('omega0:',dialog)
        label3=QLabel('l_begin:',dialog)
        label4=QLabel('l_end:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        
        def plot35():
            dialog1=QDialog()
            dialog1.setWindowTitle('离散时间指数信号频谱图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.plot_dt_exponential_spectrum(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()))
            except:
                self.empty()
                return
            apt=QLabel('amplitude:'+edit1.text(),dialog1)
            omega=QLabel('omega0:'+edit2.text(),dialog1)
            lb=QLabel('l_begin:'+edit3.text(),dialog1)
            le=QLabel('l_end:'+edit4.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(omega,10,3,1,2)
            layout1.addWidget(lb,10,6,1,2)
            layout1.addWidget(le,11,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot35)
        dialog.exec()

    def showDialog36(self):
        dialog=QDialog()
        dialog.setWindowTitle('离散时间抽样信号频谱')
        #amplitude=1, W=np.pi/2, cycles=5
        label1=QLabel('amplitude:',dialog)
        label2=QLabel('W:',dialog)
        label3=QLabel('cycles:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot36():
            dialog1=QDialog()
            dialog1.setWindowTitle('离散时间抽样信号频谱图像')
            figure=plt.figure()
            canvas = FigureCanvas(figure)
            try:
                fourier_series_and_transformation.plot_dt_sa_function_spectrum(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            apt=QLabel('amplitude:'+edit1.text(),dialog1)
            W=QLabel('W:'+edit2.text(),dialog1)
            cy=QLabel('cycles:'+edit3.text(),dialog1)
            
            layout1=QGridLayout()
            layout1.addWidget(canvas,0,0,10,10)
            layout1.addWidget(apt,10,0,1,2)
            layout1.addWidget(W,10,3,1,2)
            layout1.addWidget(cy,10,6,1,2)
            
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot36)
        dialog.exec()

    def showDialog37(self):
        dialog=QDialog()
        dialog.setWindowTitle('CT nth partial sum')
        button1=QPushButton('周期方波信号的连续时间傅里叶级数',dialog)
        button1.clicked.connect(self.showDialog371)
        button2=QPushButton('余弦信号的连续时间傅里叶级数',dialog)
        button2.clicked.connect(self.showDialog372)
        button3=QPushButton('正弦信号的连续时间傅里叶级数',dialog)
        button3.clicked.connect(self.showDialog373)
        button4=QPushButton('冲激串的连续时间傅里叶级数',dialog)
        button4.clicked.connect(self.showDialog374)
        
        layout=QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        dialog.setLayout(layout)
        dialog.exec()

    def showDialog371(self):
        dialog=QDialog()
        dialog.setWindowTitle('周期方波信号的连续时间傅里叶级数')
        #T1=1, T=2, amplitude=1, N=14, t_begin=-10, t_end=10, t_number=500
        label1=QLabel('T1:',dialog)
        label2=QLabel('T:',dialog)
        label3=QLabel('amplitude:',dialog)
        label4=QLabel('N:',dialog)
        label5=QLabel('t_begin:',dialog)
        label6=QLabel('t_end:',dialog)
        label7=QLabel('t_number:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        edit7=QLineEdit(dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(intvalidator)
        edit6.setValidator(intvalidator)
        edit7.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('int')
        edit5.setToolTip('int')
        edit6.setToolTip('int')
        edit7.setToolTip('int')
        button1=QPushButton('绘制',dialog)
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(label7,6,0,1,2)
        layout.addWidget(edit7,6,2,1,2)
        layout.addWidget(button1,7,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 and len(edit5.text())>0  and len(edit6.text())>0 and len(edit7.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        edit7.textChanged.connect(en_dis)

        def plot371():
            dialog1=QDialog()
            dialog1.setWindowTitle('周期方波信号的连续时间傅里叶级数图像')
            try:
                F=typical_signal_fs.plot_retangle(float(edit1.text()),float(edit2.text()),float(edit3.text()),int(edit4.text()),int(edit5.text()),int(edit6.text()),int(edit7.text()))
            except:
                self.empty()
                return
            T1=QLabel('T1:'+edit1.text(),dialog1)
            T=QLabel('T:'+edit2.text(),dialog1)
            apt=QLabel('amplitude:'+edit3.text(),dialog1)
            N=QLabel('N:'+edit4.text(),dialog1)
            tb=QLabel('t_begin:'+edit5.text(),dialog1)
            te=QLabel('t_end:'+edit6.text(),dialog1)
            tn=QLabel('t_number:'+edit7.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(T1,10,0,1,2)
            layout1.addWidget(T,10,3,1,2)
            layout1.addWidget(apt,10,6,1,2)
            layout1.addWidget(N,10,9,1,2)
            layout1.addWidget(tb,11,0,1,2)
            layout1.addWidget(te,11,3,1,2)
            layout1.addWidget(tn,11,6,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot371)
        dialog.exec()

    def showDialog372(self):
        dialog=QDialog()
        dialog.setWindowTitle('余弦信号的连续时间傅里叶级数')
        #theta=0 t_begin=-10, t_end=10, t_number=500
        label1=QLabel('theta:',dialog)
        label2=QLabel('t_begin:',dialog)
        label3=QLabel('t_end:',dialog)
        label4=QLabel('t_number:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('int')
        edit4.setToolTip('int')
        button1=QPushButton('绘制',dialog)
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)

        def plot372():
            dialog1=QDialog()
            dialog1.setWindowTitle('余弦信号的连续时间傅里叶级数图像')
            try:
                F=typical_signal_fs.plot_cosine(float(edit1.text()),int(edit2.text()),int(edit3.text()),int(edit4.text()))
            except:
                self.empty()
                return
            th=QLabel('theta:'+edit1.text(),dialog1)
            tb=QLabel('t_begin:'+edit2.text(),dialog1)
            te=QLabel('t_end:'+edit3.text(),dialog1)
            tn=QLabel('t_number:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(th,10,0,1,2)
            layout1.addWidget(tb,10,3,1,2)
            layout1.addWidget(te,10,6,1,2)
            layout1.addWidget(tn,11,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot372)
        dialog.exec()
    def showDialog373(self):
        dialog=QDialog()
        dialog.setWindowTitle('正弦信号的连续时间傅里叶级数')
        #theta=0 t_begin=-10, t_end=10, t_number=500
        label1=QLabel('theta:',dialog)
        label2=QLabel('t_begin:',dialog)
        label3=QLabel('t_end:',dialog)
        label4=QLabel('t_number:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('int')
        edit4.setToolTip('int')
        button1=QPushButton('绘制',dialog)
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)

        def plot373():
            dialog1=QDialog()
            dialog1.setWindowTitle('正弦信号的连续时间傅里叶级数图像')
            try:
                F=typical_signal_fs.plot_sine(float(edit1.text()),int(edit2.text()),int(edit3.text()),int(edit4.text()))
            except:
                self.empty()
                return
            th=QLabel('theta:'+edit1.text(),dialog1)
            tb=QLabel('t_begin:'+edit2.text(),dialog1)
            te=QLabel('t_end:'+edit3.text(),dialog1)
            tn=QLabel('t_number:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(th,10,0,1,2)
            layout1.addWidget(tb,10,3,1,2)
            layout1.addWidget(te,10,6,1,2)
            layout1.addWidget(tn,11,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot373)
        dialog.exec()
    def showDialog374(self):
        dialog=QDialog()
        dialog.setWindowTitle('冲激串的连续时间傅里叶级数')
        #T,N,t_begin=-10, t_end=10, t_number=500
        label1=QLabel('T:',dialog)
        label2=QLabel('N:',dialog)
        label3=QLabel('t_begin:',dialog)
        label4=QLabel('t_end:',dialog)
        label5=QLabel('t_number:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        doublevalidator=QDoubleValidator(dialog)
        intvalidator=QIntValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(intvalidator)
        edit3.setValidator(intvalidator)
        edit4.setValidator(intvalidator)
        edit5.setValidator(intvalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('int')
        edit3.setToolTip('int')
        edit4.setToolTip('int')
        edit5.setToolTip('int')
        button1=QPushButton('绘制',dialog)
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text())>0  and len(edit4.text())>0 and len(edit4.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)

        def plot374():
            dialog1=QDialog()
            dialog1.setWindowTitle('冲激串的连续时间傅里叶级数图像')
            try:
                F=typical_signal_fs.plot_impulse(float(edit1.text()),int(edit2.text()),int(edit3.text()),int(edit4.text()),int(edit5.text()))
            except:
                self.empty()
                return
            T=QLabel('T:'+edit1.text(),dialog1)
            N=QLabel('N:'+edit2.text(),dialog1)
            tb=QLabel('t_begin:'+edit3.text(),dialog1)
            te=QLabel('t_end:'+edit4.text(),dialog1)
            tn=QLabel('t_number:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(T,10,0,1,2)
            layout1.addWidget(N,10,3,1,2)
            layout1.addWidget(tb,10,6,1,2)
            layout1.addWidget(te,11,0,1,2)
            layout1.addWidget(tn,11,3,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot374)
        dialog.exec()

    def showDialog41(self):
        dialog=QDialog()
        dialog.setWindowTitle('Amplitude Modulation')
        label1=QLabel('调制信号:',dialog)
        label2=QLabel('载波信号:',dialog)
        label3=QLabel('已调信号:',dialog)
        button1=QPushButton('sinusoidal signal',dialog)
        button1.clicked.connect(self.showDialog411)
        button2=QPushButton('unit step signal',dialog)
        button2.clicked.connect(self.showDialog412)
        button3=QPushButton('unit impulse signal',dialog)
        button3.clicked.connect(self.showDialog413)
        button4=QPushButton('sinusoidal signal',dialog)
        button4.clicked.connect(self.showDialog414)
        button5=QPushButton('sinusoidal signal',dialog)
        button5.clicked.connect(self.showDialog415)
        button6=QPushButton('unit step  signal',dialog)
        button6.clicked.connect(self.showDialog416)
        button7=QPushButton('unit impulse signal',dialog)
        button7.clicked.connect(self.showDialog417)
        
        layout=QGridLayout()
        layout.addWidget(label1,0,0,1,1)
        layout.addWidget(button1,0,3,1,3)
        layout.addWidget(button2,1,3,1,3)
        layout.addWidget(button3,2,3,1,3)
        layout.addWidget(label2,3,0,1,3)
        layout.addWidget(button4,3,3,1,3)
        layout.addWidget(label3,4,0,1,3)
        layout.addWidget(button5,4,3,1,3)
        layout.addWidget(button6,5,3,1,3)
        layout.addWidget(button7,6,3,1,3)
        dialog.setLayout(layout)
        dialog.exec()

    def showDialog411(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulating sinusoidal signal')
        label1=QLabel("the amplitude:",dialog)
        label2=QLabel("the frequency:",dialog)
        label3=QLabel('the phase:',dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)   
        
        def plot_411():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulating sinusoidal signal')
            try:
                F=Amplitude_Modulation.generate_sinusoid_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude::'+edit1.text(),dialog1)
            x2=QLabel('time frequency:'+edit2.text(),dialog1)
            x3=QLabel('the phase:'+edit3.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,3,1,2)
            layout1.addWidget(x3,10,6,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_411)
        dialog.exec()

    def showDialog412(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulating unit step signal')
        label1=QLabel("the amplitude:",dialog)
        label2=QLabel("time shift:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(button1,2,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot_412():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulating unit step signal')
            try:
                F=Amplitude_Modulation.generate_unit_step_plot(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude:'+edit1.text(),dialog1)
            x2=QLabel('time shift:'+edit2.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,3,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_412)
        dialog.exec()

    def showDialog413(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulating unit impulse signal')
        label1=QLabel("the amplitude:",dialog)
        label2=QLabel("time shift:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(button1,2,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot_413():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulating unit impulse signal')
            try:
                F=Amplitude_Modulation.generate_unit_impulse_plot(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude:'+edit1.text(),dialog1)
            x2=QLabel('time shift:'+edit2.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,3,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_413)
        dialog.exec()

    def showDialog414(self):
        dialog=QDialog()
        dialog.setWindowTitle('sinusoidal signal carrier')
        label1=QLabel("the frequency of this waveform:",dialog)
        label2=QLabel("the time shift of modulating signal:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(button1,2,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        
        def plot_414():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot sinusoidal signal carrier')
            try:
                F=Amplitude_Modulation.sinusoidal_carrier_plot(float(edit1.text()),float(edit2.text()))
            except:
                self.empty()
                return
            x1=QLabel('the frequency of this waveform:'+edit1.text(),dialog1)
            x2=QLabel('the time shift of modulating signal:'+edit2.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,3)
            layout1.addWidget(x2,10,5,1,3)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_414)
        dialog.exec()

    def showDialog415(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulated sinusoidal signal')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the frequency of modulating waveform:",dialog)
        label3=QLabel("the phase of modulating waveform:",dialog)
        label4=QLabel("the frequency of carrier waveform:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(button1,4,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        
        def plot_415():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulated sinusoidal signal')
            try:
                F=Amplitude_Modulation.AM_sinusoid_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the frequency of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the phase of modulating waveform:'+edit3.text(),dialog1)
            x4=QLabel('the frequency of carrier waveform:'+edit4.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_415)
        dialog.exec()

    def showDialog416(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulated unit step signal')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the time shift of modulating waveform:",dialog)
        label3=QLabel("the frequency of carrier waveform:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot_416():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulated unit step signal')
            try:
                F=Amplitude_Modulation.AM_unit_step_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the time shift of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the frequency of carrier waveform:'+edit3.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_416)
        dialog.exec()

    def showDialog417(self):
        dialog=QDialog()
        dialog.setWindowTitle('modulated unit impulse signal')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the time shift of modulating waveform:",dialog)
        label3=QLabel("the frequency of carrier waveform:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(button1,3,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        
        def plot_417():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulated unit impulse signal')
            try:
                F=Amplitude_Modulation.AM_unit_impulse_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the time shift of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the frequency of carrier waveform:'+edit3.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_417)
        dialog.exec()

    def showDialog42(self):
        dialog=QDialog()
        dialog.setWindowTitle('sampling')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the frequency of modulating waveform:",dialog)
        label3=QLabel("the phase of modulating waveform:",dialog)
        label4=QLabel("the frequency of carrier waveform:",dialog)
        label5=QLabel("the sampling rate of sampling:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        edit5.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(button1,5,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        
        def plot_42():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot modulated sinusoidal signal')
            try:
                F=Sampling.sampling_sinusoid_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()),float(edit5.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the frequency of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the phase of modulating waveform:'+edit3.text(),dialog1)
            x4=QLabel('the frequency of carrier waveform:'+edit4.text(),dialog1)
            x5=QLabel('the sampling rate of sampling:'+edit5.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_42)
        dialog.exec()

    def showDialog43(self):
        dialog=QDialog()
        dialog.setWindowTitle('Through_LPF')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the frequency of modulating waveform:",dialog)
        label3=QLabel("the phase of modulating waveform:",dialog)
        label4=QLabel("the frequency of carrier waveform:",dialog)
        label5=QLabel("the sampling rate of sampling:",dialog)
        label6=QLabel("the cut-off frequency of the ideal LPF:",dialog)
        label7=QLabel("the delay of the output:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        edit7=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(doublevalidator)
        edit6.setValidator(doublevalidator)
        edit7.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        edit5.setToolTip('float')
        edit6.setToolTip('float')
        edit7.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(label7,6,0,1,2)
        layout.addWidget(edit7,6,2,1,2)
        layout.addWidget(button1,7,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text())>0 and len(edit6.text())>0 and len(edit7.text())>0:
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        edit7.textChanged.connect(en_dis)
        
        def plot_43():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot Through LPF')
            try:
                F=Through_LPF.through_LPF_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()),float(edit5.text()),float(edit6.text()),float(edit7.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the frequency of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the phase of modulating waveform:'+edit3.text(),dialog1)
            x4=QLabel('the frequency of carrier waveform:'+edit4.text(),dialog1)
            x5=QLabel('the sampling rate of sampling:'+edit5.text(),dialog1)
            x6=QLabel('the cut-off frequency of the ideal LPF:'+edit6.text(),dialog1)
            x7=QLabel('the delay of the output:'+edit7.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            layout1.addWidget(x7,13,0,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_43)
        dialog.exec()

    def showDialog44(self):
        dialog=QDialog()
        dialog.setWindowTitle('first order hold convertion')
        label1=QLabel("the amplitude of modulating waveform:",dialog)
        label2=QLabel("the frequency of modulating waveform:",dialog)
        label3=QLabel("the phase of modulating waveform:",dialog)
        label4=QLabel("the frequency of carrier waveform:",dialog)
        label5=QLabel("the sampling rate of sampling:",dialog)
        label6=QLabel("the delay of the output:",dialog)
        edit1=QLineEdit(dialog)
        edit2=QLineEdit(dialog)
        edit3=QLineEdit(dialog)
        edit4=QLineEdit(dialog)
        edit5=QLineEdit(dialog)
        edit6=QLineEdit(dialog)
        button1=QPushButton('绘制',dialog)
        doublevalidator=QDoubleValidator(dialog)
        edit1.setValidator(doublevalidator)
        edit2.setValidator(doublevalidator)
        edit3.setValidator(doublevalidator)
        edit4.setValidator(doublevalidator)
        edit5.setValidator(doublevalidator)
        edit6.setValidator(doublevalidator)
        edit1.setToolTip('float')
        edit2.setToolTip('float')
        edit3.setToolTip('float')
        edit4.setToolTip('float')
        edit5.setToolTip('float')
        edit6.setToolTip('float')
        layout=QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label1,0,0,1,2)
        layout.addWidget(edit1,0,2,1,2)
        layout.addWidget(label2,1,0,1,2)
        layout.addWidget(edit2,1,2,1,2)
        layout.addWidget(label3,2,0,1,2)
        layout.addWidget(edit3,2,2,1,2)
        layout.addWidget(label4,3,0,1,2)
        layout.addWidget(edit4,3,2,1,2)
        layout.addWidget(label5,4,0,1,2)
        layout.addWidget(edit5,4,2,1,2)
        layout.addWidget(label6,5,0,1,2)
        layout.addWidget(edit6,5,2,1,2)
        layout.addWidget(button1,6,0,1,2)
        dialog.setLayout(layout)

        def en_dis():
            if len(edit1.text()) > 0 and len(edit2.text())>0 and len(edit3.text()) > 0 and len(edit4.text())>0 and len(edit5.text())>0 and len(edit6.text())>0 :
                button1.setEnabled(True)
            else:
                button1.setEnabled(False)
        edit1.textChanged.connect(en_dis)
        edit2.textChanged.connect(en_dis)
        edit3.textChanged.connect(en_dis)
        edit4.textChanged.connect(en_dis)
        edit5.textChanged.connect(en_dis)
        edit6.textChanged.connect(en_dis)
        
        def plot_44():
            dialog1=QDialog()
            dialog1.setWindowTitle('plot first order hold convertion')
            try:
                F=First_Order_Hold_Convertion.first_order_hold_convertion_plot(float(edit1.text()),float(edit2.text()),float(edit3.text()),float(edit4.text()),float(edit5.text()),float(edit6.text()))
            except:
                self.empty()
                return
            x1=QLabel('the amplitude of modulating waveform:'+edit1.text(),dialog1)
            x2=QLabel('the frequency of modulating waveform:'+edit2.text(),dialog1)
            x3=QLabel('the phase of modulating waveform:'+edit3.text(),dialog1)
            x4=QLabel('the frequency of carrier waveform:'+edit4.text(),dialog1)
            x5=QLabel('the sampling rate of sampling:'+edit5.text(),dialog1)
            x6=QLabel('the delay of the output:'+edit6.text(),dialog1)
            layout1=QGridLayout()
            layout1.addWidget(F,0,0,10,10)
            layout1.addWidget(x1,10,0,1,2)
            layout1.addWidget(x2,10,5,1,2)
            layout1.addWidget(x3,11,0,1,2)
            layout1.addWidget(x4,11,5,1,2)
            layout1.addWidget(x5,12,0,1,2)
            layout1.addWidget(x6,12,5,1,2)
            dialog1.setLayout(layout1)
            dialog1.exec()

        button1.clicked.connect(plot_44)
        dialog.exec()

    def empty(self):
        QMessageBox.warning(self,'警告','输入不能为空/无效输入！')

    def errorinput(self):
        QMessageBox.warning(self,'警告','输入格式错误！')
    
    def overflow(self):
        QMessageBox.warning(self,'警告','该卷积发散!')


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main=signal()
    main.show()
    sys.exit(app.exec_())