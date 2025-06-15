# 🎓 English Quiz App

A comprehensive English Language Arts quiz application with multi-language support.

## ✨ Features

- **Multiple Choice Quizzes** - Grammar, Reading Comprehension, Spelling, and Sentence Correction
- **Multi-Language Support** - Traditional Chinese (default) and English UI
- **Intelligent Translation** - Manual translations with auto-translation fallback
- **Flexible Practice Modes** - Complete quiz, practice by topic, or practice by difficulty
- **Interactive Interfaces** - Both CLI and Web GUI available
- **Performance Tracking** - Score tracking with detailed feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- UV package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd english_quiz

# Install dependencies
uv sync
```

### Running the App

**CLI Interface (Recommended for testing):**
```bash
python quiz_cli.py
```

**Web Interface:**
```bash
streamlit run main.py
```

## 📁 Project Structure

```
english_quiz/
├── main.py                 # Streamlit web GUI
├── quiz_cli.py            # Command-line interface
├── quiz_manager.py        # Core quiz management
├── translations.py        # UI translations
├── explanation_translator.py # Explanation translation
├── sample_quiz.yaml       # Sample quiz (3 questions)
├── small_quiz.yaml        # Comprehensive quiz (23 questions)
└── README.md
```

## 📚 Quiz Format

Quizzes are stored in YAML format with support for multiple languages:

```yaml
questions:
  - id: 1
    topic: "Grammar"
    difficulty: "easy"
    question: "Which sentence is correct?"
    choices:
      - "I are happy"
      - "I am happy"
    correct_answer: 1
    explanation: "Use 'am' with 'I'."
    explanation_zh_TW: "與 'I' 一起使用 'am'。"
```

## 🌐 Language Support

- **UI Languages**: Traditional Chinese (default), English
- **Explanation Languages**: Automatic translation with manual override support
- **Easy Extension**: Add new languages by updating translation dictionaries

## 🎯 Usage Examples

### CLI Interface
1. Start the CLI: `python quiz_cli.py`
2. Load a quiz file
3. Choose practice mode:
   - Complete quiz
   - Practice by topic
   - Practice by difficulty
4. Answer questions and get instant feedback

### Web Interface
1. Start Streamlit: `streamlit run main.py`
2. Select language (Traditional Chinese/English)
3. Choose quiz and practice mode
4. Take interactive quizzes with progress tracking

## 🛠️ Dependencies

- **PyYAML** - YAML file parsing
- **Pydantic** - Data validation
- **Streamlit** - Web interface
- **googletrans** - Automatic translation
- **UV** - Package management

## 📈 Educational Levels

- **K12** - Basic grammar, spelling, reading
- **ESL** - English as Second Language learners
- **Middle School** - Intermediate concepts
- **High School** - Advanced grammar and reading
- **SAT Level** - College preparation

## 🤝 Contributing

1. Add new questions to YAML files
2. Include Traditional Chinese explanations when possible
3. Test with both CLI and web interfaces
4. Maintain educational quality and accuracy

## 📄 License

Educational use - feel free to adapt for learning purposes.

---

**Happy Learning!** 🎉