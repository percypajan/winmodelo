from django.http import HttpResponseRedirect,HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
#import datetime 
from django import forms
import openpyxl

import xlsxwriter
from calendar import mdays
from datetime import date,datetime, timedelta
import date_converter
#matplotlib
import io
from io import BytesIO
import urllib, base64
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from xhtml2pdf import pisa

from .models import *
from .forms import *

import sys
import operator

from .variables  import *
from .wbasedatosmodelos import *
from .wdiversos import *

#Para login, logout
#from django.contrib.auth import logout as do_logout
#from django.contrib.auth import authenticate
#from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth import login as do_login

#def welcome(request):
#    return render(request, "polls/wwelcome.html")

#def register(request):
#    return render(request, "polls/wregister.html")

def login(request):
    global milogin

    if request.method == "POST":
        form=LoginForm(request.POST)
        if ('ok' in request.POST):        
            if form.is_valid():
                log = form.save(commit=False) 
                usuario = Miusuario(log.login,log.clave)
                if usuario.ok:
                    milogin=usuario
                    return redirect('polls:index')
        else:            
            return redirect('polls:index')
    else:
        form = LoginForm()
    return render(request, "polls/wlogin.html", {'login':milogin, 'form': form})

def logout(request):
    global milogin
    milogin=Miusuario('anonimo','xxx')    
    return redirect('polls:index')


def index(request):
    global miperiodo
    global miperiodos
    global milogin
    global mirepmercado
    global mirepgrupo
    global mireptipo
    global mirepvalor
    global mirepbarra
    global migraficotipo
    global migraficototal    
    global migraficoregulado
    global migraficototalitem
    global colorx

    #por defecto seleccionar el primer periodo encontrado
    miperiodos=[]
    periodo=Periodo.objects.all()    
    for per in periodo:  miperiodos.append(Periodoelec(per))   
    miperiodo=miperiodos[0].per.id
    miperiodos[0].seleccionado=True

    #para  reportes de repartos
    mirepmercado=[]
    mirepmercado.append(Opcion(1,"Regulado"))
    mirepmercado.append(Opcion(2,"Libre"))
    mirepmercado.append(Opcion(3,"Regulado/Libre"))
    mirepmercado.append(Opcion(4,"Total"))
    mirepmercado[0].seleccionado=True
    mirepgrupo=[]
    mirepgrupo.append(Opcion(1,"Contrato"))    
    mirepgrupo.append(Opcion(2,"Generador"))
    mirepgrupo.append(Opcion(3,"Contrato/Generador"))
    mirepgrupo.append(Opcion(4,"Total"))

    mirepvalor=[]
    mirepvalor.append(Opcion(1,"Pot.Coincidente"))
    mirepvalor.append(Opcion(2,"Pot.Facturada"))
    mirepvalor.append(Opcion(3,"Pot.Contrata Fija"))
    mirepvalor.append(Opcion(4,"Pot.Contratada Var."))        
    mirepvalor.append(Opcion(5,"Pot. Contrata Fija Fact."))
    mirepvalor.append(Opcion(6,"Pot. Contratada Var. Fact."))   
    mirepvalor.append(Opcion(7,"Energia H.Punta"))
    mirepvalor.append(Opcion(8,"Energia H.F.Punta"))   
    mirepvalor.append(Opcion(9,"Energia Total"))   
    mireptipo=[]
    mireptipo.append(Opcion(1,"Licitación"))
    mireptipo.append(Opcion(2,"Bilateral"))
    mireptipo.append(Opcion(3,"Licitación/Bilateral"))
    mireptipo.append(Opcion(4,"Total"))
    mireptipo[0].seleccionado=True    
    mirepbarra=[]
    mirepbarra.append(Opcion(1,"Contractuales"))
    mirepbarra.append(Opcion(2,"Transferencias"))



    migraficoregulado=True
    migraficototal=True

    migraficotipo=[]
    migraficotipo.append(Opcion(1,'Diario'))
    migraficotipo.append(Opcion(6,'Diario acumulado'))    
    migraficotipo.append(Opcion(5,'Participación'))    
    migraficotipo.append(Opcion(2,'Energia mes V'))
    migraficotipo.append(Opcion(3,'Energia mes H'))
    migraficotipo.append(Opcion(4,'Energia diaria'))
    migraficotipo.append(Opcion(10,'E.diaria 3D'))    

    migraficototalitem=[]
    migraficototalitem.append(Opcion(1,'Contratos'))
    migraficototalitem.append(Opcion(2,'Generadores'))
    migraficototalitem.append(Opcion(3,'Barras'))

    colorx=[] #generar colores para graficos
    for i in range(500): 
        rc=(random.randint(0, 100)/100,random.randint(0, 100)/100,random.randint(0, 100)/100 )
        colorx.append(rc)


    pagina = 'polls/wgestion2.html'
    return render(request, pagina,{'login':milogin})

def modelolistar(request,clave1):
    global mimodelos
    global mimodelo
    global milogin

    # obtener todos los modelos
    modelo= Modelo.objects.all()
    mimodelos=modelo                #guardarlo

    pagina = 'polls/wmodelos.html'  
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo})

def modelomenu(request,clave1):
    global mimodelo
    global milogin
           
    mod   = Modelo.objects.get(pk=clave1)
    mimodelo=mod                        #guardarlo
    mm=MensajesTxt('Menu')

    pagina = 'polls/wmodelosmenu.html'
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,'mmensaje':mm})



def modeloregistro(request,clave1):
    global mimodelos
    global mimodelo
    global milogin
    mm=MensajesTxt('Registro')
    pagina = 'polls/wmodeloregistro.html'
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,'mmensaje':mm})

