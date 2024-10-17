# Serving Llama3 with Modal

## 1 Account Setup

Make sure you have signed up for a [Modal account](https://modal.com/).

## 2 Local Repository

Clone this repository to establish a local project

## 3 Secrets

To allow secure communication, you need to set up a shared secret both server-side (in Modal, where the LLM is hosted) and client-side, wherever you're going to query the LLM, whether that's locally from the command line, locally from an IDE like vscode, or from a notebook platform like Colab. 

### Server-side

Go to **Modal** → **Your account** → **Dashboard** → **Secrets** and select **creating a Custom Secret**.  Create a Custom Secret with key=DSBA_LLAMA3_KEY and value = the secret value shared among the team.

### Client-side

In your local project .env file (or equivalent repository for secrets) add two environmental variables:

DSBA_LLAMA3_KEY="<SECRET_VALUE>"
MODAL_BASE_URL="https://<MODAL WORKSPACE>--vllm-openai-compatible-serve.modal.run/v1/"


## 4 Virtual Environment

Change directory to the root folder of your local project.

Assuming Python 3.10:

```python
python3.10 -m venv venv        # Adjust for Python version - 3.11 also works

#Depending on OS, one of the following:
source venv/bin/activate       # Mac 
venv\Scripts\activate          # Windows CMD
.\venv\Scripts\activate.ps1    # Windows Powershell

#All operating systems:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5 Modal Setup

```python
python -m modal setup
```

A browser window will open and you should select your Modal account. 

You should receive a `Web authentication finished successfully!` message.


## 6 Modal Deployment

After supplying the secret in Modal, you should be able to run the following command with no error:

```bash
modal deploy llama_on_modal/api.py
```

This will then provide you a URL endpoint: <https://your-workspace-name--vllm-openai-compatible-serve.modal.run>

![Example of a successful Modal deployment](docs/modal-deploy.png)

You can view the Swagger API doc at <https://your-workspace-name--vllm-openai-compatible-serve.modal.run/docs>


## 7 Run Test

Now, you can run a test to ensure setup was successful and the model is being served:

```
$ python llama_on_modal/client.py
🧠: Looking up available models on server at https://your-workspace-name--vllm-openai-compatible-serve.modal.run/v1/. This may trigger a boot!
🧠: Requesting completion from model /models/NousResearch/Meta-Llama-3-8B-Instruct
👉: You are a poetic assistant, skilled in writing satirical doggerel with creative flair.
👤: Compose a limerick about baboons and racoons.
🤖: There once were two creatures quite fine,
Baboons and raccoons, a curious combine,
They raided the trash cans with glee,
In the moon's silver shine,
Together they dined, a messy entwine.
```
