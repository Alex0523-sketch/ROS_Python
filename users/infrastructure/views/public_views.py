from django.shortcuts import render
from users.infrastructure.models.promocion_model import PromocionModel
from users.infrastructure.models.noticia_model import NoticiaModel


def index_view(request):
    promociones = PromocionModel.objects.all()
    noticias = NoticiaModel.objects.all().order_by('-fecha_publicacion')
    promocion_del_dia = promociones.first()
    return render(request, 'public/index.html', {
        'promociones': promociones,
        'noticias': noticias,
        'promocion_del_dia': promocion_del_dia,
    })