def modelocontrato(request,clave1):
    global mimodelos
    global mimodelo
    global milogin
    mm=MensajesTxt('Contrato')
    pagina = 'polls/wmodelocontrato.html'
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,'mmensaje':mm})

def modelomedicion(request,clave1):
    global mimodelos
    global mimodelo
    global milogin
    mm=MensajesTxt('Medicion')
    pagina = 'polls/wmodelomedicion.html'
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,'mmensaje':mm})


def modeloreparto(request,clave1):
    global mimodelos
    global mimodelo
    global milogin
    global repartoexiste
    repartoexiste=False
    mm=MensajesTxt('Reparto')
    pagina = 'polls/wmodeloreparto.html'
    return render(request, pagina, {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,'mmensaje':mm})

#*****************************************************************************
# Muestra tablas de registros o contratos
#*****************************************************************************
def modeloboton1(request,clave2,clave3,clave4): 
    global mimodelos
    global mimodelo
    global milogin
    global milistadoparcial
    global mipaginas
    global mipaginasactual
    global contratovista
    global micontratoopcion

    if (clave2=='contratotabla'): #artificio para contratos pues la 1era vez viene con "licitacion", "bilateral" u "otros", la segunda con "codigos"
        if (clave3!='codigos'): 
            contratovista=clave3
        if (clave3=='codigos'):  
            clave3=contratovista


    if (clave2=='registrotabla' and clave3=='codigos'):
        mipaginasactual=clave4
        ReordenaPaginas(1)    
        micontratoopcion='Puntos de medición'
        pagina = 'polls/wregistrotabla.html' 

    if (clave2=='contratotabla' and clave3=='licitacion'):
        mipaginasactual=clave4
        ReordenaPaginas(2) 
        micontratoopcion="Contratos de Licitación con Distribuidora  "
        pagina = 'polls/wcontratotabla.html' 

    if (clave2=='contratotabla' and clave3=='bilateral'):
        mipaginasactual=clave4
        ReordenaPaginas(3 ) 
        micontratoopcion="Contratos Bilateral con Distribuidora  "
        pagina = 'polls/wcontratotabla.html' 

    if (clave2=='contratotabla' and clave3=='otros'):
        mipaginasactual=clave4
        ReordenaPaginas(4 ) 
        micontratoopcion="Contratos con clientes libres en la zona de consecion de la Distribuidora   "
        pagina = 'polls/wcontratotabla.html' 
    
    return render(request, pagina, 
         {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
          'opcion':micontratoopcion,
          'codigos':milistadoparcial,
          'paginas':mipaginas})             




#**************************************************************************
# muestra la informacion de contratos
#**************************************************************************
def modeloboton4(request,clave2,clave3):  
    global mimodelos
    global mimodelo
    global milogin
    global micontrato    
    global micontratoslicitacion
    global micontratosbilateral
    global micontratosotros
    global miopcion


    if (clave2=='contratoeditar'):

        if request.method == 'GET':     
            micontratoslicitacion=[]
            micontratosbilateral=[]
            micontratosotros=[]
            miopcion=[]

            contratos=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=0)   
            for con in contratos:  micontratoslicitacion.append(Opcion(con.id,con.descripcion))   
            contratos=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=1)   
            for con in contratos:  micontratosbilateral.append(Opcion(con.id,con.descripcion))   
            contratos=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=2)   
            for con in contratos:  micontratosotros.append(Opcion(con.id,con.descripcion))   
            miopcion.append(Opcion(1,'Licitacion'))
            miopcion.append(Opcion(2,'Bilateral'))
            miopcion.append(Opcion(3,'Clientes Libres'))

            if (len(micontratoslicitacion)>0):
                micontratoslicitacion[0].seleccionado=True
            if (len(micontratosbilateral)>0):
                micontratosbilateral[0].seleccionado=True
            if (len(micontratosotros)>0):                
                micontratosotros[0].seleccionado=True
            miopcion[0].seleccionado=True
        
        if request.method == 'POST':      #boton: 'visualizar'
            valores=request.POST
            tipo= int(valores['tipo2'])
            
            if (tipo==1):
                cadena='licitacion2'
            if (tipo==2):
                cadena='bilateral2'
            if (tipo==3):
                cadena='otros2'

            if (cadena in valores):
                valor=int(valores[cadena])
                SeleccionaContrato(tipo,valor)
                micontrato=Contrato.objects.get(pk=valor) #aqui se selecciona el  contrato sobre el cual se vera la tabla
                return redirect('polls:contratomestabla',clave2=1)
  
        pagina = 'polls/wcontratoeditar.html' 
        return render(request, pagina, 
             {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
              'licitacion':micontratoslicitacion,'bilateral':micontratosbilateral,'otros':micontratosotros,'opcion':miopcion})             

def contratomestabla(request,clave2): #para informacion de los contratos
    global mimodelos
    global mimodelo
    global milogin
    global micontrato
    global micontratoslicitacion
    global micontratosbilateral
    global micontratosotros
    global milistadoparcial    
    global mipaginasactual
    global mipaginas
    global miopcion
    
    mipaginasactual=clave2
    ReordenaPaginas(5)  

    pagina = 'polls/wcontratomestabla.html' 
    return render(request, pagina, 
             {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
              'licitacion':micontratoslicitacion,'bilateral':micontratosbilateral,'otros':micontratosotros,'opcion':miopcion,     
              'codigos':milistadoparcial,
              'paginas':mipaginas})  

