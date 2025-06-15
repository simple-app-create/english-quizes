#!/usr/bin/env python3
"""
English Quiz App - Streamlit Web GUI

A web-based GUI for the English Language Arts quiz application using Streamlit.
"""

import streamlit as st
import yaml
import random
from pathlib import Path
from quiz_manager import QuizManager, Quiz
from translations import get_text, get_available_languages, get_language_display_name
from explanation_translator import get_translated_explanation


# Configure Streamlit page
st.set_page_config(
    page_title="English Quiz App",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_available_quizzes():
    """Load all available quiz files and their metadata"""
    quiz_files = {}
    yaml_files = list(Path(".").glob("*.yaml")) + list(Path(".").glob("*.yml"))
    
    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                quiz_data = yaml.safe_load(file)
                if 'quiz_metadata' in quiz_data:
                    title = quiz_data['quiz_metadata'].get('title', file_path.stem)
                    quiz_files[title] = str(file_path)
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
    
    return quiz_files


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'screen' not in st.session_state:
        st.session_state.screen = 'welcome'
    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answered_questions' not in st.session_state:
        st.session_state.answered_questions = 0
    if 'quiz_mode' not in st.session_state:
        st.session_state.quiz_mode = 'full'
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = None
    if 'language' not in st.session_state:
        st.session_state.language = 'zh_TW'  # Default to Traditional Chinese


def show_welcome_screen():
    """Display the welcome screen"""
    lang = st.session_state.language
    
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='font-size: 3rem; color: #1f77b4; margin-bottom: 2rem;'>
            {get_text('welcome_title', lang)}
        </h1>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 3rem;'>
            {get_text('welcome_subtitle', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(get_text('start_button', lang), type="primary", use_container_width=True):
            st.session_state.screen = 'options'
            st.rerun()


def show_options_screen():
    """Display the main options screen"""
    lang = st.session_state.language
    st.markdown(f"# {get_text('quiz_options', lang)}")
    
    # Quiz Selection
    st.markdown(f"## {get_text('select_quiz', lang)}")
    available_quizzes = load_available_quizzes()
    
    if not available_quizzes:
        st.error(get_text('no_quiz_files', lang))
        return
    
    selected_quiz_title = st.selectbox(
        get_text('choose_quiz', lang),
        options=list(available_quizzes.keys()),
        help=get_text('quiz_selection_help', lang)
    )
    
    if st.button(get_text('load_quiz', lang), type="secondary"):
        try:
            quiz_file = available_quizzes[selected_quiz_title]
            st.session_state.current_quiz = st.session_state.quiz_manager.load_quiz_from_file(quiz_file)
            st.success(f"{get_text('quiz_loaded', lang)}{selected_quiz_title}")
        except Exception as e:
            st.error(f"{get_text('error_loading', lang)}{e}")
    
    if st.session_state.current_quiz:
        st.markdown("---")
        st.markdown(f"## {get_text('quiz_modes', lang)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(get_text('complete_quiz', lang), use_container_width=True):
                start_quiz_mode('full')
            
            if st.button(get_text('practice_topic', lang), use_container_width=True):
                st.session_state.screen = 'topic_selection'
                st.rerun()
        
        with col2:
            if st.button(get_text('practice_difficulty', lang), use_container_width=True):
                st.session_state.screen = 'difficulty_selection'
                st.rerun()
            
            if st.button(get_text('view_stats', lang), use_container_width=True):
                st.session_state.screen = 'stats'
                st.rerun()


def show_topic_selection():
    """Show topic selection screen"""
    st.markdown("# 📚 Practice by Topic")
    
    if not st.session_state.current_quiz:
        st.error("No quiz loaded!")
        return
    
    topics = list(set(q.topic for q in st.session_state.current_quiz.questions))
    topic_counts = {topic: len([q for q in st.session_state.current_quiz.questions if q.topic == topic]) 
                   for topic in topics}
    
    st.markdown("### Available Topics:")
    for topic in topics:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"📖 {topic}", key=f"topic_{topic}", use_container_width=True):
                st.session_state.selected_topic = topic
                start_quiz_mode('topic')
        with col2:
            st.markdown(f"*{topic_counts[topic]} questions*")
    
    if st.button("⬅️ Back to Options"):
        st.session_state.screen = 'options'
        st.rerun()


def show_difficulty_selection():
    """Show difficulty selection screen"""
    st.markdown("# ⚡ Practice by Difficulty")
    
    if not st.session_state.current_quiz:
        st.error("No quiz loaded!")
        return
    
    difficulties = list(set(q.difficulty for q in st.session_state.current_quiz.questions))
    difficulty_counts = {diff: len([q for q in st.session_state.current_quiz.questions if q.difficulty == diff]) 
                        for diff in difficulties}
    
    # Order difficulties logically
    difficulty_order = ['easy', 'medium', 'hard']
    ordered_difficulties = [d for d in difficulty_order if d in difficulties]
    ordered_difficulties.extend([d for d in difficulties if d not in difficulty_order])
    
    st.markdown("### Available Difficulty Levels:")
    for difficulty in ordered_difficulties:
        col1, col2 = st.columns([3, 1])
        with col1:
            emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(difficulty, "⚪")
            if st.button(f"{emoji} {difficulty.title()}", key=f"diff_{difficulty}", use_container_width=True):
                st.session_state.selected_difficulty = difficulty
                start_quiz_mode('difficulty')
        with col2:
            st.markdown(f"*{difficulty_counts[difficulty]} questions*")
    
    if st.button("⬅️ Back to Options"):
        st.session_state.screen = 'options'
        st.rerun()


def start_quiz_mode(mode):
    """Start a quiz in the specified mode"""
    if not st.session_state.current_quiz:
        st.error("No quiz loaded!")
        return
    
    questions = st.session_state.current_quiz.questions.copy()
    
    if mode == 'topic' and st.session_state.selected_topic:
        questions = [q for q in questions if q.topic == st.session_state.selected_topic]
    elif mode == 'difficulty' and st.session_state.selected_difficulty:
        questions = [q for q in questions if q.difficulty == st.session_state.selected_difficulty]
    
    random.shuffle(questions)
    
    st.session_state.quiz_questions = questions
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.answered_questions = 0
    st.session_state.quiz_mode = mode
    st.session_state.screen = 'quiz'
    st.rerun()


def show_quiz_screen():
    """Display the quiz taking screen"""
    if not st.session_state.quiz_questions:
        st.error("No questions available!")
        return
    
    total_questions = len(st.session_state.quiz_questions)
    current_index = st.session_state.current_question_index
    
    if current_index >= total_questions:
        show_quiz_results()
        return
    
    question = st.session_state.quiz_questions[current_index]
    
    # Progress bar and stats
    progress = (current_index + 1) / total_questions
    st.progress(progress)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Question", f"{current_index + 1} / {total_questions}")
    with col2:
        st.metric("Score", f"{st.session_state.score} / {st.session_state.answered_questions}" if st.session_state.answered_questions > 0 else "0 / 0")
    with col3:
        accuracy = (st.session_state.score / st.session_state.answered_questions * 100) if st.session_state.answered_questions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    st.markdown("---")
    
    # Question display
    st.markdown(f"### Question {current_index + 1}")
    st.markdown(f"**Topic:** {question.topic} | **Difficulty:** {question.difficulty}")
    
    # Show passage if it exists
    if question.passage:
        st.markdown("#### 📖 Passage:")
        st.markdown(f"> {question.passage}")
        st.markdown("---")
    
    st.markdown(f"#### ❓ {question.question}")
    
    # Answer choices
    answer = st.radio(
        "Select your answer:",
        options=range(len(question.choices)),
        format_func=lambda x: f"{chr(65 + x)}. {question.choices[x]}",
        key=f"q_{current_index}"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Submit Answer", type="primary"):
            # Check answer
            st.session_state.answered_questions += 1
            if answer == question.correct_answer:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer was: {question.choices[question.correct_answer]}")
            
            # Show explanation in current language
            explanation = get_translated_explanation(question, st.session_state.language)
            if explanation:
                st.info(f"💡 **Explanation:** {explanation}")
            
            # Move to next question
            st.session_state.current_question_index += 1
            
            # Auto-advance after showing result
            if st.button("Next Question ➡️"):
                st.rerun()
    
    with col2:
        if st.button("End Quiz", type="secondary"):
            show_quiz_results()
    
    with col3:
        if st.button("⬅️ Back to Options"):
            st.session_state.screen = 'options'
            st.rerun()


def show_quiz_results():
    """Display quiz results and statistics"""
    st.markdown("# 🏆 Quiz Results")
    
    total_questions = len(st.session_state.quiz_questions)
    attempted = st.session_state.answered_questions
    score = st.session_state.score
    
    if attempted > 0:
        accuracy = (score / attempted) * 100
        
        # Results display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Questions Attempted", f"{attempted} / {total_questions}")
        with col2:
            st.metric("Correct Answers", score)
        with col3:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        # Performance feedback
        if accuracy >= 90:
            st.success("🌟 Excellent work! Outstanding performance!")
        elif accuracy >= 70:
            st.success("👍 Good job! Well done!")
        elif accuracy >= 50:
            st.warning("👌 Not bad! Keep practicing to improve!")
        else:
            st.error("📚 Keep studying! You'll get better with practice!")
        
        # Progress visualization
        st.markdown("### 📊 Performance Breakdown")
        correct_pct = (score / attempted) * 100
        incorrect_pct = 100 - correct_pct
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Correct:** {correct_pct:.1f}%")
            st.progress(correct_pct / 100)
        with col2:
            st.markdown(f"**Incorrect:** {incorrect_pct:.1f}%")
            st.progress(incorrect_pct / 100)
        
        if attempted < total_questions:
            remaining = total_questions - attempted
            st.info(f"📝 {remaining} questions remaining - try again to complete the full quiz!")
    else:
        st.warning("No questions were attempted.")
    
    # Quiz metadata
    if st.session_state.current_quiz:
        st.markdown("---")
        st.markdown("### 📋 Quiz Information")
        st.write(f"**Quiz:** {st.session_state.current_quiz.quiz_metadata.title}")
        st.write(f"**Date:** {st.session_state.current_quiz.quiz_metadata.created_date}")
        
        if st.session_state.quiz_mode == 'topic':
            st.write(f"**Practice Mode:** Topic - {st.session_state.selected_topic}")
        elif st.session_state.quiz_mode == 'difficulty':
            st.write(f"**Practice Mode:** Difficulty - {st.session_state.selected_difficulty.title()}")
        else:
            st.write(f"**Mode:** Complete Quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz", type="primary"):
            st.session_state.screen = 'options'
            st.rerun()
    with col2:
        if st.button("🏠 Back to Welcome", type="secondary"):
            st.session_state.screen = 'welcome'
            st.rerun()


def show_stats_screen():
    """Display quiz statistics"""
    st.markdown("# 📊 Quiz Statistics")
    
    if not st.session_state.current_quiz:
        st.error("No quiz loaded!")
        return
    
    stats = st.session_state.quiz_manager.get_quiz_stats()
    
    # General stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Questions", stats['total_questions'])
        st.metric("Quiz Title", stats['title'])
    
    # Topics breakdown
    st.markdown("### 📚 Questions by Topic")
    topics_data = stats['topics']
    for topic, count in topics_data.items():
        st.write(f"**{topic}:** {count} questions")
    
    # Difficulties breakdown
    st.markdown("### ⚡ Questions by Difficulty")
    difficulties_data = stats['difficulties']
    for difficulty, count in difficulties_data.items():
        emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(difficulty, "⚪")
        st.write(f"**{emoji} {difficulty.title()}:** {count} questions")
    
    if st.button("⬅️ Back to Options"):
        st.session_state.screen = 'options'
        st.rerun()


def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Sidebar with theme toggle and navigation
    with st.sidebar:
        lang = st.session_state.language
        st.markdown(f"# {get_text('quiz_app', lang)}")
        
        # Language selector
        st.markdown(get_text('language', lang))
        available_langs = get_available_languages()
        current_lang_display = get_language_display_name(st.session_state.language)
        
        selected_lang_display = st.selectbox(
            get_text('choose_language', lang),
            options=list(available_langs.keys()),
            index=list(available_langs.keys()).index(current_lang_display),
            help="選擇界面語言 / Choose interface language"
        )
        
        # Update language if changed
        new_lang_code = available_langs[selected_lang_display]
        if new_lang_code != st.session_state.language:
            st.session_state.language = new_lang_code
            st.rerun()
        
        st.markdown("---")
        
        # Theme toggle (placeholder - Streamlit doesn't have built-in dark mode toggle)
        st.markdown(get_text('theme', lang))
        theme_options = [get_text('light', lang), get_text('dark', lang)]
        theme = st.selectbox(get_text('choose_theme', lang), theme_options, help="Theme selection (visual indication)")
        if theme == get_text('dark', lang):
            st.markdown(f"*{get_text('theme_selected', lang)}*")
        
        st.markdown("---")
        
        # Navigation
        st.markdown(get_text('navigation', lang))
        if st.button(get_text('home', lang)):
            st.session_state.screen = 'welcome'
            st.rerun()
        
        if st.button(get_text('options', lang)) and st.session_state.current_quiz:
            st.session_state.screen = 'options'
            st.rerun()
        
        # Current quiz info
        if st.session_state.current_quiz:
            st.markdown(get_text('current_quiz', lang))
            st.write(f"{get_text('title', lang)}{st.session_state.current_quiz.quiz_metadata.title}")
            st.write(f"{get_text('questions', lang)}{len(st.session_state.current_quiz.questions)}")
    
    # Main content based on current screen
    if st.session_state.screen == 'welcome':
        show_welcome_screen()
    elif st.session_state.screen == 'options':
        show_options_screen()
    elif st.session_state.screen == 'topic_selection':
        show_topic_selection()
    elif st.session_state.screen == 'difficulty_selection':
        show_difficulty_selection()
    elif st.session_state.screen == 'quiz':
        show_quiz_screen()
    elif st.session_state.screen == 'stats':
        show_stats_screen()


if __name__ == "__main__":
    main()
