import os.path
import os
import json


class RepoManager:
    DEFAULT_MODULE = 'examon_repo_1'
    DEFAULT_PIP = 'https://test.pypi.org/simple/'

    def __init__(self):
        self.repos = []
        self.active_repos = []

    def add(self, repo, url):
        self.repos.append({
                'name': repo,
                'pip_url': url
            })

    def remove(self, repo_name):
        index = next((index for (index, d) in enumerate(self.repos) if d["name"] == repo_name), None)
        del self.repos[index]

    def add_active(self, repo):
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
        with open(RepoManager.full_file_path(), 'r') as f:
            data = json.load(f)

        self.repos = data['repositories']['all']
        self.active_repos = data['repositories']['active']

    @staticmethod
    def full_file_path():
        home_directory = os.path.expanduser('~')
        file = f'{home_directory}/.examon'
        return file

    @staticmethod
    def persist_default():
        manager = RepoManager()
        manager.repos = [
            {
                'name': RepoManager.DEFAULT_MODULE,
                'pip_url': RepoManager.DEFAULT_PIP
            }]
        manager.active_repos = [RepoManager.DEFAULT_MODULE]
        manager.persist()

