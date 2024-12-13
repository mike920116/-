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
#主畫面
@app.route('/')
def index():
    return render_template('index.html')
#客戶清單--------------------------------------------------------------------------------------------
@app.route('/customer/list')
def customer_list(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件   
    cursor = connection.cursor() 
    
    #執行SQL    
    cursor.execute('SELECT cusno, cusname, address, contactor FROM customer order by cusno;')
    
    #取回SQL執行後的所有資料
    data = cursor.fetchall()
    
    #設定參數, 準備傳給網頁
    if data:
        #如果有資料
        params = [{'cusno': d[0], 'cusname': d[1], 'address': d[2], 'contactor': d[3]} for d in data]
    else:
        #如果無資料
        params = None
          
    #關閉資料庫連線    
    connection.close() 
    
    #將參數送給網頁, 讓資料嵌入網頁中  
    return render_template('/customer/list.html', data=params) 

#客戶新增表單--------------------------------------------------------------------------------------------
@app.route('/customer/create/form')
def customer_create_form():
    return render_template('customer/create_form.html') 

#客戶新增--------------------------------------------------------------------------------------------
@app.route('/customer/create', methods=['POST'])
def customer_create():
    try:
        #取得使用者的輸入值
        cusno = request.form.get('cusno').strip()
        cusname = request.form.get('cusname').strip()
        address = request.form.get('address').strip()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料寫入客戶資料表
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (cusno, cusname, address) VALUES (%s, %s, %s)", (cusno, cusname, address))
        
        conn.commit()
        conn.close()

        #回傳成功畫面
        return render_template('customer/create.html', success=True)
    except:
        #回傳失敗畫面
        return render_template('customer/create.html', success=False)


#客戶取出表單--------------------------------------------------------------------------------------------
@app.route('/customer/update/fetch')
def customer_update_fetch():    
    return render_template('customer/update_fetch.html') 

#客戶更改表單--------------------------------------------------------------------------------------------
@app.route('/customer/update/form', methods=['GET'])
def customer_update_form(): 
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
    return render_template('/customer/update_form.html', data=params) 

#客戶更改--------------------------------------------------------------------------------------------
@app.route('/customer/update', methods=['POST'])
def customer_update():
    try:
        #取得使用者的輸入值
        cusno = request.form.get('cusno').strip()
        cusname = request.form.get('cusname').strip()
        address = request.form.get('address').strip()
        tel = request.form.get('tel').strip()

        #取得資料庫連線
        conn = db.get_connection()

        #將資料寫入客戶資料表
        cursor = conn.cursor()
        cursor.execute("UPDATE customer SET cusname=%s, address=%s, tel=%s WHERE cusno=%s", (cusname, address, tel, cusno))
        
        conn.commit()
        conn.close()

        #回傳成功畫面
        return render_template('customer/update.html', success=True)
    except:
        #回傳失敗畫面
        return render_template('customer/update.html', success=False)
#產品--------------------------------------------------------------------------------------------

#-----------------------
# 啟動Flask網站--------------------------------------------------------------------------------------------
#-----------------------
if __name__ == '__main__':
    app.run(debug=True)