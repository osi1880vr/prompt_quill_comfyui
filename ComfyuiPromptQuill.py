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
			return 'Something went wrong, did you install Prompt Quill? https://github.com/osi1880vr/prompt_quill'

	def generate(self, query, model=None):
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
				"add_negative": (("false", "true"), {"default": "false"}),
				"negative": ("STRING", {
					"multiline": True,
					"default": ""
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

	def prompt_quill_generate(self, prompt, add_negative, negative, url, model=None):
		client = Client(url=url)

		response = client.generate(model=model, query=prompt)

		if add_negative != 'false':
			response['neg_prompt'] = f'{response["neg_prompt"]},{negative}'

		return (response['prompt'], response['neg_prompt'],)

class PromptQuillGenerateConditioning:
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
				"add_negative": ("BOOLEAN", {"default": True}),
				"negative": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"url": ("STRING", {
					"multiline": False,
					"default": default_url
				}),
				"clip": ("CLIP", )
			},
		}

	RETURN_TYPES = ("STRING", "STRING","CONDITIONING","CONDITIONING",)
	RETURN_NAMES = ("Prompt", "NegativePrompt","Prompt Conditioning", "Negative Conditioning",)

	FUNCTION = "prompt_quill_generate"
	CATEGORY = "PromptQuill"

	def encode(self, clip, text):
		tokens = clip.tokenize(text)
		cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
		return ([[cond, {"pooled_output": pooled}]], )

	def prompt_quill_generate(self, prompt, add_negative, negative, url, clip):
		client = Client(url=url)

		response = client.generate(query=prompt)

		if add_negative != 'false':
			response['neg_prompt'] = f'{response["neg_prompt"]},{negative}'

		prompt_encoded = self.encode(clip=clip, text=response['prompt'])
		neg_prompt_encoded = self.encode(clip=clip, text=response['neg_prompt'])

		return (response['prompt'], response['neg_prompt'],prompt_encoded[0],neg_prompt_encoded[0],)


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
				"summary": ("BOOLEAN", {"default": True}),
				"rephrase": ("BOOLEAN", {"default": True}),
				"rephrase_prompt": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_style": ("BOOLEAN", {"default": True}),
				"style": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_search": ("BOOLEAN", {"default": True}),
				"search": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_negative": ("BOOLEAN", {"default": True}),
				"negative": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"reset_journey": ("BOOLEAN", {"default": True}),
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
						  search, add_negative, negative, reset_journey, url):
		client = Client(url=url)

		response = client.sail(query=prompt, distance=distance, summary=summary, rephrase=rephrase,
							   rephrase_prompt=rephrase_prompt, add_style=add_style, style=style, add_search=add_search,
							   search=search, reset_journey=reset_journey)

		if add_negative != 'false':
			response['neg_prompt'] = f'{response["neg_prompt"]},{negative}'

		return (response['prompt'], response['neg_prompt'],)



class PromptQuillSailConditioning:
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
				"summary": ("BOOLEAN", {"default": True}),
				"rephrase": ("BOOLEAN", {"default": True}),
				"rephrase_prompt": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_style": ("BOOLEAN", {"default": True}),
				"style": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_search": ("BOOLEAN", {"default": True}),
				"search": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"add_negative": ("BOOLEAN", {"default": True}),
				"negative": ("STRING", {
					"multiline": True,
					"default": ""
				}),
				"reset_journey": ("BOOLEAN", {"default": True}),
				"url": ("STRING", {
					"multiline": False,
					"default": default_url
				}),
				"clip": ("CLIP", )
			},
		}

	RETURN_TYPES = ("STRING", "STRING","CONDITIONING","CONDITIONING",)
	RETURN_NAMES = ("Prompt", "NegativePrompt","Prompt Conditioning", "Negative Conditioning")

	FUNCTION = "prompt_quill_sail"
	CATEGORY = "PromptQuill"


	def encode(self, clip, text):
		tokens = clip.tokenize(text)
		cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
		return ([[cond, {"pooled_output": pooled}]], )

	def prompt_quill_sail(self, prompt, distance, summary, rephrase, rephrase_prompt, add_style, style, add_search,
						  search, add_negative, negative, reset_journey, url, clip):
		client = Client(url=url)

		response = client.sail(query=prompt, distance=distance, summary=summary, rephrase=rephrase,
							   rephrase_prompt=rephrase_prompt, add_style=add_style, style=style, add_search=add_search,
							   search=search, reset_journey=reset_journey)

		if add_negative != 'false':
			response['neg_prompt'] = f'{response["neg_prompt"]},{negative}'

		prompt_encoded = self.encode(clip=clip, text=response['prompt'])
		neg_prompt_encoded = self.encode(clip=clip, text=response['neg_prompt'])

		return (response['prompt'], response['neg_prompt'],prompt_encoded[0],neg_prompt_encoded[0],)



NODE_CLASS_MAPPINGS = {
	"PromptQuillGenerate": PromptQuillGenerate,
	"PromptQuillGenerateConditioning": PromptQuillGenerateConditioning,
	"PromptQuillSail": PromptQuillSail,
	"PromptQuillSailConditioning": PromptQuillSailConditioning,
}

NODE_DISPLAY_NAME_MAPPINGS = {
	"PromptQuillGenerate": "Prompt Quill Generate",
	"PromptQuillGenerateConditioning": "Prompt Quill Generate Conditioning",
	"PromptQuillSail": "Prompt Quill Sailing",
	"PromptQuillSailConditioning": "Prompt Quill Sailing to Conditioning",
}
