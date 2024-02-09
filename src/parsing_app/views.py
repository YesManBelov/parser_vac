from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .froms import FindForm
from .models import Vacancy


def home_view(request):
    if request.user.is_authenticated:
        form = FindForm()
        return render(request,'parsing_app/home.html', {'form': form})
    else:
        return redirect('accounts_app:login')

def list_view(request):
    if request.user.is_authenticated:
        print('Welcome')
        form = FindForm()
        city = request.GET.get('city')
        language = request.GET.get('language')
        context = {'city': city, 'language': language, 'form': form}
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter)
            # Разбивка на страницы
            paginator = Paginator(qs, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['data_list'] = page_obj

        return render(request, 'parsing_app/list.html',
                      context)
    else:
        return redirect('accounts_app:login')