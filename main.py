import sys
from calendar import timegm
from datetime import timedelta, datetime, timezone


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QListWidgetItem, QMessageBox

from license_create import create_license_file


class MainWin(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("license.ui")
        self.ui.setFixedSize(720, 466)
        self.init_ui()
        self.ui.show()

    def init_ui(self):
        self.ui.pushButton.clicked.connect(self.generate_license)

        # 读取本地模块列表文件 license_aud_list.txt 初始化界面可选模块列表
        # https://blog.csdn.net/sinat_34149445/article/details/94548871

        with open('license_aud_list.txt', 'r') as f:
            data_list = f.read().split(',')

        for i in data_list:
            box = QCheckBox(i)  # 实例化一个QCheckBox，吧文字传进去
            item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
            self.ui.listWidget.addItem(item)  # 把QListWidgetItem加入QListWidget
            self.ui.listWidget.setItemWidget(item, box)  # 再把QCheckBox加入QListWidgetItem

    def get_module_list(self) -> [str]:
        """
        得到授权模块列表
        :return: list[str]
        """
        count = self.ui.listWidget.count()  # 得到QListWidget的总个数
        cb_list = [self.ui.listWidget.itemWidget(self.ui.listWidget.item(i))
                   for i in range(count)]  # 得到QListWidget里面所有QListWidgetItem中的QCheckBox
        # print(cb_list)
        module_list = []  # 存放被选择的数据
        for cb in cb_list:  # type:QCheckBox
            if cb.isChecked():
                module_list.append(cb.text())
        # print(module_list)
        return module_list

    def generate_license(self):
        # print(self.ui.lineEdit_not_befor_in_days.text())
        # print(self.ui.lineEdit_expire_in_days.text())
        # print(self.ui.lineEdit_usr.text())
        # print(self.ui.lineEdit_mac.text())
        # print(self.get_module_list())
        # print('btn clicked')

        module_list = self.get_module_list()

        if len(module_list) == 0:
            # print('list count == 0')

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("至少选择一个模块授权")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("错误")
            # msg.setDetailedText("The details are as follows:")
            msg.exec_()
            return

        now = timegm(datetime.now(tz=timezone.utc).utctimetuple())

        nbf = now + timedelta(days=int(self.ui.lineEdit_not_befor_in_days.text())).total_seconds()
        exp = now + timedelta(days=int(self.ui.lineEdit_expire_in_days.text())).total_seconds()

        payload = {
            "iss": "智眸医疗",
            "aud": module_list,
            "nbf": nbf,
            "exp": exp,
            "usr": self.ui.lineEdit_usr.text(),
            "mac": self.ui.lineEdit_mac.text(),
        }

        # print(payload)

        create_license_file(payload)


if __name__ == '__main__':
    # 每一 pyqt5 应用程序必须创建一个应用程序对象。sys.argv 参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)

    # 我们创建一个基于 QWidget 的部件（该部件类似对话框）。。
    w = MainWin()

    # 显示 QWidget 部件
    # w.show()

    '''
    app.exec_() 里面是一个死循环，也叫作消息循环，任何界面程序都使用的一种技术
    在该消息循环里，QWidget 部件就可以接受和处理消息了（比如最大化窗口，拖动窗口等等）
    '''
    app.exec_()
