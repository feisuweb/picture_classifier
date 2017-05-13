# -*- coding: gbk -*-  

""" 
功能：对照片按照拍摄时间进行归类 
使用方法：将脚本和照片放于同一目录，双击运行脚本即可 
作者：rockman
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
            
            return yearStr+"年"+monthStr+"月"+dayStr+"日"  
        except:  
            pass  
    state = os.stat(filename)  
    return time.strftime("%Y年%m月%d日", time.localtime(state[-2]))  


def movePicFile(fullfilename,saveRootPath):  
    print("正在操作文件夹"+fullfilename)
    (filepath,filename) = os.path.split(fullfilename);
    f,e = os.path.splitext(filename)  
    if e.lower() not in ('.jpg','.png','.mp4','.mov'):  
        return  
    info = "文件名: " + filename + " "  
    t=""  
    try:  
        t = getOriginalDate( fullfilename )  
    except Exception,e:  
        print e  
        return  
    info = info + "拍摄时间：" + t + " "  
    if e.lower()  in ('.jpg','.png','.png','.gif','.jpeg'): 
        savePath = saveRootPath +'\\'+ t+"\\照片"
    if  e.lower()  in ('.mp4','.mov','.mkv'):
        savePath = saveRootPath +'\\'+ t+"\\视频"
    
    dst = savePath + '\\' + filename  
    if not os.path.exists(savePath):  
        try:
            os.makedirs(savePath)  
        except Exception,e:
            print(e)
            
    print info, dst  
    if  os.path.exists(dst):
        print ("文件已经存在.")
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

#删除空目录
def deleteEmptyDir(dir):
    if  os.path.isdir(dir):
         for item in os.listdir(dir):
             if item!='System Volume Information':#windows下没权限删除的目录：可在此添加更多不判断的目录
                 deleteEmptyDir(os.path.join(dir, item))
 
         if not os.listdir(dir):
             os.removedirs(dir)
             print("移除空目录：" + dir)    

if __name__ == "__main__":  
    root_path =os.path.dirname(os.path.realpath(__file__))
    deleteEmptyDir(root_path)
    dirlist(root_path,root_path) 
    deleteEmptyDir(root_path)
    