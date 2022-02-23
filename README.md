# Lambda-Scripts
Collection of Lambda Scripts from past projects that are no longer in operation

# Event Based Social Media App
The idea of this app was to let users create events in their area so they could meet other users.

Each of these scripts were designed using API gateway to call the script and interact with DynamoDB for a serverless backend solution. 
To ensure security, each script only had access to the actions used and tables those actions were done to through IAM. I also used IAM permissions to give API Gateway access to the script and those APIs could only be called from the Elastic Beanstalk application used to call it. This solution made the database quite secure from a direct attack, and also had the added benefit of throttling traffic that is calling the database too often to protect against volume based attacks.
1. addEvent.py
2. addUser.py
3. changeUserEventStatus.py
4. getEventData.py
5. getUserData.py
