import subprocess
import requests
from typing import Any
class Git:
    def __init__(self, username: str):
        self._username = username
        if not self._validate_username(self._username):
            raise ValueError("Username cannot be empty")
        if not self._check_if_username_exists(self._username):
            raise ValueError("Username does not exist")
        
    @staticmethod
    def _validate_username(username: str) -> bool:
        """Validates the Github Username 
        Just checks if the username is not empty for now.
        """
        print(username)
        return len(username) > 0
    @staticmethod
    def _check_if_username_exists(username: str) -> bool:
        """Check if the given GitHub username exists."""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(f"https://api.github.com/users/{username}", headers=headers)
        return response.status_code == 200


    # Username should be asked outside the class, not here.
    
    @property
    def username(self) -> str:
        return self._username
    @username.setter
    def username(self, value: str):
        self._username = value

    def get_image_url_github(self) -> str:
        return f"https://github.com/{self.username}.png"
    @property
    def name(self) -> str:
        result = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True)
        return result.stdout.strip()
    @name.setter
    def name(self, name: str):
        subprocess.run(["git", "config", "--global", "user.name", name])
    def get_github_description(self) -> str:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",

        }
        response = requests.get(f"https://api.github.com/users/{self.username}", headers=headers)
        json_response = response.json()
        bio = json_response.get("bio", "")
        return bio

    def get_github_achievements(self) -> list[dict[str, str]]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(f"https://api.github.com/users/{self.username}/achievements", headers=headers)
        json_response = response.json()
        achievements = json_response.get("achievements", [])
        return achievements
    @property
    def github_email(self) -> str:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(f"https://api.github.com/users/{self.username}", headers=headers)
        json_response = response.json()
        email = json_response.get("email", "")
        if email is None or email == "":
            email = subprocess.run(["git", "config", "--get", "user.email"], capture_output=True, text=True).stdout.strip()
        return email
    @github_email.setter
    def github_email(self, email: str):
        subprocess.run(["git", "config", "--global", "user.email", email])
    def get_repo_languages(self, languages_url: str) -> list[str]:
        """Fetch languages used in a GitHub repository"""
        try:
            response = requests.get(languages_url)
            if response.status_code == 200:
                languages = response.json()
                return list(languages.keys())
            else:
                print(f"Error fetching languages for {languages_url}: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching languages for {languages_url}: {e}")
            return []
    def get_github_repositories(self) -> list[dict[str, str | list[str]]]:
        all_repos: list[dict[str, Any]] = []
        page = 1
        per_page = 100  # Maximum allowed per page
        try:
            while True:
                url: str = f"https://api.github.com/users/{self.username}/repos"
                params: dict[str, str | int] = {
                    'page': page,
                    'per_page': per_page,
                    'sort': 'updated',  # Sort by last updated
                    'direction': 'desc'
                }
                
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    repos = response.json()
                    if not repos:  # No more repositories
                        break
                    all_repos.extend(repos)
                    page += 1
                else:
                    print(f"Error fetching page {page}: {response.status_code}")
                    break

            print(f"Fetched {len(all_repos)} repositories from GitHub")

            if all_repos:
                projects: list[dict[str, str | list[str]]] = []
                for repo in all_repos:
                    name: str = str(repo.get('name', ''))
                    description: str = str(repo.get('description') or "No description provided.")
                    tech: list[str] = self.get_repo_languages(str(repo.get('languages_url', '')))
                    url: str = str(repo.get('html_url', ''))
                    project: dict[str, str | list[str]] = {
                        'name': name,
                        'description': description,
                        'tech': tech,
                        'url': url
                    }
                    projects.append(project)
                return projects
            else:
                print("No repositories found")
                return [{}]
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            return [{}]

# if __name__ == "__main__":
    # git = Git(username="aruncs31s")
    # print(get_name())
    # print(get_image_url_github("aruncs31s"))
    # print(get_github_description("aruncs31s"))
    # print(get_github_achievements("aruncs31s"))
    # print(len(git.get_github_repositories()))