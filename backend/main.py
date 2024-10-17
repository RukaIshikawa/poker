from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class DigitalCard(BaseModel):
    name: str
    post: str
    company: str
    company_address: str
    tel: str
    email: str

@app.post("/submit")
async def receive_card(card: DigitalCard):
    # 受け取ったデータを処理する
    print("受け取ったデジタル名刺のデータ:")
    print(f"名前: {card.name}")
    print(f"会社名役職: {card.company}")
    print(f"電話番号: {card.tel}")
    print(f"メールアドレス: {card.email}")
    print(f"趣味:{card.hobby}")
    print(f"出身地:{card.introduction}")
    # 例えば、データベースに保存するなど
    return {"status": "Data received", "data": card.dict()}




def fetch_kintone_app_info(subdomain, app_id, api_token):
    # Kintone APIのエンドポイント
    url = f"https://{subdomain}.cybozu.com/k/v1/records.json"
    
    # ヘッダーにAPIトークンを設定
    headers = {
        "X-Cybozu-API-Token": api_token
    }
    
    # パラメータにアプリIDを設定
    params = {
        "app": app_id
    }
    
    # APIからデータを取得
    response = requests.get(url, headers=headers, params=params)
    
    # ステータスコードが200（成功）であることを確認
    if response.status_code == 200:
        # JSON形式のレスポンスデータを取得
        app_info = response.json()
        print("app_info",app_info)
        return app_info
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def display_app_info(app_info):
    if app_info:
        print("できた")
    else:
        print("No app information to display.")

if __name__ == "__main__":
    subdomain = "9azm0wjv6apn"  # Kintoneのサブドメイン
    app_id = "9"  # 取得したいアプリのID
    api_token = "uQz0X1B5l9lTmKOBcPhAs2eytLiXAal16buLX1m3"  # APIトークン
    
    app_info = fetch_kintone_app_info(subdomain, app_id, api_token)
    display_app_info(app_info)

@app.get("/kintone-data")
async def get_kintone_data():
    subdomain = "9azm0wjv6apn"
    app_id = "9"
    api_token = "uQz0X1B5l9lTmKOBcPhAs2eytLiXAal16buLX1m3"
    data = fetch_kintone_app_info(subdomain, app_id, api_token)
    return data