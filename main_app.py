import streamlit as st
import pymysql
from datetime import datetime


username = st.secrets.db_username
pwd = st.secrets.db_pwd
dbname = st.secrets.db_name

# MySQL 연결 설정
def create_connection():
    connection = pymysql.connect(
        host='www.richgm.site',
        user=username,
        password=pwd,
        db=dbname,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# 데이터베이스에 데이터 삽입
def insert_data(data):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # 데이터베이스에 삽입할 쿼리 작성
            query = "INSERT INTO 법인카드사용내역 (사용일시, 가맹점, 사용금액) VALUES (%s, %s, %s)"
            # 데이터베이스에 데이터 삽입
            cursor.execute(query, (data['date_field'], data['store_field'], data['number_field']))
        # 변경사항을 커밋
        connection.commit()
        st.success('데이터가 성공적으로 저장되었습니다.')
    except Exception as e:
        st.error(f'데이터 저장 중 오류 발생: {str(e)}')
    finally:
        connection.close()

# Streamlit 애플리케이션 설정
def main():
    st.title('카드사용내역 저장하기')

    # 날짜 입력
    date_field = st.date_input('사용일', datetime.today(),  format='YYYY-MM-DD')
    
    # 가맹점 입력
    store_field = st.text_input('가맹점', '', placeholder='사용 가맹점(점포)를 입력하세요')

    # 숫자 입력
    number_field = st.number_input('사용금액', min_value=0)

    # 버튼 입력
    button_field = st.button('저장')

    if button_field:
        data = {
            'date_field': date_field,
            'number_field': number_field,
            'store_field': store_field  
        }
        insert_data(data)
       

# 애플리케이션 실행
if __name__ == '__main__':
    main()
