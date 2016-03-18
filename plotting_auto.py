import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib2tikz import save as tikz_save
#fig=plt.figure()
#style.use('ggplot')
foldername='C:\\auto_exp\\'
#filenames=['neo_plate_12\\results_500.0_0.008','neo_plate_12\\results_2500.0_0.006','neo_plate_12\\results_7500.0_0.005','neo_plate_12\\results_12500.0_0.0045','neo_plate_12\\results_17500.0_0.0035']
filenames=['neo_plate_30\\results4_3500.0_0.0025','neo_plate_30\\results4_2500.0_0.0035','neo_plate_30\\results4_1500.0_0.0045','neo_plate_30\\results4_500.0_0.009','neo_plate_30\\results4_100.0_0.012']
#filenames=['neo_plate2_39\\results13_100.0_0.0012','neo_plate2_39\\results13_60.0_0.0018','neo_plate2_39\\results13_35.0_0.002','neo_plate2_39\\results13_10.0_0.005']
forcelevels=['neo_plate_30\\3.5Nup.txt','neo_plate_30\\2.5Nup.txt','neo_plate_30\\1.5Nup.txt','neo_plate_30\\0.5Nup.txt','neo_plate_30\\0.1Nup.txt']
forcelevels2=['neo_plate2_30\\0.1n_do.dat','neo_plate2_30\\0.1n_up.dat','neo_plate2_30\\0.07n_up.dat','neo_plate2_30\\0.07n_do.dat','neo_plate2_30\\0.04n_up.dat','neo_plate2_30\\0.04n_dn.dat','neo_plate2_30\\0.01n_up.dat']
def experiments(forcelevels):
    for force in forcelevels:
        file2=open(foldername+force,'r')
        data1=file2.read()
        file2.close()
        data1=data1.split('\n')
        freq=[]
        amp=[]
        for line in data1[36:]:
            linedata=line.split('\t')
            if linedata[0]!='':
                freq.append(float(linedata[0]))
                amp.append(complex(float(linedata[2]),float(linedata[1])))
        freq=np.asarray(freq)
        amp=np.asarray(amp)
        amp=amp/(2*np.pi*freq)/0.003
        freq=freq/13.2
        plt.plot(freq,np.absolute(amp),'o',label=force[-10:-4])
experiments(forcelevels)

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
        plt.plot(freq,amp,'o',markersize=5,label=force[-10:-4])
#experiments2(forcelevels2)

def analytical(filenames):
    for filename in filenames:
        file1=open(foldername+filename+'\\fort.7','r')
        data=file1.read()
        file1.close()
        data=data.split('\n')
        for linenumber in range(len(data)):
            if 'TY' in data[linenumber]:
                lineNo=linenumber
        for linenumber in range(lineNo+1, lineNo+2):
            datali=[]
            linedata=data[linenumber].split(' ')
            for i in linedata:
                if i!='':
                    datali.append(float(i))
            dof=len(datali)-5
        
        finaldata=np.zeros((1,dof))
        for linenumber in range(lineNo+1, len(data)-1):
            datali=[]
            linedata=data[linenumber].split(' ')
            for i in linedata:
                if i!='':
                    datali.append(float(i))
            tempdata=np.array([datali[4:-1]])
            temp1data=finaldata
            finaldata=np.vstack((temp1data,tempdata))
        if "neo_plate_30" in filename:
            weight=[0.98,-0.23,0.23,-0.05]#,-0.92,0.81,-0.92,0.87,-0.76,0.81,-0.76,0.67]
        if "neo_plate_12" in filename:
            weight=[3.88]#,0.225,0.225,0.0131]
        if "neo_plate2_39" in filename:
            weight=[1]#,-1,1,-1,1,-1,1,-1,1,-1,1,-1,1]
        '''if "neo_plate_36" in filename:
            weight=[0.98,0.23,-0.92,-0.46,0.81,0.65,-0.92,-0.22,0.87,0.43,0.81,0.19]
        if "neo_plate_42" in filename:
            weight=[0.98,0.23,-0.92,-0.46,-0.23,-0.05,0.22,0.11,-0.92,-0.22,0.87,0.43,0.46,0.11,-0.43,-0.21]
        if "neo_plate_45" in filename:
            weight=[0.98,-0.92,0.81,-0.65,-0.23,0.22,-0.19,0.15,-0.92,0.87,0.46,-0.43,0.81,-0.65,-0.65]
        if "neo_plate_39" in filename:
            weight=[0.98,-0.92,0.81,-0.92,0.87,-0.76,0.81,-0.76,0.67,-0.65,0.62,-0.65,0.62]
        if "neo_plate_48" in filename:
            weight=[0.98,0.92,0.81,0.92,0.87,0.76,0.81,0.76,0.677,0.23,0.46,0.65,0.22,0.43,0.19,0.15]
        if "neo_plate2_30" in filename:
            weight=[1]#,0,0,0,-1,1,-1,1,-1,1,-1,1]

        if "neo_plate_21" in filename:
            weight=[3.88,0.225,0.225,0.0131,3.44,3.44,3.05]
        if "neo_plate_3" in filename:
            weight=[3.88]
        if "neo_plate_27" in filename:
            weight=[3.88]'''#,0.225,0.225,0.0131,3.44,3.44,3.05,2.66,2.66]
        weighteddata=np.zeros((finaldata.shape[0]-1))
        for i in range(len(weight)):
            weighteddata=weighteddata+weight[i]*finaldata[1:,2*(1+i)]
        ident=filename.split('_')
        plt.plot(finaldata[1:,0],weighteddata,'-',linewidth=2,label='dof='+ident[2][:2]+', f='+str(float(ident[3])/1000.0)+r' N, $\eta$='+ident[4]+' s')

analytical(filenames)
plt.gca().set_xlim(left=0.7,right=1.4)
plt.xlabel(r'non-dimensional frequency ratio $\omega/\omega_{1,1}$')
plt.ylabel('non-dimensional amplitude (w/h)')
plt.title("visoelastic sheet response")
plt.grid(True)
#plt.legend(loc='best')
plt.savefig(foldername+'2_39dof.png')
plt.show()
#tikz_save('C:\\auto_exp\\mytikz.tex', figureheight='6cm', figurewidth='8cm')