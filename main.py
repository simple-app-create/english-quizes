#!/usr/bin/env python3
"""
English Quiz App - Streamlit Web GUI

A web-based GUI for the English Language Arts quiz application using Streamlit.
"""

import streamlit as st
import yaml
import random
import time
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union
from quiz_manager import QuizManager, Quiz, Question
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
    """Load all available quiz topics from the quizzes directory"""
    quizzes_dir = Path("quizzes")

    if not quizzes_dir.exists():
        # Create sample quizzes if directory doesn't exist
        try:
            quizzes_dir.mkdir()
            quiz_manager = QuizManager()
            quiz_manager.create_sample_quiz()
        except Exception as e:
            st.error(f"Error creating quizzes directory: {e}")
            return {}

    # Get all YAML files in the quizzes directory
    yaml_files = list(quizzes_dir.glob("*.yaml")) + list(quizzes_dir.glob("*.yml"))

    quiz_topics = {}
    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                quiz_data = yaml.safe_load(file)
                if 'quiz_metadata' in quiz_data:
                    title = quiz_data['quiz_metadata'].get('title', file_path.stem)
                    quiz_topics[title] = {
                        'path': str(file_path),
                        'topic': file_path.stem,
                        'count': len(quiz_data.get('questions', []))
                    }
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")

    return quiz_topics


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

    # Load available quiz topics
    available_topics = load_available_quizzes()

    if not available_topics:
        st.error(get_text('no_quiz_files', lang))
        return

    # Display available topics with question counts
    st.markdown(get_text('available_topics', lang))
    for title, topic_info in available_topics.items():
        st.markdown(f"- **{title}** ({topic_info['count']} {get_text('questions_unit', lang)})")

    # Topic selection for loading
    selected_topic_title = st.selectbox(
        get_text('select_topic_to_load', lang),
        options=[get_text('all_topics', lang)] + list(available_topics.keys()),
        help=get_text('select_topic_help', lang)
    )

    if st.button(get_text('load_selected_topics', lang), type="primary"):
        try:
            if selected_topic_title == get_text('all_topics', lang):
                # Load all topics
                topics = list(available_topics.keys())
                st.session_state.current_quiz = st.session_state.quiz_manager.load_quiz_from_file(topics=topics)
                st.success(get_text('loaded_all_topics', lang, count=len(st.session_state.current_quiz.questions)))
            else:
                # Load specific topic
                topic = available_topics[selected_topic_title]['topic']
                st.session_state.current_quiz = st.session_state.quiz_manager.load_quiz_from_file(topics=topic)
                st.success(get_text('loaded_topic', lang, topic=selected_topic_title, count=len(st.session_state.current_quiz.questions)))
        except Exception as e:
            st.error(get_text('error_loading', lang) + str(e))

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

    available_topics = load_available_quizzes()

    if not available_topics:
        st.error("No quiz topics found!")
        if st.button("Create Sample Quizzes"):
            try:
                quiz_manager = QuizManager()
                quiz_manager.create_sample_quiz()
                st.success("Sample quizzes created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating sample quizzes: {e}")
        return

    # Group topics by first letter for better organization
    topics_by_letter = {}
    for title, info in available_topics.items():
        first_letter = title[0].upper()
        if first_letter not in topics_by_letter:
            topics_by_letter[first_letter] = []
        topics_by_letter[first_letter].append((title, info))

    # Display topics in alphabetical order
    for letter in sorted(topics_by_letter.keys()):
        st.markdown(f"### {letter}")
        cols = st.columns(2)  # Two columns for better layout

        for i, (title, info) in enumerate(sorted(topics_by_letter[letter], key=lambda x: x[0].lower())):
            with cols[i % 2]:
                if st.button(
                    f"📖 {title} ({info['count']} questions)",
                    key=f"topic_{title}",
                    use_container_width=True,
                    help=f"Practice {title} questions"
                ):
                    try:
                        st.session_state.quiz_manager = QuizManager()
                        st.session_state.current_quiz = st.session_state.quiz_manager.load_quiz_from_file(topics=info['topic'])
                        st.session_state.selected_topic = title
                        start_quiz_mode('topic')
                    except Exception as e:
                        st.error(f"Error loading topic: {e}")

    st.markdown("---")
    if st.button("⬅️ Back to Options", use_container_width=True):
        st.session_state.screen = 'options'
        st.rerun()


