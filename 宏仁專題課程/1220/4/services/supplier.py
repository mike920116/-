# 匯入模組
from flask import request, render_template
from flask import Blueprint
from utils import db

# 產生客戶服務藍圖
supplier_bp = Blueprint('supplier_bp', __name__)

#客戶清單
@supplier_bp.route('/list')
def supplier_list(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件   
    cursor = connection.cursor() 
    
    #執行SQL    
    cursor.execute('SELECT supno, supname, contactor, tel FROM supplier order by supno;')
    
    #取回SQL執行後的所有資料
    data = cursor.fetchall()
    
    #設定參數, 準備傳給網頁
    if data:
        #如果有資料
        params = [{'supno': d[0], 'supname': d[1], 'contactor': d[2], 'tel': d[3]} for d in data]
    else:
        #如果無資料
        params = None
          
    #關閉資料庫連線    
    connection.close() 
    
    #將參數送給網頁, 讓資料嵌入網頁中  
    return render_template('/supplier/list.html', data=params)