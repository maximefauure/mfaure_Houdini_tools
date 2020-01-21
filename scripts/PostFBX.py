from shutil import copyfile
from hou import * 
import os


inPath = hou.pwd().evalParm("sopoutput")
newPath =  hou.pwd().evalParm("sopoutputCopy")


#newPath = hou.hscriptExpression("$EXPORT")+"/"+hou.hscriptExpression("$HIPNAME")+"."+str(hou.pwd())+".fbx"

copyfile( inPath, newPath)


