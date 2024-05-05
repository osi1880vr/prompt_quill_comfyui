# Copyright 2024 osiworx

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

import requests
from PIL import Image
import numpy as np
import base64
from io import BytesIO
class Client:
    default_url = "http://127.0.0.1:64738"
    def __init__(self, url=None):
        if url is None:
            # Use class variable if no argument provided
            url = Client.default_url
        self.url = url
        self.generate_url = f'{self.url}/get_prompt'



    def generate(self, query, model):
        # Prepare your JSON data
        payload = {'query': query,
                   'model':model}
        # Set the Content-Type header to indicate JSON data
        headers = {"Content-Type": "application/json"}
        # Send the POST request
        response = requests.post(self.generate_url, json=payload, headers=headers)
        # Check for successful response
        if response.status_code == 200:
            # Access the response data (if any)
            response_data = response.json()
            return response_data
        else:
            return response.text

default_url = "http://127.0.0.1:64738"
class PromptQuillGenerate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "A cute cat?"
                }),
                "url": ("STRING", {
                    "multiline": False,
                    "default": default_url
                }),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("Prompt","NegativePrompt",)

    FUNCTION = "prompt_quill_generate"
    CATEGORY = "PromptQuill"

    def prompt_quill_generate(self, prompt, url, model=None):

        client = Client(url=url)

        response = client.generate(model=model, query=prompt)

        return (response['prompt'],response['neg_prompt'],)





NODE_CLASS_MAPPINGS = {
    "PromptQuillGenerate": PromptQuillGenerate,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptQuillGenerate": "Prompt Quill Generate",
}

