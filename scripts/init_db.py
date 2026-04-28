import sqlite3
import os

def init_db():
    # 1. 檢查並建立存放資料庫的資料夾
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📁 已建立 data 資料夾")

    # 2. 連接到資料庫檔案 (如果不存在會自動建立)
    # 檔案會出現在 data/travel.db
    conn = sqlite3.connect('data/travel.db')
    cursor = conn.cursor()

    print("⏳ 正在初始化資料庫結構...")

    # 3. 建立景點資料表 (attractions)
    # id: 主鍵，自動遞增
    # name: 景點名稱
    # city: 縣市 (例如：桃園市、台北市)
    # category: 分類 (例如：自然步道、文創、美食)
    # content: 詳細介紹
    # source: 資料來源 (例如：Gemini, Ollama, Scraper)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT,
            category TEXT,
            content TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. 提交變更並關閉連線
    conn.commit()
    conn.close()
    print("✅ 資料庫初始化成功！位置：data/travel.db")

if __name__ == "__main__":
    init_db()