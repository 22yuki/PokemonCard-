import streamlit as st
import os

def hira_to_kata(text):
    result = ""
    for ch in text:
        if 0x3041 <= ord(ch) <= 0x3096:
            result += chr(ord(ch) + 0x60)
        else:
            result += ch
    return result

# Webアプリのタイトル
st.title("PTCGL 検索")

file_path = "Pokelist.txt"

if not os.path.exists(file_path):
    st.error(f"エラー: '{file_path}' が見つかりません。")
else:
    # 検索ボックス（ここで入力を受け付ける）
    search_term = st.text_input("カード名（日本語）を入力してください:")

    # 検索ボタンが押されたら、または文字が入力されたら実行
    if search_term:
        normalized_search = hira_to_kata(search_term).lower()
        results = []
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 4:
                    jp_name, en_name, pack_name, card_no = parts[0], parts[1], parts[2], parts[3]
                    normalized_jp_name = hira_to_kata(jp_name).lower()
                    
                    if normalized_search in normalized_jp_name:
                        results.append({
                            "jp_name": jp_name,
                            "en_name": en_name,
                            "pack_name": pack_name,
                            "card_no": card_no
                        })

        # 結果の表示
        st.write(f"**検索結果：{len(results)}件**")
        st.write("---")
        
        for res in results:
            # 枠で囲って見やすく表示
            with st.container():
                st.write(f"**日本語名：** {res['jp_name']}")
                st.write(f"**カード名：** {res['en_name']}")
                st.write(f"**パック名：** {res['pack_name']}")
                st.write(f"**カードNo：** {res['card_no']}")
                st.write("---")