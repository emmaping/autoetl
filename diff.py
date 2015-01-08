'''
Created on Jun 8, 2013

@author: Administrator
'''
import sys
import csv
import _winreg as wreg
import os
import re
import subprocess
import uuid
import operator
# etl1 = "E:\\Temp\\8591360_viral_local_scan\\1_viral_local_scan.etl"
# etl2 = "E:\\Temp\\8591360_viral_local_scan\\2_viral_local_scan.etl"
# counter = "diskio"
# output = "E:\\Temp\\8591360_viral_local_scan\\output_01.csv"
# f1="D:\\workspace\\AutoETL\\profile_1.txt"
# f2="D:\\workspace\\AutoETL\\profile_2.txt"
# class DiffEtl:
#     def __init__(self):
#         pass
# 
#     def main(self, args=None):
#         pass
counters = {}  
def getxperf(): 
    try:
        key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows Kits\Installed Roots')
        xperfroot = wreg.QueryValueEx(key, 'KitsRoot')
        return xperfroot[0]+"Windows Performance Toolkit\\xperf.exe"
    except EnvironmentError:
        print "Please install Xperf first"
        try:
            key.close()
        except:
            pass
        sys.exit(1) 
        
    key.Close()

def exexperf(etl, counter):
    xperf = getxperf()
    output = str(uuid.uuid4())
    cmd = [xperf, "-tle", "-symbols","-i" , etl, "-o", output,"-a"]
    cmd.extend(counter)
    subprocess.check_call(cmd, shell=True)
    return output
    
def getiosum(input, column):
    cr = csv.reader(open(input,"rb"))
    total = 0
    cr.next()
    cr.next()
    total= sum(int(x[column]) for x in cr)

    return total
def gettotalweight(input):
    datafile = file(input)
    for line in datafile:
        if "Total Weight:" in line:
            #found = True #not necessary 
            totalweight = re.findall(r'\d+', line)
    return int(totalweight[0])

def cpureport(f1, f2, output):
    
    cri1 =  csv.reader(open(f1,"rb"))
    cri2 =  csv.reader(open(f2,"rb"))
    mycsv = []
    csvlist = []
    mycsv.extend(cri2)
    cri1.next()

    for line in mycsv:
        try:
            if line:
                callstack = line[0]+line[3]

                if callstack not in csvlist:
                        csvlist.append(callstack)
            else:
                break
        except IndexError:
            continue
    with open(output, 'wb') as cwoutput:
        cw = csv.writer(cwoutput)
        mydict = {}
        value = 0
        for line1 in cri1:
            if line1:
                callstack = line1[0]+line1[3]
                try:
                    if line1[3] :
                        value = int(line1[1])
                        
                        if callstack in csvlist:
#                             print "line1[1]", line1[1]
#                             print "line1[0]+line1[3]",line1[0]+line1[3]
#                             print "index",csvlist.index(callstack)
#                             print mycsv[csvlist.index(callstack)]
#                             print "value in etl2",int(mycsv[csvlist.index(callstack)][1])
        
                            value = int(line1[1]) - int(mycsv[csvlist.index(callstack)][1])   
                    mydict[callstack] = value
                except IndexError:
                    continue
            else:
                break
        sorted_dict = sorted(mydict.iteritems(), key=operator.itemgetter(1),reverse=True)
        for item in sorted_dict:
            cw.writerow(item)
        print "******* Top 10 call stack and consumed more CPU time *******"
        for i in range(0,10):
            print sorted_dict[i][0], sorted_dict[i][1]
            
        print ("******* More detailed info refer to %s *******" %(output))

def ioreport(f1, f2, output):
    
    cri1 =  csv.reader(open(f1,"rb"))
    cri2 =  csv.reader(open(f2,"rb"))
    mycsv = []
    csvlist = []
    mycsv.extend(cri2)
    cri1.next()
    cri1.next()

    for line in mycsv:
        if line:
            csvlist.append(line[10])

    with open(output, 'wb') as cwoutput:
        cw = csv.writer(cwoutput)
        mydict = {}
        value = 0
        for line1 in cri1:
            value = int(line1[9])
            if line1[10] :
                if line1[10] in csvlist:
#                       print "line1[9]", line1[9]
#                       print "line1[10]",line1[10]
#                       print "index",csvlist.index(line1[10] )
#                       print "value in etl2",int(mycsv[csvlist.index(line1[10])+1][9])

                      value = int(line1[9]) - int(mycsv[csvlist.index(line1[10])+1][9])   
            mydict[line1[10]] = value

        sorted_dict = sorted(mydict.iteritems(), key=operator.itemgetter(1),reverse=True)
        for item in sorted_dict:
            cw.writerow(item)
        print "******* Top 10 files and consumed more IO time *******"
        for i in range(0,10):
            print sorted_dict[i][0], sorted_dict[i][1]
            
        print ("******* More detailed info refer to %s *******" %(output))

def genioreport(etl1, etl2, output):
    counter = ["diskio", "-summary"]
    f1 = exexperf(etl1, counter)
    f2 = exexperf(etl2, counter)
    t1 = getiosum(f1,9)
    t2 = getiosum(f2,9)
    if t1 < t2 :
        print ("%s takes more %d us than %s" %(etl2, t2-t1, etl1))
        ioreport(f2, f1, output)
    else:
        if getiosum(f1, 9) == getiosum(f2, 9):
            print ("%s 's IO time is same as %s" %(etl1, etl2))
            exit(0)
        else:
            print ("%s takes more %d ms than %s" %(etl1, t1 - t2, etl2))
            ioreport(f1, f2, output)
    os.remove(f1)
    os.remove(f2) 
    
def gencpureport(etl1, etl2, output):
    counter = ["profile","-detail"]
    f1 = exexperf(etl1, counter)
    f2 = exexperf(etl2, counter)
    weight1 = gettotalweight(f1)
    weight2 = gettotalweight(f2)
    if weight1 < weight2 :
        print ("%s takes more %d weight than %s" %(etl2, weight2-weight1, etl1))
        cpureport(f2, f1, output)
    else:
        if weight1 == weight2:
            print ("%s 's CPU usage is same as %s" %(etl1, etl2))
            exit(0)
        else:
            print ("%s takes more %d weight than %s" %(etl1,weight1-weight2, etl2))
            cpureport(f1, f2, output)
    os.remove(f1)
    os.remove(f2) 
          
def main(etl1, etl2, counter, output):
    if 'diskio' == counter:
        genioreport(etl1,etl2,output)
    elif 'cpu' == counter:
        gencpureport(etl1,etl2,output)
    else:
        print "Only support counter diskio and cpu by now"
