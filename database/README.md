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