def show_difficulty_selection():
    """Show difficulty selection screen"""
    st.markdown("# ⚡ Practice by Difficulty")

    available_topics = load_available_quizzes()

    if not available_topics:
        st.error("No quiz topics found!")
        if st.button("Create Sample Quizzes"):
            try:
                quiz_manager = QuizManager()
                quiz_manager.create_sample_quiz()
                st.success("Sample quizzes created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating sample quizzes: {e}")
        return

    # Define difficulty levels and their display properties
    difficulty_levels = {
        'easy': {
            'emoji': '🟢',
            'description': 'Beginner level questions',
            'color': 'green'
        },
        'medium': {
            'emoji': '🟡',
            'description': 'Intermediate level questions',
            'color': 'orange'
        },
        'hard': {
            'emoji': '🔴',
            'description': 'Advanced level questions',
            'color': 'red'
        }
    }

    # Count questions per difficulty across all topics
    difficulty_counts = {level: 0 for level in difficulty_levels}

    # Load questions from all topics to count difficulties
    try:
        quiz_manager = QuizManager()
        all_questions = quiz_manager.load_questions()
        for question in all_questions.questions:
            if question.difficulty in difficulty_counts:
                difficulty_counts[question.difficulty] += 1
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        return

    # Display difficulty levels
    st.markdown("### Select Difficulty Level:")

    for level, props in difficulty_levels.items():
        count = difficulty_counts.get(level, 0)
        if count > 0:  # Only show difficulties that have questions
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(
                    f"{props['emoji']} {level.title()}",
                    key=f"diff_{level}",
                    use_container_width=True,
                    help=props['description']
                ):
                    try:
                        st.session_state.quiz_manager = QuizManager()
                        st.session_state.current_quiz = st.session_state.quiz_manager.load_quiz_from_file()
                        st.session_state.selected_difficulty = level
                        start_quiz_mode('difficulty')
                    except Exception as e:
                        st.error(f"Error loading questions: {e}")
            with col2:
                st.markdown(f"*{count} questions*")

    st.markdown("---")
    if st.button("⬅️ Back to Options", use_container_width=True):
        st.session_state.screen = 'options'
        st.rerun()


def start_quiz_mode(mode):
    """Start a quiz in the specified mode"""
    if not hasattr(st.session_state, 'current_quiz') or not st.session_state.current_quiz:
        st.error("No quiz loaded! Please load a quiz first.")
        return

    try:
        # Get questions based on mode
        if mode == 'topic' and hasattr(st.session_state, 'selected_topic') and st.session_state.selected_topic:
            questions = [q for q in st.session_state.current_quiz.questions
                       if q.topic.lower() == st.session_state.selected_topic.lower()]
            if not questions:
                st.error(f"No questions found for topic: {st.session_state.selected_topic}")
                return

        elif mode == 'difficulty' and hasattr(st.session_state, 'selected_difficulty') and st.session_state.selected_difficulty:
            questions = [q for q in st.session_state.current_quiz.questions
                       if q.difficulty.lower() == st.session_state.selected_difficulty.lower()]
            if not questions:
                st.error(f"No {st.session_state.selected_difficulty} questions found.")
                return

        else:  # Full quiz mode
            questions = st.session_state.current_quiz.questions
            if not questions:
                st.error("No questions available in the loaded quiz.")
                return

        # Shuffle questions
        random.shuffle(questions)

        # Initialize quiz state
        st.session_state.quiz_questions = questions
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.answered_questions = 0
        st.session_state.quiz_mode = mode
        st.session_state.quiz_answers = {}
        st.session_state.quiz_feedback = {}
        st.session_state.quiz_start_time = time.time()

        # Store question IDs for tracking
        st.session_state.question_ids = [q.id for q in questions]

        # Move to quiz screen
        st.session_state.screen = 'quiz'
        st.rerun()

    except Exception as e:
        st.error(f"Error starting quiz: {str(e)}")
        st.exception(e)  # This will show the full traceback in the UI for debugging
        return


