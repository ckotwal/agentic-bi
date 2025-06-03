import base64
import streamlit as st
from io import BytesIO
import csv
import io
import pandas as pd
from core.image_manager import image_manager


class StreamlitBIMessageRenderer:
    """A simple callback handler that renders BI related information in Streamlit.
    This handler can be used for rendering the results of the BI agent in Streamlit
    """

    def __init__(self, v_store_in_session: bool = False):
        """Initialize the StreamlitBICallbackHandler.

        Args:
            store_in_session: Whether to store messages in Streamlit session state
        """
        self._store_in_session = v_store_in_session
        
    def process_message(self, content: str, message_type: str) -> None:
        """Route the content to the appropriate handler method based on message_type.

        Args:
            content: The content to be processed
            message_type: The type of message, determines which handler to use
        """
        handler_map = {
            'sql': self.process_sql,
            'image': self.process_chart,
            'chart_code': self.process_chart_code,
            'text': self.process_last_message,
            'table': self.process_data
        }
        
        handler = handler_map.get(message_type)
        if handler:
            handler(content)
        else:
            st.warning(f"No handler found for message type: {message_type}")
            print(f"Warning: No handler found for message type: {message_type}")

    def process_sql(self, sql_query: str) -> None:
        """Print the SQL query being executed.

        Args:
            sql_query: The SQL query string to be printed
        """
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_container.markdown(sql_query)
            self.store_in_session(sql_query, "sql")
        print("\n=== SQL Query ===")
        print(sql_query)
        print("=================\n")

    def store_in_session(self, content, message_type):
        if self._store_in_session:
            st.session_state.messages.append({
                "role": "assistant",
                "type": message_type,
                "content": content
            })


    def process_chart(self, image_id: str) -> None:
        """Print a message indicating chart image data was received.

        Args:
            image_data: The base64 encoded image data (only the length is printed)
        """
        response_container = st.empty()
        image_data = image_manager.load(image_id)
        response_container.image(self._decode_base64_image(image_data))
        self.store_in_session(image_id, "image")
        print(f"\n=== Chart Image Data (length: {len(image_data) if image_data else 0}) ===\n")

    def process_chart_code(self, chart_code: str) -> None:
        """Print the chart generation code.

        Args:
            chart_code: The code used to generate the chart
        """
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_container.code(chart_code)
            self.store_in_session(chart_code, "chart_code")
        print("\n=== Chart Generation Code ===")
        print(chart_code)
        print("============================\n")

    def process_last_message(self, message_content: str) -> None:
        """Print the content of the last message.

        Args:
            message_content: The content of the last message
        """
        with st.chat_message("assistant"):
            response_container = st.empty()
            response_container.markdown(message_content)
            self.store_in_session(message_content, "text")
        print("\n=== Last Message Content ===")
        print(message_content)
        print("=============================\n")

    def process_data(self, data_content: str) -> None:
        """Print the data content received from a 'convert_to_pandas' message.

        Args:
            data_content: The data content to be printed
        """
        with st.chat_message("assistant"):
            self._render_table_from_csv(data_content)
            self.store_in_session(data_content, "table")

        print("\n=== Data Content ===")
        print(data_content)

        print("====================\n")

    def _decode_base64_image(self, encoded: str):
        try:
            return BytesIO(base64.b64decode(encoded))
        except Exception as e:
            st.error(f"Error decoding image: {e}")
            return None
    def _render_table_from_csv(self, csv_text: str):
        try:
            reader = csv.reader(io.StringIO(csv_text.strip()))
            rows = list(reader)
            df = pd.DataFrame(rows[1:], columns=rows[0])
            response_container = st.empty()
            response_container.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Table rendering failed: {e}")
            st.text(csv_text)
