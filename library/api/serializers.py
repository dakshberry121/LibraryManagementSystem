from rest_framework import serializers
from api.models import book,author,member,reservationStatus

import json

class bookSerializers(serializers.ModelSerializer):

	class Meta:
		model = book
		fields = ['id', 'title', 'copies', 'available_copies', 'author']

class authorSerializers(serializers.ModelSerializer):

	class Meta:
		model = author
		fields = ['id', 'name']

class memberSerializers(serializers.ModelSerializer):

	class Meta:
		model = member
		fields = ['id', 'name', 'fine', 'contact']

class reservationStatusSerializers(serializers.ModelSerializer):
	
	class Meta:
		model = reservationStatus
		fields = ['id', 'status', 'book_id', 'member_id', 'days_up']