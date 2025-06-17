"""
Quiz Manager Module

This module handles loading, parsing, and managing YAML-based quiz data
for the English Language Arts quiz application.
"""

import yaml
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Annotated
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict


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
    choices: Annotated[List[str], Field(min_length=2, max_length=6)]
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
    
    def __init__(self, quizzes_dir: str = 'quizzes'):
        self.quizzes_dir = Path(quizzes_dir)
        self.current_quiz: Optional[Quiz] = None
        self.available_topics: List[str] = []
        self._discover_topics()
    
    def _discover_topics(self) -> None:
        """Discover available quiz topics from the quizzes directory"""
        if not self.quizzes_dir.exists():
            return
            
        self.available_topics = [
            f.stem.replace('_', ' ').title()
            for f in self.quizzes_dir.glob('*.yaml')
            if f.is_file()
        ]
    
    def get_available_topics(self) -> List[str]:
        """Get list of available quiz topics"""
        return self.available_topics
    
    def load_questions_by_topic(self, topic: str) -> List[Question]:
        """
        Load questions for a specific topic
        
        Args:
            topic: The topic to load questions for
            
        Returns:
            List of Question objects for the specified topic
        """
        # Convert topic to filename format (lowercase with underscores)
        filename = f"{topic.lower().replace(' ', '_')}.yaml"
        file_path = self.quizzes_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"No quiz file found for topic: {topic}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                quiz_data = yaml.safe_load(file)
                
            # Convert each question dict to Question object
            questions = [Question(**q) for q in quiz_data.get('questions', [])]
            
            # Validate all questions
            for q in questions:
                if not q.validate_correct_answer():
                    raise ValueError(f"Invalid correct_answer in question ID {q.id}")
                    
            return questions
            
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")
    
    def load_questions(self, topics: Optional[Union[str, List[str]]] = None) -> List[Question]:
        """
        Load questions from one or more topic files
        
        Args:
            topics: Single topic or list of topics to load. If None, loads all available topics.
            
        Returns:
            Combined list of Question objects from specified topics
        """
        if topics is None:
            topics = self.available_topics
        elif isinstance(topics, str):
            topics = [topics]
            
        all_questions = []
        
        for topic in topics:
            try:
                questions = self.load_questions_by_topic(topic)
                all_questions.extend(questions)
            except FileNotFoundError:
                print(f"Warning: No questions found for topic: {topic}")
                continue
                
        return all_questions
    
    def load_quiz_from_file(self, file_path: Optional[Union[str, Path]] = None, 
                         topics: Optional[Union[str, List[str]]] = None) -> Quiz:
        """
        Load quiz from YAML file(s)
        
        Args:
            file_path: Path to a single YAML quiz file (legacy support)
            topics: Topic or list of topics to load questions from
            
        Returns:
            Quiz: Loaded and validated quiz object
            
        Raises:
            FileNotFoundError: If no questions are found
            yaml.YAMLError: If YAML parsing fails
            ValueError: If quiz validation fails
        """
        if file_path is not None:
            # Legacy support for loading from a single file
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
        
        # Load questions from topic files
        questions = self.load_questions(topics)
        
        if not questions:
            raise FileNotFoundError("No questions found for the specified topics")
        
        # Create a quiz with the loaded questions
        quiz_data = {
            "quiz_metadata": {
                "title": f"{' + '.join(topics) if topics else 'Comprehensive'} Quiz",
                "version": "1.0",
                "created_date": "2025-06-15",
                "total_questions": len(questions),
                "description": f"Quiz covering {', '.join(topics) if topics else 'various topics'}"
            },
            "questions": [q.model_dump() for q in questions]
        }
        
        self.current_quiz = Quiz(**quiz_data)
        return self.current_quiz
    
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
        # Create sample topic files if they don't exist
        sample_questions = {
            "reading_comprehension": [
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
                }
            ],
            "grammar": [
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
                }
            ],
            "spelling": [
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
        
        # Create the quizzes directory if it doesn't exist
        self.quizzes_dir.mkdir(exist_ok=True)
        
        # Save sample questions to topic files
        for topic, questions in sample_questions.items():
            file_path = self.quizzes_dir / f"{topic}.yaml"
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump({"questions": questions}, f, default_flow_style=False, allow_unicode=True)
        
        # Reload available topics
        self._discover_topics()
        
        # Create a combined quiz data structure
        all_questions = [q for sublist in sample_questions.values() for q in sublist]
        sample_data = {
            "quiz_metadata": {
                "title": "English Language Arts Sample Quiz",
                "version": "1.0",
                "created_date": "2025-06-15",
                "total_questions": len(all_questions),
                "description": "A sample quiz covering various ELA topics"
            },
            "questions": all_questions
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


def create_sample_quiz_file() -> None:
    """Create sample topic YAML files in the quizzes directory"""
    manager = QuizManager()
    sample_quiz = manager.create_sample_quiz()
    print(f"Sample quiz topics created in: {manager.quizzes_dir}")


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
