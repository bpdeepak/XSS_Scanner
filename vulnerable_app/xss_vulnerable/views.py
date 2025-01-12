from django.shortcuts import render
from .models import Comment

# Reflected XSS Example
def search(request):
    query = request.GET.get('query', '')
    return render(request, 'home.html', {'query': query})

# Stored XSS Example
def comments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        # Save directly without sanitizing (vulnerable)
        Comment.objects.create(username=username, content=content)
    all_comments = Comment.objects.all()
    return render(request, 'comments.html', {'comments': all_comments})

# DOM-Based XSS Example
def dom_xss(request):
    """
    A page to demonstrate DOM-based XSS vulnerability.
    """
    return render(request, 'dom_xss.html')
