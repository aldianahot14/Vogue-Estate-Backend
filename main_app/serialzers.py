from rest_framework import serializers
from .models import Client, Agent, Listing

class AgentListingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class AgentSerializer(serializers.ModelSerializer):
    # this needs to be defined in the Agent model
    has_listing = serializers.SerializerMethodField()
    listings = AgentListingsSerializer(many=True, read_only=True)
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
    class Meta:
        model = Client
        fields = '__all__'

# will add in user last so we don't have to add auth yet and can easily test using the local host

