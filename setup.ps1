# Create a virtual environment
python -m venv env

# Activate the virtual environment
.\env\Scripts\Activate.ps1

# Install required packages from req.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
