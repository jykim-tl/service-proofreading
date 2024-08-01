# 런타임 3.10 으로 돌려야 import 오류 발생하지 않음.
from openai import OpenAI
import json
import logging
import os

# from urllib.parse import parse_qs

API_KEY = os.environ['apiKey']
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def respond(err, totalTokens, parsedContent):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps({"totalTokens":totalTokens, "parsedText": parsedContent["parsedText"], "aiEditedText" : parsedContent["aiEditedText"]}).encode('utf8'),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    # params = parse_qs(event)
    # image_url = params['imageUrl']
    image_url = event['imageUrl']
    
    client = OpenAI(api_key=API_KEY)
    
    promptText = '''
    I want the answer to be given in a JSON format, which has two keys. "parsedText" and "aiEditedText". So It should be in perfect json format like {"parsedText":"first task result", "aiEditedText":"second task result"}. DO NOT INCLUDE ```json in the prefix and ``` in the postfix.
    
    First, read the text in the attached image and put it in the parsedText.
    
    Second, proofread the sentences in the attached image and put it in the aiEditedText.
    When you find typos, grammar mistakes, and unnatural phrases, please use markdown strikethroughs for the errors and provide corrections in markdown bold.
    Markdown strikethroughs use double ~~, not single ~. For example ~~the~~, not ~the~. Do not add any other comments to the response.
    '''
    
    print(image_url)

    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": promptText
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image_url
              },
            },
          ],
        }
      ],
      # max_tokens=500,
    )
    
    totalTokens = response.usage.total_tokens
    print('TOTAL TOKENS USED',totalTokens)
    print('==================================================')
    content = response.choices[0].message.content
    print(content)
    print('==================================================')
    parsedContent = json.loads(content)
    print(parsedContent)

    return respond(None, totalTokens, parsedContent)
