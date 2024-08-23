def getCommentGuide(subjectName:str, levelName:str):
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
                - Please provide constructive feedback on a student's summary essay. The student is at an AR 3 (Lexile 650) level and must have written a summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion.
                    - Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
                    - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
                - The overall comment should be one paragraph, without bullet points, no longer than 8 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement if necessary.

            - Short Speech Writing Instructions
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3 (Lexile 650) level and has written a speech that includes at least 8 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 8 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 8 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
               
            ''',
            "V2":'''
            - If the image includes Summary Writing at the top of the page, then follow the Summary Writing Instructions.
            - If the image includes Short Speech Writing at the top of the page, then follow the Short Speech Writing Instructions.
            - If the image inlcudes none of them, follow Summary Writing Instructions.

            - Summary Writing Instructions
                - Please provide constructive feedback on a student's summary essay. The student is at an AR 3 (Lexile 650) level and must have written a summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion.
                    - Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
                    - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
                - The overall comment should be one paragraph, without bullet points, no longer than 8 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement if necessary.

            - Short Speech Writing Instructions
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3 (Lexile 650) level and has written a speech that includes at least 8 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 8 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 8 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
            ''',
            "V3":'''
            - If the image includes Summary Writing at the top of the page, then follow the Summary Writing Instructions.
            - If the image includes Short Speech Writing at the top of the page, then follow the Short Speech Writing Instructions.
            - If the image inlcudes none of them, follow Summary Writing Instructions.

            - Summary Writing Instructions
                - Please provide constructive feedback on a student's summary essay. The student is at an AR 3.5 (Lexile 700) level and must have written a summary based on a given template. The feedback should be written in a friendly and encouraging tone, focusing on the following area study:
                    - Organization: Comment on the clarity and structure of the topic sentence, body paragraphs, and conclusion.
                    - Vocabulary: Evaluate the student’s word choice, suggesting ways they might vary their vocabulary or use synonyms to improve paraphrasing.
                    - Paraphrasing: Assess the effectiveness of the student’s paraphrasing, offering advice on how they can better rephrase content if necessary.
                - The overall comment should be one paragraph, without bullet points, no longer than 10 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement if necessary.

            - Short Speech Writing Instructions
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 3.5 (Lexile 700) level and must have written a speech that includes at least 10 sentences: one topic sentence, one conclusion sentence, and body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 10 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 10 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
            '''     
        },       
        "DEBATE":{
            "O1":'''
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 4 (Lexile 750) level and must have written a speech that includes at least 12 sentences: one topic sentence, one conclusion sentence, and one body paragraph. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as benefits, harms, necessity, etc., about the given resolution.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 12 sentences. If they haven't, suggest ways to expand their ideas or add details to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 12 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
            ''',
            "O2":'''
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 4.5 (Lexile 800) level and has written a speech that includes at least 16 sentences: one topic sentence, one conclusion sentence, and two body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs,and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as problems, benefits, effects or side effects, necessity, harms, alternatives, etc., about the given resolution.
                    - Use of Outside Sources: Assess the student's use of outside source evidence to support their argument. Offer suggestions on how to better integrate research or provide additional evidence if needed.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Sentence Structure: Evaluate the variety and complexity of the student's sentence structures. Encourage them to use different types of sentences (simple, compound, complex) to enhance the flow and clarity of their speech. l Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 16 sentences. If they haven't, suggest ways to expand their ideas, add supporting details, or incorporate more research to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 13 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
            ''',
            "O3":'''
                - Please provide constructive feedback on a student's short speech, written using the provided template. The student is at an AR 5 (Lexile 850) level and has written a speech that includes at least 16 sentences: one topic sentence, one conclusion sentence, and three body paragraphs. The feedback should be written in a friendly and encouraging tone, focusing on the following areas:
                    - Organization: Comment on the clarity and structure of the speech, ensuring the topic sentence, body paragraphs, and conclusion sentence are effectively organized.
                    - Main Idea and Supporting Details: Evaluate how well the student presents the main idea and supports it with relevant details in the body paragraphs. Recommend that the student includes details such as problems, benefits, effects or side effects, necessity, harms, alternatives, etc., about the given resolution.
                    - Use of Outside Sources: Assess the student's use of outside source evidence to support their argument. Offer suggestions on how to better integrate research or provide additional evidence if needed.
                    - Vocabulary: Assess the student's choice of vocabulary, offering suggestions for improvement if necessary.
                    - Sentence Structure: Evaluate the variety and complexity of the student's sentence structures. Encourage them to use different types of sentences (simple, compound, complex) to enhance the flow and clarity of their speech. l Paraphrasing: If relevant, mention the effectiveness of paraphrasing within the speech.
                    - Sentence Count: Ensure that the student has met the minimum requirement of 20 sentences. If they haven't, suggest ways to expand their ideas, add supporting details, or incorporate more research to meet this requirement.
                - The overall comment should be one paragraph, without bullet points, at least but no longer than 15 sentences, and should start with a compliment. The general aim should be to encourage the student while providing specific, actionable advice for improvement. Do not use too many “but”s as it may discourage the student. Provide examples for improvement as well.
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

    return commentPromptMapBySubjectName[subjectName.upper()][levelName.upper()] if subjectName.upper() == 'SPEECH' or subjectName.upper() == 'DEBATE' else commentPromptMapBySubjectName[subjectName.upper()]
    