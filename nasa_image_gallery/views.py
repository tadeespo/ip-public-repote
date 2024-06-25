# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from nasa_image_gallery.models import Favourite
from django.contrib import messages

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = []
    favourite_list = []

    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    images = []
    favourite_list = []
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get('query', '')

    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    pass


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    ##pass
    if request.method == 'POST':
        try:
            saved_favourite = services_nasa_image_gallery.saveFavourite(request)
            if saved_favourite:
                return redirect('favoritos')  # Redirige a la vista de favoritos si el favorito se guarda correctamente
            else:
                messages.error(request, 'Error al guardar el favorito.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return redirect('home')

@login_required
def deleteFavourite(request):
    ##pass
    if request.method == "POST":
        success = services_nasa_image_gallery.deleteFavourite(request)
        if success: 
            return redirect('favoritos')  # Redirigir a la lista de favoritos después de la eliminación exitosa
        else:
            messages.error(request, 'Error al guardar el favorito.')
            return redirect('favoritos')  # Aquí redirigimos de todos modos, puedes personalizar esto.
    else:
        return redirect('favoritos')


@login_required
def exit(request):
    ##pass
    logout(request)
    return redirect('home.html')
