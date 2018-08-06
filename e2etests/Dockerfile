# Use an official Python runtime as a parent image
FROM node:carbon


# Set the working directory to /app
WORKDIR /app

COPY package*.json ./

#install base
RUN npm install

#add code
VOLUME /app

# Make port 80 available to the world outside this container
EXPOSE 8080
