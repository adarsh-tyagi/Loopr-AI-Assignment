from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
from datetime import date, datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Book
from django.core.exceptions import ObjectDoesNotExist

'''
username: admin
password: admin12345
'''

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return JsonResponse({'error': 'Please provide all details for registeration'})
        existingUser = User.objects.filter(username=username).exists()
        if existingUser:
            return JsonResponse({'message': 'User already exist'})
        today_date = date.today()
        curr_time = datetime.now()
        userid = str(today_date.day) + str(today_date.month) + str(today_date.year) + str(curr_time.hour) + str(curr_time.minute) + str(curr_time.second) + str(curr_time.microsecond)
        new_user = User.objects.create_user(id=userid, username=username, password=password)
        if new_user:
            return JsonResponse({'message': f'New user created successfully with user id {new_user.id}'})
        return JsonResponse({'error': 'New user can not be created, something went wrong'})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    try:
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None or password is None:
            return JsonResponse({'error_message': 'Please provide both username and password'})
        user = authenticate(request, username=username, password=password)
        print(user)
        print(user.id)
        if not user:
            return JsonResponse({'error_message': 'Invalid Credentials'})
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})
    except Exception as e:
        return JsonResponse({'error_message': e})

@csrf_exempt
@api_view(['POST'])
def create_book(request):
    try:
        name = request.POST.get('name', None)
        author = request.POST.get('author', None)
        price = request.POST.get('price', None)
        if name and author:
            new_book = Book.objects.create(name=name, author=author, price=price)
            if new_book:
                return JsonResponse({'message': f'Book {name} by {author} added successfully'})
            return JsonResponse({'error': 'Something went wrong, book can not be added'})
        return JsonResponse({'error': 'Please provide book name and author name'})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['GET'])
def search_book(request):
    try:
        search_key = request.GET.get('search', None)
        if search_key:
            books = list(Book.objects.filter(name__startswith=search_key).values())
        else:
            books = list(Book.objects.all().values())
        result = []
        for book in books:
            book_details = {'id': book['id'], 'name': book['name'], 'author': book['author'], 'price': book['price']}
            if book['available']:
                book_details['status'] = 'available'
            else:
                book_details['status'] = 'checked out'
            result.append(book_details)
        return JsonResponse({'books': result})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['POST'])
def issue_book(request):
    try:
        book_id = request.POST.get('book_id', None)
        days = request.POST.get('days', None)
        if book_id and days and int(days) > 0 and request.user:
            try:
                book = Book.objects.get(id=book_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Book does not exist'})
            if book.available and book.user is None:
                book.issue_book(int(days), request.user)
                return JsonResponse({'message': f'Book {book.name} is issued to {request.user.username}'})
            return JsonResponse({'message': f'Book {book.name} is already issues to other user'})
        return JsonResponse({'error': 'Please provide all required details before issuing book'})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['POST'])
def return_book(request):
    try:
        book_id = request.POST.get('book_id', None)
        if book_id and request.user:
            try:
                book = Book.objects.get(id=book_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Book does not exist'})
            if not book.available and book.user is not None:
                book.return_book()
                return JsonResponse({'message': f'Book {book.name} is returned by {request.user.username}'})
            return JsonResponse({'message': f'Book {book.name} is already returned'})
        return JsonResponse({'error': 'Please provide book id before returnning'})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['DELETE'])
def delete_user(request):
    try:    
        if request.user:
            request.user.delete()
            return JsonResponse({'message': 'User deleted'})
    except Exception as e:
        return JsonResponse({'error': e})
    
@csrf_exempt
@api_view(['DELETE'])
def delete_book(request):
    try:
        book_id = request.GET.get('book_id', None)
        if book_id:
            try:
                book = Book.objects.get(id=book_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Book does not exist'})
            if book and book.available:
                book.delete()
                return JsonResponse({'message': f'Book {book.name} is removed from library'})
            return JsonResponse({'error': 'Book is not available in library'})
        return JsonResponse({'error': 'Please provied the valid book id before deleting'})
    except Exception as e:
        return JsonResponse({'error': e})