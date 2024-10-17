import streamlit as st
import requests
import json
import asyncio
import websockets


st.title('デジタル名刺')


# サイドバーにタイトルを設定
st.sidebar.title('メニュー')

st.sidebar.write('QRコードをスキャンして友達追加してください。')
st.sidebar.image('./linebot.png', use_column_width=True)
st.sidebar.write('お問い合わせはこちら')
st.sidebar.write('電話番号: 090-1234-5678')
st.sidebar.write('メールアドレス: help@help.help')



json_file_path = './test.json'

# JSONファイルを読み込む関数
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 'name' キーの値が存在するデータのみをリストに保持する
    filtered_data = [item for item in data if 'name' in item and item['name']]
    return filtered_data
    


# st.title('Reaction Text')
#st.header('Databricks Q&A bot')

if "messages" not in st.session_state:
    st.session_state.messages = []

if "displayed_messages" not in st.session_state: 
    st.session_state.displayed_messages = set()

async def receive_messages():
    uri = "wss://562a-180-60-4-132.ngrok-free.app/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            message_data = json.loads(message)
            # print(message_data)
            st.session_state.messages.append({"role":"user","content":message_data["text"], "user_id":message_data["user_id"]})

async def main():
    # url = "https://562a-180-60-4-132.ngrok-free.app/audio-text"
    # data = {"user_id": "音声テスト", "text": "ああああああああああああああ"}
    # response = requests.post(url, json=data)

    # st.title(response.status_code)
    # st.json(response.json())

    st.title('Reaction Text')
    #st.header('Databricks Q&A bot')

    with st.expander("プロフィール", expanded=True):
        # プロフィールデータ
        profiles = load_json_file(json_file_path)

        # プロフィール表示関数
        def display_profile(profile):
            st.header(profile["name"])
            
    # st.image(profile["image"], use_column_width=True) if "image" in profile and profile["image"]
            st.info(f"会社,役職: {profile['company']}")
            st.error(f"電話番号: {profile['tel']}")
            st.warning(f"メールアドレス: {profile['email']}")
            st.info(f"趣味: {profile['hobby']}")
            st.success(f"出身地: {profile['birthplace']}")



        # タイトル
        # st.title('プロフィール一覧')

        # 表示するプロフィール数を選択するウィジェット
        num_profiles = st.slider("表示するプロフィール数", 1, len(profiles), 3,key='slider9')

        # カラムを使ってプロフィールを表示
        cols = st.columns(num_profiles)
        for i in range(num_profiles):
            if i < len(profiles):  # プロフィールの数を超えないようにチェック
                with cols[i % num_profiles]:
                    display_profile(profiles[i])

    
    st.title("リアクション")
    asyncio.create_task(receive_messages())

    # while True:
    #     for i in reversed(range(len(st.session_state.messages))):
    #         message = st.session_state.messages[i]
    #         if i not in st.session_state.displayed_messages:
    #             with st.chat_message(message["role"]):
    #                 st.markdown(message["user_id"])
    #                 st.markdown(message["content"])

    #             st.session_state.displayed_messages.add(i)

    #     await asyncio.sleep(1)
    
    with st.container():
        while True:
            for i, message in enumerate(st.session_state.messages):
                # message = st.session_state.messages[i]
                if i not in st.session_state.displayed_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["user_id"])
                        st.markdown(message["content"])

                    st.session_state.displayed_messages.add(i)

            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())