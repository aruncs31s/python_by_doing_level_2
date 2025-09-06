# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from colorama import init
from modules.question import Question
from modules.status import Status
from modules.git import *
from modules.files import *



def initialize_git(username) -> Git:
    if username is None:
        while True:
            username = input("Enter your GitHub username: ")
            try:
                return Git(username=username.strip())
            except ValueError as e:
                print(e)
                print("Please try again.")
    else:
        return Git(username=username)
def initialize_files(git: Git) -> Files:   
    # Git object is need to save repositories from git to file.
    # its also used because of the API Rate limit. 
    return Files(git=git)
def initialize_status(git: Git) -> Status:
    # Git object is passed to get the Name and Email from git config.
    return Status(git=git)
def initialize_questions(status: Status) -> Question:
    # Status object is passed to keep track of the current question number.
    return Question(status=status)


def initialize_objects() -> tuple[Git, Files, Status, Question]:
    # Status object must be shared between all the other objects.
    git = initialize_git("")
    status = initialize_status(git=git)
    question_helper = initialize_questions(status=status)
    files = initialize_files(git=git)
    return git , files , status , question_helper
def initialize_repos() -> tuple[Git, Files, Status, Question]:
    git, files, status, question_helper = initialize_objects()
    
    if git.username == "" or git.username == None:
        github_username = question_helper.ask_question("What is your github username")
        git.username = github_username
        status.current_question_num += 1
    def check_if_sure() -> tuple[Git, Files, Status, Question]:
        is_sure = input(f"Are you sure that your username is {git.username} ? ")
        if is_sure.lower() in ["yes","y"]:
            git.username = git.username
            if not files.is_repos_available():
                files.save_repos_to_file("repos.json")
            return git , files , status , question_helper
        else:
            return check_if_sure()
    return check_if_sure()     
def main():
    
    git, files, status, question_helper = initialize_repos()
    status.status()
    is_correct: str = input("Is this all correct ? (yes/no) ")
    if is_correct.lower() in ["yes","y"]:
        pass
    else:
        print("Which one is incorrect ?")
        which_one = input("1. Name\n2. Username\n3. Email\n")
        if which_one == "1":
            new_name = question_helper.ask_question("What is your name")
            git.name = new_name
        elif which_one == "2":
            new_username: str = question_helper.ask_question("What is your github username")
            git.username = new_username
        elif which_one == "3":
            new_email: str = question_helper.ask_question("What is your email")
            git.github_email = new_email
        else:
            print("Invalid option. Exiting.")
            return
    about = question_helper.ask_question("Tell me something about yourself: ")
    files.about = about
    skills = question_helper.ask_question("List your skills (comma separated): ")
    files.skills = [skill.strip() for skill in skills.split(",")]
    print(f"Your skills are: {files.skills}")
    
    
    def ask_experiences() -> list[dict[str, str]]:
        experiences = []
        while True:
            add_experience = input("Do you want to add an experience? (yes/no): ")
            if add_experience.lower() in ["yes", "y"]:
                position = question_helper.ask_question("Position: ")
                company = question_helper.ask_question("Company: ")
                duration = question_helper.ask_question("Duration (e.g., 2020-2022): ")
                description = question_helper.ask_question("Description: ")
                experiences.append({
                    "position": position,
                    "company": company,
                    "duration": duration,
                    "description": description
                })
            elif add_experience.lower() in ["no", "n"]:
                break
            else:
                print("Please answer with 'yes' or 'no'.")
        return experiences
    experiences: list[dict[str, str]] = ask_experiences()
    files.experience = experiences
    print(f"Your experiences are: {files.experience}")
    print("Now Run the website using python src/app.py")
if __name__ == "__main__":
    main()