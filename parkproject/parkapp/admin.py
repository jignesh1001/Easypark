from django.contrib import admin
from parkapp.models import TYPER,OWNER,CUSTOMER,BOOK
# Register your models here.
admin.site.register(TYPER)
admin.site.register(OWNER)
admin.site.register(CUSTOMER)
admin.site.register(BOOK)