from .models import Tag
from .forms import SearchForm

def get_categories(request):
    return {'categories': Tag.objects.all()}

def search(request):
    return {'search_form': SearchForm()}
