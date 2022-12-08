import requests
import json
import os
import pandas as pd

def retrieve_message(channelid):	
	discord_message = []
	headers={
	'authorization':'NzUxMzQ1NTgwNjA4ODQ3OTI0.G3MVUO.-DO-GkbIg2mOP1jwoJxhewheNwXwdIVo-cDges'
	}
	r=requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages?before=839421701463736371&limit=100',headers=headers)
	jsonn = json.loads(r.text)
	for value in jsonn:
		print(value)
		discord_message.append({			
			"timestamp": value['timestamp'],
			"message": value['content']
			})
	return pd.DataFrame(discord_message)
# retrieve_message('808380531791233045')
df=retrieve_message('808380531791233045')
#Write a file
os.makedirs('dataset', exist_ok=True)  
df.to_csv('dataset/message5.csv')  