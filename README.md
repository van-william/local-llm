# local-llm
Local LLM Chat with Ollama and Streamlit

# Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd local-llm
   ```

4. Create a new virtual environment

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements

    ```bash
   $ pip install -r requirements.txt
   ```

6. Install Ollama at https://ollama.com/download

7. Download Ollama models
    ```bash
   $ ollama pull deepseek-r1:1.5b
   $ ollama pull llama3.2
   ```

7. Run the app by navigating to the main directory and running:
    ```bash
   $ streamlit run app.py
   ```


   ## Notes on two versions
   You can either call the ollama command line prompt directly with **subprocess** or you can use the ollama library (pip install ollama); there is minor formatting issues with the pip library, but both are included in the GitHub repository