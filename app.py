import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 页面配置 ---
st.set_page_config(page_title="AMC 8: English & Français", layout="wide")

# --- 语言资源包 (Language Dictionary) ---
# 这里是核心：所有的界面文本、题目、术语都做了双语映射
CONTENT = {
    "en": {
        "title": "AMC 8 Logic Master",
        "subtitle": "Bilingual Training: English & French",
        "sidebar_title": "🔐 The 8 Keys System",
        "sidebar_vocab": "📚 Key Vocabulary",
        "problem_title": "🧩 The Challenge",
        "input_label": "Your Answer (Integer)",
        "whiteboard": "🎨 Interactive Whiteboard",
        "question": "A class has 30 students. 20 students like **soccer**, 15 like **basketball**, and 5 like **neither**.\n\nHow many students like **both** sports?",
        "topic": "Sets & Intersection",
        "terms": {
            "Intersection": "Intersection (Overlap)",
            "Union": "Union (Total Group)",
            "Set": "Set (Collection)",
            "Neither": "Neither"
        },
        "feedback_success": "Excellent! You found the **Intersection**. Logic: Total (30) - Neither (5) = 25 real players.",
        "feedback_hint_sum": "Wait... 20 + 15 = 35. That's more than the class size (30)! Someone is counted twice.",
        "feedback_error": "Please enter a number.",
        "labels": {
            "total": "Total Students",
            "soccer": "Soccer",
            "basketball": "Basketball",
            "neither": "Neither",
            "both": "Both"
        }
    },
    "fr": {
        "title": "Maître de Logique AMC 8",
        "subtitle": "Entraînement Bilingue : Anglais & Français",
        "sidebar_title": "🔐 Système des 8 Clés",
        "sidebar_vocab": "📚 Vocabulaire Clé",
        "problem_title": "🧩 Le Défi",
        "input_label": "Votre Réponse (Entier)",
        "whiteboard": "🎨 Tableau Interactif",
        "question": "Une classe compte 30 élèves. 20 élèves aiment le **foot**, 15 aiment le **basket**, et 5 n'aiment **aucun** des deux.\n\nCombien d'élèves aiment les **deux** sports ?",
        "topic": "Ensembles & Intersection",
        "terms": {
            "Intersection": "Intersection (Chevauchement)",
            "Union": "Réunion (Groupe Total)",
            "Set": "Ensemble (Collection)",
            "Neither": "Ni l'un ni l'autre"
        },
        "feedback_success": "Bravo ! Tu as trouvé l'**Intersection**. Logique : Total (30) - Aucun (5) = 25 joueurs réels.",
        "feedback_hint_sum": "Attends... 20 + 15 = 35. C'est plus que la classe (30) ! Certains sont comptés deux fois.",
        "feedback_error": "Veuillez entrer un nombre.",
        "labels": {
            "total": "Total Élèves",
            "soccer": "Foot",
            "basketball": "Basket",
            "neither": "Aucun",
            "both": "Les deux"
        }
    }
}

# --- 题目逻辑参数 (数学是不变的) ---
PROBLEM_DATA = {
    "correct_answer": 10,
    "total": 30,
    "set_a": 20,
    "set_b": 15,
    "neither": 5
}

# --- 功能函数：绘制双语韦恩图 ---
def plot_venn(state, lang_code):
    fig, ax = plt.subplots(figsize=(6, 4))
    txt = CONTENT[lang_code]["labels"] # 获取对应语言的标签
    
    # 绘制圆
    circle_a = patches.Circle((0.35, 0.5), 0.3, alpha=0.5, color='#3B82F6', label=txt['soccer'])
    circle_b = patches.Circle((0.65, 0.5), 0.3, alpha=0.5, color='#EF4444', label=txt['basketball'])
    
    ax.add_patch(circle_a)
    ax.add_patch(circle_b)
    
    # 动态标签
    ax.text(0.1, 0.9, f"{txt['total']}: {PROBLEM_DATA['total']}", fontsize=10, weight='bold')
    ax.text(0.2, 0.5, f"{txt['soccer']}\n(20)", ha='center', color='white', weight='bold')
    ax.text(0.8, 0.5, f"{txt['basketball']}\n(15)", ha='center', color='white', weight='bold')
    ax.text(0.5, 0.15, f"{txt['neither']}: {PROBLEM_DATA['neither']}", ha='center', fontstyle='italic')

    # 状态反馈
    if state == 'success':
        overlap = patches.Circle((0.5, 0.5), 0.05, color='#F59E0B', alpha=1, zorder=10)
        ax.add_patch(overlap)
        ax.text(0.5, 0.5, "10", ha='center', weight='bold', fontsize=12)
        plt.title(f"✅ {txt['both']} = 10", color='green', weight='bold')
        
    elif state == 'hint_sum':
        plt.title("20 + 15 = 35 > 30 ??", color='red')
        
    else:
        ax.text(0.5, 0.5, "?", ha='center', fontsize=14)
        # 不显示标题，保持简洁

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# --- 主程序 ---
def main():
    # 1. 语言选择器 (放在侧边栏顶部)
    with st.sidebar:
        st.markdown("### 🌍 Language / Langue")
        lang = st.radio(
            "Choose Mode / Choisir le mode:",
            ("English 🇺🇸", "Français 🇫🇷")
        )
        # 将选项转换为代码 'en' 或 'fr'
        lang_code = "en" if "English" in lang else "fr"
        
        c = CONTENT[lang_code] # 加载当前语言的文本包

        st.title(c["sidebar_title"])
        st.progress(35)
        
        st.markdown(f"### {c['sidebar_vocab']}")
        for term, definition in c["terms"].items():
            st.markdown(f"**{term}**: {definition}")

    # 2. 主标题
    st.title(c["title"])
    st.caption(c["subtitle"])
    st.markdown(f"**Topic:** {c['topic']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {c['problem_title']}")
        st.info(c["question"]) # 显示题目
        
        # 交互区域
        user_input = st.number_input(c["input_label"], step=1, value=0)
        
        # 提交按钮 (Streamlit number_input 需要配合按钮使用更佳，或者直接回车)
        if user_input > 0:
            if user_input == PROBLEM_DATA['correct_answer']:
                st.success(c["feedback_success"])
                current_state = 'success'
            elif user_input == (PROBLEM_DATA['set_a'] + PROBLEM_DATA['set_b']):
                st.warning(c["feedback_hint_sum"])
                current_state = 'hint_sum'
            else:
                st.warning("Thinking... / Réfléchit...")
                current_state = 'error'
        else:
            current_state = 'start'

    with col2:
        st.markdown(f"### {c['whiteboard']}")
        # 传入语言代码，让图表也变成对应语言
        fig = plot_venn(current_state, lang_code)
        st.pyplot(fig)
        
        if current_state == 'success':
            st.balloons()

if __name__ == "__main__":
    main()
