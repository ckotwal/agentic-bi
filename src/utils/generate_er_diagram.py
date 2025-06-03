import sqlalchemy as sa
from eralchemy import render_er

# Create a temporary ER diagram from the DDL file using ERAlchemy
import os

# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Construct the path to the DDL file
input_path = os.path.join(project_root, 'src', 'ddl', 'chinook.ddl')
output_path = "/mnt/data/chinook_er.png"

# Render ER diagram from the DDL file
render_er(input_path, output_path)

output_path