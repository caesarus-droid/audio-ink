#!/bin/bash
echo "Starting AudioInk setup..."
python3 setup.py

if [ $? -eq 0 ]; then
    echo
    echo "Setup completed successfully!"
    echo
    echo "To start the application:"
    echo "1. Activate the virtual environment:"
    echo "   source venv/bin/activate"
    echo "2. Run the application:"
    echo "   python run.py"
    echo
    echo "The application will be available at http://localhost:5000"
else
    echo
    echo "Setup failed. Please check the error messages above."
fi 