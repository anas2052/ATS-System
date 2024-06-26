from dotenv import load_dotenv

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to Image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path = r"C:\Users\Shank\OneDrive\Documents\Anas Files\Projects\poppler-24.02.0\Library\bin")

        first_page = images[0]
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format= 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["PDF"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
#submit2 = st.button("How can I Improvise my skills")
#submit2 = st.button("What are the keywords that are missing")
submit4 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full stack Web Development,
Big Data Engineering, DEVOPS, Data Analyst, your taks is to review the provided resume against the job 
description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlights the strengths and weakness of the application in relation to the specified job requirement.
"""

input_prompt3 = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in any of the technology, software engineering, data science, full stack web development, cloud enginner, 
cloud developers, devops engineer and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{uploaded_file}
description:{input_text}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload the resume")