import requests
import json
import os
from typing import Optional

BASE_API_URL = os.getenv("BASE_API_URL")
ADVICE_LANGFLOW_ID = os.getenv("ADVICE_LANGFLOW_ID")
ADVICE_APPLICATION_TOKEN = os.getenv("ADVICE_APPLICATION_TOKEN")
GOALS_LANGFLOW_ID = os.getenv("GOALS_LANGFLOW_ID")
GOALS_APPLICATION_TOKEN = os.getenv("GOALS_APPLICATION_TOKEN")

def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


def get_nutrition(question:str, profile:str):
    TWEAKS = {
    "TextInput-73Z67": {
        "input_value": question
    },
    "TextInput-BMuZe": {
        "input_value": dict_to_string(profile)
    },
    }
    return run_model("", 
                     model="nutrition",
                     model_id=ADVICE_LANGFLOW_ID,
                     tweaks=TWEAKS, 
                     application_token=ADVICE_APPLICATION_TOKEN
                     )


def get_goals(goals:str, profile:str):
    TWEAKS = {
    "TextInput-7TfcP": {
        "input_value": ",".join(goals)
    },
    "TextInput-kJ5K3": {
        "input_value": dict_to_string(profile)
    },
    }
    response = run_model("", 
                         model="goals", 
                         model_id=GOALS_LANGFLOW_ID,
                         tweaks=TWEAKS, 
                         application_token=GOALS_APPLICATION_TOKEN
                         )
    return json.loads(response)


def run_model(message: str,
    model:str, 
    model_id: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :message: The message to send to the flow
    :model: The model to send the flow to
    :endpoint: The ID or the endpoint name of the flow
    :tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    
    api_url = f"{BASE_API_URL}/lf/{model_id}/api/v1/run/{model}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    data = response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
    
    return data