# 런타임 3.10 으로 돌려야 import 오류 발생하지 않음.
from openai import OpenAI
import json
import logging
import os
from commentGuides import getCommentGuide

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
      print(body)
      parsedBody = json.loads(body)
      imageUrl:str = parsedBody['imageUrl']
      levelName:str = parsedBody['levelName']
      subjectName:str = parsedBody['subjectName']
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

    errorPrefix = "(("
    errorPostfix = "))"
    proofreadPrefix = "[["
    proofreadPostfix = "]]"

    groupPrefix = "{{"
    groupPrefixVersion2 = "} }"
    groupPostfix = "}}"
    groupPostfixVersion2 = "} }"

    promptText = f'''
    You will be given (an) image(s) that include English text. DO NOT consider it to be Spanish or any other language.
    I want you to parse, edit, and provide feedback on the provided text in English.
    I want the response to be in three parts: First is "parsedText", second is "aiEditedText", and third is "comment".
    DO NOT include `json` or any formatting symbols like backticks as a prefix or postfix in your response.

    1. **parsedText:
      - Carefully extract all readable text from the attached image(s), excluding any text inside the box labeled "Template."
      - Ignore the following sentence if encountered: `Education For Evaluation Purposes Only (remove with TRIAL key)`.
      - Separate paragraphs where appropriate.
      - Ignore any book titles, author names, or page numbers typically found at the top or bottom of the image.
      - Validate the text for logical consistency to ensure coherent sentences. If something appears incomplete or broken, flag it as such without correcting it.
      - Store this raw, unaltered text in the `parsedText` field.
    2. **aiEditedText:    
      - Proofread the content from `parsedText`, focusing on grammar, spelling, and unnatural phrasing.
      - Double-check that capitalization is properly applied.
      - Use the following format for any corrections:
        - Error Version: {errorPrefix} error version {errorPostfix}
        - Corrected Version: {proofreadPrefix} corrected version {proofreadPostfix}
        - Encapsulation: Encapsulate both versions beginning with {groupPrefix} and ending with {groupPostfix}.
        - Example: {groupPrefix} {errorPrefix} they has {errorPostfix} {proofreadPrefix} they have {proofreadPostfix} {groupPostfix}
      - Only apply the format to the specific location of the error, not the entire sentence.
      - If no corrections are needed, retain the uncorrected text in `aiEditedText`. DO NOT discard any portion of the text.
      - If the error version and the corrected version are the same, it means you have accidentally edited an already correct word, phrase, or sentence. Revert it to its original form.
      - Ensure the final output strictly follows the correction format.
    3.**comment:    
      - Write a single-paragraph, first-person comment providing constructive feedback. DO NOT list suggestions in bullet points.
      - Remember that the comment will be given to elementary school students, so avoid using complex words.
      - Consider the overall context of the text. If certain content or sentence structures repeat, give feedback on this.
      - Quote specific words using single quotes (' ') and base the comment on the student's original text, not the corrected version.
      - DO NOT break lines in the comment.
      - Start the paragraph with this exact prefix: `- Comment:`
      - If no valid sentences are found in the image, return "Blank Page" as the comment output.
      {getCommentGuide(subjectName.upper(), levelName.upper())} 
    '''
    cautionText = '''
    IMPORTANT:
      - Ensure that the final output is in perfect JSON format, like this:
        - {"parsedText":"first task result", "aiEditedText":"second task result", "comment":"comments provided"}
      - Make sure to close the value of each string with double quotes (" "). The response will be parsed using the json.loads() function in Python.
    '''
    
    promptText+=cautionText
    
    print(f"IMAGE_URL : {imageUrl}")
    # print(f"PROMPT_TEXT : {promptText}")

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
      
      print('==================================================')
      print('================= START promptText ===============')
      print(promptText)
      print('================== END promptText ================')
      print('==================================================')
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

      aiEditedSample = parsedContent["aiEditedText"].replace(errorPrefix, '<s>').replace(errorPostfix, '</s>').replace(proofreadPrefix, '<b>').replace(proofreadPostfix, '</b>').replace(groupPrefix, "<span style='color: red;'>").replace(groupPostfix, "</span>").replace(groupPrefixVersion2, "<span style='color: red;'>").replace(groupPostfixVersion2, "</span>")
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


# for local test
if __name__ == "__main__":
    event = {
       "body": "{\"imageUrl\": \"https://s3.ap-northeast-2.amazonaws.com/cdn.topialive.co.kr/pdf-homework/1727176352118/1727176352461.png\",\"levelName\": \"L1\",\"subjectName\": \"WRITING\"}"
    }
    context = []
    lambda_handler(event,context)