from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Agent, Client, Listing
from .serialzers import AgentSerializer, ClientSerializer, AgentListingsSerializer, ListingSerializer

# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Vougue Estate home route!'}
        return Response(content)
    
class AgentList(generics.ListCreateAPIView):
    queryset= Agent.objects.all()
    serializer_class= AgentSerializer

class AgentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= Agent.objects.all()
    serializer_class= AgentSerializer
    # might change id to name so the url says name instead of the number will discuss with team perhaps after testing
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # use one of the two will test with both when whe have everything running 
        # listings_associated = Listing.objects.filter(id__in=instance.listings.all())
        listings_associated = instance.listings.all()
        listings_serializer= AgentListingsSerializer(listings_associated, many=True)
        
        return Response({
            'agent': serializer.data,
            'listings_associated': listings_serializer.data
        })

class AgentListingsList(generics.ListCreateAPIView):
    serializer_class= AgentListingsSerializer 

    def get_queryset(self):
        # might change to agent name will discuss with team perhaps after testing 
        agent_id= self.kwargs['agent_id']
        return Listing.objects.filter(agent_id=agent_id)
    
    def perform_create(self, serializer):
        agent_id = self.kwargs['agent_id']
        agent = Agent.objects.get(id=agent_id)
        serializer.save(agent=agent)

class AgentListingsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgentListingsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        agent_id = self.kwargs['id']
        return Listing.objects.filter(agent_id = agent_id)
    
class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()

class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Client.objects.all()
    serializer_class = ClientSerializer
    # might change this to username will dicuss with the team
    lookup_field = 'id'

    
