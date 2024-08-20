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

def respond(err, totalTokens, result, promptText):
    response = {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps({
            "totalTokens": totalTokens,
            "parsedText": result["parsedText"],
            "aiEditedText": result["aiEditedCommentConcat"],
            # "promptText": promptText
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

    gradeMapByLevelName = {
       "V1":'2nd',
       "V2":'3rd',
       "V3":'3rd',
       "O1":'4th',
       "O2":'4th',
       "O3":'4th'
    }  

    # subjectName 대문자로 전환하여 조회해서 사용할 경우
    # commentPromptMapBySubjectName ={
    #    "SPEECH":"It was written as a speech homework.",
    #    "DEBATE":"",
    #    "WRITING":"",
    #    "GRAMMAR&WRITING":"",
    # }
    
    promptText = f'''
    I want the answer to be given in three parts. First is "parsedText", second is "aiEditedText", and third is "comment".

    DO NOT include ``` as a prefix or postfix in your response.

    1. parsedText:
      - First, read all the text in the attached image, except for the text inside the box labeled "Template." Assign the text you've read to the parsedText field.
    2. aiEditedText:    
      - Second, proofread the text from parsedText by following the instructions below and place the corrected version in the aiEditedText field:
        - If there is nothing to correct, copy the text as it is.
        - If you find errors such as typos, grammatical mistakes, or unnatural phrases, provide the corrected version using the specified format below. But, BE SURE TO only apply this format on where error and proofread version are, not the whole sentence.
        - Use the following format:
          - Error Version: #$~-error version-~
          - Corrected Version: *+proofread version+*$#
          - Example: #$~-they has-~ *+they have+*$#
    3.Comment:
      - Third, provide comments from the teacher evaluating the overall work on the original text by following the instructions below.
        - It was written by an elementary school student who is learning English as a foreign language. The student's English level is equivalent to that of a {gradeMapByLevelName[levelName.upper()]} grader in the U.S.
        - When quoting specific words from the original text, use single quotes (' ') instead of double quotes (" "). And do not list suggestions, write in normal paragraph.
        - Please use a friendly tone and mention specific parts of the essay, highlighting three key positive aspects. Also, point out the areas that need improvement with model examples and explain why these aspects are problematic, using two key terms.
    '''
        
    # commentBySubjectPrompt = commentPromptMapBySubjectName[subjectName.upper()]
    # promptText += commentBySubjectPrompt

    cautionText = '''
    IMPORTANT:
      - Ensure that the final output is in perfect JSON format, like this:
        - {"parsedText":"first task result", "aiEditedText":"second task result", "comment":"comments provided"}
      - Make sure to close the value of each string with double quotes (" "). The response will be parsed using the json.loads() function in Python.
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
        max_tokens = 4096 # gpt-4o model's max  
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
      # print(parsedContent)

      aiEditedSample = parsedContent["aiEditedText"].replace("~-", '<s>').replace("-~", '</s>').replace("*+", '<b>').replace("+*", '</b>').replace("#$", '<span style="color: red;">').replace("$#", '</span>')
      # print(f"aiEditedSample: {aiEditedSample}")

      aiEditedCommentConcat = aiEditedSample + '</br>' + parsedContent["comment"]

      result = {
         "parsedText" :parsedContent["parsedText"],
         "aiEditedCommentConcat" : aiEditedCommentConcat,
      }
            
      return respond(None, totalTokens, result, promptText)
    except Exception as e:
      logger.error(f"Exception during OpenAI API call: {e}")
      raise_error(f"Exception during OpenAI API call: {e}")
