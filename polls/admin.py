from django.contrib import admin

# Register your models here.
from .models import *
#Question,Choice,
admin.site.register(Usuario)
admin.site.register(Modelo)
admin.site.register(Codigo)
admin.site.register(Periodo)
admin.site.register(Registro)
admin.site.register(Cliente)
admin.site.register(Generador)
admin.site.register(FactorPerdidas)
admin.site.register(Barra)
admin.site.register(BarraTransferencia)
#admin.site.register(TipoContrato)
admin.site.register(Contrato)
admin.site.register(ContratoMes)
admin.site.register(Dias)
admin.site.register(Reparto)
admin.site.register(Area)