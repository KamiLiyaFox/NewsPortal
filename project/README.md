<h1 align="center">News Portal</h1>

<h3 align="center">My personal repository to learn Django from <a href="https://github.com/KamiLiyaFox/NewsPortal.git">NewsPortal/DjangoProject.com</a></h3>

<br>

<h2 align="center">Using <code>virtualenv</code></h2>

(note: used as a "container" environment for the project)

### Создание виртуального окружения 

```bash
python -m venv venv
```

### Start a new `virtualenv` "container"

```bash
virtualenv directory/name
```

To use Python instead:

```bash
virtualenv -p python directory/name
```

### Usage

#### activate

```bash
venv\Scripts\activate
```

#### deactivate

```bash
deactivate
```


<h2 align="center">Install Django</h2>

С `virtualenv` [activated](#usage), запустите следующую команду:

```bash
pip install Django
```


<h1 align="center">The Django Project Tutorial</h1>

Tutorial Reference: [https://docs.djangoproject.com/en/4.2/intro/tutorial01/](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)

<br>

### Start нового Django project

```bash
django-admin startproject mysite
```

### Run the Development Django Web Server

```bash
python manage.py runserver
```

<br>

<h2 align="center">Models</h2>

### Models and Database Migration

from: [https://docs.djangoproject.com/en/4.2/intro/tutorial02/#activating-models](https://docs.djangoproject.com/en/4.2/intro/tutorial02/#activating-models)

_**The 3-Step Guide to Model Changes**_
* _**change**_ your models (in `models.py`)
* run `python manage.py makemigrations` to _**create**_ migration for those changes
* run `python manage.py migrate` to _**apply**_ those changes to the databases

<br>

### Django/Python Shell (important)

Rather than calling `python` in our `virtualenv`, we use

```bash
python manage.py shell
```

`manage.py` will set "the DJANGO_SETTINGS_MODULE environment variable, which gives Django the Python import path to your mysite/settings.py file."

<br>

<h2 align="center">Views</h2>

### `URLConf`

"A [`URLConf`](https://docs.djangoproject.com/en/4.2/intro/tutorial03/#overview) maps URL patterns to **views**."
See [`djnago.urls`](https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#module-django.urls).

### Responsibility

From: [Django >> #write-views-that-actually-do-something](https://docs.djangoproject.com/en/4.2/intro/tutorial03/#write-views-that-actually-do-something)

(**Important**) Each view _**must be**_ responsible for at least 1 of 2 things:
* returning an `HttpResponse` object
* raising an HTTP 404 exception

The rest, you can determine...
* read database records
* use Django's template system or a 3rd party's
* generate a PDF, XML, ZIP, etc.
* execute Python libraries

### The `render()` shortcut method
From: [Django >> #a-shortcut-render](https://docs.djangoproject.com/en/4.2/intro/tutorial03/#a-shortcut-render)

**Motivation:** It is very common to perform the following idiom:
```Python
from django.http import HttpResponse
from django.template import loader

def view_name(request):

    # (1) load the template
    template = loader.get_template('app_name/index.html')

    # (2) fill the context dictionary
    context = {
        'context_dictionary': context_object,
    }

    # (3) return the required HttpResponse
    return HttpResponse(template.render(context, request))
```

**Shortcut:** Django provides the following as a Shortcut

```Python
from django.shortcuts import render

def view_name(request):
  # (1) fill the context
  context = {'context_dictionary': context_object}

  # (2) render loads the response and satisfies the HttpResponse
  return render(request, 'app_name/index.html', context)
```

### The `get_object_or_404()` shortcut method
From: [Django >> #a-shortcut-get-object-or-404](https://docs.djangoproject.com/en/4.2/intro/tutorial03/#a-shortcut-get-object-or-404)

**Motivation:** It is very common to perform the following idiom; in addition, not using the subsequent shortcut couples the _view_ and _model_ layers of Django architecture which is ill-advised:
```Python
from django.http import Http404
from django.shortcuts import render

def view_name(request):

  # (1) perform a get()
  try:
    var_name = Object.objects.get(<object_key>)

  # (2) if get() is undefined, raise an exception
  except Object.DoesNotExist:
    raise Http404("<Object> does not exist")

  # (3) render a response
  return render(request, 'app_name/view_name.html', {'var_name': var_name})
```

**Shortcut:** Django provides the following as a Shortcut

```Python
from django.shortcuts import get_object_or_404, render

def view_name(request):

  # (1) perform the try/except idiom
  var_name = get_object_or_404(<object>)

  # (2) render a response
  return render(request, 'app_name/view_name.html', {'var_name': var_name})
```

<br>

<h3 align="center">Generic Views</h3>

For some of the views defined in the [tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial04/#use-generic-views-less-code-is-better), the author indicates that Django has generic views that can perform the same action.

Specifically, `DetailView` and `ListView` can be called by extending the  `django.views.generic` module.

The following is an example of using these generic views with the conventional naming syntax:

```Python
# <app_name>/views.py

from django.views import generic

class IndexView(generic.ListView):
    template_name = '<app_name>/<model_name>_<template_name>.html'

    # overrides the automatically generated context
    context_object_name = '<context_object_name>'

    def get_queryset(self):
        """Return the last five published <Objects>."""
        return <Object>.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = <model_name>
    template_name = '<app_name>/<model_name>_<template_name>.html'
```



<br>

<h2 align="center">Templates</h2>
Note: Django will automatically search for a directory called `templates` in each application context.

### Template Namespacing

#### Folder Structure
(**Important**)
Django chooses application templates by *order*. To prevent confusion, it is convention to "namespace" your templates by "putting those templates inside another directory named for the application itself".

* <application_name>
  * ...
  * `templates`
    * <appliaction_name> _**(this is namespacing)**_
      * ...
      * ...
  * ...

#### URLs
(**Important**) To prevent confusion in URLs, defining the `app_name` variable in `urls.py` of your Django application is convention:

In your `urls.py` file:
```Python
# <app_name>/urls.py

from django.conf.urls import url
from . import views

app_name = '<app_name>'

urlpatterns = [
  # ...
  url(<regexp>, views.<view_name>, name='<view_name>'),
  # ...
]
```

In your `templates/<app_name>/<template_name>.html` file:
```django
<!-- <app_name>/templates/<app_name>/<template_name>.html -->

<a href="{% url '<app_name>:<view_name>' %}" />
```

<br>

<h2 align="center">Customizing Djagno's Admin Form</h2>

### General Practice
Anytime you change the admin options for a model:
* create a model class
  * convention: `class <model_name>Admin(admin.ModelAdmin):`
* pass it as a subsequent argument to `admin.site.register()`

<br>

<h1 align="center">Resources</h1>

* [Django](https://www.djangoproject.com)

