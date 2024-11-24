# Setting up and Running the App

1. **Create a Virtual Environment**
    **Run the following commands to set up a virtual environment and install dependencies:**
    
    ```bash
    python3 -m venv venv-ai-agent
    source venv-ai-agent/bin/activate
    pip install -r requirements.txt
    ```

2. **Run the App**
    **Start the application using uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    **The app will run on http://127.0.0.1:8000 by default.**

3. **Sending Requests**
    **To process a PDF, use the following curl command:**
    ```bash
    curl --location 'http://127.0.0.1:8000/process_pdf/' \
    --header 'accept: application/json' \
    --form 'questions="{\"question\": [\"What is the name of the company?\"]}"' \
    --form 'file=@/path/to/your/handbook.pdf' \
    --form 'description="This PDF contains information about the Employee Handbook. It includes policies and information about the company."' \
    --form 'check_hallucination="yes"'
    ```
---

#  Parameters

  
- **`questions`**(required): A JSON-formatted string with the question key. It contains a list of questions to ask based on the PDF.**
    - Example: {"question": ["What is the name of the company?"]} 
  
- **`file`**(required): The path to the PDF file you want to upload for processing.
    - Example: /path/to/your/handbook.pdf (Required)

- **`description`**(Optional): A brief description of the content in the PDF. This helps the app understand its context.
    - Example: "This PDF contains information about Employee Handbook..."

- **`check_hallucination`**(Optional): check_hallucination: Enables checking for hallucinated responses. Use "yes" to enable this feature
    - Example: "yes" 