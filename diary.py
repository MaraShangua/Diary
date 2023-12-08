import sys
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QDateEdit
from PyQt5.QtCore import QDate


class DiaryApp(QWidget):
    def __init__(self):
        super().__init__()

        # 초기화 메소드에서 UI 구성을 호출
        self.init_ui()

    def init_ui(self):
        # UI 요소 생성
        self.label_date = QLabel('날짜:')
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())  # 현재 날짜로 초기화

        self.text_edit = QTextEdit(self)

        self.save_button = QPushButton('저장', self)
        self.save_button.clicked.connect(self.save_diary)

        self.load_button = QPushButton('읽기', self)
        self.load_button.clicked.connect(self.load_diary)

        # 레이아웃 구성
        layout = QVBoxLayout()
        layout.addWidget(self.label_date)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        # 위젯에 레이아웃 설정
        self.setLayout(layout)

        # 창 설정
        self.setWindowTitle('일기장 앱')
        self.setGeometry(100, 100, 400, 400)

    def save_diary(self):
        # 사용자가 선택한 날짜 가져오기
        selected_date = self.date_edit.date().toString('yyyy-MM-dd')

        # 사용자가 작성한 일기 내용 가져오기
        diary_content = self.text_edit.toPlainText()

        # 데이터를 파일에 저장
        file_path = f"diary_{selected_date}.txt"
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(diary_content)

        # 저장 후 메시지 또는 초기화 등의 추가 로직 구현
        print(f"일기가 {file_path}에 저장되었습니다.")
        self.text_edit.clear()

        #일기 불러오기
    # def load_diary(self):
    #     selected_date = self.date_edit.date().toString('yyyy-MM-dd')

    #     file_path = f"diary_{selected_date}.txt"

    #     if os.path.exists(file_path):

    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             self.text_edit.setText(file.read())

    #     else :
    #         QMessageBox.warning(self, '경고', '저장된 일기가 없습니다.')

    def load_diary(self):
            # 파일 불러오기 다이얼로그 열기
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "일기 불러오기", "", "텍스트 파일 (*.txt);;모든 파일 (*)", options=options)

            # 사용자가 파일을 선택하고 '열기'를 누른 경우
            if file_name:
                # 파일 읽어와서 QTextEdit에 표시
                with open(file_name, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    self.text_edit.setText(file_content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    diary_app = DiaryApp()
    diary_app.show()
    sys.exit(app.exec_())
