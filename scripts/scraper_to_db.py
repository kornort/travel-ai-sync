import requests
from bs4 import BeautifulSoup
import sqlite3
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def smart_scrape():
    url = "https://travel.tycg.gov.tw/zh-tw/event"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取卡片物件，這樣我們才能同時拿到「標題」與「連結」
        cards = soup.select('div.card-item') 
        
        conn = sqlite3.connect('data/travel.db')
        cursor = conn.cursor()

        new_count = 0
        for card in cards[:10]: # 增加到 10 筆
            name = card.select_one('h3').get_text(strip=True) if card.select_one('h3') else "未知景點"
            # 抓取超連結，這是為了以後可以做「深度爬蟲」
            link_tag = card.select_one('a.card-link')
            link = "https://travel.tycg.gov.tw" + link_tag['href'] if link_tag else ""
            
            # 【關鍵：防重檢查】先查資料庫有沒有這個名字
            cursor.execute("SELECT id FROM attractions WHERE name = ?", (name,))
            if cursor.fetchone():
                print(f"跳過已存在的資料：{name}")
                continue

            # 寫入資料
            cursor.execute('''
                INSERT INTO attractions (name, city, category, content, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, "桃園市", "熱門活動", f"詳情請見連結：{link}", "Pro_Scraper"))
            new_count += 1
            print(f"🆕 新增景點：{name}")

        conn.commit()
        conn.close()
        print(f"🎉 完善成功！本次共新增 {new_count} 筆新資料。")

    except Exception as e:
        print(f"❌ 完善過程中發生錯誤：{e}")

if __name__ == "__main__":
    smart_scrape()