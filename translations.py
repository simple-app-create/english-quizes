"""
Translation module for English Quiz App

Supports Traditional Chinese (default) and English UI languages.
"""

try:
    from googletrans import Translator
    TRANSLATOR = Translator()
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    TRANSLATOR = None
    GOOGLETRANS_AVAILABLE = False

TRANSLATIONS = {
    "zh_TW": {  # Traditional Chinese
        # Main titles and headers
        "app_title": "英語測驗應用程式",
        "welcome_title": "🎓 歡迎使用英語測驗應用程式",
        "welcome_subtitle": "透過互動式測驗測試您的英語語言藝術知識，涵蓋閱讀理解、語法、拼字等！",
        "start_button": "🚀 開始測驗",
        
        # Options screen
        "quiz_options": "🎯 測驗選項",
        "select_quiz": "📚 選擇測驗",
        "choose_quiz": "選擇要進行的測驗：",
        "quiz_selection_help": "從可用的測驗集合中選擇",
        "load_quiz": "載入測驗",
        "quiz_loaded": "✅ 已載入：",
        "quiz_modes": "🎮 測驗模式",
        "complete_quiz": "📖 完整測驗",
        "practice_topic": "🎯 依主題練習",
        "practice_difficulty": "⚡ 依難度練習",
        "view_stats": "📊 查看測驗統計",
        
        # Topic selection
        "practice_by_topic": "📚 依主題練習",
        "available_topics": "### 可用主題：",
        "select_topic_to_load": "選擇要載入的主題：",
        "all_topics": "所有主題",
        "load_selected_topics": "載入選定的主題",
        "loaded_all_topics": "已載入所有主題，共 {count} 題",
        "loaded_topic": "已載入 {topic}，共 {count} 題",
        "select_topic_help": "選擇特定主題或「所有主題」來載入全部內容",
        "back_to_options": "⬅️ 返回選項",
        
        # Quiz results buttons
        "restart_same_quiz": "🔄 重新開始相同測驗",
        "choose_new_quiz": "📚 選擇新測驗",
        
        # Common UI strings
        "loading": "載入中...",
        "please_wait": "請稍候...",
        "success": "成功！",
        "failed": "失敗",
        "retry": "重試",
        "cancel": "取消",
        "confirm": "確認",
        "close": "關閉",
        "save": "儲存",
        "delete": "刪除",
        "edit": "編輯",
        "view": "檢視",
        "help": "幫助",
        "about": "關於",
        "settings": "設定",
        
        # Difficulty selection
        "practice_by_difficulty": "⚡ 依難度練習",
        "available_difficulties": "### 可用難度等級：",
        "easy": "簡單",
        "medium": "中等",
        "hard": "困難",
        
        # Quiz screen
        "question": "問題",
        "score": "分數",
        "accuracy": "準確率",
        "topic": "主題",
        "difficulty": "難度",
        "passage": "📖 段落：",
        "select_answer": "選擇您的答案：",
        "submit_answer": "提交答案",
        "end_quiz": "結束測驗",
        "next_question": "下一題 ➡️",
        "correct": "✅ 正確！",
        "incorrect": "❌ 錯誤。正確答案是：",
        "explanation": "💡 **解釋：**",
        
        # Results screen
        "quiz_results": "🏆 測驗結果",
        "questions_attempted": "已作答題數",
        "correct_answers": "正確答案",
        "excellent": "🌟 優秀的表現！傑出的成績！",
        "good": "👍 做得很好！表現不錯！",
        "not_bad": "👌 還不錯！繼續練習來提升！",
        "keep_studying": "📚 繼續學習！練習會讓您進步！",
        "performance_breakdown": "### 📊 表現分析",
        "correct": "正確：",
        "incorrect_pct": "錯誤：",
        "questions_remaining": "📝 還有 {0} 題 - 再試一次完成整個測驗！",
        "no_questions_attempted": "沒有作答任何題目。",
        "quiz_info": "### 📋 測驗資訊",
        "quiz": "測驗：",
        "date": "日期：",
        "practice_mode": "練習模式：",
        "topic_mode": "主題 - ",
        "difficulty_mode": "難度 - ",
        "complete_mode": "完整測驗",
        "take_another": "🔄 進行其他測驗",
        "back_to_welcome": "🏠 返回歡迎頁面",
        
        # Stats screen
        "quiz_statistics": "📊 測驗統計",
        "total_questions": "總題數",
        "quiz_title": "測驗標題",
        "questions_by_topic": "### 📚 依主題分類的題目",
        "questions_by_difficulty": "### ⚡ 依難度分類的題目",
        
        # Sidebar
        "quiz_app": "🎓 測驗應用程式",
        "theme": "🎨 主題",
        "choose_theme": "選擇主題：",
        "light": "淺色",
        "dark": "深色",
        "theme_selected": "*已選擇深色主題（僅顯示）*",
        "navigation": "### 🧭 導航",
        "home": "🏠 首頁",
        "options": "⚙️ 選項",
        "current_quiz": "### 📋 目前測驗",
        "title": "**標題：** ",
        "questions": "**題目：** ",
        
        # Language
        "language": "### 🌐 語言",
        "choose_language": "選擇語言：",
        "traditional_chinese": "繁體中文",
        "english": "English",
        
        # Error messages
        "no_quiz_files": "找不到測驗檔案！請確保目前目錄中有 YAML 測驗檔案。",
        "no_quiz_loaded": "沒有載入測驗！",
        "error_loading": "載入時發生錯誤：",
        "no_questions_available": "沒有可用的題目！",
        
        # Units
        "questions_unit": "題"
    },
    
    "en": {  # English
        # Main titles and headers
        "app_title": "English Quiz App",
        "welcome_title": "🎓 Welcome to English Quiz App",
        "welcome_subtitle": "Test your English Language Arts knowledge with interactive quizzes covering Reading Comprehension, Grammar, Spelling, and more!",
        "start_button": "🚀 Start Quiz",
        
        # Options screen
        "quiz_options": "🎯 Quiz Options",
        "select_quiz": "📚 Select a Quiz",
        "choose_quiz": "Choose a quiz to take:",
        "quiz_selection_help": "Select from available quiz collections",
        "load_quiz": "Load Quiz",
        "quiz_loaded": "✅ Loaded: ",
        "quiz_modes": "🎮 Quiz Modes",
        "complete_quiz": "📖 Complete Quiz",
        "practice_topic": "🎯 Practice by Topic",
        "practice_difficulty": "⚡ Practice by Difficulty",
        "view_stats": "📊 View Quiz Stats",
        
        # Topic selection
        "practice_by_topic": "📚 Practice by Topic",
        "available_topics": "### Available Topics:",
        "select_topic_to_load": "Select a topic to load:",
        "all_topics": "All Topics",
        "load_selected_topics": "Load Selected Topics",
        "loaded_all_topics": "Loaded all topics with {count} questions",
        "loaded_topic": "Loaded {topic} with {count} questions",
        "select_topic_help": "Select a specific topic or 'All Topics' to load everything",
        "back_to_options": "⬅️ Back to Options",
        
        # Quiz results buttons
        "restart_same_quiz": "🔄 Restart Same Quiz",
        "choose_new_quiz": "📚 Choose New Quiz",
        
        # Common UI strings
        "loading": "Loading...",
        "please_wait": "Please wait...",
        "success": "Success!",
        "failed": "Failed",
        "retry": "Retry",
        "cancel": "Cancel",
        "confirm": "Confirm",
        "close": "Close",
        "save": "Save",
        "delete": "Delete",
        "edit": "Edit",
        "view": "View",
        "help": "Help",
        "about": "About",
        "settings": "Settings",
        
        # Difficulty selection
        "practice_by_difficulty": "⚡ Practice by Difficulty",
        "available_difficulties": "### Available Difficulty Levels:",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        
        # Quiz screen
        "question": "Question",
        "score": "Score",
        "accuracy": "Accuracy",
        "topic": "Topic",
        "difficulty": "Difficulty",
        "passage": "📖 Passage:",
        "select_answer": "Select your answer:",
        "submit_answer": "Submit Answer",
        "end_quiz": "End Quiz",
        "next_question": "Next Question ➡️",
        "correct": "✅ Correct!",
        "incorrect": "❌ Incorrect. The correct answer was: ",
        "explanation": "💡 **Explanation:** ",
        
        # Results screen
        "quiz_results": "🏆 Quiz Results",
        "questions_attempted": "Questions Attempted",
        "correct_answers": "Correct Answers",
        "excellent": "🌟 Excellent work! Outstanding performance!",
        "good": "👍 Good job! Well done!",
        "not_bad": "👌 Not bad! Keep practicing to improve!",
        "keep_studying": "📚 Keep studying! You'll get better with practice!",
        "performance_breakdown": "### 📊 Performance Breakdown",
        "correct": "Correct: ",
        "incorrect_pct": "Incorrect: ",
        "questions_remaining": "📝 {0} questions remaining - try again to complete the full quiz!",
        "no_questions_attempted": "No questions were attempted.",
        "quiz_info": "### 📋 Quiz Information",
        "quiz": "Quiz: ",
        "date": "Date: ",
        "practice_mode": "Practice Mode: ",
        "topic_mode": "Topic - ",
        "difficulty_mode": "Difficulty - ",
        "complete_mode": "Complete Quiz",
        "take_another": "🔄 Take Another Quiz",
        "back_to_welcome": "🏠 Back to Welcome",
        
        # Stats screen
        "quiz_statistics": "📊 Quiz Statistics",
        "total_questions": "Total Questions",
        "quiz_title": "Quiz Title",
        "questions_by_topic": "### 📚 Questions by Topic",
        "questions_by_difficulty": "### ⚡ Questions by Difficulty",
        
        # Sidebar
        "quiz_app": "🎓 Quiz App",
        "theme": "🎨 Theme",
        "choose_theme": "Choose theme:",
        "light": "Light",
        "dark": "Dark",
        "theme_selected": "*Dark theme selected (visual only)*",
        "navigation": "### 🧭 Navigation",
        "home": "🏠 Home",
        "options": "⚙️ Options",
        "current_quiz": "### 📋 Current Quiz",
        "title": "**Title:** ",
        "questions": "**Questions:** ",
        
        # Language
        "language": "### 🌐 Language",
        "choose_language": "Choose language:",
        "traditional_chinese": "繁體中文",
        "english": "English",
        
        # Error messages
        "no_quiz_files": "No quiz files found! Please ensure you have YAML quiz files in the current directory.",
        "no_quiz_loaded": "No quiz loaded!",
        "error_loading": "Error loading: ",
        "no_questions_available": "No questions available!",
        
        # Units
        "questions_unit": "questions"
    }
}


