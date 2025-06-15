#!/usr/bin/env python3
"""
English Quiz App - Command Line Interface

A command-line interface for testing and interacting with the English Language Arts quiz application.
This provides an easy way to test quiz functionality before implementing the web GUI.
"""

import sys
import random
from pathlib import Path
from quiz_manager import QuizManager, create_sample_quiz_file, Quiz, Question


class QuizCLI:
    """Command Line Interface for the Quiz App"""
    
    def __init__(self):
        self.manager = QuizManager()
        self.current_quiz = None
        self.score = 0
        self.current_question_index = 0
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("🎓 ENGLISH QUIZ APP - CLI")
        print("="*50)
        print("1. Load Quiz from File")
        print("2. Create Sample Quiz")
        print("3. Start Quiz")
        print("4. Practice by Topic")
        print("5. Practice by Difficulty")
        print("6. View Quiz Stats")
        print("7. List Quiz Files")
        print("8. Exit")
        print("-"*50)
    
    def load_quiz_menu(self):
        """Menu for loading quiz files"""
        print("\n📁 Load Quiz File")
        print("-" * 20)
        
        # List available YAML files
        yaml_files = list(Path(".").glob("*.yaml")) + list(Path(".").glob("*.yml"))
        
        if not yaml_files:
            print("No YAML quiz files found in current directory.")
            input("Press Enter to continue...")
            return
        
        print("Available quiz files:")
        for i, file in enumerate(yaml_files, 1):
            print(f"{i}. {file.name}")
        
        try:
            choice = int(input(f"\nEnter choice (1-{len(yaml_files)}): "))
            if 1 <= choice <= len(yaml_files):
                selected_file = yaml_files[choice - 1]
                self.current_quiz = self.manager.load_quiz_from_file(selected_file)
                print(f"✅ Successfully loaded: {self.current_quiz.quiz_metadata.title}")
            else:
                print("❌ Invalid choice!")
        except (ValueError, Exception) as e:
            print(f"❌ Error loading quiz: {e}")
        
        input("Press Enter to continue...")
    
    def create_sample_quiz(self):
        """Create a sample quiz file"""
        print("\n📝 Create Sample Quiz")
        print("-" * 20)
        
        filename = input("Enter filename for sample quiz (default: sample_quiz.yaml): ").strip()
        if not filename:
            filename = "sample_quiz.yaml"
        
        if not filename.endswith(('.yaml', '.yml')):
            filename += '.yaml'
        
        try:
            create_sample_quiz_file(filename)
            print(f"✅ Sample quiz created: {filename}")
        except Exception as e:
            print(f"❌ Error creating sample quiz: {e}")
        
        input("Press Enter to continue...")
    
    def start_quiz(self):
        """Start a complete quiz session"""
        if not self.current_quiz:
            print("❌ No quiz loaded! Please load a quiz first.")
            input("Press Enter to continue...")
            return
        
        print(f"\n🎯 Starting Quiz: {self.current_quiz.quiz_metadata.title}")
        print("="*60)
        print("💡 Type 'q' or 'quit' at any time to exit with current stats")
        print("="*60)
        
        questions = self.current_quiz.questions.copy()
        random.shuffle(questions)  # Randomize question order
        
        self.score = 0
        total_questions = len(questions)
        questions_attempted = 0
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{total_questions}")
            print(f"Topic: {question.topic} | Difficulty: {question.difficulty}")
            print("-" * 40)
            
            # Show passage if it exists
            if question.passage:
                print("📖 Passage:")
                print(question.passage)
                print("-" * 40)
            
            print(f"❓ {question.question}")
            print()
            
            # Display choices
            for j, choice in enumerate(question.choices):
                print(f"  {j + 1}. {choice}")
            
            # Get user answer with quit option
            while True:
                try:
                    user_input = input(f"\nYour answer (1-{len(question.choices)}) or 'q' to quit: ").strip().lower()
                    
                    # Check for quit command
                    if user_input in ['q', 'quit']:
                        print("\n🚪 Exiting quiz...")
                        self._display_quiz_results(self.score, questions_attempted, total_questions, early_exit=True)
                        return
                    
                    user_answer = int(user_input) - 1
                    if 0 <= user_answer < len(question.choices):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(question.choices)} or 'q' to quit")
                except ValueError:
                    print("Please enter a valid number or 'q' to quit")
            
            questions_attempted += 1
            
            # Check answer
            if user_answer == question.correct_answer:
                print("✅ Correct!")
                self.score += 1
            else:
                print(f"❌ Incorrect. The correct answer was: {question.choices[question.correct_answer]}")
            
            # Show explanation if available
            if question.explanation:
                print(f"💡 Explanation: {question.explanation}")
            
            print(f"Current Score: {self.score}/{questions_attempted}")
            
            if i < total_questions:
                # Allow quit during continue prompt
                continue_input = input("\nPress Enter for next question (or 'q' to quit): ").strip().lower()
                if continue_input in ['q', 'quit']:
                    print("\n🚪 Exiting quiz...")
                    self._display_quiz_results(self.score, questions_attempted, total_questions, early_exit=True)
                    return
        
        # Quiz completed normally
        self._display_quiz_results(self.score, questions_attempted, total_questions, early_exit=False)
    
    def _display_quiz_results(self, score, attempted, total, early_exit=False):
        """Display quiz results with statistics"""
        print("\n" + "="*60)
        if early_exit:
            print("🚪 QUIZ EXITED EARLY")
        else:
            print("🏆 QUIZ COMPLETED!")
        print("="*60)
        
        if attempted > 0:
            percentage = (score / attempted) * 100
            print(f"Questions Attempted: {attempted}/{total}")
            print(f"Correct Answers: {score}")
            print(f"Accuracy: {percentage:.1f}%")
            
            # Performance feedback
            if percentage >= 90:
                print("🌟 Excellent accuracy!")
            elif percentage >= 70:
                print("👍 Good job!")
            elif percentage >= 50:
                print("👌 Not bad, keep practicing!")
            else:
                print("📚 Keep studying, you'll improve!")
            
            if early_exit and attempted < total:
                remaining = total - attempted
                print(f"📝 {remaining} questions remaining - try again later!")
        else:
            print("No questions were attempted.")
        
        # Quiz metadata
        print(f"\nQuiz: {self.current_quiz.quiz_metadata.title}")
        print(f"Date: {self.current_quiz.quiz_metadata.created_date}")
        
        input("\nPress Enter to continue...")
    
    def practice_by_topic(self):
        """Practice questions filtered by topic"""
        if not self.current_quiz:
            print("❌ No quiz loaded! Please load a quiz first.")
            input("Press Enter to continue...")
            return
        
        # Get available topics
        topics = list(set(q.topic for q in self.current_quiz.questions))
        
        print(f"\n📚 Practice by Topic")
        print("-" * 20)
        print("Available topics:")
        for i, topic in enumerate(topics, 1):
            count = len([q for q in self.current_quiz.questions if q.topic == topic])
            print(f"{i}. {topic} ({count} questions)")
        
        try:
            choice = int(input(f"\nSelect topic (1-{len(topics)}): "))
            if 1 <= choice <= len(topics):
                selected_topic = topics[choice - 1]
                topic_questions = self.current_quiz.get_questions_by_topic(selected_topic)
                self._practice_questions(topic_questions, f"Topic: {selected_topic}")
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number!")
            input("Press Enter to continue...")
    
    def practice_by_difficulty(self):
        """Practice questions filtered by difficulty"""
        if not self.current_quiz:
            print("❌ No quiz loaded! Please load a quiz first.")
            input("Press Enter to continue...")
            return
        
        # Get available difficulties
        difficulties = list(set(q.difficulty for q in self.current_quiz.questions))
        
        print(f"\n🎚️ Practice by Difficulty")
        print("-" * 25)
        print("Available difficulty levels:")
        for i, difficulty in enumerate(difficulties, 1):
            count = len([q for q in self.current_quiz.questions if q.difficulty == difficulty])
            print(f"{i}. {difficulty.title()} ({count} questions)")
        
        try:
            choice = int(input(f"\nSelect difficulty (1-{len(difficulties)}): "))
            if 1 <= choice <= len(difficulties):
                selected_difficulty = difficulties[choice - 1]
                difficulty_questions = self.current_quiz.get_questions_by_difficulty(selected_difficulty)
                self._practice_questions(difficulty_questions, f"Difficulty: {selected_difficulty.title()}")
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Please enter a valid number!")
            input("Press Enter to continue...")
    
    def _practice_questions(self, questions, practice_type):
        """Helper method to practice a subset of questions"""
        if not questions:
            print(f"❌ No questions found for {practice_type}")
            input("Press Enter to continue...")
            return
        
        print(f"\n🎯 {practice_type} Practice")
        print(f"Total questions: {len(questions)}")
        print("💡 Type 'q' or 'quit' at any time to exit with current stats")
        print("-" * 50)
        
        random.shuffle(questions)
        self.score = 0
        questions_attempted = 0
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{len(questions)}")
            print("-" * 40)
            
            if question.passage:
                print("📖 Passage:")
                print(question.passage)
                print("-" * 40)
            
            print(f"❓ {question.question}")
            print()
            
            for j, choice in enumerate(question.choices):
                print(f"  {j + 1}. {choice}")
            
            while True:
                try:
                    user_input = input(f"\nYour answer (1-{len(question.choices)}) or 'q' to quit: ").strip().lower()
                    
                    # Check for quit command
                    if user_input in ['q', 'quit']:
                        print(f"\n🚪 Exiting {practice_type} practice...")
                        self._display_practice_results(self.score, questions_attempted, len(questions), practice_type, early_exit=True)
                        return
                    
                    user_answer = int(user_input) - 1
                    if 0 <= user_answer < len(question.choices):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(question.choices)} or 'q' to quit")
                except ValueError:
                    print("Please enter a valid number or 'q' to quit")
            
            questions_attempted += 1
            
            if user_answer == question.correct_answer:
                print("✅ Correct!")
                self.score += 1
            else:
                print(f"❌ Incorrect. The correct answer was: {question.choices[question.correct_answer]}")
            
            if question.explanation:
                print(f"💡 {question.explanation}")
            
            print(f"Score: {self.score}/{questions_attempted}")
            
            if i < len(questions):
                continue_choice = input("\nContinue? (y/n/q to quit, Enter for yes): ").lower().strip()
                if continue_choice == 'n':
                    break
                elif continue_choice in ['q', 'quit']:
                    print(f"\n🚪 Exiting {practice_type} practice...")
                    self._display_practice_results(self.score, questions_attempted, len(questions), practice_type, early_exit=True)
                    return
        
        # Practice completed normally or user chose 'n' to stop
        self._display_practice_results(self.score, questions_attempted, len(questions), practice_type, early_exit=False)
    
    def _display_practice_results(self, score, attempted, total, practice_type, early_exit=False):
        """Display practice results with statistics"""
        print(f"\n🏆 {practice_type} Practice {'Exited Early' if early_exit else 'Complete'}!")
        print("-" * 50)
        
        if attempted > 0:
            percentage = (score / attempted) * 100
            print(f"Questions Attempted: {attempted}/{total}")
            print(f"Score: {score}/{attempted} ({percentage:.1f}%)")
            
            if early_exit and attempted < total:
                remaining = total - attempted
                print(f"📝 {remaining} questions remaining")
        else:
            print("No questions were attempted.")
        
        input("Press Enter to continue...")
    
    def view_quiz_stats(self):
        """Display statistics about the current quiz"""
        if not self.current_quiz:
            print("❌ No quiz loaded! Please load a quiz first.")
            input("Press Enter to continue...")
            return
        
        stats = self.manager.get_quiz_stats()
        
        print(f"\n📊 Quiz Statistics")
        print("="*40)
        print(f"Title: {stats['title']}")
        print(f"Total Questions: {stats['total_questions']}")
        print()
        print("Questions by Topic:")
        for topic, count in stats['topics'].items():
            print(f"  • {topic}: {count}")
        print()
        print("Questions by Difficulty:")
        for difficulty, count in stats['difficulties'].items():
            print(f"  • {difficulty.title()}: {count}")
        
        input("\nPress Enter to continue...")
    
    def list_quiz_files(self):
        """List all available quiz files"""
        print(f"\n📁 Available Quiz Files")
        print("-" * 25)
        
        yaml_files = list(Path(".").glob("*.yaml")) + list(Path(".").glob("*.yml"))
        
        if not yaml_files:
            print("No YAML quiz files found in current directory.")
        else:
            for file in yaml_files:
                print(f"  📄 {file.name}")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main CLI loop"""
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.load_quiz_menu()
                elif choice == '2':
                    self.create_sample_quiz()
                elif choice == '3':
                    self.start_quiz()
                elif choice == '4':
                    self.practice_by_topic()
                elif choice == '5':
                    self.practice_by_difficulty()
                elif choice == '6':
                    self.view_quiz_stats()
                elif choice == '7':
                    self.list_quiz_files()
                elif choice == '8':
                    print("\n👋 Thank you for using English Quiz App!")
                    sys.exit(0)
                else:
                    print("❌ Invalid choice! Please enter 1-8.")
                    input("Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point for CLI"""
    cli = QuizCLI()
    cli.run()


if __name__ == "__main__":
    main()
