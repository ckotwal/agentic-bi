import os
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch
import pytest
from core.viz_tools import VizTools
from core.image_manager import image_manager



def test_visualization():
    """
    Test the visualization functionality by initializing the LLM and calling visualize_pandas_dataframe.
    This is an integration test that verifies the basic functionality of the visualization tools.
    """
    load_dotenv()
    # Setup test data
    sample_data = """First_Name,Last_Name,Total_Sales
                    Jane,Peacock,833.04
                    Margaret,Park,775.4
                    Steve,Johnson,720.16
"""
    prompt = "Show a bar chart of values by name"
    
    # Create a mock LLM that returns a predefined response for the chart goal
    class MockLLM:
        def invoke(self, prompt):
            # Return a simple chart goal based on the prompt
            return MagicMock(content="Plot bar chart: Name vs Total_Sales from dataframe")  # Echo back the prompt as the goal
    
    # Initialize the LLM with our mock
    mock_llm = MockLLM()
    VizTools.init(mock_llm)
    
    # Call the method under test
    result = VizTools.mock_visualize_pandas_dataframe(prompt, sample_data)
    
    # Verify the results
    assert isinstance(result, dict)
    assert 'code' in result
    assert 'image' in result
    assert isinstance(result['code'], str)
    assert isinstance(result['image'], str)
    
    # Print the results for inspection
    print("\nVisualization test results:")
    print(f"Generated code : {result['code']} ")
    print(f"Image data: {image_manager.load(result['image'])}")
    
    # Verify the code contains expected elements
    assert 'import' in result['code']
    assert 'plt' in result['code'] or 'sns' in result['code']
    
    return result


if __name__ == "__main__":
    # This allows running the test directly with Python
    result = test_visualization()
    print("\nTest completed successfully!")

