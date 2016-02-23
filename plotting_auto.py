import numpy as np
import matplotlib.pyplot as plt
foldername='C:\\auto_exp\\neo_plate_30\\'
filenames=['results_100.0_0.012','results_500.0_0.009','results_1500.0_0.0045','results_2500.0_0.0035']
forcelevels=['0.1Nup.txt','0.5Nup.txt','1.5Nup.txt','2.5Nup.txt','3.5Nup.txt']
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
    plt.plot(freq,np.absolute(amp),'.',label=force)
for filename in filenames:
    file1=open(foldername+filename+'\\fort.7','r')
    data=file1.read()
    file1.close()
    data=data.split('\n')
    count=0
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
    weight=[0.98,-0.23,0.23,-0.057,-0.928,0.81,-0.92,0.87,-0.76,0.67]
    weighteddata=np.zeros((finaldata.shape[0]-1))
    for i in range(len(weight)):
        weighteddata=weighteddata+weight[i]*finaldata[1:,2*(1+i)]
    plt.plot(finaldata[1:,0],weighteddata,label=filename)
    plt.xlabel('frequency ratio')
    plt.ylabel('amplitude (w/h)')
    plt.title("visoelastic sheet response")
    plt.grid(True)
    plt.legend()
plt.show()