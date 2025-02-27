from mongo import *
import uuid


async def handle_register(data):
    email = data["email"]
    password = data["password"]
    account = accounts.find_one({"email":email,"password":password})
    if account is None:
        accounts.insert_one({"email":email,"password":password})
        return True
    else:
        return False
    
async def handle_login(data):
    email = data["email"]
    password = data["password"]
    account = accounts.find_one({"email":email,"password":password})
    if account is not None:
        token = str(uuid.uuid4())
        return True,token
    else:
        return False,None

async def handle_add_subject(data,email):
    data = data["data"]
    subjects.insert_one({"user":email,"data":data})
    return True

async def handle_request_subjects(email):
    subject = subjects.find({"user":email})
    sub = []
    for i in subject:
        subject = i["data"]["subject"]
        sub.append(subject)
    return sub

async def handle_view_result(data):
    student_no = int(data["student_no"])
    stud = students.find_one({"student_no":student_no})
    if stud is not None:
        return stud["data"]
    else:
        data = [{
            'subject': 'No Answer Sheet Found',
            'total_marks': 0,
            'obtained_marks': 0,
            'answers': [
                {
                    'question_no':0,
                    'allocated_mark':0,
                    'obtained_mark':0
                }
            ]
        }]
        return data