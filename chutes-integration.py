import aiohttp
import asyncio
import json
import os
from dotenv import load_dotenv
load_dotenv()

async def invoke_chute(message:str):
	api_token = os.getenv("CHUTE_API_TOKEN")
	if not api_token:
		print("API token not found. Please set the CHUTE_API_TOKEN environment variable.")
		return

	headers = {
		"Authorization": "Bearer " + api_token,
		"Content-Type": "application/json"
	}
	
	body =     {
	  "model": "deepseek-ai/DeepSeek-R1",
	  "messages": [
		{
		  "role": "user",
		  "content": message
		}
	  ],
	  "stream": True,
	  "max_tokens": 1024,
	  "temperature": 0.7
	}

	async with aiohttp.ClientSession() as session:
		async with session.post(
			"https://llm.chutes.ai/v1/chat/completions", 
			headers=headers,
			json=body
		) as response:				
			answer = ""
			async for line in response.content:
				line = line.decode("utf-8").strip()
				if line.startswith("data: "):
					
					data = line[6:]
					if data == "[DONE]":
						break
					try:
						chunk = data.strip()
						chunk = json.loads(chunk)
						if chunk:
							if type(chunk.get("choices")[0].get("delta").get("content")) == str:
								answer += chunk.get("choices")[0].get("delta").get("content")
					except Exception as e:
						print(f"Error parsing chunk: {e}")
			print(answer)

def ai_invoke(message:str):
	asyncio.run(invoke_chute(message))