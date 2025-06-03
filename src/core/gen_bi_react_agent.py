# https://python.langchain.com/docs/integrations/tools/sql_database/
#Name the employees and their total sales across years.  draw a bar chart of the results
import os
import json
import pathlib
from typing import Dict, Any, List, Optional, Iterator

from dotenv import load_dotenv
from langchain import hub
from langchain.chat_models.base import BaseChatModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from core.viz_tools import VizTools


class GenBIReactAgent:
    """A class representing a Generative BI React Agent.
    
    This agent handles natural language queries, converts them to SQL,
    executes them, and provides visualizations when appropriate.
    """
    
    def __init__(self, db_uri: str = None, model_name: str = "openai:gpt-4.1"):
        """Initialize the GenBIReactAgent.
        
        Args:
            db_uri: The database URI to connect to
            model_name: The name of the language model to use
        """
        # Initialize database connection
        if db_uri is None:
            DB_USER = os.getenv("DB_USER", "postgres")
            DB_PASSWORD = os.getenv("DB_PASSWORD", "password12")
            DB_HOST = os.getenv("DB_HOST", "db")
            DB_PORT = os.getenv("DB_PORT", "5432")
            DB_NAME = os.getenv("DB_NAME", "chinook")
            db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        self.db = SQLDatabase.from_uri(db_uri)
        
        # Initialize language model
        self.llm = self._init_chat_model(model_name)
        
        # Initialize SQL toolkit
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        
        # Set up the agent prompt
        prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
        assert len(prompt_template.messages) == 1
        suffix = " Do not attempt to integrate any images or charts generated into your final response."
        self.system_message = prompt_template.format(dialect="PostgreSQL", top_k=30) + suffix
        print(self.system_message)
        
        # Initialize visualization tools
        VizTools.init(self.llm)
        
        # Create agent executor
        self.react_agent = self._create_react_agent()
    
    def _init_chat_model(self, model_name: str) -> BaseChatModel:
        """Initialize and return the chat model."""
        from langchain.chat_models import init_chat_model
        return init_chat_model(model_name)
    
    def _create_react_agent(self):
        """Create and return the agent executor with all necessary tools."""
        tools = self.toolkit.get_tools() + VizTools.get_tools()
        return create_react_agent(self.llm, tools, prompt=self.system_message,
                                  checkpointer=(InMemorySaver()), debug=False)
    
    def _process_message(self, message, bi_agent_callback_handler):
        """Process a tool message and invoke appropriate callbacks.
        
        Args:
            message: The message to process
            bi_agent_callback_handler: The callback handler for BI agent events
        """
        if not hasattr(message, 'type') or not hasattr(message, 'name') or not hasattr(message, 'content'):
            return
            
        if message.type != 'tool' or not bi_agent_callback_handler:
            return
            
        try:
            if message.name == 'sql_db_query_checker':
                self._process_sql(bi_agent_callback_handler, message)
            elif message.name == 'visualize_pandas_dataframe':
                self._process_chart(bi_agent_callback_handler, message)
            elif message.name == 'convert_to_pandas':
                self._process_data(bi_agent_callback_handler, message)
                        
        except Exception as e:
            print(f"Error processing message: {e}")

    def _process_data(self, bi_agent_callback_handler, message):
        if hasattr(bi_agent_callback_handler, 'process_data'):
            if hasattr(message, 'content') and message.content is not None:
                bi_agent_callback_handler.process_data(str(message.content))

    def _process_chart(self, bi_agent_callback_handler, message):
        try:
            content_dict = json.loads(message.content)
            if 'image' in content_dict and hasattr(bi_agent_callback_handler, 'process_chart'):
                bi_agent_callback_handler.process_chart(str(content_dict['image']))
            if 'code' in content_dict and hasattr(bi_agent_callback_handler, 'process_chart_code'):
                bi_agent_callback_handler.process_chart_code(str(content_dict['code']))
        except json.JSONDecodeError:
            print("Failed to decode message content as JSON")

    def _process_sql(self, bi_agent_callback_handler, message):
        if hasattr(bi_agent_callback_handler, 'process_sql'):
            bi_agent_callback_handler.process_sql(str(message.content))

    def stream(self, query: str, session_id: str = None, bi_agent_callback_handler=None) -> str:
        """Process a query and return the content of the last message.
        
        Args:
            query: The natural language query to process
            session_id: Optional session ID for conversation tracking
            bi_agent_callback_handler: Optional callback handler for BI agent events
            
        Returns:
            str: The content of the last message, or an empty string if no message or content
        """
        input_dict = {"messages": [("user", query)]}
        last_message = None

        # Run the agent
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }

        for event in self.react_agent.stream(input_dict, config=config, stream_mode="values"):
            if "messages" in event and event["messages"]:
                print(f"Received {len(event['messages'])} messages:")
                last_message = event["messages"][-1]
                
                # Process the message with callback handler if available
                if bi_agent_callback_handler is not None and hasattr(last_message, 'type') and last_message.type == 'tool':
                    self._process_message(last_message, bi_agent_callback_handler)
                    
                last_message.pretty_print()
        
        # Safely return the content of the last message or an empty string
        if hasattr(last_message, 'content') and last_message.content is not None:
            if bi_agent_callback_handler is not None and hasattr(bi_agent_callback_handler, 'process_last_message'):
                bi_agent_callback_handler.process_last_message(last_message.content)
            return str(last_message.content)
        return ""



def main():
    """Main entry point for the GenBI React Agent application."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Database path
    db_path = "sqlite:///" + str(pathlib.Path(__file__).parent.parent.resolve() / "chinook.db")
    
    # Initialize the agent
    agent = GenBIReactAgent(db_uri=db_path)
    
    print("GenBI React Agent initialized. Type 'q' to quit.")
    
    # Main interaction loop
    while True:
        try:
            user_input = input("\nEnter your query: ").strip()
            if user_input.lower() == 'q':
                print("Exiting...")
                break
                
            # Process the query and display results
            agent.stream(user_input, "1", bi_agent_callback_handler=PrintBICallbackHandler())

                    
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


class PrintBICallbackHandler:


    """A simple callback handler that prints BI-related information.
    
    This handler can be used for debugging or logging purposes to see the data
    being processed by the BI agent.
    """
    
    def process_sql(self, sql_query: str) -> None:
        """Print the SQL query being executed.
        
        Args:
            sql_query: The SQL query string to be printed
        """
        print("\n=== SQL Query ===")
        print(sql_query)
        print("=================\n")
    
    def process_chart(self, image_data: str) -> None:
        """Print a message indicating chart image data was received.
        
        Args:
            image_data: The base64 encoded image data (only the length is printed)
        """
        print(f"\n=== Chart Image Data (length: {len(image_data) if image_data else 0}) ===\n")
    
    def process_chart_code(self, chart_code: str) -> None:
        """Print the chart generation code.
        
        Args:
            chart_code: The code used to generate the chart
        """
        print("\n=== Chart Generation Code ===")
        print(chart_code)
        print("============================\n")

    def process_last_message(self, message_content: str) -> None:
        """Print the content of the last message.

        Args:
            message_content: The content of the last message
        """
        print("\n=== Last Message Content ===")
        print(message_content)
        print("=============================\n")

    def process_data(self, data_content: str) -> None:
        """Print the data content received from a 'convert_to_pandas' message.
        
        Args:
            data_content: The data content to be printed
        """
        print("\n=== Data Content ===")
        print(data_content)
        print("====================\n")



if __name__ == "__main__":
    main()
    
