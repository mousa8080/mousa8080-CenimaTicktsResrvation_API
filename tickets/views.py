
from urllib import request
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from tickets.serializers import GuestSerializer,MovieSerializer,ReservationSerializer, postSerializer
from .models import Guest,Movie,Reservation, post
from rest_framework import status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,mixins,viewsets
from django.http import Http404
from rest_framework.authentication import BaseAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .Permissions import IsAuthOrReadOnly


#1 without rest and no model query FBV
def no_rest_no_model(request):
  guests=[
          {
              'id':'1',
              'Name':'ahmed',
              'Mobile':'0123456789',
              
          },
          {
              'id':'2',
              'Name':'mohamed',
              'Mobile':'0123456789',
          }
  ]
  return JsonResponse(guests,safe=False)

#2 model data dufault django without rest
def no_rest_from_model(request):
  data=Guest.objects.all()
  response={
    'guests':list(data.values('id','name','mobile')),
    
    }
  return JsonResponse(response)

#list==Get
#Create==Post
#pk query==Get
#Update==Put
#Delete destroy==Delete

#3 functoin based views
#3.1 GET POST
@api_view(['GET','POST'])
def FBV_list(request):
  #GET
  if request.method=='GET':
    guests=Guest.objects.all()
    serializer=GuestSerializer(guests,many=True)
    return Response(serializer.data)
  #POST
  elif request.method=='POST':
    serializer=GuestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_PK(request,pk):
  try:
    guest=Guest.objects.get(pk=pk)
  except Guest.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  #GET
  if request.method=='GET':
    serializer=GuestSerializer(guest)
    return Response(serializer.data)
  #PUT
  elif request.method=='PUT':
    serializer=GuestSerializer(guest,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
  #DELETE
  if request.method=='DELETE':
    guest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  

#CBV class based views
#4.1 list and Create ==GET and POST 
class CBV_list(APIView):
  def get(self,request):
    guests=Guest.objects.all()
    serializer=GuestSerializer(guests,many=True)
    return Response(serializer.data)

  def post(self,request):
    serializer=GuestSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#4.2  GET PUT DELETE class based view --pk
class CBV_PK(APIView):
  def get_object(self,pk):
    try:
      return Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
      raise Http404
  def get(self,request,pk):
    guest=self.get_object(pk)
    serializer=GuestSerializer(guest)
    return Response(serializer.data)
  
  def put(self,request,pk):
    guest=self.get_object(pk)
    serializer=GuestSerializer(guest,data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
  def delete(self,request,pk):
    guest=self.delete_object(pk)
    guest.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    


#5 mixins
#5.1 mixins list 
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
  queryset=Guest.objects.all()
  serializer_class=GuestSerializer
  def get(self,request):
    return self.list(request)
  def post(self,request):
    return self.create(request)
  
# 5.2 mixins pk
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
  queryset=Guest.objects.all()
  serializer_class=GuestSerializer
  def get(self,request,pk):    
    return self.retrieve(request)
  def put(self,request,pk):
    return self.update(request)
  def delete(self,request,pk):
    return self.destroy(request)

# 6 Generics
#6.1 generics get and post
class generics_list(generics.ListCreateAPIView):
  queryset=Guest.objects.all()
  serializer_class=GuestSerializer
  authentication_classes=[TokenAuthentication]
  # permissioin_classes=[IsAuthenticated]
  #local authentication and permission

#6.2 generics get put and delete
class generics_list_pk(generics.RetrieveUpdateDestroyAPIView):
  queryset=Guest.objects.all()
  serializer_class=GuestSerializer
  permissioin_classes=[TokenAuthentication]
  # authentication_classes=[BaseAuthentication]
  #local authentication and permission

#7 viewsets 
class Viewsets_guests(viewsets.ModelViewSet):
  queryset=Guest.objects.all()
  serializer_class=GuestSerializer

class Viewsets_movies(viewsets.ModelViewSet):
  queryset=Movie.objects.all()
  serializer_class=MovieSerializer
  filter_backends=[filters.SearchFilter]
  search_fields=['movie']

class Viewsets_reservations(viewsets.ModelViewSet):
  queryset=Reservation.objects.all()
  serializer_class=ReservationSerializer

  #best function  pisnes  function based views
  #find movie
@api_view(['GET'])
def find_movie(request):
  movies=Movie.objects.filter(movie=request.data['movie'],hall=request.data['hall'])
  serializer=MovieSerializer(movies,many=True)
  return Response(serializer.data)

# 9 create new reservation 
@api_view(['POST'])
def new_reservation(request):

  movie=Movie.objects.get(movie=request.data['movie'],hall=request.data['hall'])
  guest=Guest()
  guest.name=request.data['name']
  guest.mobile=request.data['mobile']
  guest.save()
  
  reservation=Reservation()
  reservation.guest=guest
  reservation.movie=movie
  reservation.save()
  
  return Response(status=status.HTTP_201_CREATED)

#10 post author editor
class post_pk(generics.RetrieveUpdateDestroyAPIView):
  permission_classes=[IsAuthOrReadOnly]
  queryset=post.objects.all()
  serializer_class=postSerializer