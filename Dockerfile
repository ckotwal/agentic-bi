# Use a Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the src directory to /app/src
COPY src /app/src

# Copy the images directory to /app/images
COPY images /app/images

# Copy the .streamlit directory to /app/.streamlit
COPY .streamlit /app/.streamlit

# Install dependencies from src/requirements.txt
RUN pip install --no-cache-dir -r src/requirements.txt

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Set the entrypoint to streamlit run src/chatbot_ui.py
ENTRYPOINT ["streamlit", "run", "src/chatbot_ui.py"]
