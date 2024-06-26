import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging

import streamlit as slt

from src.mcqgenerator.mcqgeneration import generate_evaluate_chain
from src.mcqgenerator.logger import logging



with open('E:\\3rd year\\genai\\mcqgen\\mcqgen\\mcqgenai\\Response.json','rb') as file:
    response_json=json.load(file)

slt.title("MCQS GENERATOR Application with LangChain ")

with slt.form("user_input"):
    
    upload_file=slt.file_uploader("Upload a text file")

    mcq_count=slt.number_input("Number of MCQS",min_value=3, max_value=50)

    subject=slt.text_input("Subject")

    tone=slt.text_input("tone",placeholder="simple")

    button =slt.form_submit_button("Create MCQS")

    if button and upload_file is not None and mcq_count and subject and tone :
        with slt.spinner("loading"):
            try:
                text=read_file(upload_file)

                inputs={
                    "text": text,
                    "number": mcq_count,
                    "subject":subject,
                    "tone": tone,
                    "response_json": json.dumps(response_json)
                  }
                response=generate_evaluate_chain(inputs)

            except Exception as e:
                logging.error(traceback.format_exc())
                traceback.print_exception(type(e),e,e.__traceback__)
                slt.error(traceback.format_exc())
            
            else:
                if isinstance(response,dict):
                    quiz=response.get("quiz")
                    review=response.get("review")
                    review_data = review.split("\n")
                    if quiz is not None:
                        
                        table_data=get_table_data(quiz)
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        
                        slt.table(df)
                       
                        
                        slt.text_area(label="Review",value=review_data)
                        slt.success("MCQS Generated Successfully")

                       
                    else:
                        
                        slt.error("No MCQs generated")
                else:
                    slt.write(response)
                


