from rest_framework import serializers

from .models import Client, Agent, Listing, ListingImage
from django.contrib.auth.models import User 


# include User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user



class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['image']


class AgentListingsSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True)

    class Meta:
        model = Listing
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])  # Extract images data
        listing = Listing.objects.create(**validated_data)  # Create Listing instance
        for image_data in images_data:
            ListingImage.objects.create(property=listing, **image_data)  # Create ListingImage instances
        return listing



        
class AgentSerializer(serializers.ModelSerializer):
    # this needs to be defined in the Agent model
    has_listing = serializers.SerializerMethodField()
    listings = AgentListingsSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Agent
        fields = '__all__'
    
    def get_has_listing(self, obj):
        return obj.has_listing()
    


# added this so you can see all listings 
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

# will add in user last so we don't have to add auth yet and can easily test using the local host

