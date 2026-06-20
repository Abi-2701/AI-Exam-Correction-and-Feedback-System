# AI Exam Correction and Feedback System

## Overview

AI Exam Correction and Feedback System is an intelligent answer sheet evaluation platform that automates the process of correcting subjective answers using OCR, NLP, and Generative AI techniques.

The system extracts handwritten or typed answers from uploaded answer sheets, analyzes the content, compares it against expected answers, generates marks, and provides personalized feedback to students.



## Features

✅ PDF Answer Sheet Upload

✅ OCR-based Text Extraction

✅ NLP-based Content Analysis

✅ AI-powered Evaluation

✅ Automatic Mark Generation

✅ Personalized Feedback

✅ MongoDB Storage

✅ WebSocket Support for Real-Time Processing



## Technology Stack

### Backend
- Python
- FastAPI / Flask (mention actual framework)
- WebSocket

### AI & NLP
- Generative AI
- NLP
- OCR

### Database
- MongoDB

### Document Processing
- PDF Processing
- Image Processing

### Architecture
+----------------------+
| Student Answer Sheet |
+----------+-----------+
           |
           v
+----------------------+
| PDF Processing Layer |
| (pdftoimg.py)        |
+----------+-----------+
           |
           v
+----------------------+
| Image Enhancement    |
| (pre_process.py)     |
+----------+-----------+
           |
           v
+----------------------+
| OCR Engine           |
| (ocr.py)             |
+----------+-----------+
           |
           v
+----------------------+
| NLP Analysis Layer   |
| (nlp.py)             |
+----------+-----------+
           |
           v
+----------------------+
| GenAI Evaluation     |
| (genai.py)           |
+----------+-----------+
           |
           +--------+
           |        |
           v        v

+---------------+  +---------------+
| Marking Engine|  | Feedback Gen  |
+-------+-------+  +-------+-------+
        \              /
         \            /
          v          v

+----------------------+
| MongoDB Database     |
| (mongo.py)           |
+----------+-----------+
           |
           v
+----------------------+
| Dashboard / Client   |
+----------------------+



## Project Structure

backend/
├── main.py
├── genai.py
├── ocr.py
├── nlp.py
├── pre_process.py
├── pdftoimg.py
├── base64topdf.py
├── mongo.py
├── ws.py
├── utils.py



## System Workflow

1. User uploads answer sheet.
2. PDF is converted into images.
3. Images are preprocessed.
4. OCR extracts text.
5. NLP analyzes extracted content.
6. Generative AI evaluates answers.
7. Marks are generated.
8. Feedback is created.
9. Results are stored in MongoDB.
10. Output is displayed to the user.



## Future Enhancements

- Multi-language evaluation
- Improved handwriting recognition
- LLM-powered adaptive feedback
- Institution dashboard
- Performance analytics