def show_quiz_screen():
    """Display the quiz taking screen"""
    # Initialize quiz state if not exists
    if not hasattr(st.session_state, 'quiz_questions') or not st.session_state.quiz_questions:
        st.error("No questions available! Please start a new quiz.")
        if st.button("Back to Options"):
            st.session_state.screen = 'options'
            st.rerun()
        return

    total_questions = len(st.session_state.quiz_questions)
    current_index = st.session_state.current_question_index

    # Check if we've reached the end of the quiz
    if current_index >= total_questions:
        show_quiz_results()
        return

    question = st.session_state.quiz_questions[current_index]

    # Calculate time spent
    time_spent = time.time() - st.session_state.quiz_start_time
    minutes, seconds = divmod(int(time_spent), 60)

    # Display progress and stats
    st.markdown("### 📊 Quiz Progress")

    # Progress bar
    progress = (current_index) / total_questions
    st.progress(progress)

    # Stats columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Question", f"{current_index + 1} of {total_questions}")
    with col2:
        st.metric("Score", f"{st.session_state.score} / {st.session_state.answered_questions}")
    with col3:
        accuracy = (st.session_state.score / st.session_state.answered_questions * 100) if st.session_state.answered_questions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col4:
        st.metric("Time Spent", f"{minutes:02d}:{seconds:02d}")

    st.markdown("---")

    # Question display with better formatting
    st.markdown(f"""
    <div class="quiz-question">
        <h3>Question {current_index + 1}</h3>
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <span class="badge">Topic: {question.topic}</span>
            <span class="badge">Difficulty: {question.difficulty.title()}</span>
        </div>

        {f'<div class="passage"><strong>📖 Passage:</strong><div class="passage-content">{question.passage}</div></div><hr>' if question.passage else ''}
    """, unsafe_allow_html=True)

    # Display the question and answer choices in a single form
    with st.form(key='quiz_form'):
        # Display the question
        st.markdown(f"<p>❓ {question.question}</p>", unsafe_allow_html=True)

        # Display answer choices as radio buttons
        options = question.choices
        user_answer = st.radio(
            "Select your answer:",
            options=options,
            key=f"question_{current_index}",
            index=None
        )

        # Submit and navigation buttons
        col1, col2 = st.columns([1, 2])

        with col1:
            submitted = st.form_submit_button("Submit Answer", type="primary")

        with col2:
            if st.form_submit_button("Quit Quiz", type="secondary"):
                if st.session_state.answered_questions > 0:
                    show_quiz_results()
                else:
                    st.session_state.screen = 'options'
                    st.rerun()

        if submitted:
            if user_answer is None:
                st.warning("Please select an answer before submitting.")
            else:
                # Check if answer is correct
                is_correct = (user_answer == options[question.correct_answer])

                # Update score
                if is_correct:
                    st.session_state.score += 1
                st.session_state.answered_questions += 1

                # Store answer and feedback
                st.session_state.quiz_answers[current_index] = {
                    'question': question.question,
                    'user_answer': user_answer,
                    'correct_answer': options[question.correct_answer],
                    'is_correct': is_correct,
                    'explanation': question.get_explanation(st.session_state.language) if hasattr(question, 'get_explanation') else None
                }

                # Move to next question or show results
                if current_index + 1 < total_questions:
                    st.session_state.current_question_index += 1
                    st.rerun()
                else:
                    show_quiz_results()

    # Display explanation for previous question if available
    if current_index > 0 and (current_index - 1) in st.session_state.quiz_answers:
        prev_answer = st.session_state.quiz_answers[current_index - 1]

        if prev_answer['is_correct']:
            st.success("✅ Correct! " + (prev_answer['explanation'] or "Great job!"))
        else:
            st.error(f"❌ Incorrect. The correct answer is: **{prev_answer['correct_answer']}**")
            if prev_answer['explanation']:
                st.info(f"💡 {prev_answer['explanation']}")

        st.markdown("---")


