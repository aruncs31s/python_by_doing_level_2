from modules.git import Git
import json
from typing import List, Dict



class Files:
    def __init__(self, git: Git):
        self.git = git

    def save_repos_to_file(self, filename: str):
        repos: List[Dict[str, str | list[str]]] = self.git.get_github_repositories()
        with open(filename, 'w') as f:
            json.dump(repos, f, indent=4)
        print(f"Repositories saved to {filename}")

    def is_repos_available(self) -> bool:
        try:
            with open("repos.json", "r") as f:
                data = json.load(f)
                print(f"Found {len(data)} repositories in repos.json")
                return len(data) > 0
        except FileNotFoundError:
            print("repos.json file not found.")
            return False

    def get_repos_from_file(self) -> list[Dict[str, str | list[str]]]:
        try:
            with open("repos.json", "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []
    def save_save_username(self,filename: str = 'data.json'):
        data = {
            'username': self.git.username
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)    
        print(f"Username saved to {filename}")
    @staticmethod 
    def load_username(filename: str = 'data.json') -> str :
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data.get('username', "")
        except FileNotFoundError:
            with open(f"src/{filename}", 'r') as f:
                data = json.load(f)
                return data.get('username', "")
    @property
    def about(self) -> str:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data.get("about", "No Abouts")
        except FileNotFoundError:
            return "No Abouts"
    @about.setter
    def about(self, about: str):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data["about"] = about
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("About section updated.")
    @property
    def skills(self) -> List[str]:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data.get("skills", [])
        except FileNotFoundError:
            return []
    @skills.setter
    def skills(self, skills: List[str]):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data["skills"] = skills
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Skills section updated.")
    @property
    def experiences(self) -> List[Dict[str, str]]:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data.get("experience", [])
        except FileNotFoundError:
            return []
    @experiences.setter
    def experiences(self, experience: List[Dict[str, str]]):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data["experience"] = experience
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Experience section updated.")
        
# if __name__ == "__main__":
#    username = input("Enter GitHub username: ")
#    files = Files(git=Git(username=username))
#    files.save_repositories_to_file("repos.json")