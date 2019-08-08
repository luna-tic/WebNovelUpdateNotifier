FROM python:3.7

# Install pipenv
RUN pip install -U pip && \
    pip install pipenv
    
COPY app/ /app
WORKDIR /app

# Install python packages
RUN pipenv install --system

CMD python run.py