#***********************************************************************************
# edicion
#***********************************************************************************
def registroaccion(request,clave2,clave3):
    global mimodelos
    global mimodelo
    global milogin
    global micodigo
    global milistadoparcial    
    global mipaginasactual
    global micontratoopcion

    edita=True
    if request.method == 'POST':
            
            if (clave2=='registroagregar' or clave2=='registroeditar'):
                formcodigo=CodigoForm(mimodelo.cliente,request.POST)

            if ('ok' in request.POST):
                if formcodigo.is_valid():
                    cod = formcodigo.save(commit=False)  #commit false pues cuando es NUEVO le falta el dato de modelo_id.
                    cod.modelo_id=mimodelo.id  
                    cod.usuario0=milogin.login
                    cod.fecha0  =datetime.now()  

                    if not cod.signo: #Mercado Libre
                        cod.modo=False #resta (-)

                    if (clave2=='registroeditar'):
                        cod.id=clave3    
         
                    cod.save()
                    ReordenaPaginas(1 )
            return redirect('polls:modeloboton1',clave2='registrotabla',clave3='codigos',clave4=mipaginasactual )

    else:
            if (clave2=='registroagregar'):
                formcodigo=CodigoForm(mimodelo.cliente)             

            if (clave2=='registroeditar'):
                cod    =Codigo.objects.get(pk=clave3)
                micodigo = cod                       #guardarlo
                formcodigo=CodigoForm(mimodelo.cliente,instance=cod)

            if (clave2=='registroborrar'):
                cod    =Codigo.objects.get(pk=clave3)
                cod.delete()  
                ReordenaPaginas(1 )
                return redirect('polls:modeloboton1',clave2='registrotabla',clave3='codigos',clave4=mipaginasactual )
            
            ReordenaPaginas(1 )
            
            pagina = 'polls/wregistroaccion.html'  
            return render(request, pagina, 
                       {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                        'opcion':micontratoopcion,
                        'codigos':milistadoparcial,
                        'paginas':mipaginas,
                        'edita':edita,'formcodigo':formcodigo})    

def contratoaccion(request,clave2,clave3):
    global mimodelos
    global mimodelo
    global milogin
    global micontrato
    global micontratoopcion
    global milistadoparcial    
    global mipaginasactual
    global mipaginas

    visualizar=True
    edita=True

    if (contratovista=='licitacion'):
        orden=2
    if (contratovista=='bilateral'):
        orden=3
    if (contratovista=='otros'):
        orden=4

    if request.method == 'POST':
            if (clave2=='contratoagregar' or clave2=='contratoeditar'):
                if (orden==2 or orden==3): #licitacion o bilateral
                    formcontrato=ContratoForm1(mimodelo.cliente,request.POST)  #Lic/Bil
                if (orden==4): #otros
                    formcontrato=ContratoForm2(mimodelo.cliente,request.POST)  #Libres 3eros

            if ('ok' in request.POST):
                if formcontrato.is_valid():
                    cod = formcontrato.save(commit=False)  #commit false pues cuando es NUEVO le falta el dato de modelo_id.
                    cod.usuario0=milogin.login
                    cod.fecha0  =datetime.now()  

                    cod.modelo_id=mimodelo.id  
                    if (orden==2):
                        cod.tipo=0 #licitacion
                        cod.cliente=mimodelo.cliente
                    if (orden==3):
                        cod.tipo=1 #bilateral
                        cod.cliente=mimodelo.cliente
                    if (orden==4): 
                        cod.tipo=2 #otros (cliente libre 3eros)
                        #Poner como area a ninguna del cliente igual al modelo
                        area=Area.objects.filter(cliente=mimodelo.cliente_id,clase=0) #clase 0 es ninguna
                        if (len(area)>0):
                            cod.area=area[0]
                        cod.libre=True

                    if (clave2=='contratoeditar'):
                        cod.id=clave3               
                     
                    cod.save()
                    ReordenaPaginas(orden )

            return redirect('polls:modeloboton1',clave2='contratotabla',clave3='codigos',clave4=mipaginasactual ) 
    else:
            
            if (clave2=='contratoagregar'):
                if (orden==2 or orden==3): #licitacion o bilateral
                    formcontrato=ContratoForm1(mimodelo.cliente,)
                if (orden==4): #otros
                    formcontrato=ContratoForm2(mimodelo.cliente,)                             

            if (clave2=='contratoeditar'):
                cod    =Contrato.objects.get(pk=clave3)
                micontrato = cod                       #guardarlo
                if (orden==2 or orden==3): #licitacion o bilateral
                    formcontrato=ContratoForm1(mimodelo.cliente,instance=cod)
                if (orden==4): #otros
                    formcontrato=ContratoForm2(mimodelo.cliente,instance=cod)                             

            if (clave2=='contratoborrar'):
                cod    =Contrato.objects.get(pk=clave3)
                cod.delete()  
                ReordenaPaginas(orden )
                return redirect('polls:modeloboton1',clave2='contratotabla',clave3='codigos',clave4=mipaginasactual ) 
            ReordenaPaginas(orden )

            pagina = 'polls/wcontratoaccion.html'  
            return render(request, pagina, 
                       {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                        'ver':visualizar,
                        'opcion':micontratoopcion,
                        'codigos':milistadoparcial,
                        'paginas':mipaginas,
                        'edita':edita,'formcontrato':formcontrato})    
                        


