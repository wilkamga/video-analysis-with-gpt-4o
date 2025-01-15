# Video Analysis with GPT-4o

The aim of this repository is to demonstrate the capabilities of GPT-4o to analyze and extract insights from a video file or a video URL (e.g., YouTube).

The steps to process a video are the following:
1. Split the video into segments of N seconds (or not, if 0 seconds is specified).
2. Extract the frames of the video, 1 frame per second.
3. Transcribe the audio with Whisper, if selected.
4. Analyze the frames and the audio (optional) to extract the description, summarization, or any other insights depending on the prompt.

## Prerequisites
+ An Azure subscription, with [access to Azure OpenAI](https://aka.ms/oai/access).
+ An Azure OpenAI service with the service name and an API key.
+ A deployment of GPT-4o model on the Azure OpenAI Service.
+ A deployment of Whisper model on the Azure OpenAI Service.

I used Python 3.12.5, [Visual Studio Code with the Python extension](https://code.visualstudio.com/docs/python/python-tutorial), and the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) to test this example.

### Set up a Python virtual environment in Visual Studio Code

1. Open the Command Palette (Ctrl+Shift+P).
1. Search for **Python: Create Environment**.
1. Select **Venv**.
1. Select a Python interpreter. Choose 3.10 or later.

It can take a minute to set up. If you run into problems, see [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments).

### Environment Configuration

Create a `.env` file in the root directory of your project with the following content. You can use the provided [`.env-sample.ini`](.env-sample.ini) as a template:

```
SYSTEM_PROMPT="You are an expert on Video Analysis. You will be shown a series of images from a video. Describe what is happening in the video, including the objects, actions, and any other relevant details. Be as specific and detailed as possible."

AZURE_OPENAI_ENDPOINT=<your_azure_openai_endpoint>
AZURE_OPENAI_API_KEY=<your_azure_openai_api_key>
AZURE_OPENAI_API_VERSION=<your_azure_openai_api_version>
AZURE_OPENAI_DEPLOYMENT_NAME=<your_azure_openai_deployment_name>

WHISPER_ENDPOINT=<your_whisper_endpoint>
WHISPER_API_KEY=<your_whisper_api_key>
WHISPER_API_VERSION=<your_whisper_api_version>
WHISPER_DEPLOYMENT_NAME=<your_whisper_deployment_name>
```

The needed libraries are specified in [requirements.txt](requirements.txt).

Here is the code of this demo: [video-analysis-with-gpt-4o.py](video-analysis-with-gpt-4o.py)

A screenshot:
<img src="./Screenshot.png" alt="Sample Screenshot"/>

To run the application, execute this command:
```
streamlit run video-analysis-with-gpt-4o.py
```

To deploy the application on your Azure tenant in an Azure Container Registry (Docker), follow this [guide: Build and store an image by using Azure Container Registry](https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/3-exercise-build-images) and then create and deploy the web app following this [guide: Create and deploy a web app from a Docker image](https://learn.microsoft.com/en-us/training/modules/deploy-run-container-app-service/5-exercise-deploy-web-app).
