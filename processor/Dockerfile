FROM python:3.11-slim
RUN pip install kafka-python torch deltalake pandas --extra-index-url https://download.pytorch.org/whl/cpu
COPY processor.py .
CMD ["python","processor.py"]
