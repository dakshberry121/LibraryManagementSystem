from django.shortcuts import render
from http.client import HTTPResponse
from api.models import book,author,member,reservationStatus
from api.serializers import bookSerializers, authorSerializers, memberSerializers, reservationStatusSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import statistics
from statistics import mode

# Create your views here.

class bookList(APIView):

	def get(self, request, format=None):
		book_list = book.objects.all()
		serializer = bookSerializers(book_list, many=True)
		return Response(serializer.data)

	def post(self, request ,format=None):
		book_list = book.objects.all()
		result = {}

		result['title'] = request.data['title']
		result['copies'] = request.data['copies']
		result['available_copies'] = request.data['copies']
		result['author'] = request.data['author']

		serializer = bookSerializers(data=result)
		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class authorList(APIView):

	def get(self, request, format=None):
		author_list = author.objects.all()
		serializer = authorSerializers(author_list, many=True)
		return Response(serializer.data)

	def post(self, request ,format=None):
		author_list = author.objects.all()
		result = {}

		result['name'] = request.data['name']

		serializer = authorSerializers(data=result)
		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class memberList(APIView):

	def get(self, request, format=None):
		member_list = member.objects.all()
		serializer = memberSerializers(member_list, many=True)
		return Response(serializer.data)

	def post(self, request ,format=None):
		member_list = member.objects.all()
		result = {}

		result['name'] = request.data['name']
		result['fine'] = 0
		result['contact'] = request.data['contact']
		

		serializer = memberSerializers(data=result)
		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class bookreservation(APIView):
	def get(self,request, pk, format=None):
		reservation_list = reservationStatus.objects.all()
		result = []
		for reservation in reservation_list:
			if reservation.book_id == pk:
				result.append(reservation)

		serializer = reservationStatusSerializers(result, many=True)
		return Response(serializer.data)

	def post(self,request, pk, format=None):
		reservation_list = reservationStatus.objects.all()
		result = {}
		book_res = {}

		book_list = book.objects.all()
		for books in book_list:
			if books.id == pk:
				book_res = books
				break

		modified_book = {}

		if book_res.available_copies > 0:
			result['status'] = 'reservation'
			result['book_id'] = book_res.id
			result['member_id'] = request.data['member_id']
			result['days_up'] = 1
			available_copies = book_res.available_copies - 1
			modified_book['available_copies'] = available_copies
			modified_book['id'] = book_res.id
			modified_book['author'] = book_res.author
			modified_book['copies'] = book_res.copies
			print(modified_book['available_copies'])
			serializer1 = bookSerializers(book_res, data=modified_book)
			if serializer1.is_valid():
				serializer1.save()

		elif book_res.available_copies <= 0:
			result['status'] = 'requested'
			result['book_id'] = book_res.id
			result['member_id'] = request.data['member_id']
			result['days_up'] = 0

		serializer = reservationStatusSerializers(data=result)
		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def put(self,request, pk, format=None):
		reservation_list = reservationStatus.objects.all()
		book_list = book.objects.all()

		modified_book = {}
		actual_book = {}

		result = {}
		for reservation in reservation_list:
			if reservation.book_id == pk and reservation.member_id == request.data['member_id']:
				result = reservation
				break

		for i in book_list:
			if i.id == pk:
				modified_book = i
				actual_book = i


		modified_book.available_copies = actual_book.available_copies + 1

		serializer1 = bookSerializers(actual_book, data=modified_book)
		if serializer1.is_valid():
			serializer1.save()

		serializer = reservationStatusSerializers(result, data=request.data)
		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class overduebooks(APIView):
	def get(self, request, format=None):
		reservation_list = reservationStatus.objects.all()

		result_list = []
		for reservation in reservation_list:
			if reservation['status'] == 'reservation':
				result_list.append(reservation)

		serializer = reservationStatusSerializers(result_list, many=True)
		return Response(serializer.data)

class finecalcMember(APIView):
	def get(self,request, pk, format=None):
		reservation_list = reservationStatus.objects.all()

		result_list = []
		fine_days = 0
		for reservation in reservation_list:
			if reservation['days_up'] > 10:
				fine_days = reservation['days_up'] - 10
				member_info = {}
				member= member.objects.get(pk=reservation['member_id'])
				fine = member['fine'] + fine_days*50
				member_info['fine'] = fine
				member_info['name'] = member['name']
				member_info['contact'] = member['contact']

				serializer = memberSerializers(member, data=member_info)
				if serializer.is_valid():
					serializer.save()

				result_list.append(member_info)

		serializer = memberSerializers(result_list, many=True)
		return Response(serializer.data)


class popularbooks(APIView):
	def get(self, request, format=None):
		reservation_list = reservationStatus.objects.all()

		book_track_list = []
		for reservation in reservation_list:
			book_track_list.append(reservation['book_id'])

		popular_book_id = mode(book_track_list)

		book = book.objects.get(pk=popular_book_id)

		serializer = bookSerializers(book, many=True)
		return Response(serializer.data)




class mostactivemember(APIView):
	def get(self, request, format=None):
		reservation_list = reservationStatus.objects.all()

		member_track_list = []
		for reservation in reservation_list:
			member_track_list.append(reservation['member_id'])

		active_member_id = mode(member_track_list)

		member = member.objects.get(pk=active_member_id)

		serializer = memberSerializers(member, many=True)
		return Response(serializer.data)


			




