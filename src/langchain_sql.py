from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings

from src.utils import few_shots, sql_credential, mysql_prompt

class SQLChain:
    def __init__(self):
        load_dotenv()
        self.llm = GoogleGenerativeAI(model='gemini-pro', temperature=0.5)
        self.db = SQLDatabase.from_uri(
            f"mysql+pymysql://{sql_credential['db_user']}:{sql_credential['db_password']}@{sql_credential['db_host']}/{sql_credential['db_name']}",
                                       sample_rows_in_table_info=3)
       
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.to_vectorize = [" ".join(example.values()) for example in few_shots]
        self.vectorstore = Chroma.from_texts(self.to_vectorize, self.embeddings, metadatas=few_shots)
        
        self.example_selector = SemanticSimilarityExampleSelector(vectorstore=self.vectorstore, k=2)
        
        self.custom_prompt = PromptTemplate(
            input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
            template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        )
        
        self.few_shot_prompt = FewShotPromptTemplate(
            example_selector=self.example_selector,
            example_prompt=self.custom_prompt,
            prefix=mysql_prompt,
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"] 
        )
        
    def exec_query(self, input: str) -> dict:
        chain = SQLDatabaseChain.from_llm(self.llm, self.db, prompt=self.few_shot_prompt, verbose=True)
        res = chain.run(input)
        return res   
    
           