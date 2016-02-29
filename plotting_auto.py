import numpy as np
import matplotlib.pyplot as plt
foldername='C:\\auto_exp\\'
filenames=['neo_plate_36\\results1_2500.0_0.0035','neo_plate_36\\results2_2500.0_0.0035','neo_plate_36\\results3_2500.0_0.0035','neo_plate_30\\results5_2500.0_0.0035','neo_plate_30\\results4_2500.0_0.0035','neo_plate_30\\results3_2500.0_0.0035','neo_plate_30\\results2_2500.0_0.0035']
forcelevels=['neo_plate_36\\2.5Nup.txt']
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
        plt.plot(freq,np.absolute(amp),'-+',label=force[-10:-4])
experiments(forcelevels)

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
            weight=[0.98,-0.23,0.23,-0.05,-0.92,0.81,-0.92,0.87,-0.76,0.81,-0.76,0.67]
        if "neo_plate_36" in filename:
            weight=[0.98,0.23,-0.92,-0.46,0.81,0.65,-0.92,-0.22,0.87,0.43,0.81,0.19]
        if "neo_plate_42" in filename:
            weight=[0.98,0.23,-0.92,-0.46,-0.23,-0.05,0.22,0.11,-0.92,-0.22,0.87,0.43,0.46,0.11,-0.43,-0.21]
        if "neo_plate_45" in filename:
            weight=[0.98,-0.92,0.81,-0.65,-0.23,0.22,-0.19,0.15,-0.92,0.87,0.46,-0.43,0.81,-0.65,-0.65]
        weighteddata=np.zeros((finaldata.shape[0]-1))
        for i in range(len(weight)):
            weighteddata=weighteddata+weight[i]*finaldata[1:,2*(1+i)]
        ident=filename.split('_')
        plt.plot(-0.1+finaldata[1:,0],weighteddata,'-',label='dof='+ident[2][:2]+', f='+str(float(ident[3])/1000.0)+r' N, $\eta$='+ident[4]+' s')

analytical(filenames)
plt.gca().set_xlim(right=2.0)
plt.xlabel(r'non-dimensional frequency ratio $\omega/\omega_{1,1}$')
plt.ylabel('non-dimensional amplitude (w/h)')
plt.title("visoelastic sheet response")
plt.grid(True)
plt.legend(loc='upper right')
plt.savefig(foldername+'test.png')
plt.show()
