# -*- coding: gbk -*-  

""" 
���ܣ�����Ƭ��������ʱ����й��� 
ʹ�÷��������ű�����Ƭ����ͬһĿ¼��˫�����нű����� 
���ߣ�����
"""  

import shutil  
import os  
import sys
import time  
import exifread  


class ReadFailException(Exception):  
    pass  

def getOriginalDate(filename):  
    try:  
        fd = open(filename, 'rb')  
    except:  
        raise ReadFailException, "unopen file[%s]\n" % filename  
    data = exifread.process_file( fd )  
    if data:  
        try:  
            t = data['EXIF DateTimeOriginal']  
            # t is 2012:11:22 15:35:14
            yearStr=str(t)[0:4]
            monthStr=str(t)[5:7]
            dayStr=str(t)[8:10]
            
            return yearStr+"��"+monthStr+"��"+dayStr+"��"  
        except:  
            pass  
    state = os.stat(filename)  
    return time.strftime("%Y��%m��%d��", time.localtime(state[-2]))  


def movePicFile(fullfilename,saveRootPath):  
    print("���ڲ����ļ���"+fullfilename)
    (filepath,filename) = os.path.split(fullfilename);
    f,e = os.path.splitext(filename)  
    if e.lower() not in ('.jpg','.png','.mp4','.mov'):  
        return  
    info = "�ļ���: " + filename + " "  
    t=""  
    try:  
        t = getOriginalDate( fullfilename )  
    except Exception,e:  
        print e  
        return  
    info = info + "����ʱ�䣺" + t + " "  
    if e.lower()  in ('.jpg','.png','.png','.gif','.jpeg'): 
        savePath = saveRootPath +'\\'+ t+"\\��Ƭ"
    if  e.lower()  in ('.mp4','.mov','.mkv'):
        savePath = saveRootPath +'\\'+ t+"\\��Ƶ"
    
    dst = savePath + '\\' + filename  
    if not os.path.exists(savePath):  
        try:
            os.makedirs(savePath)  
        except Exception,e:
            print(e)
            
    print info, dst  
    if  os.path.exists(dst):
        print ("�ļ��Ѿ�����.")
        return 
    shutil.copy2( fullfilename, dst )  
    os.remove( fullfilename )  

def dirlist(path,saveRootPath):
    filelist = os.listdir(path)
    for filename in filelist:
        filepath = os.path.join(path,filename)
        if os.path.isdir(filepath):
            dirlist(filepath,saveRootPath)
        else:
            movePicFile(filepath,saveRootPath)
    return

#ɾ����Ŀ¼
def deleteEmptyDir(dir):
    if  os.path.isdir(dir):
         for item in os.listdir(dir):
             if item!='System Volume Information':#windows��ûȨ��ɾ����Ŀ¼�����ڴ���Ӹ��಻�жϵ�Ŀ¼
                 deleteEmptyDir(os.path.join(dir, item))
 
         if not os.listdir(dir):
             os.removedirs(dir)
             print("�Ƴ���Ŀ¼��" + dir)    

if __name__ == "__main__":  
    root_path =os.path.dirname(os.path.realpath(__file__))
    deleteEmptyDir(root_path)
    dirlist(root_path,root_path) 
    deleteEmptyDir(root_path)
    