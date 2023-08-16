FROM python:3.11

# Set the working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src to the folder
COPY ./app ./app

# Copy the .env file to the image
COPY .env ./

# Start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
