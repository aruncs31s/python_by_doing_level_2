from modules.git import Git
class Status():
    def __init__(self,git: Git):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._current_question_num = 0
            self._git = git
    @property
    def current_question_num(self) -> int:
        return self._current_question_num
    @current_question_num.setter
    def current_question_num(self, value: int):
        self._current_question_num = value

    def progress(self):
        print(f"Question {self._current_question_num} asked.")
    def status(self):
        print(f" Name {self._git.name} ")

        print(f" Username : {self._git.username} ")
        print(f" Email : {self._git.github_email} ")