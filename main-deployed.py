# 런타임 3.10 으로 돌려야 import 오류 발생하지 않음.
from openai import OpenAI
import json
import logging
import os

# from urllib.parse import parse_qs

API_KEY = os.environ['apiKey']
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def raise_error():
    raise ValueError("Check Event Body.")

def respond(err, totalTokens, parsedContent):
    response = {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps({
            "totalTokens": totalTokens,
            "parsedText": parsedContent["parsedText"],
            "aiEditedText": parsedContent["aiEditedText"]
        }).encode('utf8'),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    print('######### RESPONSE #########')
    print(response)
    
    return response


def lambda_handler(event, context):
    # params = parse_qs(event)
    print(event)
    try:
      body = event['body']
      parsedBody = json.loads(body)
      imageUrl = parsedBody['imageUrl']
      levelName = parsedBody['levelName']
      subjectName = parsedBody['subjectName']
    except Exception as e:
      print(f"Caught an error: {e}")
      raise_error()
    
    client = OpenAI(api_key=API_KEY)
    
    """
    24.08.13 jy.kim
    levelName, subjectName 기준으로 prompt 변경 필요.
    proofreading 수준 및 comment 수준 결정해야함.
    """

    commentPromptMapByLevelName ={
       "V1":"",
       "V2":"",
       "V3":"",
       "O1":"",
       "O2":"",
       "O3":"",
    }

    # subjectName 대문자로 전환하여 조회해서 사용.
    commentPromptMapBySubjectName ={
       "SPEECH":"",
       "DEBATE":"",
       "WRITING":"",
    }
    
    promptText = '''
    I want the answer to be given in a JSON format, which has two keys. "parsedText" and "aiEditedText". So It should be in perfect json format like {"parsedText":"first task result", "aiEditedText":"second task result"}. DO NOT INCLUDE ```json in the prefix and ``` in the postfix.
    
    First, read the text in the attached image and put it in the parsedText.
    
    Second, proofread the sentences in the attached image and put it in the aiEditedText.
    When you find typos, grammar mistakes, and unnatural phrases, please use markdown strikethroughs for the errors and provide corrections in markdown bold.
    Markdown strikethroughs use double ~~, not single ~. For example ~~the~~, not ~the~. Do not add any other comments to the response.
    '''
    
    print(imageUrl)

    try:
      response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {
            "role": "user",
            "content": [
               {
                  "type":"text",
                  "text": promptText
               },
               {
                "type": "image_url",
                "image_url": {"url": imageUrl}
               }
            ]
          }
        ],        
      )
      
      totalTokens = response.usage.total_tokens
      print('TOTAL TOKENS USED', totalTokens)
      print('==================================================')
      content = response.choices[0].message.content
      print(content)
      print('==================================================')
      parsedContent = json.loads(content)
      print(parsedContent)
  
      return respond(None, totalTokens, parsedContent)
    except Exception as e:
      logger.error(f"Exception during OpenAI API call: {e}")
      raise_error()
