from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY='exam-local-key'; DEBUG=True; ALLOWED_HOSTS=['127.0.0.1','localhost']
INSTALLED_APPS=['django.contrib.contenttypes','django.contrib.staticfiles','clinic']
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware']
ROOT_URLCONF='medibook.urls'; TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request']}}]
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
STATIC_URL='static/'; MEDIA_URL='media/'; MEDIA_ROOT=BASE_DIR/'media'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
