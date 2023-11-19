FROM python:3.10
WORKDIR /ai_chat

RUN pip install --upgrade pip
COPY /requirement.txt /ai_chat/requirement.txt
RUN pip3 install -r requirement.txt

COPY / /ai_chat/
CMD ["python3" , "main.py"]