# Embedded file name: D:/Software/Houdini 16.5/houdini/scripts/python\ProjViewer\PV.py
import os
import hou
import re
import subprocess
from PySide2 import QtWidgets, QtUiTools, QtGui, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import numpy as np




class MfProjectViewer(QtWidgets.QWidget):

    def __init__(self):
        super(MfProjectViewer, self).__init__()
        self.scriptpath = 'C:/Users/Public/pipeline/shared/maximef/Houdini/MF_PROJECT/scripts/MfProjectViewer'
                
        self.tmpPath = hou.homeHoudiniDirectory()+'/Proj_Path.txt'
        try:
            pathfile = open(self.tmpPath)
        except IOError:
               #If not exists, create the file
               pathfile = open(self.tmpPath, 'w+')

        txtcon = pathfile.readline()
        pathfile.close()
        self.oripath = txtcon.replace('\\', '/')
        self.proj = self.oripath
        self.transition = '0'
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(self.scriptpath + '/UI.ui')


        self.setproj = self.ui.findChild(QtWidgets.QPushButton, 'setproj')
        self.setproj.setText("ADD PATH")

        self.openPathList = self.ui.findChild(QtWidgets.QPushButton, 'openPathList')        
        self.openPathList.clicked.connect(self.OpenPathList)

        self.scenelist = self.ui.findChild(QtWidgets.QListWidget, 'scenelist')
        #self.label = self.ui.findChild(QtWidgets.QLabel, 'label_2')
        self.height = self.ui.findChild(QtWidgets.QSpinBox, 'spinbox')
        self.setproj.clicked.connect(self.setproject)


        self.folderlist = self.ui.findChild(QtWidgets.QComboBox, 'folderlist')
        self.folderlist.activated.connect(self.Refresh)
        self.folderlist.activated.connect(self.CreateInterface)
        self.height.valueChanged.connect(self.changeHeight)


        self.saveas = self.ui.findChild(QtWidgets.QPushButton, 'save_as')        
        self.saveas.clicked.connect(self.saveprojectAs)

        self.save = self.ui.findChild(QtWidgets.QPushButton, 'save')        
        self.save.clicked.connect(self.saveProject)

        self.incrementsave = self.ui.findChild(QtWidgets.QPushButton, 'increment_save')        
        self.incrementsave.clicked.connect(self.incrementSave)
        
        self.imagesPath = self.ui.findChild(QtWidgets.QPushButton, 'imagesPath')
        self.imagesPath.setText('images path : ')
        self.imagesPath.clicked.connect( self.SubmitImagesPath )

        self.cachesPath = self.ui.findChild(QtWidgets.QPushButton, 'cachesPath')
        self.cachesPath.setText('caches path : ')
        self.cachesPath.clicked.connect( self.SubmitCachesPath )

        self.elementsPath= self.ui.findChild(QtWidgets.QPushButton, 'elementsPath')
        self.elementsPath.setText('elements path : ')
        self.elementsPath.clicked.connect( self.SubmitElementsPath )

        self.outPath = self.ui.findChild(QtWidgets.QPushButton, 'outPath')
        self.outPath.setText('out path : ')
        self.outPath.clicked.connect( self.SubmitOutPath )        

        self.refreshBtn = self.ui.findChild(QtWidgets.QPushButton, 'refreshBtn')        
        self.refreshBtn.clicked.connect(self.CreateInterface)

        self.openFolder = self.ui.findChild(QtWidgets.QPushButton, 'openFolder')        
        self.openFolder.clicked.connect(self.OpenFolder)

        self.openHoudiniFolder = self.ui.findChild(QtWidgets.QPushButton, 'openHoudiniFolder')        
        self.openHoudiniFolder.clicked.connect(self.OpenHoudiniFolder)
        
        
        
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)


        self.Refresh()
        self.CreateInterface()
        self.scenelist.setIconSize(QSize(150, 150))
        #self.label.setMaximumHeight(200)
        heightfile = open(self.scriptpath + '/mf_ProjV/Height.txt')
        heightS = heightfile.readline()
        try:
            height = int(heightS)
        except ValueError:
            height = 500

        self.scenelist.setMaximumHeight(height)
        self.scenelist.setMinimumHeight(height)
        self.height.setValue(height)
        heightfile.close()

    def changeHeight(self, data):
        self.scenelist.setMaximumHeight(data)
        self.scenelist.setMinimumHeight(data)
        f = open(self.scriptpath + '/mf_ProjV/Height.txt', 'wt')
        f.write(str(data))
        f.close()

    def saveprojectAs(self):
        cur_desktop = hou.ui.curDesktop()
        scene = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
        a = hou.hipFile.name()

        k = a.split('/')
        hip = ''
       
        hip = hou.ui.selectFile(title='Save', file_type=hou.fileType.Hip, start_directory=self.projpath )
        if hip != '':
            hou.hipFile.save(file_name=hip)

        f = hou.frame()
        fn = hou.hipFile.basename().split('.')
        del fn[-1]
        filename = '.'.join(fn)
        path = hou.hipFile.path().split('/')
        del path[-1]
        filepath = '/'.join(path) + '/_thumbnails/' + filename + '.jpg'
        newpath =  '/'.join(path) + '/_thumbnails' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            
        flip_options = scene.flipbookSettings().stash()
        flip_options.frameRange((f, f))
        flip_options.useResolution(1)
        flip_options.resolution((500, 500))
        flip_options.output(filepath)
        scene.flipbook(scene.curViewport(), flip_options)
        self.CreateInterface()

    def saveProject(self):
        cur_desktop = hou.ui.curDesktop()
        scene = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
        hip = hou.hipFile.name()
        hou.hipFile.save(file_name=hip)

        f = hou.frame()
        fn = hou.hipFile.basename().split('.')
        del fn[-1]
        filename = '.'.join(fn)
        path = hou.hipFile.path().split('/')
        del path[-1]
        filepath = '/'.join(path) + '/_thumbnails/' + filename + '.jpg'
        newpath =  '/'.join(path) + '/_thumbnails' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        flip_options = scene.flipbookSettings().stash()
        flip_options.frameRange((f, f))
        flip_options.useResolution(1)
        flip_options.resolution((500, 500))
        flip_options.output(filepath)
        scene.flipbook(scene.curViewport(), flip_options)
        self.CreateInterface()

    def incrementSave(self):

        new_suffix_format = '_0001'
        regex = re.compile('(.*?)(\d+)(\.\w+)')
        hip = hou.hipFile
        filename = hip.path()
        match = regex.match(filename)
        if match:
            filename, number, ext = match.groups()
            filename += str(int(number) + 1).rjust(len(number), '0') + ext
        else:
            filename, ext = os.path.splitext(filename)
            filename += new_suffix_format + ext

        if os.path.isfile(filename):
            overwrite = hou.ui.displayConfirmation(
                'The file "{}" already exists. Do you want to overwrite it?'
                .format(filename))
            if not overwrite:
                return


        #flipbook
        cur_desktop = hou.ui.curDesktop()
        scene = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
        hip.save(filename)

        f = hou.frame()
        fn = hou.hipFile.basename().split('.')
        del fn[-1]
        filename = '.'.join(fn)
        path = hou.hipFile.path().split('/')
        del path[-1]
        filepath = '/'.join(path) + '/_thumbnails/' + filename + '.jpg'
        
        flip_options = scene.flipbookSettings().stash()
        flip_options.frameRange((f, f))
        flip_options.useResolution(1)
        flip_options.resolution((500, 500))
        flip_options.output(filepath)
        scene.flipbook(scene.curViewport(), flip_options)

        self.CreateInterface()
        
    def setproject(self):
        setpath = hou.ui.selectFile(title='Set Project', file_type=hou.fileType.Directory)
        newpath = os.path.dirname(setpath) + '/'
        if newpath != '/':
            self.proj = newpath
            f = open(hou.homeHoudiniDirectory()+'/Proj_Path.txt', 'a+')
            f.write("\n"+newpath)
            f.close()

        #self.setproj.setText(str(newpath))
        self.Refresh()
        self.CreateInterface()

    def SubmitCachesPath(self):

        setcachepath = hou.ui.selectFile(title='Set cache path', file_type=hou.fileType.Directory)
        newcachepath = os.path.dirname(setcachepath)
        if newcachepath != '':
            f = open(self.scriptpath + '/mf_ProjV/cache_Path.txt', 'wt')
            f.write(newcachepath)
            f.close()
        
        self.Refresh()
        self.CreateInterface()
        hou.hscript( "setenv CACHES = "+newcachepath )
        self.cachesPath.setText('caches path : '+newcachepath)
        hou.ui.displayMessage("CACHES VARIABLES UPDATED")

    def SubmitImagesPath(self):

        setimagespath = hou.ui.selectFile(title='Set images path', file_type=hou.fileType.Directory)
        newimagespath = os.path.dirname(setimagespath)
        if newimagespath != '':
            f = open(self.scriptpath + '/mf_ProjV/images_Path.txt', 'wt')
            f.write(newimagespath)
            f.close()
        
        self.Refresh()
        self.CreateInterface()
        hou.hscript( "setenv IMAGES = "+newimagespath )
        self.imagesPath.setText('images path : '+newimagespath)
        hou.ui.displayMessage("IMAGES VARIABLES UPDATED")

    def SubmitElementsPath(self):

        setElementspath = hou.ui.selectFile(title='Set Elements path', file_type=hou.fileType.Directory)
        newElementspath = os.path.dirname(setElementspath)
        if newElementspath != '':
            f = open(self.scriptpath + '/mf_ProjV/images_Path.txt', 'wt')
            f.write(newElementspath)
            f.close()
        
        self.Refresh()
        self.CreateInterface()
        hou.hscript( "setenv ELMTS = "+newElementspath )
        self.ElementsPath.setText('Elements path : '+newElementspath)
        hou.ui.displayMessage("Elements VARIABLES UPDATED")

    def SubmitOutPath(self):

        setOutpath = hou.ui.selectFile(title='Set Out path', file_type=hou.fileType.Directory)
        newOutpath = os.path.dirname(setOutpath)
        if newOutpath != '':
            f = open(self.scriptpath + '/mf_ProjV/images_Path.txt', 'wt')
            f.write(newOutpath)
            f.close()
        
        self.Refresh()
        self.CreateInterface()
        hou.hscript( "setenv OUT = "+newOutpath )
        self.outPath.setText('out path : '+newOutpath)
        hou.ui.displayMessage("OUT VARIABLES UPDATED")



    def Refresh(self):
        if self.proj != self.transition and self.proj != '':
            self.folderlist.clear()

                #Open the file back and read the contents
            #f=open(hou.homeHoudiniDirectory()+'/Proj_Path.txt', "r")



            fl =np.genfromtxt(hou.homeHoudiniDirectory()+'/Proj_Path.txt', dtype=str)
            for folder in fl:
                self.folderlist.addItem(folder)

            self.transition = self.proj
        self.projpath = str(self.folderlist.currentText()) 

        
        
    def OpenHoudiniFolder(self):
    
        """
        path = self.projpath[:-1]
        path = path.replace("/","\\")
        expression = 'explorer "'+str(path)+'"'
        #print expression

        subprocess.Popen(expression)
        """
        
        hipFile  = hou.ui.selectFile(start_directory=self.projpath[:-1], title="openFile", file_type=hou.fileType.Hip, chooser_mode=hou.fileChooserMode.Read) 
     
        if os.path.isfile(hipFile) :
            hou.hipFile.load(hipFile) 
        else :
            hou.hipFile.load(hipFile+'nc')     
        
    def OpenFolder(self):
    
        
        path = self.projpath[:-1]
        path = path.replace("/","\\")
        expression = 'explorer "'+str(path)+'"'
        #print expression

        subprocess.Popen(expression)
        
 
       
    def OpenPathList(self):
        path = hou.homeHoudiniDirectory()+'/Proj_Path.txt'
        path = path.replace("/","\\")
        expression = 'explorer "'+str(path)+'"'
        #print expression

        subprocess.Popen(expression)

    def CreateInterface(self):
        self.scenelist.clear()
        """
        try:
            for file in os.listdir(self.projpath+"_thumbnails"):
                if  file.endswith('.jpg') :
                    fn = file.split('.')
                    del fn[-1]
                    name = '.'.join(fn)
                    instex0 = self.projpath+"_thumbnails/"+ file
                    jpg0 = QtGui.QPixmap(instex0).scaled(200, 200)
                    icon = QtGui.QIcon(jpg0)
                    item = QListWidgetItem(icon, '')
                    item.setText(name)
                    item.setMinimumWeight = 100
                    item.setMaximumWeight = 100
                    self.scenelist.addItem(item)
                    endfile = file
                    

            try:
                instex1 = self.projpath + endfile
                jpg1 = QtGui.QPixmap(instex1).scaled(500, 500)
                self.label.setPixmap(jpg1)
            except UnboundLocalError:
                pass

        except WindowsError:
            pass
        """
        try:
            for file in os.listdir(self.projpath):
                if  file.endswith('.hip') or file.endswith('.hipnc') or file.endswith('.hiplc'):
                    fn = file.split('.')
                    del fn[-1]
                    name = '.'.join(fn)
                    #print name
                    instex0 = self.projpath+"_thumbnails/"+name+".jpg"
                    jpg0 = QtGui.QPixmap(instex0).scaled(200, 200)
                    icon = QtGui.QIcon(jpg0)
                    item = QListWidgetItem(icon, '')
                    item.setText(name)
                    item.setMinimumWeight = 100
                    item.setMaximumWeight = 100
                    self.scenelist.addItem(item)
                    endfile = file
                    

            try:
                instex1 = self.projpath + endfile
                jpg1 = QtGui.QPixmap(instex1).scaled(500, 500)
                #self.label.setPixmap(jpg1)
            except UnboundLocalError:
                pass

        except WindowsError:
            pass

        self.scenelist.doubleClicked.connect(self.openHIP)
        self.scenelist.clicked.connect(self.viewTex)

    def viewTex(self, item):
        texname = item.data()
        instex = self.projpath + texname + '.jpg'
        jpg = QtGui.QPixmap(instex).scaled(500, 500)
        #self.label.setPixmap(jpg)

    def openHIP(self, item):
        filename = item.data()
        
        hipFile = self.projpath + filename + '.hip'
        if os.path.isfile(hipFile) :
            hou.hipFile.load(hipFile) 
        else :
            hou.hipFile.load(hipFile+'nc') 

def createInterface():    
    return MfProjectViewer()