import logging
import pymxs
import os
from PySide2 import QtWidgets, QtCore, QtGui


_logger = logging.getLogger(__name__)
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
# FileToolUI_var_str = u'2022-01-15 : 파일명 변경 #18'
# FileToolUI_var_str = u'2022-10-06 : 2023버전'
FILE_TOOL_VERSION = '2025-08-05 : 2024버전'

ui = None

_logger.info("hellow max python")
class FileNameSet():
    u''' ui및 파일 정보를 관리할 데이터셋
    '''
    def __init__(
            self, file_index = 0, path_full = "", path_dir = "",
            file_name = "", ext = ".max", num_head = "a",
            num = "00", annotation = ""):
        self.index = file_index
        self.full_path = path_full # @"F:\21_3dMaxScript\_TestMaxFile\test1, Va00.max"
        self.dir = path_dir #
        self.name = file_name # name
        self.file_name = ""
        self.extension = ext
        self.number_head = num_head
        self.number_str: str = num
        self.annotation = annotation

    def set_version_number_up(self):
        """ 버전 넘버를 올려준다"""
        # _logger.info(u'debug: set_version_number_up in')
        # _logger.info(u'debug: number_str는' + self.number_str)
        if len(self.number_str) == 0:
            # _logger.info(u'debug: number_str 가 없어서 0으로 초기화')
            self.number_str = "0"
        int_converter = int(self.number_str)
        # _logger.info(u'debug: int로 변환')
        new_number = int_converter + 1
        # _logger.info(u'debug: ' + self.number_str + u' 에 + 1함')
        self.number_str = str(new_number)
        if len(self.number_str) < 2:
            self.number_str = '0'+ self.number_str
        # _logger.info(u'debug: number_str 를' + str(new_number) + u'으로 설정함')
        self.update()

    def get_version_str(self):
        """ 버전 문자열을 반환한다 """
        return("V" + self.number_head + self.number_str)

    # def change_file_name(self, change_name):
    #     self.name = change_name
    #     self.update()

    def update(self):
        """ 파일이름을 업데이트 한다 """
        underbar = "_"
        if not self.annotation:
            underbar = ""
        file_name = (
            f"{self.name}, V{self.number_head}{self.number_str}"
            f"{underbar}{self.annotation}")
        self.file_name = file_name
        self.full_path = f"{self.dir}{file_name}{self.extension}"


class FBXSetting():
    """ fbx 익스포트 설정 클래스"""
    def __init__(self):
        pass



class ChangeFileNameUI(QtWidgets.QDialog):
    """ 파일명 변경 UI """
    def __init__(self, parent = QtWidgets.QWidget.find(RT.windows.getMAXHWND())):
        super(ChangeFileNameUI, self).__init__(parent)
        #
        self._input_file_name_set = FileNameSet()
        self._set_file_name = ''
        #
        self.main_layout = QtWidgets.QVBoxLayout()
        self.input_qlineedit = QtWidgets.QLineEdit()
        self.main_layout.addWidget(self.input_qlineedit)
        self.rename_btn = QtWidgets.QPushButton('변경 실행', default = True, autoDefault = True)
        self.main_layout.addWidget(self.rename_btn)
        self.rename_btn.clicked.connect(self.rename_files)
        # _logger.info('init')
        self.setLayout(self.main_layout)
        self.setWindowTitle('이름 수정')

    def get_current_file_data(self, file_name_set):
        '''
            기본으로 설정할  파일명 이름을 주는 것
            생성후 처음에 실행해줘서 기본이름을 찾을 수 있음.
        '''
        self._input_file_name_set = file_name_set
        self.input_qlineedit.setText(file_name_set.name)

    def closeEvent(self, event):  # noqa: C0103
        '''닫을때 파일 툴을 재실행해서 변경된 내용 업데이트'''
        if event:
            ui = FileToolUI()
            ui.show()

    def rename_files(self):
        ''' 파일명 수정 '''
        # 조건체크
        input_name_set = self._input_file_name_set
        # file_name_src_text =  input_name_set.name
        input_name_set.update() # file_name 안전장치용
        file_name_src_text =  input_name_set.file_name
        file_rename_text = self.input_qlineedit.text()
        dir_path = input_name_set.dir
        _logger.info(file_name_src_text)
        _logger.info(file_rename_text)
        if file_name_src_text == file_rename_text:
            _logger.info('파일명이 같습니다.')
            return False
        # 작업폴더 파일 수집
        maxfiles = RT.GetFiles(
            dir_path + "\\" + file_name_src_text + "*.max")
        # _logger.info('renameFiles : ' + input_name_set.full_path)
        # maxfiles = RT.GetFiles(dir_path + u"\\" + input_name_set.file_name + u".max")
        # test
        for file_path in maxfiles:
            # _logger.info(file_path)
            new_path = file_path.replace(file_name_src_text, file_rename_text)
            os.rename(file_path, new_path)
        # 백업 파일 수집
        max_backup_files = RT.GetFiles(
            dir_path + "\\_bak\\" + input_name_set.name + ", V*.max")
        # 작업폴더 파일을 백업으로 보내고
        # _logger.info(u'파일명 변경')
        for file_path in max_backup_files:
            new_path = file_path.replace(file_name_src_text, file_rename_text)
            os.rename(file_path, new_path)
        self.close()


