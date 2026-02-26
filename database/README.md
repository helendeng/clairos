# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install all requirements
pip install -r requirements.txt

# 4. Verify installation
python -c "import qdrant_client; import sentence_transformers; import pandas; print('✓ All packages installed successfully!')"

# To store chunks into database:
python main.py

# To visualize the chunks in the database:
python visualize_database.py

# Clean database:
python clean_database.py

# Generate json files for RAG:
python json_output.py