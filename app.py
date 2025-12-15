import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# --- 页面配置 ---
st.set_page_config(page_title="AMC 8: English & Français", layout="wide")

# --- 核心内容库 (增加了 solution_steps 和 video) ---
CONTENT = {
    "en": {
        "title": "AMC 8 Logic Master",
        "subtitle": "Bilingual Training: English & French",
        "sidebar_title": "🔐 The 8 Keys System",
        "sidebar_vocab": "📚 Key Vocabulary",
        "problem_title": "🧩 The Challenge",
        "input_label": "Your Answer (Integer)",
        "button_check": "Check Answer",
        "button_solution": "Show Step-by-Step Solution", # 新按钮
        "whiteboard": "🎨 Interactive Whiteboard",
        "question": "A class has 30 students. 20 students like **soccer**, 15 like **basketball**, and 5 like **neither**.\n\nHow many students like **both** sports?",
        "topic": "Sets & Intersection",
        "terms": {
            "Intersection": "Intersection (Overlap)",
            "Union": "Union (Total Group)",
            "Neither": "Neither"
        },
        "feedback_success": "Excellent! You found the Intersection.",
        "feedback_wrong": "Not quite. Don't worry, learning happens when we fix mistakes.",
        "solution_title": "📝 AI Teacher's Solution",
        "video_title": "📺 Video Explanation",
        "steps": [
            {
                "title": "Step 1: Find the 'Real Players'",
                "desc": "First, we remove the students who play **Neither** sport from the total.",
                "math": r"30 \text{ (Total)} - 5 \text{ (Neither)} = 25 \text{ (Real Players)}"
            },
            {
                "title": "Step 2: Add the Groups",
                "desc": "Next, add up the students who like Soccer and Basketball directly.",
                "math": r"20 \text{ (Soccer)} + 15 \text{ (Basketball)} = 35 \text{ (Sum of Lists)}"
            },
            {
                "title": "Step 3: Find the Overlap",
                "desc": "The sum (35) is larger than the real players (25). The difference is the students counted twice (the Intersection).",
                "math": r"35 - 25 = 10 \text{ (Both)}"
            }
        ],
        "video_url": "https://www.youtube.com/watch?v=massOa38KD8", # 示例：Khan Academy Venn Diagrams
        "labels": {"total": "Total", "soccer": "Soccer", "basketball": "Basket", "neither": "Neither", "both": "Both"}
    },
    "fr": {
        "title": "Maître de Logique AMC 8",
        "subtitle": "Entraînement Bilingue : Anglais & Français",
        "sidebar_title": "🔐 Système des 8 Clés",
        "sidebar_vocab": "📚 Vocabulaire Clé",
        "problem_title": "🧩 Le Défi",
        "input_label": "Votre Réponse (Entier)",
        "button_check": "Vérifier",
        "button_solution": "Voir la Solution Détaillée", # 新按钮
        "whiteboard": "🎨 Tableau Interactif",
        "question": "Une classe compte 30 élèves. 20 élèves aiment le **foot**, 15 aiment le **basket**, et 5 n'aiment **aucun** des deux.\n\nCombien d'élèves aiment les **deux** sports ?",
        "topic": "Ensembles & Intersection",
        "terms": {
            "Intersection": "Intersection (Chevauchement)",
            "Union": "Réunion (Groupe Total)",
            "Neither": "Ni l'un ni l'autre"
        },
        "feedback_success": "Bravo ! Tu as trouvé l'Intersection.",
        "feedback_wrong": "Pas tout à fait. Ne t'inquiète pas, c'est en se trompant qu'on apprend.",
        "solution_title": "📝 La Solution du Prof AI",
        "video_title": "📺 Explication Vidéo",
        "steps": [
            {
                "title": "Étape 1 : Trouver les 'Vrais Joueurs'",
                "desc": "D'abord, on retire du total les élèves qui n'aiment **Aucun** sport.",
                "math": r"30 \text{ (Total)} - 5 \text{ (Aucun)} = 25 \text{ (Vrais Joueurs)}"
            },
            {
                "title": "Étape 2 : Additionner les Groupes",
                "desc": "Ensuite, on additionne directement les élèves du Foot et du Basket.",
                "math": r"20 \text{ (Foot)} + 15 \text{ (Basket)} = 35 \text{ (Somme brute)}"
            },
            {
                "title": "Étape 3 : Trouver le Chevauchement",
                "desc": "La somme (35) est plus grande que le nombre de joueurs (25). La différence correspond aux élèves comptés deux fois.",
                "math": r"35 - 25 = 10 \text{ (Les deux)}"
            }
        ],
        "video_url": "https://www.youtube.com/watch?v=massOa38KD8",
        "labels": {"total": "Total", "soccer": "Foot", "basketball": "Basket", "neither": "Aucun", "both": "Les deux"}
    }
}

