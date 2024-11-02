## Serving Llama3 with Modal

### Preparation

- Sign up for a [Modal account](https://modal.com/).
- Clone this repository to establish a local project

### Set Up Secrets

To allow secure communication, you need to set up a shared secret both server-side (in Modal, where the LLM is hosted) and client-side, wherever you're going to query the LLM, whether that's locally from the command line, locally from an IDE like vscode, or from a notebook platform like Colab. 

1. Go to **Modal** → **Your account** → **Dashboard** → **Secrets** and select **creating a Custom Secret**.  Create a Custom Secret with:
- Key: DSBA_LLAMA3_KEY 
- Value: <A secret string of characters>
- Name: dsba-llama3-key

2. Create a .env file in this folder. Add two environmental variables:

```
DSBA_LLAMA3_KEY="<SECRET_VALUE>"
MODAL_BASE_URL="https://<MODAL WORKSPACE>--vllm-openai-compatible-serve.modal.run/v1/"
```

### Set Up Virtual Environment

1. Open a command line interface in this folder.  

2. Create a virtual environment using venv.  Assuming Python 3.10:

```python
python3.10 -m venv venv        # Adjust for Python version - 3.11 also works
```

3. Activate your virtual environment with one of the following commands:
```
source venv/bin/activate       # Mac 
```

```
venv\Scripts\activate          # Windows CMD
```

```
.\venv\Scripts\activate.ps1    # Windows Powershell
```

4. Upgrade pip (optional, but good practice) 
```
python -m pip install --upgrade pip
```

5. Install required packages:
```
python -m pip install -r requirements.txt
```

### Set Up and Deploy Modal

1. Set up Modal:

```
python -m modal setup
```

2. A browser window will open.  Select your Modal account. 

You should receive a `Web authentication finished successfully!` message.


3. Deploy Modal

```bash
modal deploy api.py
```

This will then provide you a URL endpoint: <https://your-workspace-name--vllm-openai-compatible-serve.modal.run>

![Example of a successful Modal deployment](llama_modal/modal-deploy.png)

You can view the Swagger API doc at <https://your-workspace-name--vllm-openai-compatible-serve.modal.run/docs>


### Run Test

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
