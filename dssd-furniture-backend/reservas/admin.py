# reservas/admin.py

from django.contrib import admin
from .models import ReservaMaterial, ReservaLugarFabricacion

admin.site.register(ReservaMaterial)
admin.site.register(ReservaLugarFabricacion)