def get_text(key: str, language: str = "zh_TW", **kwargs) -> str:
    """
    Get translated text for the given key and language with googletrans fallback.
    
    Args:
        key: Translation key
        language: Language code ('zh_TW' or 'en')
        **kwargs: Format arguments for string formatting
        
    Returns:
        Translated text string
    """
    try:
        text = TRANSLATIONS[language][key]
        if kwargs:
            return text.format(**kwargs)
        return text
    except KeyError:
        # Fallback to English if key not found in selected language
        try:
            text = TRANSLATIONS["en"][key]
            if kwargs:
                return text.format(**kwargs)
            return text
        except KeyError:
            # Use googletrans as final fallback
            if GOOGLETRANS_AVAILABLE and TRANSLATOR is not None:
                try:
                    # Convert underscore-separated key to readable text
                    english_text = key.replace('_', ' ').title()
                    
                    # Map language codes to googletrans codes
                    lang_map = {
                        'zh_TW': 'zh-tw',
                        'en': 'en'
                    }
                    
                    target_lang = lang_map.get(language, 'zh-tw')
                    
                    if target_lang == 'en':
                        translated_text = english_text
                    else:
                        result = TRANSLATOR.translate(english_text, dest=target_lang)
                        translated_text = result.text
                    
                    if kwargs:
                        return translated_text.format(**kwargs)
                    return translated_text
                    
                except Exception as e:
                    # If googletrans fails, return formatted key
                    return f"[{key}]"
            else:
                # Return key if googletrans not available
                return f"[{key}]"


def get_available_languages() -> dict:
    """Get available languages for the dropdown."""
    return {
        "繁體中文": "zh_TW",
        "English": "en"
    }


def get_language_display_name(language_code: str) -> str:
    """Get the display name for a language code."""
    lang_map = {
        "zh_TW": "繁體中文",
        "en": "English"
    }
    return lang_map.get(language_code, "繁體中文")
