#-----------------------
# 匯入flask及db模組
#-----------------------
from flask import Flask, render_template, request
import db

#-----------------------
# 產生一個Flask網站物件
#-----------------------
app = Flask(__name__)

#-----------------------
# 在網站中定義路由
#-----------------------
# 主畫面
@app.route('/')
def index():
    return render_template('index.html') 

# 客戶清單
@app.route('/customer/list')
def customer_list(): 
    # 取得資料庫連線
    connection = db.get_connection() 
    
    # 產生執行sql命令的物件
    cursor = connection.cursor() 
    
    # 執行SQL
    cursor.execute('SELECT cusno, cusname, address, contactor FROM customer order by cusno;')
    
    # 取回SQL執行後的所有資料
    data = cursor.fetchall()
    
    # 設定參數, 準備傳給網頁
    if data:
        params = [{'cusno': d[0], 'cusname': d[1], 'address': d[2], 'contactor': d[3]} for d in data]
    else:
        params = None
    # 關閉資料庫連線
    connection.close() 
    
    # 將參數送給網頁
    return render_template('/customer/list.html', data=params)

# 產品清單
@app.route('/product/list')
def product_list(): 
    # 取得資料庫連線
    connection = db.get_connection() 
    
    # 取得當前頁面，預設為第 1 頁
    page = request.args.get('page', 1, type=int)
    
    # 每頁顯示 10 筆資料
    per_page = 10
    
    # 計算資料的起始索引位置
    offset = (page - 1) * per_page
    
    # 產生執行sql命令的物件
    cursor = connection.cursor() 
    
    # 取得總資料數
    cursor.execute('SELECT COUNT(*) FROM product')
    total_count = cursor.fetchone()[0]
    
    # 計算總頁數
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)
    
    # 執行SQL，取得當前頁面的資料
    cursor.execute('SELECT prono, proname, price, stockAmt FROM product ORDER BY prono LIMIT %s OFFSET %s', (per_page, offset))
    
    # 取回SQL執行後的所有資料
    data = cursor.fetchall()
    
    # 設定參數，準備傳給網頁
    if data:
        params = [{'prono': d[0], 'proname': d[1], 'price': d[2], 'stockAmt': d[3]} for d in data]
    else:
        params = None
          
    # 關閉資料庫連線
    connection.close() 
    
    # 將參數送給網頁，並傳遞分頁資訊
    return render_template('/product/list.html', data=params, page=page, total_pages=total_pages)

#客戶查詢表單
@app.route('/customer/read/form')
def customer_read_form():
    return render_template('customer/read_form.html') 

#客戶查詢
@app.route('/customer/read', methods=['GET'])
def customer_read():    
    #取得資料庫連線    
    connection = db.get_connection()  
    
    #取得執行sql命令的cursor
    cursor = connection.cursor()   
    
    #取得傳入參數
    cusno = request.values.get('cusno').strip()
    
    #執行sql命令並取回資料    
    cursor.execute('SELECT * FROM customer WHERE cusno=%s', (cusno,))
    data = cursor.fetchone()

    if data:
        params = {'cusno':data[0], 'cusname':data[1], 'address':data[4], 'tel':data[8]}
    else:
        params = None
        
    #關閉連線   
    connection.close()  
        
    #回傳網頁
    return render_template('/customer/read.html', data=params)

#-----------------------
# 啟動Flask網站
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)
