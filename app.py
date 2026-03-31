import streamlit as st
import re
import os
import json
import random
import math

# === 화면 설정 ===
st.set_page_config(page_title="AWS SAA 마스터", layout="wide", page_icon="☁️")

# === 스타일 ===
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    [data-testid="stSidebar"] { background-color: #262730; border-right: 1px solid #444; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #FAFAFA !important; }
    .question-card { background-color: #1E1E1E; border: 1px solid #333; border-radius: 12px; padding: 35px; border-left: 6px solid #FF9900; margin-bottom: 30px; }
    .question-header { font-size: 1.5rem; font-weight: 700; color: #FF9900; margin-bottom: 20px; }
    .question-content { font-size: 18px; line-height: 1.7; color: #E0E0E0; font-weight: 400; }
    
    /* 체크박스 (다중 선택) 스타일 */
    .stCheckbox { background-color: #262730; padding: 15px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #444; }
    .stCheckbox label p { color: #FAFAFA !important; font-size: 17px !important; }
    
    /* 라디오 버튼 (단일 선택) 스타일 - 뭉침 현상 완벽 해결! */
    div[role="radiogroup"] { gap: 0 !important; }
    div[role="radiogroup"] > label { 
        background-color: #262730; 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 12px !important; 
        border: 1px solid #444; 
    }
    div[role="radiogroup"] > label p { color: #FAFAFA !important; font-size: 17px !important; }

    .success-box { background-color: #1b4d3e; color: #a3cfbb; padding: 20px; border-radius: 10px; margin-top: 15px; }
    .error-box { background-color: #4c2b2b; color: #f1aeb5; padding: 20px; border-radius: 10px; margin-top: 15px; }
    .stButton button { background-color: #FF9900; color: white; font-size: 18px; font-weight: bold; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# === 데이터 로드 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, 'my_progress.json')
TARGET_FILE = os.path.join(BASE_DIR, "AWS_Total_Clean.md")

@st.cache_data
def load_clean_questions():
    if not os.path.exists(TARGET_FILE): return []
    with open(TARGET_FILE, 'r', encoding='utf-8') as f: content = f.read()
    
    parts = re.split(r'^(?:##\s+|문제\s+)(\d+)\.?', content, flags=re.MULTILINE)
    all_questions = []
    
    for i in range(1, len(parts), 2):
        try:
            q_id = parts[i].strip()
            raw_text = parts[i+1]
            q_data = {'id': q_id}
            
            raw_text = raw_text.replace('문제 내용:', '문제')
            raw_text = raw_text.replace('선택지:', '선택지')
            raw_text = raw_text.replace('정답:', '정답')
            raw_text = raw_text.replace('해설:', '해설')

            def extract(key, end_keys):
                s = raw_text.find(key)
                if s == -1: return ""
                sub = raw_text[s+len(key):]
                e = len(sub)
                for ek in end_keys:
                    idx = sub.find(ek)
                    if idx != -1 and idx < e: e = idx
                return sub[:e].strip()

            q_data['question'] = extract('문제', ['선택지', '정답'])
            opts_text = extract('선택지', ['정답'])
            ans_text = extract('정답', ['해설', '---'])
            q_data['explanation'] = extract('해설', ['---', '##', '문제 '])

            opts = {}
            # 💡 [A-F]로 수정하여 F번 선택지까지 완벽하게 분리
            matches = re.findall(r'([A-F])[.:]\s*(.*?)(?=(?:[A-F][.:]|$))', opts_text, flags=re.DOTALL)
            for match in matches:
                clean_opt = re.sub(r'\s*[-•◦]+$', '', match[1]).strip()
                opts[match[0]] = clean_opt
            q_data['options'] = opts
            
            clean_ans = ans_text.replace(':', '').strip()
            q_data['answer'] = [x.strip() for x in re.split(r'[,\s]+', clean_ans) if x.strip()]

            if q_data['options']:
                all_questions.append(q_data)
        except Exception: 
            continue
            
    return all_questions

def load_progress():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: return {"wrong_ids": [], "solved_ids": []}
    return {"wrong_ids": [], "solved_ids": []}

def save_progress(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False)

# === 메인 화면 ===
def main():
    st.markdown('<h1 style="color:#FF9900;">☁️ AWS SAA-C03 (Master)</h1>', unsafe_allow_html=True)
    all_qs = load_clean_questions()
    
    if not all_qs:
        st.error("❌ 'AWS_Total_Clean.md' 파일이 없습니다. (또는 파싱할 수 있는 문제가 없습니다.)")
        st.stop()

    if 'history' not in st.session_state: st.session_state.history = load_progress()
    if 'idx' not in st.session_state: st.session_state.idx = 0
    
    with st.sidebar:
        st.header("📊 학습 현황")
        st.metric("✅ 정답", f"{len(st.session_state.history['solved_ids'])}")
        st.metric("❌ 오답", f"{len(st.session_state.history['wrong_ids'])}")
        st.divider()
        mode = st.radio("학습 모드", ["📝 실전 모의고사 (65문항)", "🔀 전체 랜덤 풀기", "❌ 오답 노트"])
        
        selected_qs = []
        new_mode_key = ""
        
        if "실전" in mode:
            new_mode = 'exam'
            set_size = 65
            total_sets = math.ceil(len(all_qs) / set_size)
            set_ops = [f"Set {i+1} ({i*set_size+1}~{min((i+1)*set_size, len(all_qs))}번)" for i in range(total_sets)]
            curr_set = st.selectbox("세트 선택", set_ops)
            s_idx = int(curr_set.split()[1]) - 1
            start = s_idx * set_size
            selected_qs = all_qs[start : start + set_size]
            new_mode_key = f"exam_{s_idx}"
        elif "랜덤" in mode:
            new_mode = 'random'
            selected_qs = all_qs[:]
            new_mode_key = "random"
        elif "오답" in mode:
            new_mode = 'wrong'
            w_ids = set(st.session_state.history['wrong_ids'])
            selected_qs = [q for q in all_qs if q['id'] in w_ids]
            new_mode_key = f"wrong_{len(selected_qs)}"
            
        if 'last_mode' not in st.session_state: st.session_state.last_mode = ""
        if st.session_state.last_mode != new_mode_key:
            st.session_state.quiz_list = selected_qs
            st.session_state.idx = 0
            if new_mode == 'random': random.shuffle(st.session_state.quiz_list)
            st.session_state.last_mode = new_mode_key
            st.rerun()

        st.divider()
        if st.button("🗑️ 초기화"):
            if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
            st.session_state.history = {"wrong_ids": [], "solved_ids": []}
            st.rerun()

    if not st.session_state.quiz_list:
        if "오답" in mode: st.info("🎉 오답 노트가 비어있습니다!")
        else: st.info("표시할 문제가 없습니다.")
        st.stop()
        
    if st.session_state.idx >= len(st.session_state.quiz_list): st.session_state.idx = 0
    q = st.session_state.quiz_list[st.session_state.idx]
    
    st.markdown(f"**진행중:** {st.session_state.idx + 1} / {len(st.session_state.quiz_list)} (ID: {q['id']}번)")
    st.progress((st.session_state.idx + 1) / len(st.session_state.quiz_list))
    
    st.markdown(f"""
    <div class="question-card">
        <div class="question-header">Q{q['id']}</div>
        <div class="question-content">{q['question'].replace(chr(10), '<br>')}</div>
    </div>""", unsafe_allow_html=True)
    
    with st.form(f"f_{q['id']}"):
        ans_count = len(q['answer'])
        picks = []
        
        if ans_count == 1:
            st.markdown(f"**선택지 (1개 선택):**")
            pick = st.radio(
                "정답 선택",
                options=sorted(q['options'].keys()),
                format_func=lambda x: f"{x}. {q['options'][x]}",
                label_visibility="collapsed"
            )
            if pick: picks.append(pick)
        else:
            st.markdown(f"**선택지 ({ans_count}개 선택):**")
            for k, v in sorted(q['options'].items()):
                if st.checkbox(f"{k}. {v}"): picks.append(k)
                
        if st.form_submit_button("정답 확인", use_container_width=True):
            ans = sorted(q['answer'])
            picks = sorted(picks)
            st.session_state.history['solved_ids'].append(q['id'])
            
            if ans_count > 1 and len(picks) != ans_count:
                st.warning(f"⚠️ {ans_count}개를 골라야 합니다. (현재 {len(picks)}개 선택)")
            elif ans == picks:
                st.success("✅ 정답!")
                if q['id'] in st.session_state.history['wrong_ids']:
                    st.session_state.history['wrong_ids'].remove(q['id'])
            else:
                st.error(f"❌ 오답 (정답: {', '.join(ans)})")
                if q['id'] not in st.session_state.history['wrong_ids']:
                    st.session_state.history['wrong_ids'].append(q['id'])
            save_progress(st.session_state.history)
            with st.expander("📝 해설 / 참고", expanded=True): st.info(q['explanation'])

    c1, c2 = st.columns(2)
    if c1.button("< 이전", use_container_width=True) and st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.rerun()
    if c2.button("다음 >", use_container_width=True):
        st.session_state.idx += 1
        st.rerun()

if __name__ == '__main__':
    main()