from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from shortener.models import Url
import uuid
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        link = request.POST.get('link', '')

        # Validate the URL format
        url_validator = URLValidator()
        try:
            url_validator(link)
        except ValidationError:
            return HttpResponseBadRequest('Invalid URL format')

        # Generate a unique short code
        short_code = generate_short_code()

        try:
            # Save the URL and short code to the database
            new_url = Url.objects.create(link=link, short_code=short_code)
        except Exception as e:
            return HttpResponseBadRequest(f'Error occurred while saving URL: {e}')

        # Construct the shortened URL
        shortened_url = request.build_absolute_uri('/') + short_code

        # Return the shortened URL
        return HttpResponse(shortened_url)
    else:
        return HttpResponseBadRequest('Invalid request method')

def go(request, pk):
    try:
        # Retrieve the URL details from the database
        url_details = Url.objects.get(short_code=pk)
    except Url.DoesNotExist:
        return HttpResponseBadRequest('Shortened URL does not exist')
    except Exception as e:
        return HttpResponseBadRequest(f'Error occurred while retrieving URL details: {e}')

    # Redirect the user to the original URL
    return redirect(url_details.link)

def generate_short_code():
    # Generate a unique short code using UUID
    short_code = str(uuid.uuid4())[:8]
    
    # Check if the generated short code already exists in the database
    while url.objects.filter(short_code=short_code).exists():
        # Regenerate short code if it already exists
        short_code = str(uuid.uuid4())[:8]
    
    return short_code
