ndof=54
equation=[]
for i in range(ndof):
    file1=open('E:\\Thesis\\visco\\kelvinVoigtVisco\\check400\\pr'+str(i+1)+'.dat','r')
    data1=file1.read()
    file1.close()
    data1=data1.split('\n')
    innerloop=int(len(data1)/600)+1
    for j in range(innerloop):
        if len(data1)>600:
            if data1[600][-1]=="*":
                data2=data1[0:600]
                sign=data2[599][-2]
                data2[599]=data2[599][:-2]
                data1=data1[600:]
            else:
                data2=data1[0:601]
                sign=data2[600][-2]
                data2[600]=data2[600][:-2]
                data1=data1[601:]               
        else:
            data2=data1
            sign=''
        file2=open('E:\\Thesis\\visco\\kelvinVoigtVisco\\check400\\vr'+str(i+1)+'_'+str(j+1)+'.dat','w')
        for line in data2:
            file2.write(line+'\n')
        file2.close()
        equation.append('vr'+str(i+1)+'_'+str(j+1)+' '+str(sign))
    equation.append('\n')
file3=open('E:\\Thesis\\visco\\kelvinVoigtVisco\\check400\\equ_seq.dat','w')
for line in equation:
    file3.write(line)
file3.close()