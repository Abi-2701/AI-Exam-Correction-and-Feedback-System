from nlp import *
from pdftoimg import *
from ocr import *
from pre_process import *
from base64topdf import *
import asyncio
import random
import string
import os, json
from genai import *
from mongo import *

def filename(length=7):
    characters = string.ascii_letters + string.digits
    if length > len(characters):
        raise ValueError("Length cannot exceed the number of available characters")
    return ''.join(random.sample(characters, length))

def get_subject_data(email,subject):
    sub = subjects.find_one({"user": email, "data.subject": {"$regex": subject, "$options": "i"}})
    if sub:
        data = sub["data"]
        return data
    else:
        return False
    
def get_question_details(document, question_number):
    """Retrieves question details based on question number."""
    for question in document['questions']:
        if question['question_no'] == str(question_number):  #Convert to string to compare
            return {
                'keywords': question['keywords'],
                'answer': question['answer'],
                'marks': question['marks']
            }
    return None

def get_total_marks(questions_data):
    total_marks = 0
    for question in questions_data:
        try:
            total_marks += int(question['marks'])
        except (KeyError, ValueError) as e:
            print(f"Error processing marks for question {question.get('question_no', 'N/A')}: {e}")
    return total_marks

def process_data(data,email):
    name = filename()
    data_uri = data["file"]
    student_no = int(data['student_no'])
    subject = data['subject']
    sub_data = get_subject_data(email,subject)
    if sub_data:
        base64_to_pdf(data_uri, f"{name}.pdf")
        image_paths = pdf_to_images(f"{name}.pdf")
        os.remove(f"{name}.pdf")
        extracted_data_list = upload_images_and_extract_text(image_paths)
        for i in image_paths:
            os.remove(i)
        data = pre_process(extracted_data_list)
        total_marks = get_total_marks(sub_data["questions"])
        obtained_marks = 0
        detected_answers = []
        for i in data:
            if i is not None:
                question_details = get_question_details(sub_data, str(i))
                if question_details:
                    keywords_string = question_details['keywords']
                    keywords = [keyword.strip().lower() for keyword in keywords_string.split(',')]
                    marks,_,_=grade_answer(keywords,question_details['answer'],data[i],int(question_details['marks']))
                    obtained_marks=obtained_marks+marks
                    detected_answers.append({"question_no": int(i), "allocated_mark": int(question_details['marks']), "obtained_mark": marks})
                else:
                    id_q = json.loads(identify_question_no(sub_data["questions"],data[i]))
                    que_no = id_q["question_no"]
                    question_details = get_question_details(sub_data, str(que_no))
                    if question_details:
                        keywords_string = question_details['keywords']
                        keywords = [keyword.strip().lower() for keyword in keywords_string.split(',')]
                        marks,_,_=grade_answer(keywords,question_details['answer'],data[i],int(question_details['marks']))
                        obtained_marks=obtained_marks+marks
                        detected_answers.append({"question_no": int(que_no), "allocated_mark": int(question_details['marks']), "obtained_mark": marks})
        final_info = {
            "subject": subject,
            "total_marks": total_marks,
            "obtained_marks": obtained_marks,
            "answers": detected_answers
        }
        student_data = students.find_one({"student_no": student_no})
        if student_data:
            if "data" in student_data and isinstance(student_data["data"], list):
                student_data["data"].append(final_info)
                students.update_one({"student_no": student_no}, {"$set": {"data": student_data["data"]}})
            else:
                students.update_one({"student_no": student_no}, {"$push": {"data": final_info}})
        else:
            students.insert_one({"student_no": student_no, "data": [final_info]})