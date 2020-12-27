from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:

        model = get_user_model()
        fields = ("email", "name", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    # we must be authenticated in order to be authorized to change our user data
    # with token , first we need to have our token 
    # go to api/users/create/ 
    # create a user
    # go to api/users/token/, add your profile data below 
    # a token'll be generated 
    # copy this token and open modheader 
    # add a request headers for name : Authorization and for the value : Token with the token
    # it helps to find the user with the token and with that we can authenticate
    # With patch we can change a specific field EX: we can change the name without providing other field value
    # with put we have to change all the datas 

    ##### WHAT IS HTTP REQUEST HEADERS?
    # https://www.techopedia.com/definition/27178/http-header#:~:text=HTTP%20headers%20are%20the%20name,Hypertext%20Transfer%20Protocol%20(HTTP).&text=HTTP%20headers%20are%20mainly%20intended,and%20client%20in%20both%20directions.
    
    def update(self, instance, validated_data):
        """ update user , set the password with encryption and return user"""
        # instance = user instance 
        # validated_data = datas that the user patch in order to edit user profile

        # delete the password from data that the user submit with edited data
        password = validated_data.pop("password", None)
        # the we call the update method from Modelserilaizer
        # it returns a user with edited data 
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password) # set the password with encryption
            user.save() # save the user 

        return user

    

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )  # authenticate the user 
        if not user: # if bad credentials then no user authenticated
            msg = _('Unable to authenticate with provided credentials')# translate the msg
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user # else add the user and validate those credentials
        return attrs