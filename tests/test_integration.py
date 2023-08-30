from examon.lib.examon_engine_factory import ExamonEngineFactory
from examon.view.formatter_options import FormatterOptions
from examon.view.input.answer_question import AutoAnswerInputter

from examon_core.examon_item_registry import ItemRegistryFilter
from examon_core.examon_item_registry import ExamonItemRegistry
import pytest

from fixtures_loader import FixturesLoader


@pytest.fixture(autouse=True)
def run_around_tests():
    ExamonItemRegistry.reset()
    FixturesLoader.load_fixtures()
    yield
    ExamonItemRegistry.reset()


class TestEndToEnd:
    def test_e2e(self):
        registry_filter = ItemRegistryFilter(tags_any=['a'])
        inputter = AutoAnswerInputter(['1', '2', '3'])
        quiz_engine = ExamonEngineFactory.build(ExamonItemRegistry.registry(registry_filter),
                                                FormatterOptions()['null'], inputter)
        quiz_engine.run()
        assert quiz_engine.summary() == (3, 3)

    def test_e2e_2(self):
        registry_filter = ItemRegistryFilter(tags_any=['a'])
        inputter = AutoAnswerInputter(['1', '2', '2'])
        quiz_engine = ExamonEngineFactory.build(ExamonItemRegistry.registry(registry_filter),
                                                FormatterOptions()['null'], inputter)
        quiz_engine.run()
        assert quiz_engine.summary() == (2, 3)
