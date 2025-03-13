from rest_framework import serializers # type: ignore
from tickets.models import Guest,Movie,Reservation, post

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields='__all__'


class GuestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Guest
    fields='__all__'
    # fields=['pk','reservations','name','mobile']#uuid ,slug

class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reservation
    fields='__all__'
class postSerializer(serializers.ModelSerializer):
  class Meta:
    model = post
    fields='__all__'