PROBLEM_DATA = {"correct_answer": 10, "total": 30, "set_a": 20, "set_b": 15, "neither": 5}

# --- 绘图函数 (保持不变) ---
def plot_venn(state, lang_code):
    fig, ax = plt.subplots(figsize=(6, 4))
    txt = CONTENT[lang_code]["labels"]
    
    circle_a = patches.Circle((0.35, 0.5), 0.3, alpha=0.5, color='#3B82F6', label=txt['soccer'])
    circle_b = patches.Circle((0.65, 0.5), 0.3, alpha=0.5, color='#EF4444', label=txt['basketball'])
    ax.add_patch(circle_a)
    ax.add_patch(circle_b)
    
    ax.text(0.1, 0.9, f"{txt['total']}: 30", fontsize=10, weight='bold')
    ax.text(0.2, 0.5, f"{txt['soccer']}\n(20)", ha='center', color='white', weight='bold')
    ax.text(0.8, 0.5, f"{txt['basketball']}\n(15)", ha='center', color='white', weight='bold')
    ax.text(0.5, 0.15, f"{txt['neither']}: 5", ha='center', fontstyle='italic')

    if state == 'success':
        overlap = patches.Circle((0.5, 0.5), 0.05, color='#F59E0B', alpha=1, zorder=10)
        ax.add_patch(overlap)
        ax.text(0.5, 0.5, "10", ha='center', weight='bold', fontsize=12)
        plt.title(f"✅ {txt['both']} = 10", color='green', weight='bold')
    elif state == 'solution':
        # 在查看答案模式下，也显示正确结果
        overlap = patches.Circle((0.5, 0.5), 0.05, color='#F59E0B', alpha=1, zorder=10)
        ax.add_patch(overlap)
        ax.text(0.5, 0.5, "10", ha='center', weight='bold', fontsize=12)
        plt.title("Solution Mode", color='#6B7280', weight='bold')
    elif state == 'error':
        ax.text(0.5, 0.5, "?", ha='center', fontsize=20, color='red', weight='bold')
        plt.title("???", color='red')
    else:
        ax.text(0.5, 0.5, "?", ha='center', fontsize=14)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# --- 主逻辑 ---
def main():
    if 'status' not in st.session_state: st.session_state['status'] = 'start'
    if 'show_solution' not in st.session_state: st.session_state['show_solution'] = False

    with st.sidebar:
        st.markdown("### 🌍 Language / Langue")
        lang = st.radio("Choose Mode:", ("English 🇺🇸", "Français 🇫🇷"))
        lang_code = "en" if "English" in lang else "fr"
        c = CONTENT[lang_code]
        st.title(c["sidebar_title"])
        st.progress(35)
        st.markdown(f"### {c['sidebar_vocab']}")
        for k, v in c["terms"].items(): st.markdown(f"**{k}**: {v}")

    st.title(c["title"])
    st.caption(c["subtitle"])

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(f"### {c['problem_title']}")
        st.info(c["question"])
        
        user_input = st.number_input(c["input_label"], step=1, value=0)
        
        # 按钮逻辑
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button(c["button_check"], type="primary"):
                st.session_state['show_solution'] = False # 重置解析状态
                if user_input == PROBLEM_DATA['correct_answer']:
                    st.session_state['status'] = 'success'
                else:
                    st.session_state['status'] = 'error'

        # 状态反馈
        if st.session_state['status'] == 'success':
            st.success(c["feedback_success"])
        elif st.session_state['status'] == 'error':
            st.error(c["feedback_wrong"])
            # 只有答错了，才显示查看解析按钮
            with col_btn2:
                if st.button(c["button_solution"]):
                    st.session_state['show_solution'] = True
                    st.session_state['status'] = 'solution' # 更新状态以便绘图

        # --- 核心：详解区域 (无交互，纯输出) ---
        if st.session_state['show_solution']:
            st.markdown("---")
            st.markdown(f"### {c['solution_title']}")
            
            # 循环输出步骤
            for step in c["steps"]:
                with st.container():
                    st.markdown(f"**{step['title']}**")
                    st.write(step['desc'])
                    st.latex(step['math']) # 使用 Latex 显示公式，显得专业
                    st.markdown("") # 空行
            
            st.markdown("---")
            st.markdown(f"### {c['video_title']}")
            # 嵌入视频
            st.video(c["video_url"])

    with col2:
        st.markdown(f"### {c['whiteboard']}")
        fig = plot_venn(st.session_state['status'], lang_code)
        st.pyplot(fig)
        if st.session_state['status'] == 'success':
            st.balloons()

if __name__ == "__main__":
    main()
