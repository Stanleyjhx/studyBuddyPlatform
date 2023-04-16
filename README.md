# NexUs - A Study Buddy Platform
## Description: 
A SaaS application that helps NUS students in finding study buddies, based on shared courses, majors, and availability.

## Frontend
Frontend is developed using ReactJS.

## Backend
Backend is developed using Flask. 
For CRUD, we use RDS Mysql as main storage and  ElastiCache as a middle cache layer to support fast and desired user experience.

### Backend Setup
Steps:
1. run `mysql.server start` to start mysql server.
2. run redis-server to start redis server.
3. run `PYTHONPATH=$PROJECTPATH python route.py` where $PROJECTPATH is the path to your project, e.g. ~/nexus/backend
