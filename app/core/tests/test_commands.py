from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

# Problem: Sometimes there is some issues with the database
# when the app is running sometimes the database is not available
# it throws an exeption 
# our two test that we gonna implement are 
#1) a test that check when the database is ready 
#2) a test that check when the database is not ready 
# for the second test, we'll loop until the database is ready

# the patch function can be used as a context manager or a decorator

# OperationnaError is an error that is thrown by django when the db is not available
class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        #this test is runned when the database is ready 
        # "django.db.utils.ConnectionHandler.__getitem__": it's where we check if 
        # our database is available or not 
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True # the value that we want to return for our mock 
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 1)
            # call_count return how many time the patch function is called
    # this decorator return the time sleep has an argument for our test method 

    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db """
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            # the side_effect function raises an Error when the mock test is called 
            #the main thing in this test is to loop or call the side_effect function 5 times
            # just to wait for our database to be available and for the 6 times the db 'll be ready
            #Our test is True when the call count >= 5 
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, 6)


