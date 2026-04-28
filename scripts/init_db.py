import sqlite3
import os

def init_db():
    # 1. 確保資料夾存在
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📁 已建立 data 資料夾")

    # 2. 連接到資料庫
    conn = sqlite3.connect('data/travel.db')
    cursor = conn.cursor()

    print("⏳ 正在初始化專業版地理階層資料表...")

    # 3. 建立具備「縣市」與「鄉鎮市區」層級的資料表
    # province_state: 存放第一級行政區（如：桃園市、雲林縣）
    # district: 存放第二級行政區（如：中壢區、斗六市）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            province_state TEXT,
            district TEXT,
            category TEXT,
            content TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ 資料庫初始化成功！")
    print("📊 目前結構：[ID, 名稱, 縣市, 鄉鎮市區, 分類, 內容, 來源, 建立時間]")

if __name__ == "__main__":
    init_db()