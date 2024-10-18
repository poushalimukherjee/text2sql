from langchain.agents import Agent
from langchain.prompts import PromptTemplate
from langchain.output_parsers import RegexParser
from pydantic import BaseModel, Field

class TextToSQLAgent(Agent, BaseModel):
    llm: object = Field(...)
    sql_executor: object = Field(...)
    prompt_template: PromptTemplate = Field(
        default_factory=lambda: PromptTemplate(
            template="Convert the following text to an SQL query: {text}",
            input_variables=["text", "agent_scratchpad"]
        )
    )
    output_parser: RegexParser = Field(
        default_factory=lambda: RegexParser(
            regex=r"SELECT .* FROM .* WHERE .*",
            output_keys=["query"]
        )
    )

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self.llm_chain = self.prompt_template | self.llm

    def _get_default_output_parser(self) -> RegexParser:
        return self.output_parser

    def create_prompt(self, text: str) -> str:
        return self.prompt_template.format(text=text, agent_scratchpad="")

    @property
    def llm_prefix(self) -> str:
        return "LLM:"

    @property
    def observation_prefix(self) -> str:
        return "Observation:"

    def run(self, text: str):
        prompt = self.create_prompt(text)
        sql_query = self.llm_chain(prompt)
        return self.sql_executor.execute(sql_query)


# from langchain.agents import Agent
# from app.prompts.prompt_templates import prompt_template

# class TextToSQLAgent(Agent):
#     def __init__(self, llm, sql_executor):
#         self.llm = llm
#         self.prompt_template = prompt_template
#         self.sql_executor = sql_executor

#     def run(self, text):
#         prompt = self.prompt_template.format(text=text)
#         sql_query = self.llm.generate(prompt)
#         return self.sql_executor.execute(sql_query)
    
# from langchain.agents import Agent
# from langchain.prompts import PromptTemplate
# # from langchain.output_parsers import OutputParser, SimpleOutputParser
# # from langchain.output_parsers import SimpleOutputParser
# from langchain.output_parsers.structured import StructuredOutputParser
# from langchain.chains import LLMChain
# from pydantic import BaseModel, Field

# class TextToSQLAgent(Agent, BaseModel):
#     llm: object = Field(...)
#     sql_executor: object = Field(...)
#     prompt_template: PromptTemplate = Field(
#         default=PromptTemplate(
#             template="Convert the following text to an SQL query: {text}",
#             input_variables=["text"]
#         )
#     )
#     llm_chain: LLMChain = Field(...)
#     output_parser: StructuredOutputParser = Field(
#         default_factory=lambda: StructuredOutputParser(response_schemas={})
#     )

#     class Config:
#         arbitrary_types_allowed = True

#     def __init__(self, **data):
#         super().__init__(**data)
#         self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

#     def _get_default_output_parser(self) -> StructuredOutputParser:
#         return self.output_parser

#     def create_prompt(self, text: str) -> str:
#         return self.prompt_template.format(text=text)

#     @property
#     def llm_prefix(self) -> str:
#         return "LLM:"

#     @property
#     def observation_prefix(self) -> str:
#         return "Observation:"

#     def run(self, text: str):
#         prompt = self.create_prompt(text)
#         sql_query = self.llm_chain.generate(prompt)
#         return self.sql_executor.execute(sql_query)

# class TextToSQLAgent(Agent, BaseModel):
#     llm: any
#     sql_executor: any
#     prompt_template: PromptTemplate = PromptTemplate(
#         template="Convert the following text to an SQL query: {text}",
#         input_variables=["text"]
#     )

#     def _get_default_output_parser(self) -> StructuredOutputParser:
#         # Implement the default output parser
#         return StructuredOutputParser()

#     def create_prompt(self, text: str) -> str:
#         return self.prompt_template.format(text=text)

#     @property
#     def llm_prefix(self) -> str:
#         return "LLM:"

#     @property
#     def observation_prefix(self) -> str:
#         return "Observation:"

#     def run(self, text: str):
#         prompt = self.create_prompt(text)
#         sql_query = self.llm.generate(prompt)
#         return self.sql_executor.execute(sql_query)  
