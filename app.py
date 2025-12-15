import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 页面配置 ---
st.set_page_config(page_title="AMC 8 AI Tutor: Bilingual Demo", layout="wide")

# --- 样式优化：让中英文排版更舒服 ---
st.markdown("""
<style>
    .en-text { font-size: 20px; font-weight: bold; color: #2c3e50; font-family: sans-serif; }
    .cn-text { font-size: 16px; color: #7f8c8d; margin-top: 5px; }
    .term { background-color: #e8f4f8; padding: 2px 5px; border-radius: 4px; border: 1px solid #bce0fd; }
    .highlight { color: #d35400; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 核心数据结构：中英双语题目 ---
PROBLEM = {
    "title_en": "Sets and Venn Diagrams",
    "title_cn": "集合与韦恩图",
    
    # 英文原题 (AMC 风格)
    "question_en": "A class has 30 students. 20 students like <span class='term'>soccer</span>, 15 like <span class='term'>basketball</span>, and 5 like <span class='term'>neither</span>. How many students like <span class='term'>both</span>?",
    
    # 中文辅助翻译
    "question_cn": "某班级有 30 名学生。其中 20 人喜欢足球，15 人喜欢篮球，5 人两种都不喜欢。请问：既喜欢足球又喜欢篮球的有多少人？",
    
    # 关键术语库 (用于侧边栏)
    "vocab": {
        "Set": "集合",
        "Intersection": "交集 (重叠部分)",
        "Union": "并集 (所有喜欢球的人)",
        "Neither": "两者都不",
        "Both": "两者都"
    },
    
    "correct_answer": 10,
    "total": 30,
    "set_a": 20, # Soccer
    "set_b": 15, # Basketball
    "neither": 5
}

# --- 功能函数：绘制韦恩图 (保持不变，增加双语标签) ---
def plot_venn(highlight_overlap=False):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    circle_a = patches.Circle((0.35, 0.5), 0.3, alpha=0.5, color='#3498db', label='Soccer')
    circle_b = patches.Circle((0.65, 0.5), 0.3, alpha=0.5, color='#e74c3c', label='Basketball')
    
    ax.add_patch(circle_a)
    ax.add_patch(circle_b)
    
    # 双语标签
    ax.text(0.1, 0.9, f"Total (总数): {PROBLEM['total']}", fontsize=10)
    ax.text(0.2, 0.5, "Soccer\n(足球)", ha='center', color='white', fontweight='bold')
    ax.text(0.8, 0.5, "Basketball\n(篮球)", ha='center', color='white', fontweight='bold')
    ax.text(0.5, 0.15, f"Neither (都不): {PROBLEM['neither']}", ha='center', fontstyle='italic')

    if highlight_overlap:
        overlap = patches.Circle((0.5, 0.5), 0.05, color='#f1c40f', alpha=1, zorder=10)
        ax.add_patch(overlap)
        ax.text(0.5, 0.5, "Both\n(10)", ha='center', fontweight='bold')
        plt.title("Key Found: The Intersection! (找到钥匙：交集)", color='green')
    else:
        ax.text(0.5, 0.5, "?", ha='center', fontsize=14)
        plt.title("Venn Diagram Model (韦恩图模型)")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# --- 核心逻辑：双语诊断引擎 ---
def analyze_input(user_input):
    try:
        val = int(user_input)
    except:
        return "这不是一个数字。Please enter an integer.", "error"

    if val == PROBLEM['correct_answer']:
        # 回复中夹杂英文术语
        return "✨ Excellent! 完全正确。\n\n你成功找到了 **Intersection (交集)**。\n逻辑是：Total - Neither = Union (真正玩球的人)，然后用容斥原理算出重叠部分。", "success"
    
    elif val == PROBLEM['set_a'] + PROBLEM['set_b']:
        return f"🤔 你算出了 {val}。\n\n想一想，Total (总人数) 才 {PROBLEM['total']} 人。\n如果直接相加，那些 **Both (两种都喜欢)** 的同学是不是被数了两次？", "hint"
    
    elif val == (PROBLEM['set_a'] + PROBLEM['set_b'] - PROBLEM['total']):
        return f"👀 Close! 很接近了。\n\n但是你忘记了那些 **Neither (两种都不喜欢)** 的同学。\n计算 **Union (并集)** 时，要先从总人数里减去那些不玩球的人哦。", "hint"
    
    else:
        return "💡 答案不太对。让我们看右边的图。\n试着把 **Soccer** 和 **Basketball** 的圆圈想象成两张贴纸，贴在白板上...", "hint"

# --- 界面构建 (UI) ---

# 1. 侧边栏：单词卡 + 进度
st.sidebar.header("🔑 Key Vocabulary (本题钥匙)")
for en, cn in PROBLEM['vocab'].items():
    st.sidebar.markdown(f"**{en}**: {cn}")

st.sidebar.divider()
st.sidebar.markdown("### 🗺️ Level Progress")
st.sidebar.markdown("✅ Level 1-2: Arithmetic")
st.sidebar.markdown("👉 **Level 3: Word Problems**")

# 2. 主区域
st.title("AMC 8 AI Coach")
st.caption("双语思维训练 | Bilingual Thinking Training")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("🧩 The Challenge")
    # 使用 HTML 渲染中英双语格式
    st.markdown(f"<div class='en-text'>{PROBLEM['question_en']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='cn-text'>💡 提示：{PROBLEM['question_cn']}</div>", unsafe_allow_html=True)
    
    st.divider()

    # 聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": "Ready? Try to solve this logic puzzle. 我会根据你的思路提供双语提示。"}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your answer here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        response_text, status = analyze_input(user_input)
        
        st.session_state.messages.append({"role": "ai", "content": response_text})
        with st.chat_message("ai"):
            st.markdown(response_text) # 支持 markdown 粗体
            
        st.session_state.last_status = status

with col2:
    st.markdown("#### 🎨 Interactive Whiteboard")
    current_status = st.session_state.get('last_status', 'normal')
    is_correct = (current_status == 'success')
    fig = plot_venn(highlight_overlap=is_correct)
    st.pyplot(fig)
    
    if current_status == 'hint':
        st.info("💡 Tip: 注意看左侧的粗体英文单词。")
