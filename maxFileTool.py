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
        
        #maxScriptsDir = MaxPlus.PathManager.GetScriptsDir()
        fileDir = MaxPlus.FileManager.GetFileNameAndPath()
        testLabel = QtWidgets.QLabel(u"대상 경로 " + fileDir)
        mainLayout.addWidget(testLabel)
        fileName = u"파일 이름"
        testEdit = QtWidgets.QLineEdit(fileName, self)
        #testEdit.setPlaceholderText("파일 이름")
        mainLayout.addWidget(testEdit)
        testBtn = QtWidgets.QPushButton(u"저장")
        mainLayout.addWidget(testBtn)
        self.setLayout(mainLayout)


#if __name__ == "__main__":
try:
    ui.close()
except:
    pass
ui = FileToolUI()
ui.show()