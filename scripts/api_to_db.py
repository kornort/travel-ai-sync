import requests
import sqlite3

def fetch_open_data_to_db():
    # 這是桃園觀光 Open Data 的 API 網址 (JSON 格式)
    # 這裡以桃園觀光導覽網提供的 Open Data API 為例
    url = "https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=bed8a800-be39-4750-89a6-324b71f5d5fa&rid=ef439815-aa4a-4384-8263-99933c05307b"
    
    print("📡 正在從桃園 Open Data 平台抓取海量數據...")
    
    try:
        response = requests.get(url)
        # 政府 API 通常回傳大整數編碼，轉為 JSON
        data = response.json()
        
        # 假設資料結構在 'infos' 或是直接就是一個清單
        # 這裡根據桃園 API 的常見結構進行處理
        attractions = data.get('infos', [])
        
        conn = sqlite3.connect('data/travel.db')
        cursor = conn.cursor()
        
        print(f"✅ 成功獲取 {len(attractions)} 筆原始資料！開始結構化寫入...")
        
        new_count = 0
        for item in attractions:
            name = item.get('Name')
            city = "桃園市"
            category = item.get('Class1', '未分類')
            # 整合地址與介紹作為 AI 分析的素材
            content = f"地址：{item.get('Add')} | 簡介：{item.get('Toldescribe')[:200]}..."
            source = "TYCG_OpenData_API"

            # 檢查重複 (這就是你想要的專業處理)
            cursor.execute("SELECT id FROM attractions WHERE name = ?", (name,))
            if cursor.fetchone():
                continue

            cursor.execute('''
                INSERT INTO attractions (name, city, category, content, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, city, category, content, source))
            new_count += 1

        conn.commit()
        conn.close()
        print(f"🚀 完工！本次新增 {new_count} 筆桃園在地景點，資料庫已大幅擴充！")

    except Exception as e:
        print(f"❌ API 抓取失敗：{e}")

if __name__ == "__main__":
    fetch_open_data_to_db()