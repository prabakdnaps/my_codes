import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib2tikz import save as tikz_save
#fig=plt.figure()
#style.use('ggplot')
foldername='C:\\auto_exp\\'
#filenames=['neo_plate_54\\0.5N_54dofZ1.dat','neo_plate_54\\1.5N_54dofZ1.dat','neo_plate_54\\2.5N_54dofZ1.dat','neo_plate_54\\3.5N_54dofZ1.dat','neo_plate_54\\0.1N_54dofZ.dat']
#forcelevels=['neo_plate_54\\0.1Nup_exp.dat','neo_plate_54\\0.5Nup_exp.dat','neo_plate_54\\1.5Nup_exp.dat','neo_plate_54\\2.5Nup_exp.dat','neo_plate_54\\3.5Nup_exp.dat']
filenames=['neo_plate2_39\\0.1N_39dofZ.dat','neo_plate2_39\\0.07N_39dofZ.dat','neo_plate2_39\\0.04N_39dofZ.dat','neo_plate2_39\\0.01N_39dofZ.dat']
forcelevels=['neo_plate2_39\\0.01n_up.dat','neo_plate2_39\\0.04n_up.dat','neo_plate2_39\\0.04n_dn.dat','neo_plate2_39\\0.07n_up.dat','neo_plate2_39\\0.07n_do.dat','neo_plate2_39\\0.1n_up.dat','neo_plate2_39\\0.1n_do.dat']
def experiments2(forcelevels):
    for force in forcelevels:
        file2=open('C:\\auto_exp\\'+force,'r')
        data1=file2.read()
        file2.close()
        data1=data1.split('\n')
        freq=[]
        amp=[]
        for line in data1[:-1]:
            linedata=line.split('\t')
            freq.append(float(linedata[0]))
            amp.append(float(linedata[1]))
        plt.plot(freq,amp,'+',markersize=5)
experiments2(forcelevels)
def experiments3(filenames):
    for force in filenames:
        file2=open('C:\\auto_exp\\'+force,'r')
        data1=file2.read()
        file2.close()
        data1=data1.split('\n')
        freq=[]
        amp=[]
        for line in data1[:-1]:
            linedata=line.split('\t')
            freq.append(float(linedata[0]))
            amp.append(float(linedata[1]))
        plt.plot(freq,amp,'-',markersize=5)
experiments3(filenames)
#plt.gca().set_xlim(left=0.5,right=1.5)
plt.xlabel(r'Frequency, $\Omega$')
plt.ylabel('Amplitude, A')
plt.title("SDOF Response")
plt.grid(True)
plt.legend(loc='best')
plt.savefig(foldername+'2_39dof.png')
plt.show()
tikz_save('C:\\auto_exp\\mytikz.tex', figureheight='6cm', figurewidth='8cm')