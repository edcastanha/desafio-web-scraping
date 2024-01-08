from django.middleware.csrf import get_token
from django.shortcuts import render

# === Frontend ===
def index(request):
    key = {}
    key["csrf_token"] = get_token(request)
    return render(request, "index.html", key)
