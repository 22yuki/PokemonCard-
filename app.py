import streamlit as st
import os


# パック名と公式画像URLの記号の対応表
PACK_CODES = {
    "Temporal Forces": "SV05",
    "Twilight Masquerade": "SV06",
    "Shrouded Fable": "SV6PT5",
    "Stellar Crown": "SV07",
    "Surging Sparks": "SV08",
    "Prismatic Evolutions": "SV8PT5",
    "Journey Together": "SV09",
    "Destined Rivals": "SV10",
    "White Flare": "RSV10PT5",
    "Black Bolt": "ZSV10PT5",
    "Mega Evolution": "ME01",
    "Phantasmal Flames": "ME02",
    "Ascended Heroes": "ME2PT5",
    "Perfect Order": "ME03",
    "Chaos Rising": "ME04",
    "Pitch Black": "ME05"
}


def hira_to_kata(text):
    result = ""
    for ch in text:
        if 0x3041 <= ord(ch) <= 0x3096:
            result += chr(ord(ch) + 0x60)
        else:
            result += ch
    return result


def format_card_no(card_no):
    """先頭の0を削除する（例: '002' -> '2', '083' -> '83'）"""
    # .lstrip('0') で左側の0を消します
    formatted = card_no.lstrip('0')
    # もし全部0だった場合（'000'など）は空になるので、その場合は'0'を返す
    return formatted if formatted else '0'


st.title("PTCGL カード検索ツール")


file_path = "Pokelist.txt"


if not os.path.exists(file_path):
    st.error(f"エラー: '{file_path}' が見つかりません。")
else:
    search_term = st.text_input("カード名（日本語）を入力してください:")


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


        st.write("---")
        st.write(f"**検索結果：{len(results)}件**")
        
        for res in results:
            # 1. パック名から記号を取得
            pack_name = res['pack_name']
            set_code = PACK_CODES.get(pack_name)
            
            # 2. 画像URLの生成
            img_url = None
            if set_code:
                # 0を消したカード番号を取得
                formatted_no = format_card_no(res['card_no'])
                # URLを組み立て
                img_url = f"https://assets.pokemon.com/static-assets/content-assets/cms2/img/cards/web/{set_code}/{set_code}_EN_{formatted_no}.png"


            # 3. 画面レイアウト（左に画像、右にテキスト）
            with st.container():
                # 画面を [1対2] の割合で2列に分割
                col1, col2 = st.columns([1, 2.5])
                
                # 左の列（画像）
                with col1:
                    if img_url:
                        # 画像を表示。枠の幅に合わせて自動調整
                        st.image(img_url, use_container_width=True)
                    else:
                        st.info("No Image")
                
                # 右の列（テキスト）
                with col2:
                    st.write(f"**日本語名：** {res['jp_name']}")
                    st.write(f"**カード名：** {res['en_name']}")
                    st.write(f"**パック名：** {res['pack_name']}")
                    st.write(f"**カードNo：** {res['card_no']}")
            
            st.write("---")