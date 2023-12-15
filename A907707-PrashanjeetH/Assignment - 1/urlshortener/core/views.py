from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
import random
from datetime import datetime
from core.models import UrlModel
from core.forms import UrlForm
import re

def isValidURL(str):
 
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    p = re.compile(regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False

def generate_unique_id():

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    unique_id = ''.join(random.choice(chars) for _ in range(5))
    if UrlModel.objects.filter(url_id=unique_id).exists():
        # check if it can be over write
        url = UrlModel.objects.filter(url_id=unique_id)[0]
        print(f"Already Exists = {url.url_id}")
        diff = datetime.now - url.created_on
        # validity of any url is 2 days
        if diff.days < 2 :
            return generate_unique_id()
    return unique_id


def index(request):

    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            # generate unique id
            unique_id = generate_unique_id()
            # check if unique ID already exists or not
            rcvd_url = form.cleaned_data["original_url"]
            if not (rcvd_url.startswith('http://') or rcvd_url.startswith('https://')):
                rcvd_url = 'https://'+rcvd_url
            if isValidURL(rcvd_url):
                new_entry = UrlModel(original_url = rcvd_url, url_id = unique_id, created_on=datetime.now())
                new_entry.save()
                print(f"Entry Created: {new_entry}")
                context_data = {
                    "form" : UrlForm(),
                    "short_url" : unique_id,
                }
            else:
                context_data = {
                    'message': 'Please enter a valid URL',
                    'form': UrlForm()
                }
                return render(request, 'index.html', context = context_data)
    else:
        form = UrlForm()
        context_data = {
            "form" : form,
        }
    return render(request, 'index.html', context = context_data)


# # Vulnerable to SQL injection
# def short_url(request, id):
#     url = UrlModel.objects.get(url_id = id)
#     tables = UrlModel.objects.raw("""
# SELECT * FROM core_UrlModel;
#     """)
#     print("executed!")
#     print(f"{url[0] = }")
#     # print(f"{url.original_url}")
#     return HttpResponseRedirect(url.original_url)


# # Manual checks before doing anythin with input fields
# def short_url(request, id):
#     if 'delete' in id.lower() or 'drop' in id.lower():
#         context_data = {
#             'message': 'Please check the URL again.',
#             'form': UrlForm()
#         }
#     else:
#         url = UrlModel.objects.raw("""SELECT * FROM Core_UrlModel WHERE url_id = %s""", [id,])
#         if url:
#             print(f"{url[0] = }")
#             # print(f"{url.original_url}")
#             return HttpResponseRedirect(url[0].original_url)
#         else:
#             context_data = {
#             'message': 'The URL you are trying to access is either wrong or Broken. ',
#             'form': UrlForm()
#         }
#     return render(request, 'index.html', context = context_data)

        

# Correct way of implementation 
def short_url(request, id):
    url = UrlModel.objects.filter(url_id = id).exists()
    if url:
        url = UrlModel.objects.get(url_id = id)
        print(f"{url.original_url}")
        return HttpResponseRedirect(url.original_url)
    else:
            context_data = {
            'message': 'The URL you are trying to access is either wrong or Broken. ',
            'form': UrlForm()
        }
    return render(request, 'index.html', context = context_data)
