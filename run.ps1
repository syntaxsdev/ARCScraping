# Get the directory path of the script
$scriptDir = Split-Path $MyInvocation.MyCommand.Path

# Change to the directory where the script is located
Set-Location $scriptDir

# Run the Python script
python interface.py