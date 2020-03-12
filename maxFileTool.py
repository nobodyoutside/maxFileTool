import MaxPlus
import pymxs
import os
from PySide2 import QtWidgets, QtCore, QtGui

RT = pymxs.runtime
# max열기
# max파일 섬네일
# max파일 프리뷰
# fbx 익스포트
print("hellow max python")

class FileToolUI(QtWidgets.QDialog):

    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(FileToolUI, self).__init__(parent)
        self.setWindowTitle(u"파일툴")
        self.initUI()

    def initUI(self):
        mainLayout = QtWidgets.QVBoxLayout()
        maxFileListLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(maxFileListLayout)
        inputFileNameLayout =  QtWidgets.QHBoxLayout()
        mainLayout.addLayout(inputFileNameLayout)
        buttonLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(buttonLayout)

        #maxScriptsDir = MaxPlus.PathManager.GetScriptsDir()
        fileDir = MaxPlus.FileManager.GetFileNameAndPath()
        testLabel = QtWidgets.QLabel(u"대상 경로 " + fileDir)
        maxFileListLayout.addWidget(testLabel)
        filesList_QListView = QtWidgets.QListView()
        filesList_QListView.ResizeMode = QtWidgets.QListView.Adjust
        filesList_QListView.LayoutMode
        filesList_QListView.ViewMode = QtWidgets.QListView.ListMode
        maxFileListLayout.addWidget(filesList_QListView)
        fileName = u"파일 이름"
        maxFileNameEdit = QtWidgets.QLineEdit(fileName, self)
        #testEdit.setPlaceholderText("파일 이름")
        inputFileNameLayout.addWidget(maxFileNameEdit)
        fileAnnotaion = QtWidgets.QLineEdit("주석", self)
        inputFileNameLayout.addWidget(fileAnnotaion)
        saveMaxBtn = QtWidgets.QPushButton(u"max로 저장")
        buttonLayout.addWidget(saveMaxBtn)
        saveFbxBtn = QtWidgets.QPushButton(u"fbx로 저장")
        buttonLayout.addWidget(saveFbxBtn)

        self.setLayout(mainLayout)

    def GetFileList(self):
        pass

    def SaveMaxFile(self, fileName, annotaion):
        pass

    def ExportFBX(self, fileName):
        pass

    def InPutFileName(self, fileNameString):
        pass
#맥스 스크립트 창에서는 사용 못함 즉 필요없음. 
#if __name__ == "__main__":
try:
    ui.close()
except:
    pass
ui = FileToolUI()
ui.show()