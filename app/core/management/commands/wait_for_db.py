import time
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.db import connections

# base command allows us to create base django command like "python3 manage.py createsuperuser"
# here the command that we create is "python manage.py wait_for_db"
#connections is the connection swith the database 


class Command(BaseCommand):

    """Django command to pause execution until database is ready """

    def handle(self, *args, **options):
        # a function handle should contain the logic of the command 
        self.stdout.write("Waiting for database") # write on the terminal the msg
        db_conn = None # at first our db is not ready so our connection is false
        
        while not db_conn: # while our db_connection is not ready:
            try:
                # our db connections with our databse "default " is the Database key in our settings file 
                db_conn = connections["default"]

            except OperationalError: # if our database is not ready => throw an operationnalerror: 
                self.stdout.write("Database is not available yet Wait 1 sec..")
                time.sleep(1)
                # it print into the terminal that msg and sleep the process 1 sec 

        self.stdout.write(self.style.SUCCESS("Database is ready !"))
        # once the db_conne = True => our database is ready to go 