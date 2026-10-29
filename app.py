import streamlit as st
import os
import base64

# スクリプトがあるディレクトリ（絶対パス）を取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    "Pitch Black": "ME05",
    "30th Celebration": "30TH",
    "Delta Reign": "ME06"
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
    formatted = card_no.lstrip('0')
    return formatted if formatted else '0'

# ローカルの NoIMG.png を Base64 に変換する関数（絶対パス対応）
def get_base64_image(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded}"
        except Exception:
            return None
    return None

st.title("PTCGL カード検索")

txt_path = os.path.join(BASE_DIR, "Pokelist.txt")
no_img_path = os.path.join(BASE_DIR, "NoIMG.png")
no_img_data_url = get_base64_image(no_img_path)

if not os.path.exists(txt_path):
    st.error(f"エラー: 'Pokelist.txt' が見つかりません。")
else:
    search_term = st.text_input("カード名（日本語/英語）またはパック名を入力:")

    if search_term:
        # 入力文字の表記ゆれ対策
        search_raw = search_term.lower().strip()
        search_kata = hira_to_kata(search_term).lower().strip()

        results = []

        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 4:
                    jp_name, en_name, pack_name, card_no = parts[0], parts[1], parts[2], parts[3]

                    normalized_jp = hira_to_kata(jp_name).lower()
                    normalized_en = en_name.lower()
                    normalized_pack = pack_name.lower()

                    if (search_kata in normalized_jp) or (search_raw in normalized_en) or (search_raw in normalized_pack):
                        results.append({
                            "jp_name": jp_name,
                            "en_name": en_name,
                            "pack_name": pack_name,
                            "card_no": card_no
                        })

        st.write("---")
        st.write(f"**検索結果：{len(results)}件**")

        for res in results:
            pack_name = res['pack_name']
            set_code = PACK_CODES.get(pack_name)

            img_url = None
            if set_code:
                formatted_no = format_card_no(res['card_no'])
                img_url = f"https://assets.pokemon.com/static-assets/content-assets/cms2/img/cards/web/{set_code}/{set_code}_EN_{formatted_no}.png"

            # 画像ボックスのHTML生成
            if img_url:
                if no_img_data_url:
                    # 公式画像の読み込みに失敗(404)した場合、自動で NoIMG.png に差し替える
                    img_box = f'''<img src="{img_url}" alt="" onerror="this.onerror=null; this.src='{no_img_data_url}';" style="width: 100%; height: auto; display: block; border-radius: 4px;">'''
                else:
                    # 万が一 NoIMG.png すら読み込めない場合のフォールバック（グレーのボックス）
                    img_box = f'''<img src="{img_url}" alt="" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" style="width: 100%; height: auto; display: block; border-radius: 4px;"><div style="display:none; height: 90px; background-color: #2b2b30; align-items: center; justify-content: center; color: #888; border-radius: 4px; font-size: 0.70rem; text-align: center;">No Image</div>'''
            else:
                # パックコード自体がない場合
                if no_img_data_url:
                    img_box = f'<img src="{no_img_data_url}" alt="No Image" style="width: 100%; height: auto; display: block; border-radius: 4px;">'
                else:
                    img_box = '<div style="height: 90px; background-color: #2b2b30; display: flex; align-items: center; justify-content: center; color: #888; border-radius: 4px; font-size: 0.70rem;">No Image</div>'

            card_html = f"""<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; border: 1px solid #33333a; padding: 10px; border-radius: 8px; background-color: #1f1f23; color: #ffffff;">
<div style="flex: 0 0 70px;">
{img_box}
</div>
<div style="flex: 1; font-size: 0.85rem; color: #ffffff; line-height: 1.5;">
<p style="margin: 0 0 3px 0;"><strong style="color: #90caf9;">日本語名：</strong> {res['jp_name']}</p>
<p style="margin: 0 0 3px 0;"><strong style="color: #90caf9;">カード名：</strong> {res['en_name']}</p>
<p style="margin: 0 0 3px 0;"><strong style="color: #90caf9;">パック名：</strong> {res['pack_name']}</p>
<p style="margin: 0;"><strong style="color: #90caf9;">カードNo：</strong> {res['card_no']}</p>
</div>
</div>"""

            st.markdown(card_html, unsafe_allow_html=True)