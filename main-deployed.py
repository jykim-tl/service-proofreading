# 런타임 3.10 으로 돌려야 import 오류 발생하지 않음.
from openai import OpenAI
import json
import logging
import os

# from urllib.parse import parse_qs

API_KEY = os.environ['apiKey']
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def raise_error(msg):
    raise ValueError(msg)

def respond(err, totalTokens, result):
    response = {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps({
            "totalTokens": totalTokens,
            "parsedText": result["parsedText"],
            "aiEditedText": result["aiEditedCommentConcat"]
        }).encode('utf8'),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    # print('######### RESPONSE #########')
    # print(response)
    
    return response


def lambda_handler(event, context):
    # params = parse_qs(event)
    
    try:
      body = event['body']
      parsedBody = json.loads(body)
      imageUrl = parsedBody['imageUrl']
      levelName = parsedBody['levelName']
      subjectName = parsedBody['subjectName']
    except Exception as e:
      print(f"Caught an error: {e}")
      raise_error("CHECK EVENT BODY It should include imageUrl, levelName, subjectName")

    print(f"PARSED_BODY : {parsedBody}")
    
    client = OpenAI(api_key=API_KEY)
    
    """
    24.08.13 jy.kim
    levelName, subjectName 기준으로 prompt 변경 필요.
    proofreading 수준 및 comment 수준 결정해야함.
    """

    commentPromptMapByLevelName ={
       "V1":"This is written by an elementary school student who is learning English as a foreign language and has an English level equivalent to a 2nd grader in the U.S.",
       "V2":"",
       "V3":"",
       "O1":"",
       "O2":"",
       "O3":"",
    }

    # subjectName 대문자로 전환하여 조회해서 사용.
    commentPromptMapBySubjectName ={
       "SPEECH":"It was written as a speech homework.",
       "DEBATE":"",
       "WRITING":"",
       "GRAMMAR&WRITING":"",
    }
    
    promptText = '''
    I want the answer to be given in three parts. First is "parsedText", second is "aiEditedText", and third is "comment".
    DO NOT INCLUDE ``` prefix and ``` in the postfix.    
    
    First, read the text in the attached image and put it in the parsedText.
    
    Second, proofread the sentences in the attached image and put it in the aiEditedText.
    When you find typos, grammar mistakes, and unnatural phrases, please use markdown strikethroughs for the errors and provide corrections in markdown bold.
    Markdown strikethroughs use double ~~, not single ~. For example ~~the~~, not ~the~.
    Also, PLEASE MAKE SURE TO add specified characters at the beginning and end of typos, grammar mistakes, and unnatural phrases.
    Starting with #$ and ending with $#. For example, #$~~Unnatural pharases~~ **Edited version.**$#

    Third, provide comments to the original text following given directions.
    When writing comments, if you want to quote some of the words used , please use single quote(') not double quote("). And do not list suggestions, write in normal paragraph.
    If you do not get further direction, only keep in mind that this comment will be provided back to elementary school student.
    '''
    
    commentByLevelPrompt = commentPromptMapByLevelName[levelName.upper()]
    commentBySubjectPrompt = commentPromptMapBySubjectName[subjectName.upper()]

    promptText += commentByLevelPrompt
    promptText += commentBySubjectPrompt

    cautionText = '''
    Also, PLEASE MAKE SURE to maintain perfect json format like json format like {"parsedText":"first task result", "aiEditedText":"second task result", "comment":"comments provided"} after comments are added.
    Especially, please make sure to close the value of string with double quote(").    
    Because your response will be parsed in python script with json.loads() function.
    '''
    
    promptText+=cautionText
    
    print(f"IMAGE_URL : {imageUrl}")
    print(f"PROMPT_TEXT : {promptText}")

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
      # splitContent = content.split('###')
      # parsedText = splitContent[0]
      # aiEditedText = splitContent[1].replace("#$", '<span style="color: red;">').replace("$#", '</span>').replace("@#", '</br>')
      # jsonFormatted = {parsedText,aiEditedText}
      print('==================================================')
      # parsedContent = json.loads(jsonFormatted)
      parsedContent = json.loads(content)
      print(parsedContent)

      aiEditedSample = parsedContent["aiEditedText"].replace("#$", '<span style="color: red;">').replace("$#", '</span>')
      print(f"aiEditedSample: {aiEditedSample}")

      aiEditedCommentConcat = aiEditedSample + '</br>' + parsedContent["comment"]

      result = {
         "parsedText" :parsedContent["parsedText"],
         "aiEditedCommentConcat" : aiEditedCommentConcat,
      }
            
      return respond(None, totalTokens, result)
    except Exception as e:
      logger.error(f"Exception during OpenAI API call: {e}")
      raise_error(f"Exception during OpenAI API call: {e}")