def contratomesaccion(request,clave2,clave3):
    global mimodelos
    global mimodelo
    global milogin
    global micontrato
    global micontratomes
    global milistadoparcial    
    global mipaginasactual
    global mipaginas
    

    visualizar=True
    edita=True
    if request.method == 'POST':
            if (clave2=='contratomesagregar' or clave2=='contratomeseditar'):
                formcontratomes=ContratoMesForm(request.POST)
            
            if ('ok' in request.POST):
                if formcontratomes.is_valid():


                    cod = formcontratomes.save(commit=False)  #commit false pues cuando es NUEVO le falta el dato de modelo_id.
                    cod.contrato_id=micontrato.id  
                    cod.usuario0=milogin.login
                    cod.fecha0  =datetime.now()  
                    if (clave2=='contratomeseditar'):
                        cod.id=clave3               
                     
                    cod.save()
                    ReordenaPaginas(5 )
            
            pagina = 'polls/wcontratomestabla.html' 
            return redirect('polls:contratomestabla',clave2=1 )
    else:
            
            if (clave2=='contratomesagregar'):
                formcontratomes=ContratoMesForm()             

            if (clave2=='contratomeseditar'):
                cod    =ContratoMes.objects.get(pk=clave3)
                #micontratomes = cod                       #guardarlo
                formcontratomes=ContratoMesForm(instance=cod)

            if (clave2=='contratomesborrar'):
                cod    =ContratoMes.objects.get(pk=clave3)
                cod.delete()  
                ReordenaPaginas(5 )
                return redirect('polls:contratomestabla',clave2=1)
            
            ReordenaPaginas(5 )

            pagina = 'polls/wcontratomesaccion.html'  
            return render(request, pagina, 
                       {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                        'licitacion':micontratoslicitacion,'bilateral':micontratosbilateral,'otros':micontratosotros,'opcion':miopcion,     
                        'ver':visualizar,
                        'codigos':milistadoparcial,
                        'paginas':mipaginas,
                        'edita':edita,'formcontratomes':formcontratomes})    
                        


#*****************************************************************************
# carga archivo excel
#*****************************************************************************
def modeloboton2(request,clave2,clave3,clave4):
    global mimodelos
    global mimodelo
    global milogin
    global miperiodos
    global miperiodo
    global milistadoparcial
    global mipaginasactual

    # lectura de mediciones  ***********************************************************
    if ((clave2=='medicioncarga' or clave2=='librecarga') and clave3=='codigos'): 
        mipaginasactual=clave4

        if (clave2=='medicioncarga'):
            tipo=1
            ReordenaPaginas(1 )     
        if (clave2=='librecarga'):
            tipo=2
            ReordenaPaginas(4 )     

        for cod in milistadoparcial: cod.auxiliar1=InspeccionarsihaydatosEnergia(miperiodo,cod,tipo,cod.barra,0)
        for cod in milistadoparcial: cod.auxiliar2=InspeccionarsihaydatosPotencia(miperiodo,cod,tipo,cod.barra,0)

        if request.method == 'POST':      
            valores=request.POST
            valores2=request.FILES

            SeleccionaPeriodo(int(valores['periodo2']))    
            miperiodo=int(valores['periodo2'])
            clase=int(valores['tipo2'])
            if (clase==1):
                potencia=False
            else:
                potencia=True     
            if (len(valores)==3) : #dos valores> periodo y archivo seleccionados

                SeleccionaPeriodo(int(valores['periodo2']))
                miperiodo=int(valores['periodo2'])

                # cargar archivo excel
                excel_file = request.FILES["cargaexcel"]
                data=Excelobtenerregistro(excel_file)

                ncol=len(data)
                
                for i in range(ncol):
                    if (tipo==1):
                        cod=Codigo.objects.filter(modelo_id=mimodelo.id,nombre=data[i][0])
                        if (len(cod)==1):
                            BDgrabaregistro(milogin.login,miperiodo,cod[0].id,tipo,cod[0].barra,potencia,data[i])   #mediciones 

                    if (tipo==2):
                        cod=Contrato.objects.filter(modelo_id=mimodelo.id,codigo=data[i][0])
                        if (len(cod)==1):
                            BDgrabaregistro(milogin.login,miperiodo,cod[0].id,tipo,cod[0].barra,potencia,data[i])   #otros c.libre 
                        
                data=[]

            # inspeccionar todos los datos existentes para mostrarlos
            for cod in milistadoparcial: cod.auxiliar1=InspeccionarsihaydatosEnergia(miperiodo,cod,tipo,cod.barra,0)
            for cod in milistadoparcial: cod.auxiliar2=InspeccionarsihaydatosPotencia(miperiodo,cod,tipo,cod.barra,0)

        if (tipo==1):
                opcion = "Registros de medición"
                pagina = 'polls/wregistrocarga.html'   
        if (tipo==2):
                opcion = "Registros de Clientes Libres"
                pagina = 'polls/wlibrecarga.html'   

        return render(request, pagina, 
             {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
              'periodo':miperiodos,
              'opcion':opcion,
              'codigos':milistadoparcial,
              'paginas':mipaginas})    


