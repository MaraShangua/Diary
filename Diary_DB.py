import sys, mysql.connector
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QDateEdit, QInputDialog
from PyQt5.QtCore import QDate
from mysql.connector import Error

try:
    # MySQL 연결 설정
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="0000",
        database="diary"
    )

    # 커서 생성
    cursor = connection.cursor()

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

            # 기존에 있던 데이터인지 확인
            if connection.is_connected():
                cursor = connection.cursor()

                # 확인할 데이터
                table_name = "entries"
                condition_column = "date"
                condition_value = selected_date

                # SELECT 쿼리 실행
                select_query = f"SELECT * FROM {table_name} WHERE {condition_column} = '{condition_value}'"
                cursor.execute(select_query)

                # 결과 가져오기
                result = cursor.fetchall()

                if len(result) > 0:
                    table_name = "entries"
                    condition_column = "date"
                    condition_value = selected_date

                    # DELETE 쿼리 실행
                    delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = '{condition_value}'"
                    cursor.execute(delete_query)
                    connection.commit()

                # 데이터를 데이터베이스에 저장
                insert_query = "INSERT INTO entries (date, content) VALUES (%s, %s)"
                cursor.execute(insert_query, (selected_date, diary_content))

                # 변경 사항을 커밋
                connection.commit()

                # 저장 후 초기화 로직 구현
                self.text_edit.clear()

            #일기 불러오기(날짜 입력해서 불러오기)
        def load_diary(self):
            text, ok_pressed = QInputDialog.getText(self, 'Input Dialog', '날짜 입력')

            if ok_pressed:
                query = "SELECT content FROM entries WHERE date = %s"
                cursor.execute(query, (text,))
                result_content = cursor.fetchall()

                content_str = "\n".join(str(row[0]) for row in result_content)

                self.text_edit.setText(content_str)
            

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        diary_app = DiaryApp()
        diary_app.show()
        sys.exit(app.exec_())

except Error as e:
    print(f"에러: {e}")

finally:
    # 연결 종료
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("연결이 닫혔습니다.")