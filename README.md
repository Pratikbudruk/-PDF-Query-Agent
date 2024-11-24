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
# Using Docker to Run the Code
**Follow these steps to build and run the app using Docker:**

1. **Build the Docker Image**: Run the following command to build the Docker image:
   ```bash
   docker build -t pdf-processing-app .
    ```
   
2. **Run the Docker Container**: Start a container from the built image:
   ```bash
   docker run -p 8000:8000 pdf-processing-app
   ```
   
3. **Access the App**: The app will be available at http://127.0.0.1:8000.

Expected Response
Here is an example of what the response will look like:
```bash
{"What is the name of the company?":"The name of the company is Zania, Inc. The CEO mentioned in the closing statement is Shruti Gupta. The company's ethics code and mission statement are also provided in the document.",
"Who is the CEO of the company?":"Shruti Gupta is the CEO of Zania, Inc.",
"What is their vacation policy?":"Employees accrue vacation time based on the period worked, up to a maximum accrual amount. Vacation requests should be made in advance, and the company considers business needs when granting them. Unused vacation may be forfeited upon separation of employment unless state law dictates otherwise.","What is the termination policy?":"The termination policy outlines common-sense infractions that could lead to discipline, including immediate termination of employment. Management may provide verbal and written warnings before taking disciplinary actions, which can include demotion, transfer, forced leave, or termination. The specific terms of termination procedures are governed by state laws, and disciplinary actions may be taken without prior warning or procedure."}
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

---

# Notes
- **`Updating OpenAI Model`:**
    In the agents.py file, you can specify which OpenAI model to use. Look for the section in the code where the model is configured and update it to your desired model, such as gpt-3.5-turbo, gpt-4, etc.
    Ensure that your OpenAI API key and billing plan support the selected model.

- **`Optional Parameters`:**
    The description field is optional. If provided, it helps the app validate the context of the questions.
    The check_hallucination field is also optional. Use "yes" to enable hallucination checks.