#*****************************************************************************
# Grafico
#*****************************************************************************
def modeloboton3(request,clave2,clave3):
    global mimodelos
    global mimodelo
    global milogin
    global miperiodos
    global miperiodo
    global migraficocontrato
    global migraficocodigo
    global migraficotipo
    global colorx

    #para clave2='grafico' y clave=1

    if (clave2=='registrografico'):
        uri=0 
        migraficocontrato=[]
        migraficocodigo=[]
        contratos=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=2)   
        codigos  =Codigo.objects.filter(modelo_id=mimodelo.id)   
        for con in contratos:  migraficocontrato.append(Opcion(con.id,con.codigo))
        for cod in codigos:    migraficocodigo.append(Opcion(cod.id,cod.nombre))

        if request.method == 'POST':      
            valores=request.POST
            if ( len(valores)>1) : #dos valores> periodo y archivo seleccionados

                SeleccionaPeriodo(int(valores['periodo2']))
                miperiodo=int(valores['periodo2'])

                tipo   =valores['tipo2'] #tipo de gráfico
                listado0=request.POST.getlist('tipo2')  
                for i in range(len(listado0)):  listado0[i] =int(listado0[i])  
                for c in migraficotipo:         c.seleccionado= c.id in listado0                  

                #********************************** OBTENER REGISTROS DE CODIGOS SELECCIONADOS  *************
                nombresa=[]
                cods=[]
                for c in migraficocodigo: c.seleccionado=False
                listadoa=request.POST.getlist('VerCod')
                for i in listadoa:
                    cod=Codigo.objects.get(id=int(i))
                    cods.append(cod)
                    nombresa.append(cod.nombre)
                    for c in migraficocodigo:
                        if c.id==int(i):
                            c.seleccionado=True
                ya=BDobtieneregistro(miperiodo,cods,1,False) #busca energia


                nombresb=[]
                cods=[]
                for c in migraficocontrato: c.seleccionado=False                
                listadob=request.POST.getlist('VerLib')
                for i in listadob:
                    cod=Contrato.objects.get(id=int(i))
                    cods.append(cod)
                    nombresb.append(cod.codigo)
                    for c in migraficocontrato:
                        if c.id==int(i):
                            c.seleccionado=True

                yb=BDobtieneregistro(miperiodo,cods,2,False)  #busca energia                   
                y=ya+yb
                nombres=nombresa+nombresb

                uri=Creagrafico(tipo,nombres,y,colorx)
                

        pagina = 'polls/wregistrografico.html'  
    
        return render(request, pagina, 
                    {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                     'periodo':miperiodos,   
                     'codigos':migraficocodigo,'libres':migraficocontrato,
                     'tipog':migraficotipo,
                     'data':uri})             


         


def ReordenaPaginas(tipo):  #Nota: mipaginasactual ya tiene un valor predefinido
    global milistadoparcial
    global mipaginas
    global mipaginasactual
    global maxitempaginas
    global maxitempaginas18
    global micontrato
    global mimodelo
    global MiRepartoReporte

    max=maxitempaginas if (tipo!=5) else maxitempaginas2

    if (tipo==1): # es para registrocodigos
        listado=Codigo.objects.filter(modelo_id=mimodelo.id)   
    if (tipo==2): # es para contratocodigos licitacion
        listado=Contrato.objects.filter(modelo_id=mimodelo.id, tipo =0)
    if (tipo==3): # es para contratocodigos bilaterales
        listado=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=1)   
    if (tipo==4): # es para contratocodigos libres
        listado=Contrato.objects.filter(modelo_id=mimodelo.id,tipo=2)   
    if (tipo==5): # es para contratomes
        listado=ContratoMes.objects.filter(contrato=micontrato.id)
    if (tipo==6): # es para reporte de Licitaciones
        listado=MiRepartoReporte
        

    largo=len(listado)
    if (largo==0):
        milistadoparcial=[]
        return
    n=round_up( largo, max)
    if (n==0):
        n=1
    if (mipaginasactual<1):
        mipaginasactual=1
    if (mipaginasactual>n):
        mipaginasactual=n
    mipaginas=[]
    for i in range(n):
        pag=Pagina(i+1,False)
        if (i+1 == mipaginasactual):
            pag.activa=True
        mipaginas.append(pag)

    if (tipo==1): # es para registrocodigos
        milistadoparcial=Codigo.objects.filter(modelo_id=mimodelo)[( max*(mipaginasactual-1)):( max*(mipaginasactual))]
    if (tipo==2): # es para contratocodigos licitacion
        milistadoparcial=Contrato.objects.filter(modelo_id=mimodelo,tipo=0)[( max*(mipaginasactual-1)):( max*(mipaginasactual))]
    if (tipo==3): # es para contratocodigos bilateral
        milistadoparcial=Contrato.objects.filter(modelo_id=mimodelo,tipo=1)[( max*(mipaginasactual-1)):( max*(mipaginasactual))]
    if (tipo==4): # es para contratocodigos otros
        milistadoparcial=Contrato.objects.filter(modelo_id=mimodelo,tipo=2)[( max*(mipaginasactual-1)):( max*(mipaginasactual))]
    if (tipo==5): # es para contratosmes
        milistadoparcial=ContratoMes.objects.filter(contrato=micontrato.id)[( max*(mipaginasactual-1)):( max*(mipaginasactual))]
    if (tipo==6): # es para Repartos reporte
        milistadoparcial=[]
        ini=max*(mipaginasactual-1)
        fin=max*(mipaginasactual)
        if (fin>largo): 
            fin=largo
        for i in range(ini,fin):
            milistadoparcial.append(MiRepartoReporte[i])

#activar seleccionar el periodo indicado
def SeleccionaPeriodo(id):
    global miperiodos
    for i in miperiodos:
        i.seleccionado=True  if i.per.id==id else False


#activar seleccionar el contrato indicado
def SeleccionaContrato(tipo,id):
    global micontratoslicitacion
    global micontratosbilateral
    global micontratosotros
    global miopcion

    for i in miopcion:
        i.seleccionado=True if i.id==tipo else False

    if (tipo==1):
        for i in micontratoslicitacion:
            i.seleccionado=True  if i.id==id else False
    if (tipo==2):
        for i in micontratosbilateral:
            i.seleccionado=True  if i.id==id else False
    if (tipo==3):
        for i in micontratosotros:
           i.seleccionado=True  if i.id==id else False


#***************************************************************************************************
# Para PDF
#***************************************************************************************************
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
#***************************************************************************************************
# Reparto
#***************************************************************************************************

def repartopdf(request):
    pagina = 'polls/whaciapdfreparto.html' 
    results="hola"
    pdf= render_to_pdf( pagina,  {'pagesize':'A4', 'titulo':results})     

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Download.pdf" 
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
   
