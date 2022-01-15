import MaxPlus
import pymxs # pylint: disable=import-error
import os
from PySide2 import QtWidgets, QtCore, QtGui

RT = pymxs.runtime
# max열기
# max파일 섬네일
# max파일 프리뷰
# fbx 익스포트
# 
# FileToolUI_var_str = u'20210316_백업기능추가'
# FileToolUI_var_str = u'20210317_파일삭제 확인창'
# FileToolUI_var_str = u'20210317_2선택예외처리'
# 2021-07-30 16:34:25 LoadMaxFile 버그
# FileToolUI_var_str = u'2021-07-30'
FileToolUI_var_str = u'2022-01-15 : 파일명 변경 #18'
print(u"hellow max python")
class FileNameSet():
    u''' ui및 파일 정보를 관리할 데이터셋
    '''
    def __init__(self,file_index = 0, path_full = u"", path_dir = u"", file_name = u"", ext = u".max", num_head = u"a", num = u"00", annotation = u""):
        self.index = file_index
        self.full_path = path_full # @"F:\21_3dMaxScript\_TestMaxFile\test1, Va00.max"
        self.dir = path_dir # 
        self.name = file_name # name
        self.file_name = u""
        self.extension = ext
        self.number_head = num_head
        self.number_str = num
        self.annotation = annotation
    def Set_version_number_up(self):
        # print(u'debug: Set_version_number_up in')
        # print(u'debug: number_str는' + self.number_str)
        if len(self.number_str) == 0:
            # print(u'debug: number_str 가 없어서 0으로 초기화')
            self.number_str = 0
        int_converter = int(self.number_str)
        # print(u'debug: int로 변환')
        new_number = int_converter + 1
        # print(u'debug: ' + self.number_str + u' 에 + 1함')
        self.number_str = str(new_number)
        if len(self.number_str) < 2:
            self.number_str = u'0'+ self.number_str
        # print(u'debug: number_str 를' + str(new_number) + u'으로 설정함')
        self.update()
    def Get_version_str(self):
        return (u"V" + self.number_head + self.number_str)
    # def change_file_name(self, change_name):
    #     self.name = change_name
    #     self.update()
    def update(self):
        underbar = "_"
        if not self.annotation:
            underbar = u""
        file_name = u"{}, V{}{}{}{}".format(self.name, self.number_head, self.number_str, underbar, self.annotation)
        self.file_name = file_name
        self.full_path = u"{}{}{}".format(self.dir, file_name, self.extension)
class FBXSetting():
    pass
class ChangeFileNameUI(QtWidgets.QDialog):
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(ChangeFileNameUI, self).__init__(parent)
        #
        self._input_file_nameSet = FileNameSet()
        self._set_file_name = u''
        #
        self.main_layout = QtWidgets.QVBoxLayout()
        self.input_qlineedit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.input_qlineedit)
        self.rename_btn = QtWidgets.QPushButton(u'변경 실행', default = True, autoDefault = True)
        self.main_layout.addWidget(self.rename_btn)
        self.rename_btn.clicked.connect(self.renameFiles)
        # print('init')
        self.setLayout(self.main_layout)
        self.setWindowTitle(u'이름 수정')
    def getCurrentFileData(self, file_name_set):
        '''
            기본으로 설정할  파일명 이름을 주는 것
            생성후 처음에 실행해줘서 기본이름을 찾을 수 있음.
        '''
        self._input_file_nameSet = file_name_set
        self.input_qlineedit.setText(file_name_set.name)
    def closeEvent(self, event):
        u'''닫을때 파일 툴을 재실행해서 변경된 내용 업데이트'''
        if event:
            ui = FileToolUI()
            ui.show()
    def renameFiles(self):
        u''' 파일명 수정 '''
        # 조건체크
        input_name_set = self._input_file_nameSet
        # file_name_src_text =  input_name_set.name
        input_name_set.update() # file_name 안전장치용
        file_name_src_text =  input_name_set.file_name
        file_rename_text = self.input_qlineedit.text()
        dir_path = input_name_set.dir
        print(file_name_src_text)
        print(file_rename_text) 
        if file_name_src_text == file_rename_text:
            print('파일명이 같습니다.')
            return False
        # 작업폴더 파일 수집
        maxfiles = RT.GetFiles(dir_path + u"\\" + file_name_src_text + u"*.max")
        # print('renameFiles : ' + input_name_set.full_path)
        # maxfiles = RT.GetFiles(dir_path + u"\\" + input_name_set.file_name + u".max")
        # test
        for file_path in maxfiles:
            # print(file_path)
            new_path = file_path.replace(file_name_src_text, file_rename_text )
            os.rename(file_path, new_path)
        # 백업 파일 수집
        max_backup_files = RT.GetFiles(dir_path + u"\\_bak\\" + input_name_set.name + u", V*.max")
        # 작업폴더 파일을 백업으로 보내고
        # print(u'파일명 변경')
        for file_path in max_backup_files:
            new_path = file_path.replace(file_name_src_text, file_rename_text )
            os.rename(file_path, new_path)
        # global ui
        # ui = FileToolUI()
        # ui.show()
        self.close()
