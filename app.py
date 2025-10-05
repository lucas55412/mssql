from flask import *
import pyodbc
import subprocess

app = Flask(__name__)
app.secret_key = "secretkey123"  # 用於 flash

# 讀取資料庫設定
def read_db_config(file_path='1.txt'):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config

db_config = read_db_config()

# 檢查 Docker 容器是否啟動
def check_container(container_name='sql2022'):
    try:
        output = subprocess.check_output(
            ['docker', 'inspect', '-f', '{{.State.Running}}', container_name]
        )
        return output.strip() == b'true'
    except subprocess.CalledProcessError:
        return False

# 取得資料庫連線
def get_db_connection():
    if not check_container():
        raise Exception("Docker container sql2022 is not running!")

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']};"
        "Encrypt=no"  # 避免 self-signed 證書錯誤
    )
    return pyodbc.connect(conn_str)

# 首頁
@app.route('/')
def index():
    return redirect(url_for('login'))

# 註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "IF NOT EXISTS (SELECT * FROM Users WHERE username=?) "
                "INSERT INTO Users (username, password) VALUES (?, ?)",
                username, username, password
            )
            conn.commit()
            conn.close()
            flash("註冊成功，請登入")
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('register'))
    return render_template('register.html')

# 登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Users WHERE username=? AND password=?",
                username, password
            )
            user = cursor.fetchone()
            conn.close()
            if user:
                flash(f"歡迎 {username} 登入！")
                return redirect(url_for('login'))
            else:
                flash("帳號或密碼錯誤")
        except Exception as e:
            flash(str(e))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
