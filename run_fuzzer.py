#author : muhe
#Fuzz script.
#Useage : python run_fuzzer.py fuzzer_work_dir file_dir

import os
import re
import sys
import psutil
import threading
import subprocess
import shutil
from time import sleep

fileDir = ""
fileDict = {}
fileCount = 0
crashCount = 0
programName = "flashplayer_22_sa_debug.exe"
#killDbg = "taskkill.exe /F /IM windbg.exe"
copyfileCmd=""
killProgram = "taskkill.exe /F /IM " + programName
fuzzFilename = "fuzz.swf"
workDir = ""
runCmd = programName +" "+ fuzzFilename

def argsHandle():
    global fileDir
    global workDir
    if(len(sys.argv) != 3):
        showHelp()
        sys.exit()
    workDir = sys.argv[1]
    fileDir = sys.argv[2]
    if fileDir:
        getFileList(fileDir)

def getFileList(fuzzFolder):
    global fileCount
    global fileDict
    for root,dirs,files in os.walk(fuzzFolder):
        for fn in files:
            fileDict[fileCount] = root+"\\"+fn
            fileCount+=1
    print "[*]Now,I got %d files at %s" % (fileCount,fuzzFolder)


def showHelp():
    print "--------------------------------------------"
    print "[!] Ussage : python %s fuzzer_work_dir file_dir" % (sys.argv[0])
    print "--------------------------------------------"

def run(fileID):
    copyFile(fileID)
    subprocess.Popen(runCmd)
    #sleep(2)
    checkCrash()
    #sleep(1)
    clean()

def copyFile(fileID):
    shutil.copyfile(fileDict.get(fileID),workDir+"fuzz.flv")

def clean():
    subprocess.Popen(killProgram)#kill programName for next one 
    sleep(1)
    if(os.path.exists(workDir+"fuzz.flv")):
        os.remove(workDir+"fuzz.flv")
    

def log(fileID):
    global crashCount
    info = "No.%d: Crash Found at:%s" % (crashCount,fileDict.get(fileID)) +"\n"
    with open("log_fuzz.txt",'a') as f:
        f.write(info)

def checkCrash():
    winDbg = "windbg.exe"
    #get process list
    try:
        processList = psutil.process_iter()
    except Exception as e:
        print e
    for p in processList:
        if(p.name == winDbg):
            print "[#]Crash Found! Writing to log now ..."
            log(fileID)
            sleep(1)
            p.kill()
        else:
            pass 

def main():
    argsHandle()
    #begin from : 7883
    for i in range(7883, fileCount):
        print "[%d].Fuzzing : %s" %(i,fileDict.get(i))  
        run(i)
        sleep(1)
        print "\n"
    print "[*]Done fuzz."
if __name__ == "__main__":
    main()