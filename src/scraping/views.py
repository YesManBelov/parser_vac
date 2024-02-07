from django.shortcuts import render, redirect

from .froms import FindForm
from .models import Vacancy



def home_view(request):
    # print(request.GET)
    # сначала без регистрации попробовать
    if request.user.is_authenticated:
        print('Welcome')
        form = FindForm()
        city = request.GET.get('city')
        language = request.GET.get('language')
        qs = []
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            qs = Vacancy.objects.filter(**_filter)

        # это без фильтрации
        # qs = Vacancy.objects.all()


        return render(request, 'scraping/home.html',
                      {'data_list': qs, 'form': form})
    else:
        return redirect('accounts:login')