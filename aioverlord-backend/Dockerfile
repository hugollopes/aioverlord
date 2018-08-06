# Use an official Python runtime as a parent image
FROM python:3.5-slim


# Set the working directory to /app
WORKDIR /app

# Copy the python dependencies into the container at /app
ADD requirements.txt /app/requirements.txt



# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install tensorflow

ADD ai_overlord_backend_app /app/ai_overlord_backend_app
ADD main.py /app/main.py
ADD static /app/static

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python3", "main.py"]
