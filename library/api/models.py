from django.db import models

# Create your models here.
class book(models.Model):
	title = models.CharField(max_length=200)
	copies = models.IntegerField()
	available_copies = models.IntegerField()
	author = models.CharField(max_length=200)

	def __str__(self):
		self.title

class author(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		self.name

class member(models.Model):
	name = models.CharField(max_length=200)
	fine = models.IntegerField()
	contact = models.IntegerField()

	def __str__(self):
		self.name

class reservationStatus(models.Model):
	status = models.CharField(max_length=100)
	book_id = models.IntegerField()
	member_id = models.IntegerField()
	days_up = models.IntegerField(blank=True)
