import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QComboBox

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz App')
        self.setGeometry(100, 100, 400, 300)

        self.genres = ['General Knowledge', 'History', 'Science', 'Geography']  # Example genres
        self.questions = []
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
        with open(filename, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                question = lines[i].strip()
                options = [lines[i+1].strip(), lines[i+2].strip(), lines[i+3].strip(), lines[i+4].strip()]
                answer = lines[i+5].strip()
                self.questions.append({'question': question, 'options': options, 'answer': answer})
                i += 6

    def change_genre(self, index):
        selected_genre = self.genres[index]
        filename = selected_genre.lower().replace(' ', '_') + '.txt'  # Example: general_knowledge.txt
        self.questions.clear()
        self.load_quiz_data(filename)

        self.current_question_index = 0
        self.correct_answers = 0
        self.update_question_ui()

    def update_question_ui(self):
        if self.questions:
            self.question_label.setText(self.questions[self.current_question_index]['question'])
            for i, option in enumerate(self.questions[self.current_question_index]['options']):
                self.option_buttons[i].setText(option)

    def check_answer(self):
        sender_button = self.sender()
        selected_option = sender_button.text()[0]  # Extracts the first character (A, B, C, D)
        correct_answer = self.questions[self.current_question_index]['answer']

        if selected_option == correct_answer:
            self.feedback_label.setText('Correct!')
            self.correct_answers += 1
        else:
            self.feedback_label.setText('Incorrect!')

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
