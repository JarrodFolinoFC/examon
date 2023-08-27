from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.lib.results_manager import ResultsManager
from examon.view.formatter_options import FormatterOptions
from examon_core.examon_item_registry import ItemRegistryFilter
from examon.lib.settings_manager_factory import SettingsManagerFactory
from examon.lib.config.examon_config import ExamonConfig
from examon.lib.config.examon_config_json_init import ExamonConfigJsonInit
from examon.lib.pip_installer import PipInstaller
from examon.lib.storage.question_factory import QuestionFactory


class RunnerCli:
    @staticmethod
    def process_command(cli_args):
        config = ExamonConfig()
        path = config.config_full_file_path()
        ExamonConfigJsonInit.persist_default_config(path)

        manager = SettingsManagerFactory.build(path)
        PipInstaller.import_packages(manager.active_packages)
        questions = cli_args.max_questions
        if questions is not None:
            questions = int(questions)

        item_registry_filter = ItemRegistryFilter(
            tags_any=RunnerCli.get_tags(cli_args),
            tags_all=RunnerCli.tags_as_array(cli_args.tags_mandatory),
            max_questions=questions,
            difficulty_category=cli_args.difficulty,
        )
        questions = QuestionFactory.load(manager.mode, config, item_registry_filter)

        examon_engine = ExamonEngineFactory.build(
            questions, FormatterOptions()[
                cli_args.formatter])
        if cli_args.dry_run:
            return
        examon_engine.run()

        if cli_args.file:
            results_manager = ResultsManager(examon_engine.responses, manager.active_packages, item_registry_filter,
                                             file_name=cli_args.file)
            results_manager.save_to_file()
            print(f'Results saved to {results_manager.full_path}')
        print(examon_engine.summary())

    @staticmethod
    def get_tags(cli_args):
        tags = []
        if cli_args.tags is not None:
            tag_str = cli_args.tags

            tags = RunnerCli.tags_as_array(tag_str)
        if cli_args.tag is not None:
            tags.append(cli_args.tag)

        return tags if len(tags) > 0 else None

    @staticmethod
    def tags_as_array(tag_str):
        if tag_str is None or tag_str == '':
            return None
        return [tag.strip() for tag in tag_str.split(',')]
