# csms-summarize
AI Text Summarization Project

Overview
This project is an AI-based text summarization tool designed to generate concise, coherent, and customizable summaries from a variety of document types.
It employs both extractive and abstractive summarization techniques using NLP models, such as those from the Hugging Face Transformers library.

The project structure:

csms_summarize/

data/                   # Directory for storing input data
models/                 # Directory for storing trained/pre-trained models
src/                    # Directory for source code
notebooks/              # Jupyter notebooks for experimentation
.gitignore              # Files to be ignored by Git
README.md               # Project documentation
environment.yml         # Conda environment specification


Installation Guide

Prerequisites:
[Anaconda](https://www.anaconda.com/download)
[Visual Studio Code](https://code.visualstudio.com/download)
Python 3.12

Step 1: Clone the Repository
First, clone the repository to your local machine:

        git clone https://github.com/Xyveran/csms_summarize
        cd {wherever you want to have this}

Step 2: Set Up Conda Environment
        Create and activate the Conda environment using the provided environment.yml file:

        conda env create -f environment.yml
        conda activate summarization_env

If you don’t have the environment.yml file, you can manually create the environment:

        conda create -n summarization_env python=3.12
        conda activate summarization_env

Step 3: Install Dependencies Using pip
Once the environment is active, run the following command to install the packages listed in the requirements.txt file:

        pip install -r requirements.txt

Step 4: Set Up Visusal Studio Code
Install the Python extension for VS Code.
Select the Conda environment:
Open VS Code.
Press Ctrl+Shift+P and search for "Python: Select Interpreter".
Choose the summarization_env environment.
