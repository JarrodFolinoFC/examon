import os
from examon.lib.storage.write.examon_writer_factory import ExamonWriterFactory
from examon.lib.config.config_dir_factory import ConfigDirFactory
from examon_core.examon_item_registry import ExamonItemRegistry
from sqlalchemy import create_engine


class Helpers:

    @staticmethod
    def clean():
        ExamonItemRegistry.reset()

    @staticmethod
    def setup_everything2(f):
        dir_factory_build = Helpers.setup_directories()

        # Add to in memory model
        f()

        # ingest
        db_name = f'{dir_factory_build.examon_dir}/examon.db'
        ExamonWriterFactory.build(dir_factory_build.code_files_full_path(),
                                  db_name,
                                  ExamonItemRegistry.registry()).run()

        return create_engine(f"sqlite+pysqlite:///{db_name}", echo=True)

    @staticmethod
    def setup_directories():
        # Reset Models
        ExamonItemRegistry.reset()
        cwd = os.getcwd()
        dir_factory_build = ConfigDirFactory.build(f'{cwd}/tests/tmp/.examon')
        # clean
        ConfigDirFactory.clean(dir_factory_build)
        # setup config dirs
        ConfigDirFactory.init_everything(dir_factory_build)
        return dir_factory_build
