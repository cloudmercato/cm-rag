"""
.. note::
    + Easy usage and access
    - Unable to define large tables (from `df.head()`)
    - Lack of column context definition
    - Average of result is bad
    - Use `eval`
"""
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core import PromptTemplate
from django.utils.functional import cached_property
from core.files import FileManager
from core.llm import OllamaManager

FLAVOR_PROMPT = """\
You are working with a pandas dataframe in Python.
This dataframe represents the flavors from different cloud providers.
The name of the dataframe is `df`.
This is a dict representing the columns of the dataframe and examples of values:
{df_str}

Follow these instructions:
{instruction_str}
Query: {query_str}

Expression: """


class PandasQueryEngine(PandasQueryEngine):
    def _get_table_context(self):
        return str(self._df.columns.to_list())


class PandasManager:
    def __init__(
        self,
        verbose=True,
    ):
        self.verbose = verbose

    @cached_property
    def files(self):
        return FileManager()

    @cached_property
    def ollama(self):
        return OllamaManager(
        ).ollama

    @cached_property
    def flavor_df(self):
        return self.files.read_csv('flavors')

    @cached_property
    def flavor_query_engine(self):
        prompt = PromptTemplate(FLAVOR_PROMPT)
        query_engine = PandasQueryEngine(
            df=self.flavor_df,
            llm=self.ollama,
            verbose=self.verbose,
        )
        query_engine.update_prompts({"pandas_prompt": prompt})
        return query_engine
