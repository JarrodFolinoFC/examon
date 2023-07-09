from examon.view.repo_manager import RepoManager

import pytest


@pytest.fixture(scope="function", autouse=True)
def clear_print_logs():
    RepoManager().reset()


class TestRepoManager:
    def test_initiates_with_empty_repos(self):
        repo_manager = RepoManager()
        assert repo_manager.repos == []
        assert repo_manager.active_repos == []

    def test_add_repo(self):
        repo_manager = RepoManager()
        repo_manager.add('examon')
        assert repo_manager.repos == [
            {'name': 'examon'}
        ]
        assert repo_manager.active_repos == []

    def test_add_repo_empty_string(self):
        repo_manager = RepoManager()
        repo_manager.add('')
        assert repo_manager.repos == []
        assert repo_manager.active_repos == []


    def test_add_repo_None(self):
        repo_manager = RepoManager()
        repo_manager.add(None)
        assert repo_manager.repos == []
        assert repo_manager.active_repos == []

    def test_add_repo_with_url(self):
        repo_manager = RepoManager()
        repo_manager.add('examon', 'http://something.com')
        assert repo_manager.repos == [
            {'name': 'examon', 'url': 'http://something.com'}
        ]
        assert repo_manager.active_repos == []

    def test_reset(self):
        repo_manager = RepoManager()
        repo_manager.add('examon', 'http://something.com')
        repo_manager.reset()
        assert repo_manager.active_repos == []
        assert repo_manager.repos == []


    def test_remove_repo(self):
        repo_manager = RepoManager()
        repo_manager.add('examon', 'http://something.com')
        repo_manager.remove('examon')
        assert repo_manager.active_repos == []
        assert repo_manager.repos == []

    def test_remove_repo_non_existing(self):
        pass


    def test_add_active_repo(self):
        repo_manager = RepoManager()
        repo_manager.add('examon')
        repo_manager.add_active('examon')
        assert repo_manager.active_repos == ['examon']

    def test_remove_active_repo(self):
        repo_manager = RepoManager()
        repo_manager.add('examon')
        repo_manager.add_active('examon')
        repo_manager.remove_active('examon')
        assert repo_manager.active_repos == []


    def test_add_active_repo_existing(self):
        repo_manager = RepoManager()
        repo_manager.add('examon')
        repo_manager.add_active('examon')
        repo_manager.add_active('examon')
        assert repo_manager.active_repos == ['examon']

    def test_as_dict(self):
        repo_manager = RepoManager()
        repo_manager.add('examon')
        repo_manager.add_active('examon')
        assert repo_manager.as_dict() == {
            'repositories':
                {
                    'all': [{'name': 'examon'}],
                    'active': ['examon']
                }
        }

