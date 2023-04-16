# NexUs - A Study Buddy Platform
## Description: 
A SaaS application that helps NUS students in finding study buddies, based on shared courses, majors, and availability.

## Frontend
Frontend is developed using ReactJS.

### Frontend Setup
Steps:
1. run npm install to install all the dependencies.
2. run npm start to start the React Project, the default port is 4000.
3. Setup environment variables including backend ip and port as shown on the .env-example file, copy and change the value in the .env file.

## Backend
Backend is developed using Flask. 
For CRUD, we use RDS Mysql as main storage and  ElastiCache as a middle cache layer to support fast and desired user experience.

### Backend Setup
Steps:
1. run `mysql.server start` to start mysql server.
2. run redis-server to start redis server.
3. run `PYTHONPATH=$PROJECTPATH python route.py` where $PROJECTPATH is the path to your project, e.g. ~/nexus/backend
