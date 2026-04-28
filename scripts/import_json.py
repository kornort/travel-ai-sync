import json
import sqlite3
import os

def import_local_json():
    json_path = 'taoyuan_data.json'
    
    if not os.path.exists(json_path):
        print(f"❌ 找不到檔案：{json_path}。請確保 JSON 檔案放在專案根目錄。")
        return

    try:
        # 讀取 JSON 資料
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        conn = sqlite3.connect('data/travel.db')
        cursor = conn.cursor()
        
        # 支援 list 或 dict 格式
        attractions = data if isinstance(data, list) else data.get('infos', [])
        
        print(f"✅ 成功載入。準備進行精準地理拆解並寫入...")
        
        count = 0
        for item in attractions:
            name = item.get('name')
            if not name: continue

            # --- 核心：精準資料清洗邏輯 ---
            address = item.get('add', "")
            province = ""
            district = ""
            
            # 尋找「市」或「縣」作為基準點
            for target in ["市", "縣"]:
                pos = address.find(target)
                if pos != -1:
                    # 抓取基準點及其前方2個字 (例如：桃園市)
                    province = address[max(0, pos-2) : pos+1]
                    # 抓取基準點後方3個字 (例如：中壢區)
                    district = address[pos+1 : pos+4]
                    break
            
            # 補底邏輯：如果切分失敗則給予預設
            if not province:
                province = "桃園市"
                district = "未知區"
            # ---------------------------

            # 防重複檢查
            cursor.execute("SELECT id FROM attractions WHERE name = ?", (name,))
            if cursor.fetchone():
                continue

            tel = item.get('tel', '無電話')
            desc = item.get('toldescribe', '無詳細描述')
            full_content = f"地址：{address}\n電話：{tel}\n介紹：{desc}"
            
            # 寫入資料庫
            cursor.execute('''
                INSERT INTO attractions (name, province_state, district, category, content, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, province, district, item.get('category', '景點資料'), full_content, "OpenData_Fixed_Import"))
            count += 1

        conn.commit()
        conn.close()
        print(f"🚀 清洗完成！資料庫已存入 {count} 筆整齊的資料。")

    except Exception as e:
        print(f"❌ 導入失敗：{e}")

if __name__ == "__main__":
    import_local_json()