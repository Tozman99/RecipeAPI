from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model


#client helps us to simulate get and post request on our view , it hels 
#to see the response of the request 

# we need to create a setup function,
# in order to make our test For instance check if in the django admin 
#the user list is there 


class AdminSiteTests(TestCase):

    def setUp(self):
        """Setup our test in order to perfom login test on admin page"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="efgege@gmail.com", password="randompass"
        )
        self.user = get_user_model().objects.create_user(
            email="fewgggrh@gmail.com", password="random12"
        )
        self.client.force_login(self.admin_user)

    def test_users_listed(self):
        """Perfom request to our User table in admin page
             it tests if user on our user table """

        # to look for a table in admin page , 
        # the name of the view for this specific table view is 
        # theapplication_thetable_theview = 
        # this is the pattern used by django
        #for creatin gadmin views 
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_user_change_page(self):
        """Test that the user edit page works"""
        #the url : admin/core/user_id
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """Test That add user page works"""
        
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        





    