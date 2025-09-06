from modules.status import Status


class Question():
    def __init__(self,status: Status):
        self.status = status
    def prompt_question(self, question: str) -> str:
        return input(f"Question {self.status.current_question_num}: {question} ? ")

    def ask_question(self, question: str) -> str:
        return self.prompt_question(question)
