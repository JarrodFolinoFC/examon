import os.path
import os
import json
import subprocess
import sys


class RepoManager:
    DEFAULT_MODULE = 'examon_repo_1'
    DEFAULT_PIP = 'https://test.pypi.org/simple/'

    def __init__(self, settings_file='.examon'):
        self.repos = []
        self.active_repos = []
        self.settings_file = settings_file

    def install(self):
        print(f"installing {len(self.repos)} repos")
        for repo in self.repos:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", repo['name']])

    def reset(self):
        self.repos = []
        self.active_repos = []

    def add(self, repo_name, url=None):
        if repo_name is None or repo_name == '':
            return

        data = {'name': repo_name}
        if url:
            data |= {'url': url}
        self.repos.append(data)

    def remove(self, repo_name):
        index = next(
            (index for (
                index,
                d) in enumerate(
                self.repos) if d["name"] == repo_name),
            None)
        del self.repos[index]

    def add_active(self, repo):
        if repo not in self.active_repos:
            self.active_repos.append(repo)

    def remove_active(self, repo_name):
        self.active_repos.remove(repo_name)

    def import_repos(self):
        print(f'Importing Repos ({len(self.active_repos)})')
        for repo in self.active_repos:
            __import__(repo, fromlist=['*'])

    def as_dict(self):
        return {
            'repositories':
                {
                    'all': self.repos,
                    'active': self.active_repos
                }
        }

    def persist(self):
        f = open(RepoManager.full_file_path(), "w")
        json_object = json.dumps(self.as_dict(), indent=4)
        f.write(json_object)
        f.close()

    def load(self):
        with open(self.full_file_path(), 'r') as f:
            data = json.load(f)

        self.repos = data['repositories']['all']
        self.active_repos = data['repositories']['active']

    def full_file_path(self):
        home_directory = os.path.expanduser('~')
        file = f'{home_directory}/{self.settings_file}'
        return file

    def persist_default(self):
        self.repos = [
            {
                'name': RepoManager.DEFAULT_MODULE,
                'pip_url': RepoManager.DEFAULT_PIP
            }]
        self.active_repos = [RepoManager.DEFAULT_MODULE]
        self.persist()