def CalculaMiReparto(reparto):

    reparto.Inspeccion()
    if reparto.ok:    
        reparto.CreaPeriodo()  # crea periodos hp y hfp
        reparto.BuscaBarras()   # obtiene todas las barras, con coincidentes (posicion 0) y registros merc.regulado, merc.libre y clientes libres
        reparto.BuscaContratos()# licitacion,bilaterales: regulados y libres (no  clientes 3eros)
        reparto.BuscaPotenciasContratadas() # inspecciona contratos de licitaciones y bilaterales,
        reparto.CalculaPotenciasFacturadas() # determina potencias contratadas fijas/var por barras
        reparto.CalculaEnergia()
        reparto.GrabaBaseDatos(miperiodo)

def repartocalculo(request,clave2,clave3):  
    global mimodelos
    global mimodelo
    global milogin
    global milistadoparcial
    global mipaginas
    global mipaginasactual
    global miperiodo
    global mimaximademanda
    global mirepmercado
    global mirepgrupo
    global mirepvalor    
    global mireptipo
    global reparto
    global mireportetitulo
    global MiRepartoReporte
    global MiRepartoCabecera

    mensaje=''
    if (clave2=='calculo'): 
        mensaje=[]
        mensaje.append('')
        mensaje.append('Al terminar de determinar el cálculo del reparto se muestra aqui la cantidad de información utilizada ...')
        mensaje.append('Si ya han sido determinados no es necesario volver a realizarlo')
        if request.method == 'POST':      #boton: 'visualizar'
            valores=request.POST
            SeleccionaPeriodo(int(valores['periodo2']))    
            miperiodo=int(valores['periodo2'])     

            mes=Periodo.objects.get(pk=miperiodo)
            mimaximademanda = (mes.maxdemandadia-1)*96+mes.maxdemandahora-1
            repo='Reporte:\n'
            reparto=MiReparto(milogin,mimodelo.id,miperiodo,mimaximademanda)
            CalculaMiReparto(reparto)
            mensaje=reparto.msg    


        pagina = 'polls/wrepartotabla.html' 
        html_out=render(request, pagina, 
          {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
           'periodo':miperiodos,
           'mensaje':mensaje })      
        return html_out

    if (clave2=='reporte'):
        for i in mirepgrupo: i.ver=True
        for i in mireptipo: i.ver=True
        for i in mirepmercado: i.ver=True
        for i in mirepvalor: i.ver=True

        titulo=[]
        data=[]
        mireportetitulo=''
        if request.method == 'GET':      #boton: 'visualizar'

                mipaginasactual=int(clave3)
                ReordenaPaginas(6)  

                pagina = 'polls/wrepartoreporte.html' 
                context= {'login':milogin,'modelos': mimodelos, 'modelo': mimodelo,
                     'periodo':miperiodos, 
                     'mensaje':mireportetitulo,
                     'mercado':mirepmercado,'agrupacion':mirepgrupo,'tipo':mireptipo,'valor':mirepvalor,
                     'titulo':MiRepartoCabecera,'data':milistadoparcial,
                     'paginas':mipaginas}
                html_out=render(request, pagina, context )  
                return html_out 

        if request.method == 'POST':      #boton: 'visualizar'
                valores=request.POST

                SeleccionaPeriodo(int(valores['periodo2']))    
                miperiodo   =int(valores['periodo2'])
                mercado     =int(valores['mercado2'])
                agrupacion  =int(valores['agrupacion2'])
                tipo        =int(valores['tipo2']) 
                valor       =int(valores['valor2'])

                mirepmercado=SeleccionaOpcion(mirepmercado,mercado)
                mirepgrupo  =SeleccionaOpcion(mirepgrupo  ,agrupacion)
                mireptipo   =SeleccionaOpcion(mireptipo   ,tipo)
                mirepvalor  =SeleccionaOpcion(mirepvalor  ,valor)

                mireportetitulo="Mercado: "+mirepmercado[mercado-1].opcion                    
                merc=[]
                if (mercado!=2): #solo libre
                    merc.append(False)
                if (mercado!=1): #solo regulado
                    merc.append(True)

                tip=[]
                if (tipo!=2): #solo bilateral
                    tip.append(0)
                if (tipo!=1): #solo licitacion
                    tip.append(1)
                reporte=Reparto.objects.filter( mesano=miperiodo,  libre__in=merc, tipo__in=tip, modelo=mimodelo.id )
                
                rep=RepartoTabla(reporte,mercado,agrupacion,tipo,valor)
                MiRepartoCabecera=rep.cabecera
                MiRepartoReporte =rep.reporte

                mipaginasactual=1
                ReordenaPaginas(6)      

                pagina = 'polls/wrepartoreporte.html' 
                context= {'login':milogin,'modelos': mimodelos, 'modelo': mimodelo,
                             'periodo':miperiodos, 
                             'mensaje':mireportetitulo,
                             'mercado':mirepmercado,'agrupacion':mirepgrupo,'tipo':mireptipo,'valor':mirepvalor,
                             'titulo':MiRepartoCabecera,'data':milistadoparcial,
                             'paginas':mipaginas}
                html_out=render(request, pagina, context )      

                return html_out    



