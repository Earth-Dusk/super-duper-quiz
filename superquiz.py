import os
import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.questions = []
        self.initUI()
        # Shuffle questions and answers initially
        random.shuffle(self.questions)
        for question in self.questions:
            random.shuffle(question['options'])

    def initUI(self):
        self.setWindowTitle('Quiz App')
        self.setGeometry(100, 100, 400, 300)

        self.genres = ['General Knowledge', 'History', 'Science', 'Geography']  # Example genres
        self.load_quiz_data('general_knowledge.txt')  # Default to load general knowledge questions

        self.current_question_index = 0
        self.correct_answers = 0

        self.genre_combo_box = QComboBox()
        self.genre_combo_box.addItems(self.genres)
        self.genre_combo_box.currentIndexChanged.connect(self.change_genre)

        self.question_label = QLabel(self.questions[self.current_question_index]['question'])
        self.feedback_label = QLabel('')

        self.option_buttons = []
        for option in self.questions[self.current_question_index]['options']:
            button = QPushButton(option)
            button.clicked.connect(self.check_answer)
            self.option_buttons.append(button)

        layout = QVBoxLayout()
        layout.addWidget(self.genre_combo_box)
        layout.addWidget(self.question_label)
        for button in self.option_buttons:
            layout.addWidget(button)
        layout.addWidget(self.feedback_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_quiz_data(self, filename):
        self.questions.clear()  # Clear any existing questions
        with open(filename, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                question = lines[i].strip()
                if i + 5 < len(lines):  # Ensure there are enough lines for question, options, and answer
                    options = [lines[i+1].strip(), lines[i+2].strip(), lines[i+3].strip(), lines[i+4].strip()]
                    answer = lines[i+5].strip().split()[-1]  # Extract the last character (A, B, C, D) from "Answer: X"
                    self.questions.append({'question': question, 'options': options, 'answer': answer})
                    i += 6  # Move to the next set of question lines
                else:
                    break  # Exit the loop if there aren't enough lines left

    def change_genre(self, index):
        selected_genre = self.genres[index]
        filename = selected_genre.lower().replace(' ', '_') + '.txt'  # Example: general_knowledge.txt
        self.load_quiz_data(filename)

        self.current_question_index = 0
        self.correct_answers = 0
        self.update_question_ui()
        random.shuffle(self.questions)
        for question in self.questions:
            random.shuffle(question['options'])

    def update_question_ui(self):
        if self.questions:
            self.question_label.setText(self.questions[self.current_question_index]['question'])
            for i, option in enumerate(self.questions[self.current_question_index]['options']):
                self.option_buttons[i].setText(option)
            self.feedback_label.setText('')  # Clear feedback label

            # Enable all option buttons for the new question
            for button in self.option_buttons:
                button.setEnabled(True)

    def check_answer(self):
        sender_button = self.sender()
        selected_option = sender_button.text().split(')')[0]  # Extracts the first character (A, B, C, D)
        correct_answer = self.questions[self.current_question_index]['answer']

        if selected_option == correct_answer:
            self.feedback_label.setText('Correct!')
            self.correct_answers += 1
        else:
            self.feedback_label.setText(f'Incorrect! Correct answer: {correct_answer}')

        # Disable all option buttons after answering
        for button in self.option_buttons:
            button.setEnabled(False)

        # Move to the next question or finish the quiz
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.update_question_ui()
        else:
            self.question_label.setText('Quiz completed!')
            self.feedback_label.setText(f'You scored {self.correct_answers} out of {len(self.questions)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec())
