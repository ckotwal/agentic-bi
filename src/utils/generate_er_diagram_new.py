import os
from eralchemy import render_er

# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Construct the path to the DDL file
input_path = os.path.join(project_root, 'src', 'ddl', 'chinook.ddl')

# Create a 'generated' directory if it doesn't exist
generated_dir = os.path.join(project_root, 'generated')
os.makedirs(generated_dir, exist_ok=True)

# Set the output path for the ER diagram
output_path = os.path.join(generated_dir, 'chinook_er.png')

# Render ER diagram from the DDL file
render_er(input_path, output_path)

print(f"ER diagram generated at: {output_path}")
output_path
