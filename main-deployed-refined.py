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
      print(body)
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
    
    commentPromptMapBySubjectName ={
       "SPEECH":
       {
          "V1":'''
        - If the image includes Summary Writing at the top of the page, then follow the Summary Writing Instructions.
        - If the image includes Short Speech Writing at the top of the page, then follow the Short Speech Writing Instructions.
        - If the image inlcudes none of them, follow Summary Writing Instructions.

        - Summary Writing Instructions
          - Please provide constructive feedback on a student's summary essay. The student is at an AR 3 (Lexile 650) level and must have written a 12-sentence summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion. l Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
            - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
          - The overall comment should be one paragraph, without bullet points, no longer than 7 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.

        - Short Speech Writing Instructions
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3 (Lexile 650) level and has written a speech that includes at least 8 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 8 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 7 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
       ''',
          "V2":'''
        - If the image includes Summary Writing at the top of the page, then follow the Summary Writing Instructions.
        - If the image includes Short Speech Writing at the top of the page, then follow the Short Speech Writing Instructions.
        - If the image inlcudes none of them, follow Summary Writing Instructions.

        - Summary Writing Instructions
          - Please provide constructive feedback on a student's summary essay. The student is at an AR 3 (Lexile 650) level and must have written a 12-sentence summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion. l Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
            - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
          - The overall comment should be one paragraph, without bullet points, no longer than 7 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.

        - Short Speech Writing Instructions
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3 (Lexile 650) level and has written a speech that includes at least 8 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 8 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 7 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
       ''',
        "V3":'''
        - If the image includes Summary Writing at the top of the page, then follow the Summary Writing Instructions.
        - If the image includes Short Speech Writing at the top of the page, then follow the Short Speech Writing Instructions.
        - If the image inlcudes none of them, follow Summary Writing Instructions.

        - Summary Writing Instructions
          - Please provide constructive feedback on a student's summary essay. The student is at an AR 3.5 (Lexile 700) level and must have written at least a 12-sentence summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion.
            - Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
            - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
          - The overall comment should be one paragraph, without bullet points, no longer than 8 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.

        - Short Speech Writing Instructions
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3.5 (Lexile 700) level and must have written a speech that includes at least 10 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 10 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 8 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
        '''},       
       "DEBATE":{
          "O1":'''
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 4 (Lexile 750) level and must have written a speech that includes at least 12 sentences: one topic sentence, one conclusion sentence, and one body paragraph. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 12 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 8 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
          ''',
          "O2":'''
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 4.5 (Lexile 800) level and has written a speech that includes at least 16 sentences: one topic sentence, one conclusion sentence, and two body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as problems, benefits, effects or side effects, necessity, harms, alternatives, etc., about the given resolution.
            - Use of Outside Sources: Assess the student's use of outside source evidence to support their argument. Offer suggestions on how to better integrate research or provide additional evidence if needed.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Sentence Structure: Evaluate the variety and complexity of the student's sentence structures. Encourage them to use different types of sentences (simple, compound, complex) to enhance the flow and clarity of their speech. l Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 16 sentences. If they haven't, suggest ways to expand their ideas, add supporting details, or incorporate more research to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 10 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
          ''',
          "O3":'''
          - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 5 (Lexile 850) level and has written a speech that includes at least 16 sentences: one topic sentence, one conclusion sentence, and three body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
            - Grammar: Briefly mention any significant grammar issues, but do not focus too heavily on them.
            - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
            - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as problems, benefits, effects or side effects, necessity, harms, alternatives, etc., about the given resolution.
            - Use of Outside Sources: Assess the student's use of outside source evidence to support their argument. Offer suggestions on how to better integrate research or provide additional evidence if needed.
            - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
            - Sentence Structure: Evaluate the variety and complexity of the student's sentence structures. Encourage them to use different types of sentences (simple, compound, complex) to enhance the flow and clarity of their speech. l Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
            - Sentence Count: Ensure that the student has met the minimum requirement of 20 sentences. If they haven't, suggest ways to expand their ideas, add supporting details, or incorporate more research to meet this requirement.
          - The overall comment should be one paragraph, without bullet points, no longer than 10 sentences, and should aim to encourage the student while providing specific, actionable advice for improvement.
          ''',
       },
       "WRITING":f'''
       - It was written by an elementary school student who is learning English as a foreign language. The student's English level is equivalent to that of a {gradeMapByLevelName[levelName.upper()]} grader in the U.S.
       - Please use a friendly tone and mention specific parts of the essay, highlighting three key positive aspects. Also, point out the areas that need improvement with model examples and explain why these aspects are problematic, using two key terms.
       ''',
       "GRAMMAR&WRITING":f'''
        - It was written by an elementary school student who is learning English as a foreign language. The student's English level is equivalent to that of a {gradeMapByLevelName[levelName.upper()]} grader in the U.S.
        - Please use a friendly tone and mention specific parts of the essay, highlighting three key positive aspects. Also, point out the areas that need improvement with model examples and explain why these aspects are problematic, using two key terms.
        ''',
    }
    
    promptText = f'''
    I want the answer to be given in three parts. First is "parsedText", second is "aiEditedText", and third is "comment".

    DO NOT include ``` as a prefix or postfix in your response.

    1. parsedText:
      - First, read all the text in the attached image, except for the text inside the box labeled "Template." Assign the text you've read to the parsedText field. DO NOT PROOFREAD what is in the parsedText field.
    2. aiEditedText:    
      - Second, proofread the text assigned at parsedText by following the instructions below and place the corrected version in the aiEditedText field:
        - If there is nothing to correct, copy the text as it is.
        - If you find errors such as typos, grammatical mistakes, or unnatural phrases, provide the corrected version using the specified format below. But, BE SURE TO only apply this format on where error and proofread version are, not the whole sentence.
        - Use the following format:
          - Error Version: #$~@error version@~
          - Corrected Version: *@proofread version@*$#
          - Example: #$~@they has@~ *@they have@*$#
    3.Comment:
      - Third, provide comments from the teacher evaluating the overall work on the original text by following the instructions below.
        - When quoting specific words from the original text, use single quotes (' ') instead of double quotes (" "). And do not list suggestions, write in normal paragraph.        
        {commentPromptMapBySubjectName[subjectName.upper()][levelName.upper()]}
    '''        
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

      aiEditedSample = parsedContent["aiEditedText"].replace("~@", '<s>').replace("@~", '</s>').replace("*@", '<b>').replace("@*", '</b>').replace("#$", "<span style='color: red;'>").replace("$#", "</span>")
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
       "body": "{\"imageUrl\": \"https://s3.ap-northeast-2.amazonaws.com/cdn-staging.topialive.co.kr/pdf-homework/1723875053228/1723875054109.png\",\"levelName\": \"V2\",\"subjectName\": \"SPEECH\"}"
    }
    context = []
    lambda_handler(event,context)