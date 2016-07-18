import os, time
import smtplib
import time

def auto_exe(folder_loc, file_name, conPara):
    os.system('del command.bat')
    com=open('command.bat','w')
    com.write('cd '+folder_loc+'\n')
    com.write('auto '+file_name+ ' '+str(conPara)+'\n')
    com.close()
    os.system('command.bat')

def newrun(folder_loc, file_name):
    os.system('del command.bat')
    com=open('command.bat','w')
    com.write('cd '+folder_loc+'\n')
    com.write('newrun\n')
    com.close()
    os.system('command.bat')

def third_control(folder_loc2, file_name, row):
    file1=open(folder_loc2+'//r.'+file_name+'.3','r')
    data=file1.read()
    file1.close()
    file2=open(folder_loc2+'//r.'+file_name+'.3','w')
    data=data.split('\n')
    for line in data:
        if 'IRS' in line:
            linedata=line.split(' ')
            linedata[2]=str(row)
            linedata=" ".join(linedata)
            line=linedata
        file2.write(line+'\n')
    file2.close()

def second_control(folder_loc2,file_name,force):
    file1=open(folder_loc2+'//r.'+file_name+'.2','r')
    data=file1.read()
    file1.close()
    file2=open(folder_loc2+'//r.'+file_name+'.2','w')
    data=data.split('\n')
    for line in data:
        if 'RL1' in line:
            linedata=line.split(' ')
            linedata[2]=str(force)
            linedata=" ".join(linedata)
            line=linedata
        file2.write(line+'\n')
    file2.close()
    
def row_find(folder_loc2,file_name):
    file1=open(folder_loc2+'//fort.6','r')
    data=file1.read()
    file1.close()
    data=data.split('\n')
    line=data[len(data)-4]
    line=line.split(' ')
    for i in range(len(line)-1):
        if line[i]=='EP':
            for j in range(10):
                if line[i+j+1]!='':
                    return line[i+j+1]
                    break

def main():
    start_time=time.time()
    #initialize with program name and folder name
    eta=[0.008]
    forcelevels=[28.0]
    folder_loc='C:\\Users\\Praba\\Documents\\Farbod_auto\\tomlinson'
    folder_loc2='C://Users//Praba//Documents//Farbod_auto//tomlinson'
    file_name='duffing'
    #loop for changing the force levels and runnging the AUTO to get the response
    count=1
    for run in range(len(forcelevels)):
       #changes a particular value in Fortran file; in this case eta
        file1=open(folder_loc+'\\'+file_name+'.for','r')
        data=file1.read()
        file1.close()
        file2=open(folder_loc+'\\'+file_name+'.for','w')
        data=data.split('\n')
        for ii in range(len(data)-1):
            if ii==47:
                linedata=data[ii].split('\t')
                linedata[-1]='eta='+str(eta[run])
                data[ii]='\t'.join(linedata)
            file2.write(data[ii]+'\n')
        file2.close()
        #compiles fortran file and created exe file
        os.system('del command.bat')
        com=open('command.bat','w')
        com.write('cd '+folder_loc+'\n')
        com.write('df -c -extend_source:132 '+file_name+'.for\n')
        com.write('df -c -extend_source:132 autlib1.f\n')
        com.write('df -c -extend_source:132 autlib2.f\n')
        com.write('df -c -extend_source:132 autlib3.f\n')
        com.write('df -c -extend_source:132 autlib4.f\n')
        com.write('df -c -extend_source:132 autlib5.f\n')
        com.write('df -c -extend_source:132 eispack.f\n')
        com.close()
        os.system('command.bat')
        time.sleep(5)
        while True:
            statinfo = os.stat(folder_loc+'\\autlib1.obj')
            if statinfo.st_size >10000:
                break
            else:
                com=open('command.bat','w')
                com.write('cd '+folder_loc+'\n')
                com.write('df -c -extend_source:132 autlib1.f\n')
                com.close()
                os.system('command.bat')
                time.sleep(3)
        time.sleep(5)
        os.system('del command.bat')
        com=open('command.bat','w')
        com.write('cd '+folder_loc+'\n')
        com.write('df /exe '+file_name+'.obj autlib*.obj eispack.obj\n')
        com.close()
        os.system('command.bat')

        conPara=2
        print 'force level = '+str(forcelevels[run])+' N'
        start_time=time.time()
        #changing the second control file   
        print 'starting second control file change'   
        second_control(folder_loc2,file_name,forcelevels[run])
        #executing the first run
        print 'starting second control run'
        auto_exe(folder_loc,file_name, conPara)
        print 'finding the row'
        #changing the 3 control file
        row=row_find(folder_loc2,file_name)
        print 'found row = '+str(row)
        print 'starting third control file change'   
        third_control(folder_loc2,file_name,row)        
        #executing the newrun
        print 'starting newrun'
        newrun(folder_loc,file_name)
        print 'starting third run'
        #executing the second run
        conPara=3
        auto_exe(folder_loc,file_name, conPara)
        print 'saving the results'
        os.system('mkdir '+folder_loc+'\\results_'+str(forcelevels[run])+'_'+str(eta[run]))
        os.system('copy '+folder_loc+'\\fort* '+ folder_loc+'\\results_'+str(forcelevels[run])+'_'+str(eta[run])+'\\fort*')
        os.system('del '+folder_loc+'\\fort*')
        os.system('del '+folder_loc+'\\*.obj')
        os.system('del '+folder_loc+'\\*.exe')
        final_time=time.time()-start_time

        print 'Time elasped for '+str(count)+' cycle = '+str(final_time)
        print 'Estimated time for finishing all the cycles = '+str((len(forcelevels)-count)*final_time)
        count=count+1
        print count
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('prabakaran.des@gmail.com','Pandinattu@01092014')
    msg="\nRun completed"
    server.sendmail('prabakaran.des@gmail.com','prabakaran.balasubramanian@mail.mcgill.ca',msg)
main()
#print('auto '+file_name+ ' '+str(conPara))
#os.system('auto '+file_name+ ' '+str(conPara))