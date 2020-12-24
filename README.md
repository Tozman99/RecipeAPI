# RecipeAPI
This is the recipe API 



# DockerFile 

In the Dockerfile The RUN adduser -D user  command helps to create a user that has higher priviliges than regular users and he can access to the process with the tag -D

It's a good practice to change the user cause it's better for security,
by default the user is root and it's unrecommanded 


# travis-ci travis-ci.org
- We have to enable our project 
- Create a  .travis.yml that tells travis-ci what services and language we have to use 
- here before_script we have to install docker-compose 
- script: run  our test 
Linting tool highlights syntactical and stylistic problems in 
python code 

# in the app we create a .flake8 file for linting and we specify the linting tool 
# and we exclude file that doesn't respect the PEP recommandation of 79 characters
# it helps to find our problems faster 

# then we commit our code and normally on travis-ci we should have our commit created 

The goal of travis-ci is to run tests every time we push our coude into the gituhb repo

# check breanches on travis-ci website if the code run et exited with 0 then erveything works fine 

# command for running testcase 

docker-compose run app sh -c "python manage.py test"
