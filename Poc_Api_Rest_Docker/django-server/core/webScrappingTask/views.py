

# Frontend
def index(request):
    # Obtém o token CSRF
    key = {}
    key.update(csrf(request))
    return render(request, "index.html")
