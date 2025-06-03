from typing import Annotated, Dict, Any
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from lida import Manager, TextGenerationConfig, llm
from lida.datamodel import Goal
import os
import pandas as pd
from io import StringIO

from core.image_manager import image_manager


class VizTools:
    """A class containing tools for data visualization and analysis."""
    
    # Class variable to store the language model
    langchain_llm = None
    
    # Prompt templates
    DATA_ANALYSIS_PROMPT = """
    Analyze the following data: {sql_query_result}
    Your job is to answer the following question: {prompt}
    Be concise and technical in your response and restrict it to less than 50 words
    Do not ask any other questions or attempt to generate any code and visualizations
    """
    
    DATA_CONVERSION_PROMPT = """
    You are an expert Pandas developer who has to convert the following data: {sql_query_result}
    which is a python list of tuples to a CSV string. The CSV String will be used to create
    a Pandas dataframe by using the read_csv method on the dataframe. The first row
    of the CSV String should be comma separated list of the column names which can be derived from {prompt} 
    Make intelligent guesses about the datatypes and convert empty values to appropriate
    numeric and string values. If its not possible to convert return ERROR. Return only the
    CSV string and nothing else. Example output is
    First_Name,Last_Name,Age
    John,Doe,30
    Per,Games,21
    """

    CHART_PROMPT = """
    You need to give clear instructions to generate a chart for the following data: {sql_query_result}
    which will be converted into a Pandas dataframe. From the {prompt} extract concise and clear instructions
    to generate a chart in less than 8 words
    """
    
    @staticmethod
    def init(llm_model):

        """Initialize the VizTools class with a language model.

        Args:
            llm_model: The language model to use
        """

        VizTools.langchain_llm = llm_model
    
    @staticmethod
    @tool
    def analyze_data(
            prompt: Annotated[str, "The original HumanMessage prompt"],
            sql_query_result: Annotated[str, "The output LLM answer after the sql_db_query is run "]) -> str:
        """Analyze data to extract insights as per the prompt"""
        if VizTools.langchain_llm is None:
            raise ValueError("VizTools not initialized. Call VizTools.init() first.")
            
        formatted_prompt = VizTools.DATA_ANALYSIS_PROMPT.format(sql_query_result=sql_query_result, prompt=prompt)
        print(f"Prompt:{formatted_prompt}")
        response = VizTools.langchain_llm.invoke(formatted_prompt)
        return response.content if response.content else "No analysis could be generated"
    
    @staticmethod
    @tool
    def convert_to_pandas(
            prompt: Annotated[str, "The original HumanMessage prompt"],
            sql_query_result: Annotated[str, "The output LLM answer after the sql_db_query is run "]) -> str:
        """Convert data to a format compatible with a Pandas dataframe"""
        if VizTools.langchain_llm is None:
            raise ValueError("VizTools not initialized. Call VizTools.init() first.")
            
        formatted_prompt = VizTools.DATA_CONVERSION_PROMPT.format(sql_query_result=sql_query_result, prompt=prompt)
        response = VizTools.langchain_llm.invoke(formatted_prompt)
        print(f"Converted data:{response.content}")
        return response.content if response.content else "CONVERT_ERROR"
    
    @staticmethod
    @tool
    def visualize_pandas_dataframe(
            prompt: Annotated[str, "The original HumanMessage prompt"],
            sql_query_result: Annotated[str, "The output CSV string after the convert_to_pandas tool is run "]) -> Dict[str, Any]:
        """Visualize a Pandas dataframe by drawing a chart"""
        if VizTools.langchain_llm is None:
            raise ValueError("VizTools not initialized. Call VizTools.init() first.")
            

        api_key = os.getenv("OPENAI_API_KEY")
        lida = Manager(text_gen=llm("openai", api_key=api_key))
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.0,
            model="gpt-4",
            use_cache=True)
        data = pd.read_csv(StringIO(sql_query_result))
        print(f"Dataframe:{data}")
        summary = lida.summarize(
            data,
            summary_method="llm",
            textgen_config=textgen_config)
        print(f"Summary:{summary}")

        prompt = VizTools._extract_chart_goal(sql_query_result, prompt)
        print(f"Chart Prompt:{prompt}")

        charts = lida.visualize(
            summary=summary,
            goal=(Goal(question=prompt, visualization=prompt, rationale="")),
            textgen_config=textgen_config,
            library="seaborn")

        if not charts:
            return "VIZ_ERROR"

        image_id = image_manager.store(charts[0].raster)
        #return a reference to the image to avoid session bloat
        return {"code": charts[0].code, "image": image_id}

    @staticmethod
    def _extract_chart_goal(data, prompt):
        formatted_chart_prompt = VizTools.CHART_PROMPT.format(sql_query_result=data, prompt=prompt)
        response = VizTools.langchain_llm.invoke(formatted_chart_prompt)
        prompt = response.content if response.content else prompt
        return prompt

    @classmethod
    def get_tools(cls) -> list:
        """Get a list of all tool-annotated methods in this class.
        
        Returns:
            list: A list containing the tool-annotated methods
        """
        return [
            cls.analyze_data,
            cls.convert_to_pandas,
            cls.visualize_pandas_dataframe
        ]


    @staticmethod
    def mock_visualize_pandas_dataframe(
            prompt: Annotated[str, "The original HumanMessage prompt"],
            sql_query_result: Annotated[str, "The output CSV string after the convert_to_pandas tool is run "]) -> Dict[str, Any]:
        """Visualize a Pandas dataframe by drawing a chart"""
        if VizTools.langchain_llm is None:
            raise ValueError("VizTools not initialized. Call VizTools.init() first.")


        api_key = os.getenv("OPENAI_API_KEY")
        lida = Manager(text_gen=llm("openai", api_key=api_key))
        textgen_config = TextGenerationConfig(
            n=1,
            temperature=0.0,
            model="gpt-4",
            use_cache=True)
        df = pd.read_csv(StringIO(sql_query_result))
        print(f"Dataframe:{df}")
        summary = lida.summarize(
            df,
            summary_method="llm",
            textgen_config=textgen_config)
        print(f"Summary:{summary}")

        prompt = VizTools._extract_chart_goal(sql_query_result, prompt)
        print(f"Chart Prompt:{prompt}")

        charts = lida.visualize(
            summary=summary,
            goal=(Goal(question=prompt, visualization=prompt, rationale="")),
            textgen_config=textgen_config,
            library="seaborn")

        if not charts:
            return "VIZ_ERROR"

        image_id = image_manager.store(charts[0].raster)
        #return a reference to the image to avoid session bloat
        return {"code": charts[0].code, "image": image_id}