class FileToolUI(QtWidgets.QDialog):
    _version = 1.0
    alphabet_lower_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    _annotation_default_str = "주석"
    _backup_dir_name = '_bak\\'
    _isCurrentFolder_backupFolder = False
    def __init__(self, parent = QtWidgets.QWidget.find(RT.windows.getMAXHWND())):
        super(FileToolUI, self).__init__(parent)
        RT.clearlistener()
        # _logger.info("FileToolUI __init__")
        self.m_main_dir_path = RT.getFilenamePath(RT.maxfilepath)
        self.m_backup_dir_path = self.m_main_dir_path + FileToolUI._backup_dir_name
        self.m_current_MaxFilePath = RT.getFilenamePath(RT.maxfilepath)
        if self.m_current_MaxFilePath.endswith("_bak\\"):
            self._isCurrentFolder_backupFolder = True
        self.m_current_maxfile_name = RT.getFilenameFile(RT.maxFileName).split(',')[0]
        self.m_current_file_set = self.get_current_filenameset()
        self.fileSet_List = []
        self.setWindowTitle("파일툴 - " + FILE_TOOL_VERSION)
        self.init_ui()

    def init_ui(self):
        """ UI 초기화 """
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
        self.dirLabel = QtWidgets.QLabel("[대상 경로] " + self.m_main_dir_path)
        self.filesList_tree_widget = QtWidgets.QTreeWidget()
        self.filesList_tree_widget.setSortingEnabled(True)
        self.filesList_tree_widget.setExpandsOnDoubleClick(False)
        self.filesList_tree_widget.setHeaderLabels(
            ["파일이름", "버전", "설명", "풀경로"])
        head_item = self.filesList_tree_widget.headerItem()
        head_item.setSizeHint(0, QtCore.QSize(200, 25))
        head_view = self.filesList_tree_widget.header()
        self.filesList_tree_widget.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy(QtCore.Qt.CustomContextMenu))
        self.filesList_tree_widget.customContextMenuRequested.connect(
            self.file_list_menu)
        #간혹 파일명이랑 경로가 달라지는 경우가 있어서 임시 주석처리
        #head_view.setSectionHidden(3,True)
        head_view.resizeSection(0, 200)
        head_view.resizeSection(1, 35)
        # 입력란
        self.maxFileNameEdit = QtWidgets.QLineEdit(
            self.m_current_maxfile_name, self)
        self.version_label = QtWidgets.QLabel("Va00")
        self.fileannotationEdit = QtWidgets.QLineEdit(
            FileToolUI._annotation_default_str, self)
        # 버튼 생성
        self.saveMaxBtn = QtWidgets.QPushButton("max로 저장", default = False, autoDefault = False)
        self.savePlueMaxBtn = QtWidgets.QPushButton("버전업 저장", default = False, autoDefault = True)
        self.saveFbxBtn = QtWidgets.QPushButton("fbx로 저장", default = False, autoDefault = False)
        self.openFolder = QtWidgets.QPushButton("경로 열기", default = False, autoDefault = False)
        # 로그창
        self.state_bar_qlabel = QtWidgets.QLabel("대기중")
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
        self.saveMaxBtn.clicked.connect(lambda : self.save_max_file(isVersionUp_bool = False))
        self.savePlueMaxBtn.clicked.connect(lambda : self.save_max_file(isVersionUp_bool = True))
        self.filesList_tree_widget.doubleClicked.connect(self.load_max_file)
        self.openFolder.clicked.connect(self.open_dir_current_file) #clicked.connects는 인자명으로 전달, 함수 아님
        self.maxFileNameEdit.returnPressed.connect(self.return_name_edit)
        # 삭제용 우클릭 메뉴
        # QContextMenuEvent
        #
        # 메인 레이아웃 추가
        self.setLayout(self.main_layout)
        self.update_ui()

    # 메뉴 행동
    def file_list_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        menu.addAction('이 파일로 복구', self.file_restore)
        menu.addAction('파일삭제', self.file_delete)
        # menu.addAction(u'모든백업삭제', self.FileAllBackUpFileDelete)
        menu.addAction('파일명 변경', self.make_window_rename)
        menu.exec_(QtGui.QCursor.pos())

    def make_window_rename(self):
        u'''모든 파일명을 수정'''
        start_setText = self.state_bar_qlabel.setText
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText('잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_modelIndex = index_QModelIndex.sibling(
            index_QModelIndex.row(),3)
        current_file_nameSet = self.get_new_file_nameset(
            -1, target_modelIndex.data())
        # 작업 파일이 날아가는 실수를 방지하기 위해서 수정하는 파일과 현 맥스 파일이름이 같은 경우 저장을 한다.
        if self.maxFileNameEdit.text() == current_file_nameSet.name:
            RT.saveMaxFile(RT.maxFilePath, useNewFile = True)
        input_eidt_qdialog = ChangeFileNameUI()
        input_eidt_qdialog.get_current_file_data(current_file_nameSet)
        input_eidt_qdialog.show()
        self.close()
        # _logger.info(u'파일명 수정')

    def file_restore(self):
        '''해당 파일을 최신작업 파일로 복구한다'''
        start_setText = self.state_bar_qlabel.setText
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText('잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_name_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),0)
        get_current_working_file  = RT.GetFiles(
            self.m_main_dir_path + "\\" + target_name_modelIndex.data() + "*.max")
        maxfile_list = []
        file_number = 0
        for max_file in get_current_working_file:
            _logger.info (max_file)
            file_number += 1
            maxfile_list.append(self.get_new_file_nameset(file_number, max_file))
        # _logger.info(u'debug: 최대버전찾기')
        target_ver = -1
        for name_set in maxfile_list:
            _logger.info(name_set.full_path)
            this_number = int(name_set.number_str)
            if target_ver < this_number:
                target_ver = this_number
        target_fullpath_modelIndex = index_QModelIndex.sibling(
            index_QModelIndex.row(),3)
        old_full_path = target_fullpath_modelIndex.data()
        # _logger.info(u'debug: 복구될 파일 : ' +old_full_path)
        restore_nameset = self.get_new_file_nameset(-1, old_full_path)
        # 작업 경로의 파일은 복구 작업을 하지 않기 위해서
        # _logger.info(u'debug: 복구될 경로 : ' + restore_nameset.dir)
        # _logger.info(u'debug: 작업 경로 : ' + self.m_main_dir_path)
        if restore_nameset.dir == self.m_main_dir_path:
            start_setText('해당 파일은 최신 파일이라 복구 되지 않습니다.')
            return False
        restore_nameset.dir = self.m_main_dir_path
        target_nuber_modelIndex = index_QModelIndex.sibling(
            index_QModelIndex.row(),1)
        old_number = target_nuber_modelIndex.data()
        # _logger.info(u'debug: 이전 번호 : ' + old_number)
        restore_nameset.annotation = "파일 복구_" + restore_nameset.get_version_str()
        _logger.info(restore_nameset.annotation)
        restore_nameset.number_str = str(target_ver)
        restore_nameset.set_version_number_up()
        # _logger.info(u'debug: ' + old_full_path)
        # _logger.info(u'debug: ' + restore_nameset.full_path)
        if restore_nameset.name == self.maxFileNameEdit.text():
            start_setText('파일명 변경전 열린 파일을 저장...')
            self.save_max_file()
        os.rename(old_full_path, restore_nameset.full_path)
        self.update_ui()


    def file_delete(self):
        ''' 파일 삭제 '''
        start_setText = self.state_bar_qlabel.setText
        add_two_str = '{} {}'.format
        qBox = QtWidgets.QMessageBox
        # _logger.info(u'debug: 파일 삭제')
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        if not a_QItemSelectionModel.hasSelection():
            start_setText('잘못된 선택입니다.')
            return
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        target_modelIndex = index_QModelIndex.sibling(
            index_QModelIndex.row(),3)
        # 경고창
        #QtWidgets.QMessageBox.question(self, "파일삭제", "question_str")
        yes_nod_buttons = qBox.Yes
        yes_nod_buttons |= qBox.No
        delete_file_full_path_str = target_modelIndex.data()
        delete_file_name_str = RT.filenameFromPath(delete_file_full_path_str)
        question_str = f"{delete_file_name_str} 파일을 삭제 하시겠습니다."
        response_StandardButton = qBox.question(
            self, "파일삭제", question_str, yes_nod_buttons, qBox.No)
        if response_StandardButton == qBox.Yes:
            maxscript_string = 'deleteFile @"{}"'.format(
                delete_file_full_path_str)
            # MaxPlus.Core.EvalMAXScript(maxscript_string)
            RT.execute(maxscript_string)
            start_setText(f"{delete_file_name_str}을 삭제 하였습니다.")
        else:
            start_setText('삭제 취소')
        self.get_file_list()

    def file_all_backup_file_delete(self):
        """ 모든 백업 파일을 삭제 """
        a_QItemSelectionModel = self.filesList_tree_widget.selectionModel()
        index_QModelIndex = a_QItemSelectionModel.currentIndex()
        pass

    # UI 업데이트
    def return_name_edit(self):
        """ 입력 파일명 수정"""
        self.version_label.setText("Va00")
        _logger.info("debug: returnNameEdit")

    def update_ui(self):
        """ UI 업데이트 """
        _logger.info("debug: UpdateUI")
        self.move_backup_file()
        self.get_file_list()
        self.filesList_tree_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        # 열려있는 파일 정보 업데이트
        self.current_file_ui_data_update()

    def make_fileset_list(self, target_dir, target_extension = "max"):
        maxfiles = RT.GetFiles(f"{target_dir}*.{target_extension}")
        set_liset = []
        file_index = 0
        for file_full_path_str in maxfiles:
            new_file_set = self.get_new_file_nameset(file_index, file_full_path_str)
            set_liset.append(new_file_set)
            file_index = file_index + 1
        return set_liset


    def get_file_list(self, maxfiles = []):
        """ 리스트이 파일 목록을 반환 """
        maxfiles = RT.GetFiles(self.m_current_MaxFilePath + "*.max")
        self.fileSet_List = []
        self.current_dir_file_set_list = []
        self.baup_dir_file_set_liset = []
        self.unique_name_list = []
        self.unique_file_set_collection_list = []
        # 파일을 수집하여 네임셋으로 저장
        self.current_dir_file_set_list = self.make_fileset_list(
            self.m_current_MaxFilePath)
        for file_set in self.current_dir_file_set_list:
            self.unique_name_list.append(file_set.name)
        # 백업파일 정리
        ## 같은 이름 수집
        for unique_name_string in self.unique_name_list:
            unique_file_set_collection = []
            for file_set in self.current_dir_file_set_list:
                if file_set.name == unique_name_string:
                    unique_file_set_collection.append(file_set)
            self.unique_file_set_collection_list.append(
                sorted(unique_file_set_collection
                       , key=lambda file_set: file_set.number_str))
            del unique_file_set_collection
        ## 파일 이동
        #MaxPlus.Core.EvalMAXScript(u'makeDir back_dir')
        if not self._isCurrentFolder_backupFolder:
            RT.execute(f'makeDir @\"{self.m_backup_dir_path}\"')
            for file_collection in self.unique_file_set_collection_list:
                if len(file_collection) > 1:
                    for file_set in file_collection[:-1]:
                        _logger.info(file_set.full_path)
                        if file_set.number_str == "":
                            continue
                        new_full_path = (
                            f"{self.m_backup_dir_path}{file_set.name},"
                            f" V{file_set.number_head}{file_set.number_str}"
                            f"_{file_set.annotation}{file_set.extension}")
                        RT.execute(
                            f'renameFile @\"{file_set.full_path}\"'
                            f' @\"{new_full_path}\"')
        # 리스트 재정리
        ## 현제경로 파일 수집
        self.fileSet_List = self.make_fileset_list(self.m_current_MaxFilePath)
        # 백업폴더 파일 수집
        self.backup_file_set_liset = self.make_fileset_list(
            self.m_backup_dir_path)
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

    def current_file_ui_data_update(self):
        self.m_current_file_set = self.get_current_filenameset()
        self.maxFileNameEdit.setText(self.m_current_file_set.name)
        self.version_label.setText(self.m_current_file_set.get_version_str())
        self.fileannotationEdit.setText(self.m_current_file_set.annotation)

    # FileNameSet 클래스
    def get_new_file_nameset(self,file_index, file_full_path_str):
        u''' FileNameSet 클래스 반환 '''
        file_path = RT.getFilenamePath(file_full_path_str)
        file_fullName = RT.filenameFromPath(file_full_path_str)
        temp_list = RT.getFilenameFile(file_fullName).split(',')
        file_name = temp_list[0]
        ex_text = ""
        file_ext = RT.getFilenameType(file_fullName)
        number_head = "a"
        number = "00"
        annotation = ""
        is_Version_file = False
        is_version_text = False
        # 스크립트에서 , 분리로 관리되는 파일인지 확인
        if len(temp_list) > 1:
            is_Version_file = True
            ex_text = temp_list[1]
        # ,문자로 나눠진 파일이면
        if is_Version_file :
            ex_text_list = ex_text.split('_') # ㅁㅁ, Va00
            test_str_list = ex_text_list[0].split()
            # 버전문자가 있는지 확인
            if test_str_list[0][0] == "V" and len(test_str_list[0]) == 4:
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

    def get_current_filenameset(self):
        path_full = RT.maxfilepath + RT.maxfileName
        current_file_nameSet = self.get_new_file_nameset(-1, path_full)
        return current_file_nameSet

    # File 기능
    def get_max_version(self):
        ''' 맥스 2018버전으로 임시 강제 저장
        차후에 옵션으로 저장 버전을 만들어서 반환 할 것
        '''
        return 20000

    def save_max_file(self, isVersionUp_bool = False):
        ''' 유아이 정보를 기반으로 파일을 저장
        '''
        _logger.info('버튼 연결 test: %s \n', str(isVersionUp_bool))
        annotation_str = self.fileannotationEdit.text()
        annotation_enable = True
        if annotation_str == FileToolUI._annotation_default_str:
            annotation_str = ""
        if annotation_str == "":
            annotation_enable = False
        if annotation_enable:
            annotation_str = "_" + annotation_str
        current_version_str = "Va00"
        # 버전업 저장을 위해서 버전 글자 확인
        if isVersionUp_bool:
            current_version_str = self.version_label.text()
            try:
                current_version_int = int(current_version_str[2:])
            except:
                _logger.info("넘버링 변환오류")
                _logger.info(current_version_str)
                current_version_int = 0
            new_num_str = str(current_version_int+1)
            if len(new_num_str) == 1:
                new_num_str = "0" + new_num_str
            current_version_str = current_version_str[:2] + new_num_str
        # 저장
        save_file_name = (
            self.m_current_MaxFilePath +  self.maxFileNameEdit.text() +
            ", " + current_version_str + annotation_str +
            self.m_current_file_set.extension)
        RT.saveMaxFile(
            save_file_name, saveAsVersion = self.get_max_version(),
            useNewFile = True, quit = True)
        self.update_ui()

    def export_fbx(self, fileName):
        pass

    def input_filename(self, fileNameString):
        pass

    def get_select_index(self):
        _QModelIndex = self.filesList_tree_widget.selectionModel.currentIndex()

    def load_max_file(self, index_QModelIndex):
        #test_modelIndex = index_QModelIndex
        run_string = ""
        target_modelIndex = index_QModelIndex.sibling(index_QModelIndex.row(),3)
        _logger.info('맥스파일 열기 %s', str((target_modelIndex.row())) )
        _logger.info('맥스파일 열기2 %s', str(target_modelIndex.column()) )
        _logger.info('data : %s', target_modelIndex.data())
        _logger.info('item부모 %d', index_QModelIndex.parent().row() )

        #run_string = "loadMaxFile (\"%s\") useFileUnits:true quiet:true" % (self.fileSet_List[index_QModelIndex.row()].full_path)
        run_string = "loadMaxFile (@\"%s\") useFileUnits:true quiet:true" % (target_modelIndex.data())
        _logger.info(run_string)
        # MaxPlus.Core.EvalMAXScript(run_string)
        RT.execute(run_string)
        self.current_file_ui_data_update()

    def open_dir_current_file(self):
        RT.ShellLaunch(self.m_current_MaxFilePath, "")

    def move_backup_file(self):
        ''' 파일을 최신 버전만 남기고 백업 폴더로 보냄'''
        pass

    def optimizing_backup_folder(self):
        ''' 백업 폴더의 파일을 같은 주석은 최신버전만
        그리고 주석이 없는 파일을 삭제
        단 가장 마지막의 버전은 제외 '''
        pass

    def cleanup_backup_file(self):
        ''' 모든 백업 파일을 제거 '''
        delect_file_list = []
        for file_path in delect_file_list:
            maxscript_string = f"deleteFile {file_path}"
            # MaxPlus.Core.EvalMAXScript(maxscript_string)
            RT.execute(maxscript_string)
        pass

#맥스 스크립트 창에서는 사용 못함 즉 필요없음.
#if __name__ == "__main__":
try:
    ui.close()
except:
    pass
ui = FileToolUI()
ui.show()