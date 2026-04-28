import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("錯誤：找不到 API Key，請檢查 .env 檔案！")
else:
    genai.configure(api_key=api_key)
    
    # 這裡改用 gemini-3-flash
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = "請介紹一個桃園中壢的私房景點，100字內。"
        
        response = model.generate_content(prompt)
        print("\n✨ AI 成功回應了：")
        print("-" * 30)
        print(response.text)
        print("-" * 30)
    except Exception as e:
        print(f"呼叫 API 時發生錯誤：{e}")