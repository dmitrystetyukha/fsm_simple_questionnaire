FROM python:3.10.12
# set work directory
WORKDIR /usr/src/fsm_simple_questionnaire/
# copy project
COPY . /usr/src/fsm_simple_questionnaire/
# install dependencies
RUN pip install -r requirements.txt
# run app
CMD ["python", "main.py"]