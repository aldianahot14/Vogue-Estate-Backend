from rest_framework import serializers

from .models import Client, Agent, Listing, ListingImage
from django.contrib.auth.models import User 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
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
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Update listing instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle images
        for image_data in images_data:
            image_id = image_data.get('id', None)  # Assuming each image data contains an 'id'
            if image_id:
                # Update existing image
                image_instance = ListingImage.objects.get(id=image_id, property=instance)
                for image_attr, image_value in image_data.items():
                    setattr(image_instance, image_attr, image_value)
                image_instance.save()
            else:
                # Create new image
                ListingImage.objects.create(property=instance, **image_data)

        return instance


    
class AgentSerializer(serializers.ModelSerializer):
    has_listing = serializers.SerializerMethodField()
    listings = AgentListingsSerializer(many=True, read_only=True)

    class Meta:
        model = Agent
        fields = '__all__'

    def create(self, validated_data):
        # Create Agent instance here
        agent = Agent.objects.create(**validated_data)
        return agent

    def get_has_listing(self, obj):
        return obj.has_listing()

    


# added this so you can see all listings 
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

# class ClientSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Client
#         fields = '__all__'

#     def create(self, validated_data):
#         client = Client.objects.create(**validated_data)
#         return client
    
class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        return client


# will add in user last so we don't have to add auth yet and can easily test using the local host