def show_quiz_results():
    """Display quiz results and statistics"""
    st.markdown("# 🏆 Quiz Results")

    total_questions = len(st.session_state.quiz_questions)
    attempted = st.session_state.answered_questions
    score = st.session_state.score

    if attempted == 0:
        st.warning("No questions were answered. Please try again!")
        if st.button("Back to Options"):
            st.session_state.screen = 'options'
            st.rerun()
        return

    # Calculate statistics
    accuracy = (score / attempted) * 100
    time_spent_seconds = time.time() - st.session_state.quiz_start_time
    minutes, seconds = divmod(int(time_spent_seconds), 60)

    # Display overall results
    st.markdown("## 📊 Quiz Summary")

    # Main metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Questions Attempted", f"{attempted} / {total_questions}")
    with col2:
        st.metric("Correct Answers", score)
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col4:
        st.metric("Time Spent", f"{minutes:02d}:{seconds:02d}")

    # Progress bar for correct answers
    st.markdown("### Performance")
    st.progress(score / total_questions)

    # Detailed breakdown
    st.markdown("### 📝 Question Breakdown")

    # Group questions by topic and difficulty
    topic_stats = {}
    difficulty_stats = {'easy': {'correct': 0, 'total': 0},
                        'medium': {'correct': 0, 'total': 0},
                        'hard': {'correct': 0, 'total': 0}}

    # Calculate statistics
    for i, question in enumerate(st.session_state.quiz_questions):
        # Topic stats
        topic = question.topic
        if topic not in topic_stats:
            topic_stats[topic] = {'correct': 0, 'total': 0}

        topic_stats[topic]['total'] += 1

        # Check if this question was answered
        if i in st.session_state.quiz_answers:
            if st.session_state.quiz_answers[i]['is_correct']:
                topic_stats[topic]['correct'] += 1

        # Difficulty stats
        difficulty = question.difficulty.lower()
        if difficulty in difficulty_stats:
            difficulty_stats[difficulty]['total'] += 1
            if i in st.session_state.quiz_answers and st.session_state.quiz_answers[i]['is_correct']:
                difficulty_stats[difficulty]['correct'] += 1

    # Display topic performance
    st.markdown("#### 📚 By Topic")
    for topic, stats in topic_stats.items():
        if stats['total'] > 0:
            topic_accuracy = (stats['correct'] / stats['total']) * 100
            st.markdown(f"- **{topic}**: {stats['correct']}/{stats['total']} correct ({topic_accuracy:.1f}%)")

    # Display difficulty performance
    st.markdown("#### ⚡ By Difficulty")
    for difficulty, stats in difficulty_stats.items():
        if stats['total'] > 0:
            diff_accuracy = (stats['correct'] / stats['total']) * 100
            st.markdown(f"- **{difficulty.title()}**: {stats['correct']}/{stats['total']} correct ({diff_accuracy:.1f}%)")

    # Display review section
    st.markdown("### 🔍 Review Your Answers")

    for i, question in enumerate(st.session_state.quiz_questions):
        if i in st.session_state.quiz_answers:
            answer = st.session_state.quiz_answers[i]
            with st.expander(f"Question {i+1}: {question.question}"):
                st.markdown(f"**Your answer:** {answer['user_answer']}")
                st.markdown(f"**Correct answer:** {answer['correct_answer']}")
                if answer['explanation']:
                    st.markdown(f"**Explanation:** {answer['explanation']}")

    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("🔄 Restart Quiz", use_container_width=True):
            # Reset quiz state
            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.session_state.answered_questions = 0
            st.session_state.quiz_answers = {}
            st.session_state.quiz_start_time = time.time()
            st.rerun()

    with col2:
        if st.button("🏠 Back to Main Menu", use_container_width=True):
            st.session_state.screen = 'options'
            st.rerun()

    # Quiz metadata
    if hasattr(st.session_state, 'current_quiz') and st.session_state.current_quiz:
        st.markdown("---")
        st.markdown("### 📋 Quiz Information")
        st.write(f"**Quiz:** {st.session_state.current_quiz.quiz_metadata.title}")
        st.write(f"**Date:** {st.session_state.current_quiz.quiz_metadata.created_date}")

        if hasattr(st.session_state, 'quiz_mode'):
            if st.session_state.quiz_mode == 'topic' and hasattr(st.session_state, 'selected_topic'):
                st.write(f"**Practice Mode:** Topic - {st.session_state.selected_topic}")
            elif st.session_state.quiz_mode == 'difficulty' and hasattr(st.session_state, 'selected_difficulty'):
                st.write(f"**Practice Mode:** Difficulty - {st.session_state.selected_difficulty.title()}")
            else:
                st.write("**Mode:** Complete Quiz")

    st.markdown("---")
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

    # Load available quizzes if not already loaded
    available_topics = load_available_quizzes()

    if not available_topics:
        st.warning("No quiz data available. Please create some quizzes first.")
        if st.button("Create Sample Quizzes"):
            try:
                quiz_manager = QuizManager()
                quiz_manager.create_sample_quiz()
                st.success("Sample quizzes created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating sample quizzes: {e}")
        return

    # Load all questions to calculate statistics
    try:
        quiz_manager = QuizManager()
        all_questions = quiz_manager.load_questions()
        total_questions = len(all_questions.questions) if all_questions else 0

        st.metric("Total Questions Available", total_questions)
        st.metric("Topics Available", len(available_topics))

        if total_questions == 0:
            st.warning("No questions found in the quiz database.")
            return

        # Calculate topic distribution
        topic_counts = {}
        topic_difficulty = {}

        for q in all_questions.questions:
            # Count questions per topic
            if q.topic not in topic_counts:
                topic_counts[q.topic] = 0
                topic_difficulty[q.topic] = {'easy': 0, 'medium': 0, 'hard': 0}
            topic_counts[q.topic] += 1

            # Count questions per difficulty per topic
            difficulty = q.difficulty.lower()
            if difficulty in topic_difficulty[q.topic]:
                topic_difficulty[q.topic][difficulty] += 1

        # Display topic distribution
        st.markdown("## 📚 Topic Distribution")

        # Sort topics by question count (descending)
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

        # Create a DataFrame for better visualization
        import pandas as pd
        df = pd.DataFrame({
            'Topic': [t[0] for t in sorted_topics],
            'Total Questions': [t[1] for t in sorted_topics],
            'Easy': [topic_difficulty[t[0]]['easy'] for t in sorted_topics],
            'Medium': [topic_difficulty[t[0]]['medium'] for t in sorted_topics],
            'Hard': [topic_difficulty[t[0]]['hard'] for t in sorted_topics]
        })

        # Display the table
        st.dataframe(
            df,
            column_config={
                'Topic': 'Topic',
                'Total Questions': 'Total',
                'Easy': 'Easy',
                'Medium': 'Medium',
                'Hard': 'Hard'
            },
            hide_index=True,
            use_container_width=True
        )

        # Display difficulty distribution
        st.markdown("## ⚡ Difficulty Distribution")

        difficulty_counts = {
            'Easy': sum(1 for q in all_questions.questions if q.difficulty.lower() == 'easy'),
            'Medium': sum(1 for q in all_questions.questions if q.difficulty.lower() == 'medium'),
            'Hard': sum(1 for q in all_questions.questions if q.difficulty.lower() == 'hard')
        }

        # Create a pie chart
        import plotly.express as px

        if sum(difficulty_counts.values()) > 0:
            fig = px.pie(
                names=list(difficulty_counts.keys()),
                values=list(difficulty_counts.values()),
                title="Questions by Difficulty Level",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)

        # Add a button to refresh stats
        if st.button("🔄 Refresh Statistics"):
            st.rerun()

    except Exception as e:
        st.error(f"Error loading quiz statistics: {str(e)}")

    # Add a button to go back to options
    if st.button("⬅️ Back to Options"):
        st.session_state.screen = 'options'
        st.rerun()


def main():
    """Main Streamlit application"""
    initialize_session_state()



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
            index=list(available_langs.keys()).index(current_lang_display) if current_lang_display in available_langs else 0,
            help="選擇使用者介面語言 / Choose interface language"
        )

        # Update language if changed
        new_lang_code = available_langs[selected_lang_display]
        if new_lang_code != st.session_state.language:
            st.session_state.language = new_lang_code
            st.rerun()

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