class FileToolUI(QtWidgets.QDialog):
    _version = 1.0
    alphabet_lower_list = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z']
    _annotation_default_str = u"주석"
    _backup_dir_name = u'_bak\\'
    _isCurrentFolder_backupFolder = False
    def __init__(self, parent=MaxPlus.GetQMaxMainWindow()):
        super(FileToolUI, self).__init__(parent)
        RT.clearlistener()
        # print("FileToolUI __init__")
        self.m_main_dir_path = RT.getFilenamePath(RT.maxfilepath)
        self.m_backup_dir_path = self.m_main_dir_path + FileToolUI._backup_dir_name
        self.m_current_MaxFilePath = RT.getFilenamePath(RT.maxfilepath)
        if self.m_current_MaxFilePath.endswith("_bak\\"):
            self._isCurrentFolder_backupFolder = True
        self.m_current_maxfile_name = RT.getFilenameFile(RT.maxFileName).split(',')[0]
        self.m_current_file_set = self.GetCurrentFileNameSet()
        self.fileSet_List = []
        self.setWindowTitle(u"파일툴 - " + FileToolUI_var_str)
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
        self.filesList_tree_widget.setSortingEnabled(True)
        self.filesList_tree_widget.setExpandsOnDoubleClick(False)
        self.filesList_tree_widget.setHeaderLabels([u"파일이름", u"버전", u"설명", u"풀경로"])
        head_item = self.filesList_tree_widget.headerItem()
        head_item.setSizeHint(0, QtCore.QSize(200, 25))
        head_view = self.filesList_tree_widget.header()
        self.filesList_tree_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy(QtCore.Qt.CustomContextMenu))
        self.filesList_tree_widget.customContextMenuRequested.connect(self.FileListMenu)
        #간혹 파일명이랑 경로가 달라지는 경우가 있어서 임시 주석처리
        #head_view.setSectionHidden(3,True)
        head_view.resizeSection(0, 200)
        head_view.resizeSection(1, 35)
        # 입력란
        self.maxFileNameEdit = QtWidgets.QLineEdit(self.m_current_maxfile_name, self)
        self.version_label = QtWidgets.QLabel(u"Va00")
        self.fileannotationEdit = QtWidgets.QLineEdit(FileToolUI._annotation_default_str, self)
        # 버튼 생성
        self.saveMaxBtn = QtWidgets.QPushButton(u"max로 저장", default = False, autoDefault = False)
        self.savePlueMaxBtn = QtWidgets.QPushButton(u"버전업 저장", default = False, autoDefault = True)
        self.saveFbxBtn = QtWidgets.QPushButton(u"fbx로 저장", default = False, autoDefault = False)
        self.openFolder = QtWidgets.QPushButton(u"경로 열기", default = False, autoDefault = False)
        # 로그창
        self.state_bar_qlabel = QtWidgets.QLabel(u"대기중")
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
        # 정보창
        self.main_layout.addWidget(self.state_bar_qlabel)
        # 연결
        self.saveMaxBtn.clicked.connect(lambda : self.SaveMaxFile(isVersionUp_bool = False))
        self.savePlueMaxBtn.clicked.connect(lambda : self.SaveMaxFile(isVersionUp_bool = True))
        self.filesList_tree_widget.doubleClicked.connect(self.LoadMaxFile)
        self.openFolder.clicked.connect(self.OpenDirCurrentFile) #clicked.connects는 인자명으로 전달, 함수 아님
        self.maxFileNameEdit.returnPressed.connect(self.ReturnNameEdit)
        # 삭제용 우클릭 메뉴
        # QContextMenuEvent
        #
        # 메인 레아아웃 추가
        self.setLayout(self.main_layout)
        self.UpdateUI()
        
    # 메뉴 행동
    def FileListMenu(self, pos):
        menu = QtWidgets.QMenu(self)
        menu.addAction(u'이 파일로 복구', self.FileRestore)
        menu.addAction(u'파일삭제', self.FileDelete)
        # menu.addAction(u'모든백업삭제', self.FileAllBackUpFileDelete)
        menu.addAction(u'파일명 변경', self.MakeWindowReName)
        menu.exec_(QtGui.QCursor.pos())
    def MakeWindowReName(self):
        u'''모든 파일명을 수정'''
        start_setText = self.state_bar_qlabel.setText
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText(u'잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),3)
        current_file_nameSet = self.GetNewFileNameSet(-1, target_modelIndex.data())
        # 작업 파일이 날아가는 실수를 방지하기 위해서 수정하는 파일과 현 맥스 파일이름이 같은 경우 저장을 한다.
        if self.maxFileNameEdit.text() == current_file_nameSet.name:
            MaxPlus.FileManager.Save()
        input_eidt_qdialog = ChangeFileNameUI()
        input_eidt_qdialog.getCurrentFileData(current_file_nameSet)
        input_eidt_qdialog.show()
        self.close()
        # print(u'파일명 수정')

    def FileRestore(self):
        u'''해당 파일을 최신작업 파일로 복구한다'''
        start_setText = self.state_bar_qlabel.setText
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText(u'잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_name_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),0)
        get_current_working_file  = RT.GetFiles(self.m_main_dir_path + u"\\" + target_name_modelIndex.data() + u"*.max")
        maxfile_list = []
        file_number = 0
        for max_file in get_current_working_file:
            print (max_file)
            file_number += 1
            maxfile_list.append(self.GetNewFileNameSet(file_number, max_file))
        # print(u'debug: 최대버전찾기')
        target_ver = -1
        for name_set in maxfile_list:
            print(name_set.full_path)
            this_number = int(name_set.number_str)
            if target_ver < this_number:
                target_ver = this_number
        target_fullpath_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),3)
        old_full_path = target_fullpath_modelIndex.data()
        # print(u'debug: 복구될 파일 : ' +old_full_path)
        restore_nameset = self.GetNewFileNameSet(-1, old_full_path)
        # 작업 경로의 파일은 복구 작업을 하지 않기 위해서
        # print(u'debug: 복구될 경로 : ' + restore_nameset.dir)
        # print(u'debug: 작업 경로 : ' + self.m_main_dir_path)
        if restore_nameset.dir == self.m_main_dir_path:
            start_setText(u'해당 파일은 최신 파일이라 복구 되지 않습니다.')
            return False
        restore_nameset.dir = self.m_main_dir_path
        target_nuber_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),1)
        old_number = target_nuber_modelIndex.data()
        # print(u'debug: 이전 번호 : ' + old_number)
        restore_nameset.annotation = u"파일 복구_" + restore_nameset.Get_version_str()
        print(restore_nameset.annotation)
        restore_nameset.number_str = str(target_ver)
        restore_nameset.Set_version_number_up()
        # print(u'debug: ' + old_full_path)
        # print(u'debug: ' + restore_nameset.full_path)
        if restore_nameset.name == self.maxFileNameEdit.text():
            start_setText(u'파일명 변경전 열린 파일을 저장...')
            self.SaveMaxFile()
        os.rename(old_full_path, restore_nameset.full_path)
        self.UpdateUI()
    def FileDelete(self):
        u''' 파일 삭제 '''
        start_setText = self.state_bar_qlabel.setText
        add_two_str = u'{} {}'.format
        qBox = QtWidgets.QMessageBox
        # print(u'debug: 파일 삭제')
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText(u'잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),3)
        # 경고창
        #QtWidgets.QMessageBox.question(self, "파일삭제", "question_str")
        yes_nod_buttons = qBox.Yes
        yes_nod_buttons |= qBox.No
        delete_file_full_path_str = target_modelIndex.data()
        delete_file_name_str = RT.filenameFromPath(delete_file_full_path_str)
        question_str = add_two_str(delete_file_name_str, u" 파일을 삭제 하시겠습니다.")
        response_StandardButton = qBox.question(self, u"파일삭제", question_str, yes_nod_buttons, qBox.No)
        if response_StandardButton == qBox.Yes:
            maxscript_string = u'deleteFile @"{}"'.format(delete_file_full_path_str)
            MaxPlus.Core.EvalMAXScript(maxscript_string)
            start_setText(add_two_str(delete_file_name_str, u'을 삭제 하였습니다.'))
        else:
            start_setText(u'삭제 취소')
        self.GetFileList()
    def FileAllBackUpFileDelete(self):
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        pass
    # UI 업데이트
    def ReturnNameEdit(self):
        self.version_label.setText(u"Va00")
        print(u"debug: returnNameEdit")
    def UpdateUI(self):
        print(u"debug: UpdateUI")
        self.MoveBackupFile()
        self.GetFileList()
        self.filesList_tree_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        # 열려있는 파일 정보 업데이트
        self.CurrentFileUIDataUpdate()
    def MakeFileSetList(self, target_dir, target_extension = u"max"):
        maxfiles = RT.GetFiles(target_dir + u"*.{}".format(target_extension))
        set_liset = []
        file_index = 0
        for file_full_path_str in maxfiles:
            new_file_set = self.GetNewFileNameSet(file_index, file_full_path_str)
            set_liset.append(new_file_set)
            file_index = file_index + 1
        return set_liset
    def GetFileList(self, maxfiles = []):
        maxfiles = RT.GetFiles(self.m_current_MaxFilePath + u"*.max")
        self.fileSet_List = []
        self.current_dir_file_set_list = []
        self.baup_dir_file_set_liset = []
        self.unique_name_list = []
        self.unique_file_set_collection_list = []
        # 파일을 수집하여 네임셋으로 저장
        self.current_dir_file_set_list = self.MakeFileSetList(self.m_current_MaxFilePath)
        for file_set in self.current_dir_file_set_list:
            self.unique_name_list.append(file_set.name)
        # 백업파일 정리
        ## 같은 이름 수집
        for unique_name_string in self.unique_name_list:
            unique_file_set_collection = []
            for file_set in self.current_dir_file_set_list:
                if file_set.name == unique_name_string:
                    unique_file_set_collection.append(file_set)
            self.unique_file_set_collection_list.append(sorted(unique_file_set_collection, key=lambda file_set: file_set.number_str))
            del unique_file_set_collection
        ## 파일 이동
        #MaxPlus.Core.EvalMAXScript(u'makeDir back_dir')
        if not self._isCurrentFolder_backupFolder:
            RT.execute(u'makeDir @\"{}\"'.format(self.m_backup_dir_path))
            for file_collection in self.unique_file_set_collection_list:
                if len(file_collection) > 1:
                    for file_set in file_collection[:-1]:
                        print(file_set.full_path)
                        if file_set.number_str == u"":
                            continue
                        new_full_path = u"{0}{1}, V{2}{3}_{4}{5}".format(self.m_backup_dir_path, file_set.name, file_set.number_head, file_set.number_str, file_set.annotation, file_set.extension)
                        #new_full_path = self.m_backup_dir_path +  file_set.name + ", V" + file_set.number_head + file_set.number_str + '_' + file_set.annotation + file_set.extension 
                        RT.execute(u'renameFile @\"{0}\" @\"{1}\"'.format(file_set.full_path, new_full_path ))
        # 리스트 재정리
        ## 현제경로 파일 수집
        self.fileSet_List = self.MakeFileSetList(self.m_current_MaxFilePath)
        # 백업폴더 파일 수집
        self.backup_file_set_liset = self.MakeFileSetList(self.m_backup_dir_path)
        # UI리스트 업데이트
        max_index = 0
        self.filesList_tree_widget.clear() 
        for file_set in self.fileSet_List:
            item = QtWidgets.QTreeWidgetItem(self.filesList_tree_widget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            item.setText(0, file_set.name)
            item.setText(1, file_set.number_str )
            item.setText(2, file_set.annotation)
            item.setText(3, file_set.full_path)
            for backup_file_set in self.backup_file_set_liset:
                if backup_file_set.name == file_set.name:
                    sub_item = QtWidgets.QTreeWidgetItem(item)
                    sub_item.setFlags(sub_item.flags() | QtCore.Qt.ItemIsEditable)
                    sub_item.setTextColor(0,QtGui.QColor(44, 44, 44))
                    sub_item.setText(0, backup_file_set.name)
                    sub_item.setText(1, backup_file_set.number_str )
                    sub_item.setText(2, backup_file_set.annotation)
                    sub_item.setText(3, backup_file_set.full_path)
        #메모리 정리
        del self.backup_file_set_liset
        del self.unique_file_set_collection_list
    def CurrentFileUIDataUpdate(self):
        self.m_current_file_set = self.GetCurrentFileNameSet()
        self.maxFileNameEdit.setText(self.m_current_file_set.name)
        self.version_label.setText(self.m_current_file_set.Get_version_str())
        self.fileannotationEdit.setText(self.m_current_file_set.annotation)
    # FileNameSet 클래스
    def GetNewFileNameSet(self,file_index, file_full_path_str):
        u''' FileNameSet 클래스 반환 '''
        file_path = RT.getFilenamePath(file_full_path_str)
        file_fullName = RT.filenameFromPath(file_full_path_str)
        temp_list = RT.getFilenameFile(file_fullName).split(',')
        file_name = temp_list[0]
        ex_text = u""
        file_ext = RT.getFilenameType(file_fullName)
        number_head = u"a"
        number = u"00"
        annotation = u""
        is_Version_file = False
        is_version_text = False
        # 스크립트에서 , 분리로 관리되는 파일인지 확인
        if len(temp_list) > 1:
            is_Version_file = True
            ex_text = temp_list[1]
        # ,문자로 나눠진 파일이면
        if is_Version_file :
            ex_text_list = ex_text.split(u'_') # ㅁㅁ, Va00 
            test_str_list = ex_text_list[0].split()
            # 버전문자가 있는지 확인
            if test_str_list[0][0] == u"V" and len(test_str_list[0]) == 4:
                # 문자열 구조가 맞는지 확인
                if test_str_list[0][1] in FileToolUI.alphabet_lower_list:
                    is_version_text = True
            # 버전문자가 맞으면 해당 문자를 업데이트 하고 아니면 해당문자열을 통으로 주석 처리
            if is_version_text:
                number_head = test_str_list[0][1]
                number = test_str_list[0][2:4]
                if len(ex_text_list) > 1:
                    annotation = ex_text[6:]
            else:
                annotation = ex_text

        return FileNameSet(file_index, file_full_path_str, file_path, file_name, file_ext, number_head, number, annotation)
    def GetCurrentFileNameSet(self):
        path_full = RT.maxfilepath + RT.maxfileName
        current_file_nameSet = self.GetNewFileNameSet(-1, path_full)
        return current_file_nameSet
    # File 기능
    def GetMaxVersion(self):
        u''' 맥스 2018버전으로 임시 강제 저장
        차후에 옵션으로 저장 버전을 만들어서 반환 할 것
        '''
        return 20000
    def SaveMaxFile(self, isVersionUp_bool = False):
        u''' 유아이 정보를 기반으로 파일을 저장
        '''
        print(u'버튼 연결 test: %s \n' % str(isVersionUp_bool))
        annotation_str = self.fileannotationEdit.text()
        annotation_enable = True
        if annotation_str == FileToolUI._annotation_default_str:
            annotation_str = u""
        if annotation_str == u"":
            annotation_enable = False
        if annotation_enable:
            annotation_str = u"_" + annotation_str
        current_version_str = u"Va00"
        # 버전업 저장을 위해서 버전 글자 확인
        if isVersionUp_bool:
            current_version_str = self.version_label.text()
            try:
                current_version_int = int(current_version_str[2:])
            except:
                print(u"넘버링 변환오류")
                print(current_version_str)
                current_version_int = 0
            new_num_str = str(current_version_int+1)
            if len(new_num_str) == 1:
                new_num_str = u"0" + new_num_str
            current_version_str = current_version_str[:2] + new_num_str
        # 저장
        save_file_name = self.m_current_MaxFilePath +  self.maxFileNameEdit.text() + u", " + current_version_str + annotation_str + self.m_current_file_set.extension
        #MaxPlus.FileManager.Save(save_file_name)
        MaxPlus.FileManager.SaveSceneAsVersion(save_file_name, True, True, self.GetMaxVersion())
        self.UpdateUI()
    def ExportFBX(self, fileName):
        pass
    def InPutFileName(self, fileNameString):
        pass
    def GetSelectIndex(self):
        _QModelIndex = self.filesList_tree_widget.selectionModel.currentIndex()

    def LoadMaxFile(self, index_QModelIndex):
        #test_modelIndex = index_QModelIndex
        run_string = ""
        target_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),3)
        print(u'맥스파일 열기 %s' % str((target_modelIndex.row())) )
        print(u'맥스파일 열기2 %s' % str(target_modelIndex.column()) )
        print(u'data : {}'.format(target_modelIndex.data()))
        print(u'item부모 %d' % index_QModelIndex.parent().row() )

        #run_string = "loadMaxFile (\"%s\") useFileUnits:true quiet:true" % (self.fileSet_List[index_QModelIndex.row()].full_path)
        run_string = u"loadMaxFile (@\"%s\") useFileUnits:true quiet:true" % (target_modelIndex.data())
        print(run_string)
        MaxPlus.Core.EvalMAXScript(run_string)
        self.CurrentFileUIDataUpdate()
    def OpenDirCurrentFile(self):
        RT.ShellLaunch(self.m_current_MaxFilePath, "")
    def MoveBackupFile(self):
        u''' 파일을 최신 버전만 남기고 백업 폴더로 보냄'''
        pass
    def OptimizingBackupFolder(self):
        u''' 백업 폴더의 파일을 같은 주석은 최신버전만
        그리고 주석이 없는 파일을 삭제
        단 가장 마지막의 버전은 제외 '''
        pass
    def CleanUpBackupFile(self):
        u''' 모든 백업 파일을 제거 '''
        delect_file_list = []
        for file_path in delect_file_list:
            maxscript_string = u"deleteFile {}".format(file_path)
            MaxPlus.Core.EvalMAXScript(maxscript_string)
        pass
#맥스 스크립트 창에서는 사용 못함 즉 필요없음. 
#if __name__ == "__main__":
try:
    ui.close()
except:
    pass
ui = FileToolUI()
ui.show()