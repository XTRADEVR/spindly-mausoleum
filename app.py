import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="Venice AI - Think Freely",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, .stApp { font-family: Inter, sans-serif; background: #080a12 !important; }
[data-testid="stSidebar"] { background: #0e111a !important; border-right: 1px solid #1b1f30; }
.sidebar-logo { font-size: 22px; font-weight: 800; color: white !important; margin-bottom: 25px; }
.sidebar-item.active { background: #171b2b; color: white !important; padding: 10px; border-radius: 10px; }
.badge { background: #131d33; border: 1px solid #26345c; padding: 16px; border-radius: 14px; text-align: center; font-weight: 800; color: #cbd5ff; }
.center-icon { font-size: 72px; text-align: center; margin-top: 70px; }
.think { text-align: center; font-size: 52px !important; font-weight: 800; color: white; margin-bottom: 40px; }
.small-footer { text-align: center; color: #5a6380; font-size: 11px; margin-top: 120px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-logo">V Venice</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item active">🤖 Agentic Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge">XTRADE<br>VR PRO<br>0 Credits<br><br>Upgrade to Pro</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown('<div class="center-icon">🧠</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center;font-size:52px;font-weight:800;">Think Freely</h1>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🌍 Learn about the World", use_container_width=True):
            st.session_state.prefill = "Learn about the world: "
    with c2:
        if st.button("🖼️ Generate any image", use_container_width=True):
            st.session_state.prefill = "Generate any image of: "
    with c3:
        if st.button("🎬 Create AI Video", use_container_width=True):
            st.session_state.prefill = "Create AI Video: "
    with c4:
        if st.button("📊 Flowchart or Diagram", use_container_width=True):
            st.session_state.prefill = "Create a Flowchart using MermaidJS for: "

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

model = st.selectbox("", ["Auto - Venice will choose", "DeepSeek V4.1 Flash (Uncensored) - Private", "Kimi K2.5 - Private + Anon", "Claude Fable 5.1 - Private + Anon"], label_visibility="collapsed")
prefill = st.session_state.pop("prefill", None)
prompt = st.chat_input("Ask Venice a question... / Create flowcharts and diagrams...")
if prefill: prompt = prefill

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    try:
        api_key = st.secrets.get("DEEPSEEK_API_KEY") if "DEEPSEEK_API_KEY" in st.secrets else os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            st.error("Set DEEPSEEK_API_KEY di Vercel > Environment Variables")
            st.stop()
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        system_prompt = f"You are Venice AI - Think Freely. Model: {model}. User: XTRADE VR PRO - Private + Anon. Be direct, no lecture. If image -> [IMAGE_PROMPT: ...]. If flowchart -> ```mermaid"
        response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages, stream=True, temperature=0.9)
        with st.chat_message("assistant"):
            full = st.write_stream((chunk.choices[0].delta.content or "" for chunk in response))
        st.session_state.messages.append({"role": "assistant", "content": full})
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown('<div class="small-footer">Kimi K2.5 - Private + Anon · By using Venice, you agree to our Terms and Privacy Policy.</div>', unsafe_allow_html=True)
