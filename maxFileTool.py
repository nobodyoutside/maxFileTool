import MaxPlus
import pymxs
#import os
from PySide2 import QtWidgets, QtCore, QtGui

RT = pymxs.runtime
# max열기
# max파일 섬네일
# max파일 프리뷰
# fbx 익스포트
print("hellow max python")
class FileNameSet():
    ''' ui및 파일 정보를 관리할 데이터셋
    '''
    def __init__(self,file_index, path_full, path_dir, file_name, ext, num_head ="", num = "", annotation = ""):
        self.index = file_index
        self.full_path = path_full
        self.dir = path_dir
        self.name = file_name
        self.extension = ext
        self.number_head = num_head
        self.number_str = num
        self.annotation = annotation
    def Set_version_number_up(self):
        if len(self.number_str) == 0:
            self.number_str = 0
        new_number = int(self.number_str)+1
        if len(new_number) < 2:
            new_number = '0'+ str(new_number)
        self.number_str = str(new_number) 
        self.full_path = self.dir +  self.name + ", V" + self.number_head + self.number_str + '_' + self.annotation + self.extension 
    def Get_version_str(self):
        return ("V" + self.number_head + self.number_str)



class FileToolUI(QtWidgets.QDialog):
    alphabet_lower_list = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z']
    _annotation_default_str = u"주석"
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(FileToolUI, self).__init__(parent)
        RT.clearlistener()
        self.m_main_dir_path = RT.getFilenamePath(RT.maxfilepath)
        self.m_current_MaxFilePath = RT.getFilenamePath(RT.maxfilepath)
        self.m_current_maxfile_name = RT.getFilenameFile(RT.maxFileName).split(',')[0]
        self.m_current_file_set = self.GetCurrentFileNameSet()
        self.fileSet_List = []
        self.setWindowTitle(u"파일툴")
        self.initUI()

    def initUI(self):
        self.resize(QtCore.QSize(460,300))
        self.main_layout = QtWidgets.QVBoxLayout()
        # 레이아웃
        self.maxfile_list_layout = QtWidgets.QVBoxLayout()
        self.inputFileNameLayout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.maxfile_list_layout)
        self.main_layout.addLayout(self.inputFileNameLayout)
        self.main_layout.addLayout(self.button_layout)
        # ui객체
        self.dirLabel = QtWidgets.QLabel(u"[대상 경로] " + self.m_main_dir_path)
        self.filesList_tree_widget = QtWidgets.QTreeWidget()
        self.filesList_tree_widget.setHeaderLabels([u"파일이름", u"버전", u"설명"])
        head_item = self.filesList_tree_widget.headerItem()
        head_item.setSizeHint(0, QtCore.QSize(200, 25))
        head_view = self.filesList_tree_widget.header()
        head_view.resizeSection(0, 200)
        head_view.resizeSection(1, 35)
        # 입력란
        self.maxFileNameEdit = QtWidgets.QLineEdit(self.m_current_maxfile_name, self)
        self.version_label = QtWidgets.QLabel(u"Va00")
        self.fileannotationEdit = QtWidgets.QLineEdit(FileToolUI._annotation_default_str, self)
        # 버튼 생성
        self.saveMaxBtn = QtWidgets.QPushButton(u"max로 저장")
        self.savePlueMaxBtn = QtWidgets.QPushButton(u"버전업 저장")
        self.saveFbxBtn = QtWidgets.QPushButton(u"fbx로 저장")
        self.openFolder = QtWidgets.QPushButton(u"경로 열기")
        # 파일리스트 위젯추가
        self.maxfile_list_layout.addWidget(self.dirLabel)
        self.maxfile_list_layout.addWidget(self.filesList_tree_widget)
        # 파일입력 위젯추가
        self.inputFileNameLayout.addWidget(self.maxFileNameEdit)
        self.inputFileNameLayout.addWidget(self.version_label)
        self.inputFileNameLayout.addWidget(self.fileannotationEdit)
        # 버튼 위젯 추가
        self.button_layout.addWidget(self.saveMaxBtn)
        self.button_layout.addWidget(self.savePlueMaxBtn)
        self.button_layout.addWidget(self.saveFbxBtn)
        self.button_layout.addWidget(self.openFolder)
        # 연결s
        self.maxFileNameEdit.returnPressed.connect(self.ReturnNameEdit)
        self.saveMaxBtn.clicked.connect(lambda : self.SaveMaxFile(isVersionUp_bool = False))
        self.savePlueMaxBtn.clicked.connect(lambda : self.SaveMaxFile(isVersionUp_bool = True))
        self.filesList_tree_widget.doubleClicked.connect(self.LoadMaxFile)
        self.openFolder.clicked.connect(self.OpenDirCurrentFile) #clicked.connects는 인자명으로 전달, 함수 아님
        # 메인 레아아웃 추가
        self.setLayout(self.main_layout)
        self.UpdateUI()

    # UI 업데이트
    def ReturnNameEdit(self):
        self.version_label.setText("Va00")
    def UpdateUI(self):
        print(u"UpdateUI")
        self.GetFileList()
        # 열려있는 파일 정보 업데이트
        self.CurrentFileUIDataUpdate()
    def GetFileList(self, maxfiles = []):
        maxfiles = RT.GetFiles(self.m_current_MaxFilePath + "*.max")
        self.fileSet_List = []
        # 파일을 수집하여 네임셋으로 저장
        file_index = 0
        for file_full_path_str in maxfiles:
            new_file_set = self.GetNewFileNameSet(file_index, file_full_path_str)
            self.fileSet_List.append(new_file_set)
            file_index = file_index + 1
        max_index = 0
        self.filesList_tree_widget.clear() 
        for file_str in maxfiles:
            file_name = RT.filenameFromPath(file_str)
            item = QtWidgets.QTreeWidgetItem(self.filesList_tree_widget)
            item.setText(0, self.fileSet_List[max_index].name)
            item.setText(1, self.fileSet_List[max_index].number_str )
            item.setText(2, self.fileSet_List[max_index].annotation)
            max_index = max_index + 1
    def CurrentFileUIDataUpdate(self):
        self.m_current_file_set = self.GetCurrentFileNameSet()
        self.maxFileNameEdit.setText(self.m_current_file_set.name)
        self.version_label.setText(self.m_current_file_set.Get_version_str())
        self.fileannotationEdit.setText(self.m_current_file_set.annotation)
    # FileNameSet 클래스
    def GetNewFileNameSet(self,file_index, file_full_path_str):
        ''' FileNameSet 클래스 반환 '''
        file_path = RT.getFilenamePath(file_full_path_str)
        file_fullName = RT.filenameFromPath(file_full_path_str)
        temp_list = RT.getFilenameFile(file_fullName).split(',')
        file_name = temp_list[0]
        file_ext = RT.getFilenameType(file_fullName)
        number_head = ""
        number = ""
        annotation = ""
        is_Version_file = False
        if len(temp_list) > 1 :
            split1_list = temp_list[1].split('_') # ㅁㅁ, Va00
            test_str_list = split1_list[0].split()
            if test_str_list[0][0] == "V" and len(test_str_list[0]) == 4:
                if test_str_list[0][1] in FileToolUI.alphabet_lower_list:
                    is_Version_file = True
            if is_Version_file:
                number_head = test_str_list[0][1]
                number = test_str_list[0][2:4]
            else:
                annotation = temp_list[1]
            if is_Version_file and len(split1_list) > 1:
                annotation = split1_list[1]
        return FileNameSet(file_index, file_full_path_str, file_path, file_name, file_ext, number_head, number, annotation)
    def GetCurrentFileNameSet(self):
        path_full = RT.maxfilepath + RT.maxfileName
        current_file_nameSet = self.GetNewFileNameSet(-1, path_full)
        return current_file_nameSet
    # File 기능
    def SaveMaxFile(self, isVersionUp_bool = False):
        print(u'버튼 연결 test: %s \n' % str(isVersionUp_bool))
        annotation_str = self.fileannotationEdit.text()
        annotation_enable = True
        if annotation_str == FileToolUI._annotation_default_str:
            annotation_str = ""
        if annotation_str == "":
            annotation_enable = False
        if annotation_enable:
            annotation_str = "_" + annotation_str
        current_version_str = self.version_label.text()
        # 버전업 저장
        if isVersionUp_bool:
            try:
                current_version_int = int(current_version_str[2:])
            except:
                print("넘버링 변환오류")
                print(current_version_str)
                current_version_int = 0
            new_num_str = str(current_version_int+1)
            if len(new_num_str) == 1:
                new_num_str = "0" + new_num_str
            current_version_str = current_version_str[:2] + new_num_str
        save_file_name = self.m_current_MaxFilePath +  self.maxFileNameEdit.text() + ", " + current_version_str + annotation_str + self.m_current_file_set.extension
        MaxPlus.FileManager.Save(save_file_name)
        self.UpdateUI()
    def ExportFBX(self, fileName):
        pass
    def InPutFileName(self, fileNameString):
        pass
    def LoadMaxFile(self, index_QModelIndex):
        #print('맥스파일 열기')
        run_string = "loadMaxFile (\"%s\") useFileUnits:true quiet:true" % (self.fileSet_List[index_QModelIndex.row()].full_path)
        print(run_string)
        MaxPlus.Core.EvalMAXScript(run_string)
        self.CurrentFileUIDataUpdate()
    def OpenDirCurrentFile(self):
        RT.ShellLaunch(self.m_current_MaxFilePath, "")
    def MakeBackupFile(self):
        ''' 파일을 최신 버전만 남기고 백업 폴더로 보냄'''
        pass
    def OptimizingBackupFile(self):
        ''' 백업 폴더의 파일을 같은 주석은 최신버전만
        그리고 주석이 없는 파일을 삭제
        단 가장 마지막의 버전은 제외 '''
        pass
    def CleanUpBackupFile(self):
        ''' 모든 백업 파일을 제거 '''
        pass
#맥스 스크립트 창에서는 사용 못함 즉 필요없음. 
#if __name__ == "__main__":
try:
    ui.close()
except:
    pass
ui = FileToolUI()
ui.show()