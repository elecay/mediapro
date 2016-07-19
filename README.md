## README

# Creating a virtual environment (optional)

With this you can keep different configuration environments for differents projects.

    > pip install virtualenv
    > cd mediapro
    > virtualenv mediapro --no-site-packages
    > source mediapro/bin/activate

    > deactivate    # for when your are done with the project

# Installing packages

    > pip install -r requirements.txt

# Database

Install mongoDB and start it on default port.

More info: https://docs.mongodb.com/manual/installation/

    > sudo mongod       # start the db

Check that the db is running by:
         > mongo

You should se something like:

    MongoDB shell version: 3.2.5
    connecting to: test
    Server has startup warnings: 
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] 
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] ** WARNING: Insecure configuration, access control is not enabled and no --bind_ip has been specified.
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted, 
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] **          and the server listens on all available network interfaces.
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] ** WARNING: You are running this process as the root user, which is not recommended.
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] 
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] 
    2016-07-19T02:55:18.604+0200 I CONTROL  [initandlisten] ** WARNING: soft rlimits too low. Number of files is 256, should be at least 1000
    > 

# Run the project

    > python start.py

# Postman

For manual testing install Postman:

https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop

Import folder _postman_

For API documentation see _View Docs_ under the collection _MediaProTasks_
