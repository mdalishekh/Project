from django.shortcuts import render

def test_page(request):
    return render(request, 'page.html')