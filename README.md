# medical-chatbot
Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS
How to run?
STEPS:
1) Clone the repository
   git clone https://github.com/entbappy/Build-a-Complete-Medical-Chatbot-with-LLMs-LangChain-Pinecone-Flask-AWS.git

STEP 01 - Create a virtual environment after opening the repository
(Using conda)
   conda create -n medibot python=3.10 -y
   conda activate medibot

(Or using venv)
   python3 -m venv venv
   source venv/bin/activate

STEP 02 - install the requirements
   pip install -r requirements.txt

Additional package required for Gemini (if not in requirements.txt):
   pip install langchain-google-genai
   pip install python-dotenv

Create a `.env` file in the root directory and add your Pinecone & Gemini credentials as follows:
   PINECONE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

(Implementation note)
- In the code we recommend reading GEMINI_API_KEY and then (if the Gemini client library expects it) set:
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")
  so both environment names are covered.

# run the following command to store embeddings to pinecone
   python store_index.py

# Finally run the following command
   python app.py

Now, open up:
   http://localhost:8080

Techstack Used:
- Python
- LangChain
- Flask
- Gemini (Google Generative Models)
- Pinecone
- AWS (ECR / EC2 / GitHub Actions CICD)

Deployment overview:
1. Build docker image of the source code
2. Push your docker image to ECR
3. Launch an EC2 instance
4. Pull your image from ECR on EC2
5. Run your docker image on EC2

AWS Policy / Permissions recommended for the runner:
1. AmazonEC2ContainerRegistryFullAccess
2. AmazonEC2FullAccess

Deployment steps (short):
1. Create ECR repo to store/save docker image
   - Save the URI, e.g. 315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot
2. Create EC2 machine (Ubuntu)
3. Install docker on EC2:
   sudo apt-get update -y
   sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   newgrp docker
4. Configure EC2 as self-hosted runner:
   Settings → Actions → Runner → New self-hosted runner → choose OS → run the given commands
5. Setup GitHub repository secrets:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - GEMINI_API_KEY

Notes / Tips:
- In your `.env` do **not** put quotes around values (use `KEY=value`).
- Keep `.env` listed in `.gitignore` to avoid leaking keys.
- Make sure your app reads `.env` (e.g. `from dotenv import load_dotenv; load_dotenv()`), and if you keep the internal code expecting `GOOGLE_API_KEY`, set `os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")` at startup.
- Confirm model names supported by your account (e.g. `gemini-1.5-flash`, `gemini-2.0-flash`, etc.) and use a valid one when creating the LLM client.

