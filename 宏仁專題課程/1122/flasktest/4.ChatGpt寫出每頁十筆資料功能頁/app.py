from flask import Flask, render_template, request
import db

# 產生一個Flask網站物件
app = Flask(__name__)

# 主畫面
@app.route('/')
def index():
    return render_template('index.html')

# 客戶清單
@app.route('/customer/list')
def customer_list():
    # 取得資料庫連線
    connection = db.get_connection()

    # 取得當前頁面，預設為第 1 頁
    page = request.args.get('page', 1, type=int)
    
    # 設定每頁顯示的資料筆數
    per_page = 10
    
    # 計算資料的起始索引位置
    offset = (page - 1) * per_page
    
    # 產生執行 SQL 命令的物件
    cursor = connection.cursor()

    # 取得總資料數
    cursor.execute('SELECT COUNT(*) FROM customer')
    total_count = cursor.fetchone()[0]

    # 計算總頁數
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    # 執行 SQL，取得當前頁面的資料
    cursor.execute('SELECT cusno, cusname, address, contactor FROM customer ORDER BY cusno LIMIT %s OFFSET %s', (per_page, offset))

    # 取回 SQL 執行後的所有資料
    data = cursor.fetchall()

    # 設定參數，準備傳給網頁
    if data:
        params = [{'cusno': d[0], 'cusname': d[1], 'address': d[2], 'contactor': d[3]} for d in data]
    else:
        params = None

    # 關閉資料庫連線
    connection.close()

    # 將資料傳遞給網頁
    return render_template('customer/list.html', data=params, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
