import aiohttp
import asyncio
import json

async def invoke_chute(message:str):
	with open("api_key.txt", "r") as file:
		api_key = file.read().strip()
	api_token = api_key

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

asyncio.run(invoke_chute("Hello, how are you?"))