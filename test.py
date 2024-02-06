import json
import logging
import azure.functions as func
import google.generativeai as genai
import pathlib
import textwrap

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    input_desc_text = req.params.get('desc')
    input_ac_text = req.params.get('ac')

    genai.configure(api_key='AIzaSyDNUSAs1CgQh1WF3bUbMfUBd8dFaYdaoj4')
    model = genai.GenerativeModel('gemini-pro')


    input_Template_Upper = "Given an input as user story description: "

    input_Template_Desc = input_desc_text

    input_Template_Lower = " and input as the following acceptance criteria send me all in depth top 30 of functional test cases in an array. "
    #input_Template_Lower += "of all below scenarios, for the acceptance criteria. "
    input_Template_Lower += "The functional test case must have description, expected result. "
    input_Template_Lower += "Make sure to apply and follow them directly and don't skip any of them: "
    input_Template_Lower += "1. Send me only array of functional test cases of all below acceptance criteria in JSON format "
    input_Template_Lower += "2. No introduction, No explanation, DO NOT MAKE ANY MISTAKES. Check if you did any. No DOCUMENTATION OR SINGLE SENTENCES IN THE OUTPUT "

    input_Template_Lower += " For example:"
    input_Template_Lower += '[\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Happy Path - Account has Sufficient Balance",\n'
    input_Template_Lower += '    "description": "User withdraws money with sufficient account balance",\n'
    input_Template_Lower += '    "expectedResult": "System deducts the amount from the savings account successfully"\n'
    
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Happy Path - Account has More than Enough Funds",\n'
    input_Template_Lower += '    "description": "User withdraws money with extra funds in the account",\n'
    input_Template_Lower += '    "expectedResult": "System deducts the correct amount and updates the balance"\n'
    
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Expected Error - Missing ATM Card",\n'
    input_Template_Lower += '    "description": "User tries to withdraw money without inserting the ATM card",\n'
    input_Template_Lower += '    "expectedResult": "System shows an error message about the missing ATM card",\n'
    
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Expected Error - Invalid Input",\n'
    input_Template_Lower += '    "description": "User enters a non-numeric withdrawal amount",\n'
    input_Template_Lower += '    "expectedResult": "System shows an error message about invalid input"\n'
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Test Minimum Allowed Values",\n'
    input_Template_Lower += '    "description": "User withdraws the minimum allowed amount with the account at its minimum balance",\n'
    input_Template_Lower += '    "expectedResult": "System deducts the amount and updates the balance"\n'
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Test Edge Cases 1 - Withdraw Entire Balance",\n'
    input_Template_Lower += '    "description": "User withdraws the entire balance with the account balance just enough for the withdrawal",\n'
    input_Template_Lower += '    "expectedResult": "System deducts the amount and updates the balance to zero"\n'
    input_Template_Lower += '  },\n'
    input_Template_Lower += '  {\n'
    input_Template_Lower += '    "title": "Test Edge Cases 2 - Account at Maximum Limit",\n'
    input_Template_Lower += '    "description": "User tries to withdraw money with the account at its maximum limit",\n'
    input_Template_Lower += '    "expectedResult": "System rejects the withdrawal and shows an error message"\n'
    input_Template_Lower += '  }\n'
    input_Template_Lower += ']'
    input_Template_Lower += " acceptance criteria scenarios: "
    input_Template_AC = input_ac_text

    #################
    prompt = input_Template_Upper + input_Template_Desc + input_Template_Lower + input_Template_AC

    response = model.generate_content(prompt,
                                    generation_config=genai.types.GenerationConfig(
                                    candidate_count=1,
                                    stop_sequences=None,
                                    max_output_tokens=None,
                                    top_p = 0.2,
                                    top_k = 4,
                                    temperature=0.2)
                                    )

    # response = model.generate_content(prompt)

    if not input_desc_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_desc_text = req_body.get('desc')

    if not input_ac_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            input_ac_text = req_body.get('ac')

    if input_desc_text:
        return func.HttpResponse(f"{response.text}", status_code=200)
    else:
        return func.HttpResponse(
            "Please pass input on the query string or in the request body",
            status_code=400
        )

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
