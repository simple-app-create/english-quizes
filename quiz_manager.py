"""
Quiz Manager Module

This module handles loading, parsing, and managing YAML-based quiz data
for the English Language Arts quiz application.
"""

import yaml
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from pathlib import Path


class QuizMetadata(BaseModel):
    """Metadata for the quiz"""
    title: str
    version: str = "1.0"
    created_date: str
    total_questions: int
    description: Optional[str] = None


class Question(BaseModel):
    """Individual quiz question model"""
    id: int
    topic: str
    difficulty: str = Field(..., description="easy, medium, or hard")
    question: str
    choices: List[str] = Field(..., min_items=2, max_items=6)
    correct_answer: int = Field(..., ge=0)
    passage: Optional[str] = None  # For reading comprehension questions
    explanation: Optional[str] = None
    explanation_zh_TW: Optional[str] = None  # Traditional Chinese explanation
    explanation_zh_CN: Optional[str] = None  # Simplified Chinese explanation
    tags: Optional[List[str]] = None

    def validate_correct_answer(self) -> bool:
        """Validate that correct_answer index is within choices range"""
        return 0 <= self.correct_answer < len(self.choices)
    
    def get_explanation(self, language: str = 'en') -> str:
        """
        Get explanation in specified language
        
        Args:
            language: Language code ('en', 'zh_TW', 'zh_CN')
            
        Returns:
            Explanation in requested language or fallback
        """
        # Try to get explanation in requested language
        if language == 'zh_TW' and self.explanation_zh_TW:
            return self.explanation_zh_TW
        elif language == 'zh_CN' and self.explanation_zh_CN:
            return self.explanation_zh_CN
        elif language == 'zh_TW' and self.explanation_zh_CN:
            # Fallback: use simplified Chinese for traditional Chinese
            return self.explanation_zh_CN
        
        # Default to English explanation
        return self.explanation or ""


class Quiz(BaseModel):
    """Complete quiz model"""
    quiz_metadata: QuizMetadata
    questions: List[Question]

    def get_questions_by_topic(self, topic: str) -> List[Question]:
        """Get all questions for a specific topic"""
        return [q for q in self.questions if q.topic.lower() == topic.lower()]

    def get_questions_by_difficulty(self, difficulty: str) -> List[Question]:
        """Get all questions for a specific difficulty level"""
        return [q for q in self.questions if q.difficulty.lower() == difficulty.lower()]

    def validate_all_questions(self) -> bool:
        """Validate all questions in the quiz"""
        return all(q.validate_correct_answer() for q in self.questions)


class QuizManager:
    """Main class for managing quiz operations"""
    
    def __init__(self):
        self.current_quiz: Optional[Quiz] = None
    
    def load_quiz_from_file(self, file_path: str | Path) -> Quiz:
        """
        Load quiz from YAML file
        
        Args:
            file_path: Path to the YAML quiz file
            
        Returns:
            Quiz: Loaded and validated quiz object
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If YAML parsing fails
            ValueError: If quiz validation fails
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Quiz file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                quiz_data = yaml.safe_load(file)
            
            # Create Quiz object with validation
            quiz = Quiz(**quiz_data)
            
            # Additional validation
            if not quiz.validate_all_questions():
                raise ValueError("Some questions have invalid correct_answer indices")
            
            self.current_quiz = quiz
            return quiz
            
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")
        except Exception as e:
            raise ValueError(f"Error creating quiz object: {e}")
    
    def save_quiz_to_file(self, quiz: Quiz, file_path: str | Path) -> None:
        """
        Save quiz to YAML file
        
        Args:
            quiz: Quiz object to save
            file_path: Path where to save the YAML file
        """
        file_path = Path(file_path)
        
        # Convert to dict for YAML serialization
        quiz_dict = quiz.model_dump()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(quiz_dict, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
        except Exception as e:
            raise IOError(f"Error saving quiz to file: {e}")
    
    def create_sample_quiz(self) -> Quiz:
        """Create a sample quiz for testing purposes"""
        sample_data = {
            "quiz_metadata": {
                "title": "English Language Arts Sample Quiz",
                "version": "1.0",
                "created_date": "2025-06-15",
                "total_questions": 3,
                "description": "A sample quiz covering various ELA topics"
            },
            "questions": [
                {
                    "id": 1,
                    "topic": "Reading Comprehension",
                    "difficulty": "easy",
                    "passage": "The quick brown fox jumps over the lazy dog. This sentence is famous because it contains every letter of the English alphabet at least once.",
                    "question": "Why is this sentence famous?",
                    "choices": [
                        "It contains every letter of the alphabet",
                        "It's the shortest sentence in English",
                        "It was written by Shakespeare",
                        "It contains no vowels"
                    ],
                    "correct_answer": 0,
                    "explanation": "This sentence is called a pangram because it contains all 26 letters of the English alphabet.",
                    "explanation_zh_TW": "",
                    "explanation_zh_CN": "",
                    "tags": ["pangram", "alphabet"]
                },
                {
                    "id": 2,
                    "topic": "Grammar",
                    "difficulty": "medium",
                    "question": "Which sentence uses correct subject-verb agreement?",
                    "choices": [
                        "The group of students are studying",
                        "The group of students is studying",
                        "The groups of student is studying",
                        "The groups of student are studying"
                    ],
                    "correct_answer": 1,
                    "explanation": "The subject 'group' is singular, so it takes the singular verb 'is'.",
                    "explanation_zh_TW": "",
                    "explanation_zh_CN": "",
                    "tags": ["subject-verb agreement", "singular", "plural"]
                },
                {
                    "id": 3,
                    "topic": "Spelling",
                    "difficulty": "easy",
                    "question": "Which word is spelled correctly?",
                    "choices": [
                        "Recieve",
                        "Receive",
                        "Recive",
                        "Receeve"
                    ],
                    "correct_answer": 1,
                    "explanation": "Remember: 'I before E except after C' - receive follows this rule.",
                    "explanation_zh_TW": "",
                    "explanation_zh_CN": "",
                    "tags": ["i before e", "spelling rules"]
                }
            ]
        }
        
        return Quiz(**sample_data)
    
    def get_quiz_stats(self) -> Dict[str, Any]:
        """Get statistics about the current quiz"""
        if not self.current_quiz:
            return {"error": "No quiz loaded"}
        
        topics = {}
        difficulties = {}
        
        for question in self.current_quiz.questions:
            topics[question.topic] = topics.get(question.topic, 0) + 1
            difficulties[question.difficulty] = difficulties.get(question.difficulty, 0) + 1
        
        return {
            "total_questions": len(self.current_quiz.questions),
            "topics": topics,
            "difficulties": difficulties,
            "title": self.current_quiz.quiz_metadata.title
        }


# Convenience functions for easy usage
def load_quiz(file_path: str | Path) -> Quiz:
    """Convenience function to load a quiz"""
    manager = QuizManager()
    return manager.load_quiz_from_file(file_path)


def create_sample_quiz_file(file_path: str | Path = "sample_quiz.yaml") -> None:
    """Create a sample quiz YAML file"""
    manager = QuizManager()
    sample_quiz = manager.create_sample_quiz()
    manager.save_quiz_to_file(sample_quiz, file_path)
    print(f"Sample quiz created at: {file_path}")


if __name__ == "__main__":
    # Demo usage
    print("Creating sample quiz...")
    create_sample_quiz_file()
    
    print("Loading quiz...")
    manager = QuizManager()
    quiz = manager.load_quiz_from_file("sample_quiz.yaml")
    
    print("Quiz Stats:")
    stats = manager.get_quiz_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