def repartografico(request,clave2,clave3):
    global mimodelos
    global mimodelo
    global milogin
    global miperiodos
    global miperiodo
    global migraficototal
    global migraficocontrato
    global migraficobarra
    global migraficogenerador
    global migraficoregulado
    global migraficototalitem
    global migraficotipo
    global migraficototalitem

    #para clave2='grafico' y clave=1
    
    if (clave2=='mes'):

        if request.method == 'POST':  

            valores=request.POST
            SeleccionaPeriodo(int(valores['periodo2']))
            miperiodo=int(valores['periodo2'])  

            migraficocontrato=[]
            migraficogenerador=[]
            migraficobarra=[]

            ver=InspeccionaModelo(mimodelo.id,miperiodo)
            for con in ver.contrato :  migraficocontrato.append(Opcion(con.id,con.codigo))
            for gen in ver.generador:  migraficogenerador.append(Opcion(gen.id,gen.nombre))
            for bar in ver.barra:  migraficobarra.append(Opcion(bar.id,bar.nombre))

            pagina = 'polls/wrepartograficoopcion.html'  
            return render(request, pagina, 
                    {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                     'periodo':miperiodos,
                     'regulado':migraficoregulado,'miopcion':migraficototal,'contrato':migraficocontrato,
                     'generador':migraficogenerador,'barra':migraficobarra,
                     'tipog':migraficotipo,'totalitem':migraficototalitem})  
             
        pagina = 'polls/wrepartograficomes.html'      
        return render(request, pagina, 
                    {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                     'periodo':miperiodos   })   

    if (clave2=='grafico'):
        uri=0 

        if request.method == 'POST':    
            
            uri=[]

            valores=request.POST
            if ( len(valores)>=4) : 
                nombres=[]
                y=[]
                #********************************** OBTENER REGISTROS DE CODIGOS SELECCIONADOS  *************
                tipo              = valores['tipo2'] #tipo de gráfico  'dias' 'energia1' 'energia4' 'energia2' 'energia3' 

                migraficoregulado = True if (valores['mercado']=="regulado") else False
                migraficototal    = True if (valores['opcion']=="total") else False
                graficototalitem  = valores['total']  # '1':contrato' '2':generador' '3':barras'  

                listado0=request.POST.getlist('tipo2')     
                listado1=request.POST.getlist('VerCon')
                listado2=request.POST.getlist('VerGen')
                listado3=request.POST.getlist('VerBar')     
                listado4=request.POST.getlist('total')     
      
                for i in range(len(listado0)):  listado0[i] =int(listado0[i])                
                for i in range(len(listado1)):  listado1[i] =int(listado1[i])
                for i in range(len(listado2)):  listado2[i] =int(listado2[i])
                for i in range(len(listado3)):  listado3[i] =int(listado3[i])
                for i in range(len(listado4)):  listado4[i] =int(listado4[i])

                for c in migraficotipo:      c.seleccionado= c.id in listado0                
                for c in migraficocontrato:  c.seleccionado= c.id in listado1
                for c in migraficogenerador: c.seleccionado= c.id in listado2
                for c in migraficobarra:     c.seleccionado= c.id in listado3
                for c in migraficototalitem: c.seleccionado= c.id in listado4


                if not (migraficototal==False and listado1==[] and listado2==[] and listado3==[]): #algo que graficar
                    ver=InspeccionaModelo(mimodelo.id,miperiodo)
                    barras=[]
                    for bar in ver.barra: barras.append(Auxiliar(bar.id)) 
                    mercado= 0 if migraficoregulado else 1
                    
                    
                    barrasBD=BDobtieneregistro(miperiodo,barras,3,mercado)
                    
                    y=[]
                    nombres=[]

                    if (not migraficototal):
                        

                        for con in ver.contrato:
                            if (con.id in listado1):  
                                for gen in ver.generador:
                                    if (gen.id in listado2):  
                                        for bb in range(len(barrasBD)):
                                            if (barrasBD[bb][0] in listado3):
                                                ob=Barra.objects.get(pk=barrasBD[bb][0])
                                                str=con.codigo+'/'+gen.nombre+'/'+ob.nombre
                                                nombres.append(str)    
                                                ycontrato=CreaRegistro()
                                                repartBD=Reparto.objects.filter( mesano=miperiodo,  libre=mercado, modelo=mimodelo.id,
                                                        contrato=con.id ,
                                                        generador=gen.id,
                                                        barra=barrasBD[bb][0])   
                                                for i in range(len(repartBD)): 
                                                    yr=ObtieneEnergia(barrasBD[bb],1.0,repartBD[i])                
                                                    ycontrato=SumaRegistro(ycontrato,yr)
                                                y.append(ycontrato)
                    # Graficar barras total
                    if (migraficototal):
                        if (graficototalitem=='3'):
                            for bar in ver.barra: nombres.append(bar.nombre)
                            y=barrasBD
                        if (graficototalitem=='1'):
                            for con in ver.contrato:
                                if (con.libre!=migraficoregulado):
                                    nombres.append(con.codigo)                                    
                                    ycontrato=CreaRegistro()
                                    for bb in range(len(barrasBD)):
                                        repartBD=Reparto.objects.filter( mesano=miperiodo,  libre=mercado, modelo=mimodelo.id,
                                                        contrato=con.id , barra=barrasBD[bb][0])    
                                        for i in range(len(repartBD)): 
                                            yr=ObtieneEnergia(barrasBD[bb],1.0,repartBD[i])                
                                            ycontrato=SumaRegistro(ycontrato,yr)
                                    y.append(ycontrato)
                        
                        if (graficototalitem=='2'):
                            for gen in ver.generador:
                                    nombres.append(gen.nombre)                                    
                                    ycontrato=CreaRegistro()
                                    for bb in range(len(barrasBD)):
                                        repartBD=Reparto.objects.filter( mesano=miperiodo,  libre=mercado, modelo=mimodelo.id,
                                                        generador=gen.id , barra=barrasBD[bb][0])    
                                        for i in range(len(repartBD)): 
                                            yr=ObtieneEnergia(barrasBD[bb],1.0,repartBD[i])                
                                            ycontrato=SumaRegistro(ycontrato,yr)
                                    y.append(ycontrato)
           
                    uri=Creagrafico(tipo,nombres,y,colorx)
  
            pagina = 'polls/wrepartograficoopcion.html'  
            return render(request, pagina, 
                    {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                     'periodo':miperiodos,   
                     'regulado':migraficoregulado,'miopcion':migraficototal,
                     'contrato':migraficocontrato,'generador':migraficogenerador,'barra':migraficobarra,
                     'tipog':migraficotipo,'totalitem':migraficototalitem,
                     'data':uri    })             



        pagina = 'polls/wrepartograficoopcion.html'  
        return render(request, pagina, 
                {'login':milogin,'modelos': mimodelos,'modelo': mimodelo,
                 'periodo':miperiodos,
                 'regulado':migraficoregulado,'miopcion':migraficototal,
                 'contrato':migraficocontrato,'generador':migraficogenerador,'barra':migraficobarra,
                 'tipog':migraficotipo,'totalitem':migraficototalitem})      


