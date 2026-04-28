import requests
from bs4 import BeautifulSoup
import sqlite3

def crawl_ptt_to_db():
    url = "https://www.ptt.cc/bbs/Taoyuan/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    cookies = {'over18': '1'}
    
    print(f"📡 正在掃描 PTT 桃園版，提取社群數據...")
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('.r-ent')
        
        conn = sqlite3.connect('data/travel.db')
        cursor = conn.cursor()
        
        count = 0
        for art in articles:
            title_tag = art.select_one('.title a')
            if not title_tag: continue
            
            title = title_tag.get_text()
            # 排除非景點討論的公告或閒聊
            if "[公告]" in title or "re:" in title.lower(): continue
            
            link = "https://www.ptt.cc" + title_tag['href']
            author = art.select_one('.author').get_text()
            
            # 防重複檢查
            cursor.execute("SELECT id FROM attractions WHERE name = ?", (title,))
            if cursor.fetchone():
                continue

            # 存入資料庫：將 PTT 標題存入 name，作者與連結存入 content
            cursor.execute('''
                INSERT INTO attractions (name, province_state, category, content, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, "桃園市", "社群討論", f"作者: {author}\n連結: {link}", "PTT_Taoyuan"))
            count += 1
            print(f"   [+] 成功存入討論：{title[:20]}...")

        conn.commit()
        conn.close()
        print(f"✅ 任務完成！資料庫新增了 {count} 筆來自 PTT 的社群觀點。")
        
    except Exception as e:
        print(f"❌ PTT 爬取失敗: {e}")

if __name__ == "__main__":
    crawl_ptt_to_db()