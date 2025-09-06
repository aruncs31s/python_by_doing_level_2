from flask import Flask, jsonify, render_template

from modules.git import Git
from modules.files import Files

app = Flask(__name__, template_folder="templates")



@app.route('/')
def go_home():
    loaded_username = Files.load_username() or "aruncs31s"
    git = Git(username=loaded_username)
    files = Files(git=git)
    # Extract GitHub username from URL
    github_url = "https://github.com/aruncs31s"
    github_username = github_url.split("/")[-1]  # Extract 'aruncs31s' from the URL
    avatar_url = f"https://github.com/{github_username}.png?size=200"  # GitHub avatar API
    
    # Fetch real GitHub repositories
    if files.is_repos_available():
        github_projects = files.get_repos_from_file()
    else:
        github_projects = git.get_github_repositories()
        files.save_repos_to_file("repos.json")

    portfolio = {
        "name": git.name,
        "title": "Python Developer",
        "bio": git.get_github_description(),
        "about": files.about,
        "avatar": git.get_image_url_github(),
        "github_username": git.username,
        "skills": files.skills,
        "projects": github_projects,  # Use real GitHub repositories
        "experience": files.experiences,
        "email": git.github_email,
        "github": f"https://github.com/{git.username}",
        "linkedin": f"https://linkedin.com/in/{git.username}",
        "website": f"https://{git.username}.github.io"
    }
    return render_template("home.html", portfolio=portfolio)

@app.route('/is_complete')
def is_complete() -> bool:
    result = dict({"result": True})
    return result


if __name__ == "__main__":
    app.run(debug=True)