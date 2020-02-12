import os

from git import Repo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT_REPO_DIR_NAME = "repository"
REPOSITORIES_DIR = os.path.join(BASE_DIR, GIT_REPO_DIR_NAME)


def create_repository(username, repository):
    repo_dir = create_repository_directory(username, repository)
    Repo.init(repo_dir, bare=True)
    return repo_dir


def create_repository_directory(username, repository):
    repo_dir = os.path.join(REPOSITORIES_DIR, username, repository + ".git")
    os.mkdir(repo_dir)

    return repo_dir