def repartoexcel(request,clave2,clave3):  
    global mimodelos
    global mimodelo
    global milogin
    global miperiodo
    global mirepmercado
    global mirepgrupo
    global mirepvalor    
    global mireptipo
    global mirepbarra
    global reparto
    global mireportetitulo
    global MiRepartoReporte
    global MiRepartoCabecera

    mensaje=''
    mirepmercado[2].ver=False
    mirepmercado[3].ver=False
    mireptipo[2].ver=False
    mireptipo[3].ver=False
    mirepgrupo[2].ver=False
    if (clave2=='mes'):
        
        titulo=[]
        data=[]

        
        if request.method == 'POST':      #boton: 'visualizar'
                valores=request.POST

                SeleccionaPeriodo(int(valores['periodo2']))    
                miperiodo   =int(valores['periodo2'])
                mercado     =int(valores['mercado2']) #Regulado Libre
                tipo        =int(valores['tipo2']) #Licitacion Bilateral
                mbarra      =int(valores['barra2']) #Contractual Transferencia

                mirepmercado=SeleccionaOpcion(mirepmercado,mercado)
                mireptipo   =SeleccionaOpcion(mireptipo   ,tipo)
                mirepbarra  =SeleccionaOpcion(mirepbarra  ,mbarra)

                ver=InspeccionaModelo(mimodelo.id,miperiodo)
                barras=[]
                for bar in ver.barra: barras.append(Auxiliar(bar.id)) 
                
                libre =False if (mercado  ==1)     else True
                mtipo=0       if (tipo==1)  else 1

                barrasBD=BDobtieneregistro(miperiodo,barras,3,mercado-1)
                BT=BarraTransferencia.objects.all()

                y=[]
                tit=[ [TipoExcel('t','Contrato')],
                      [TipoExcel('t','Generador')],
                      [TipoExcel('t','Barra')],
                      [TipoExcel('t','Energía (MW.h)')] ]

                if (mbarra==1): #Barra Contractual
                    for con in ver.contrato:
                        for gen in ver.generador:
                            for bb in range(len(barrasBD)):
                                repartBD=Reparto.objects.filter( mesano=miperiodo,  modelo=mimodelo.id,
                                        libre=libre, contrato=con.id , tipo = mtipo,  generador=gen.id, barra=barrasBD[bb][0])   
                                     
                                if (len(repartBD)>0):
                                    ob=Barra.objects.get(pk=barrasBD[bb][0])
                                    tit[0].append(TipoExcel('t',con.codigo))
                                    tit[1].append(TipoExcel('t',gen.nombre))
                                    tit[2].append(TipoExcel('t',ob.nombre))
                                    ycontrato=CreaRegistro()
                                    for i in range(len(repartBD)): 
                                        yr=ObtieneEnergia(barrasBD[bb],1.0,repartBD[i])                
                                        ycontrato=SumaRegistro(ycontrato,yr)
                                    y.append(ycontrato)
                                    val = sum(ycontrato[1:len(ycontrato)])
                                    tit[3].append(TipoExcel('n',val))
                if (mbarra==2): #Barra de Transferencia
                    for gen in ver.generador:
                            for bti in BT:
                                mibarra=[]
                                for bb in barrasBD:
                                    barracontrato=Barra.objects.get(pk=bb[0])
                                    if bti.id==barracontrato.barratransferencia_id:
                                        mibarra.append(barracontrato.id)

                                repartBD=Reparto.objects.filter( mesano=miperiodo,  modelo=mimodelo.id,
                                        libre=libre,  tipo = mtipo,  generador=gen.id, barra__in=mibarra)   
                                     
                                if (len(repartBD)>0):

                                    tit[0].append(TipoExcel('t',' '))
                                    tit[1].append(TipoExcel('t',gen.nombre))
                                    tit[2].append(TipoExcel('t',bti.nombre))
                                    ycontrato=CreaRegistro()
                                    for r in repartBD: 
                                        for b in barrasBD:
                                            if (b[0]==r.barra_id):
                                                bx=b
                                        factorperd=  r.barra.factorperdidas.factor     
                                        yr=ObtieneEnergia(bx,factorperd,r)                
                                        ycontrato=SumaRegistro(ycontrato,yr)
                                    y.append(ycontrato)
                                    val = sum(ycontrato[1:len(ycontrato)])
                                    tit[3].append(TipoExcel('n',val))

                if (len(y)>0):
                    output = io.BytesIO()
                    workbook = xlsxwriter.Workbook(output)
                    WriteToExcel(workbook,1,mimodelo.descripcion,mimodelo.nombre,miperiodo,tit,y)
                    workbook.close()
                    output.seek(0)
                    filename = mimodelo.nombre+'.xlsx'
                    response = HttpResponse(
                                output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            )
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename
                    return response   
        
        pagina = 'polls/wrepartoexcel.html' 
        context= {'login':milogin,'modelos': mimodelos, 'modelo': mimodelo,
                     'periodo':miperiodos, 
                     'mercado':mirepmercado,'tipo':mireptipo,'barra':mirepbarra  }
        html_out=render(request, pagina, context )      

        return html_out    
