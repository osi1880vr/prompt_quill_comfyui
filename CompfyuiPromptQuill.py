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

default_url = "http://127.0.0.1:64738"


class Client:
	default_url = default_url

	def __init__(self, url=None):
		if url is None:
			# Use class variable if no argument provided
			url = Client.default_url
		self.url = url
		self.generate_url = f'{self.url}/get_prompt'
		self.sail_url = f'{self.url}/get_next_prompt'


	def send_api_call(self,payload, url):
		# Set the Content-Type header to indicate JSON data
		headers = {"Content-Type": "application/json"}
		# Send the POST request
		response = requests.post(url, json=payload, headers=headers)
		# Check for successful response
		if response.status_code == 200:
			# Access the response data (if any)
			response_data = response.json()
			return response_data
		else:
			return response.text

	def generate(self, query, model):
		# Prepare your JSON data
		payload = {'query': query,
				   'model': model}
		return self.send_api_call(payload, self.generate_url)


	def sail(self, query, distance, summary, rephrase, rephrase_prompt, add_style, style, add_search, search, reset_journey):
		payload = {'query': query,
				   'distance': distance,
				   'summary': summary,
				   'rephrase': rephrase,
				   'rephrase_prompt': rephrase_prompt,
				   'add_style': add_style,
				   'style': style,
				   'add_search': add_search,
				   'search': search,
				   'reset_journey': reset_journey
				   }
		return self.send_api_call(payload, self.sail_url)

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

	RETURN_TYPES = ("STRING", "STRING",)
	RETURN_NAMES = ("Prompt", "NegativePrompt",)

	FUNCTION = "prompt_quill_generate"
	CATEGORY = "PromptQuill"

	def prompt_quill_generate(self, prompt, url, model=None):
		client = Client(url=url)

		response = client.generate(model=model, query=prompt)

		return (response['prompt'], response['neg_prompt'],)


class PromptQuillSail:
	def __init__(self):
		pass

	@classmethod
	def IS_CHANGED(cls, **kwargs):
		return float("NaN")

	@classmethod
	def INPUT_TYPES(s):
		return {
			"required": {
				"prompt": ("STRING", {
					"multiline": True,
					"default": "A cute cat?"
				}),
				"distance": ("INT", {"default": 20, "min": 1, "max": 10000, "step": 1}),
				"summary": (("false", "true"), {"default": "false"}),
				"rephrase": (("false", "true"), {"default": "false"}),
				"rephrase_prompt": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_style": (("false", "true"), {"default": "false"}),
				"style": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_search": (("false", "true"), {"default": "false"}),
				"search": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"reset_journey": (("false", "true"), {"default": "false"}),
				"url": ("STRING", {
					"multiline": False,
					"default": default_url
				}),
			},
		}

	RETURN_TYPES = ("STRING", "STRING",)
	RETURN_NAMES = ("Prompt", "NegativePrompt",)

	FUNCTION = "prompt_quill_sail"
	CATEGORY = "PromptQuill"

	def prompt_quill_sail(self, prompt, distance, summary, rephrase, rephrase_prompt, add_style, style, add_search,
						  search, reset_journey, url):
		client = Client(url=url)

		response = client.sail(query=prompt, distance=distance, summary=summary, rephrase=rephrase,
							   rephrase_prompt=rephrase_prompt, add_style=add_style, style=style, add_search=add_search,
							   search=search, reset_journey=reset_journey)

		return (response['prompt'], response['neg_prompt'],)


NODE_CLASS_MAPPINGS = {
	"PromptQuillGenerate": PromptQuillGenerate,
	"PromptQuillSail": PromptQuillSail
}

NODE_DISPLAY_NAME_MAPPINGS = {
	"PromptQuillGenerate": "Prompt Quill Generate",
	"PromptQuillSail": "Prompt Quill Sailing"
}
