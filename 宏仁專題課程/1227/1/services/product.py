from flask import Blueprint, render_template, request
from flask_login import login_required
from utils import db

product_bp = Blueprint('product_bp', __name__)

# 產品清單路由
@product_bp.route('/list')
@login_required
def product_list():
    connection = db.get_connection()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM product')
    total_count = cursor.fetchone()[0]
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)
    cursor.execute('SELECT prono, proname, price, stockAmt FROM product ORDER BY prono LIMIT %s OFFSET %s', (per_page, offset))
    data = cursor.fetchall()
    params = [{'prono': d[0], 'proname': d[1], 'price': d[2], 'stockAmt': d[3]} for d in data] if data else None
    connection.close()
    return render_template('/product/list.html', data=params, page=page, total_pages=total_pages)
