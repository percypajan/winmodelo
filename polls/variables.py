

from datetime import datetime, timedelta
from calendar import mdays
#para crear reportes
import pandas as pd
import numpy as np

from .models import *
from .wbasedatosmodelos import *
from .wdiversos import *

#******************* USUARIO **************************


#*******************************************************
#variables generales para modelos

mimodelos=0
mimodelo=Modelo()

micodigo=0


micontratoslicitacion=[]
micontratosbilateral=[]
micontratosotros=[]

micontrato=0
micontratomes=0
micontratoopcion=''
miperiodos=[]  #es una clase definida abajo
miperiodo=0


micodigonombre=''


milistado=[]
milistadoparcial=[]

contratovista='0'

maxitempaginas=20
maxitempaginas2=16

mipaginas=[]  #cantidad de paginas que se ven abajo 1,2,...
mipaginasactual=1

miopcion=[]

migraficoregulado=True
migraficototal=True

migraficotipo=[]
migraficotootalitem=[]
migraficocontrato=[]
migraficocodigo=[]
migraficogenerador=[]
migraficobarra=[]

mirepmercado=[]
mirepgrupo=[]
mirepvalor=[]
mireptipo=[]
mirepbarra=[]


mimaximademanda=0
#variable para usar reparto
repartoexiste=False
reparto=0
repo=''
mireportetitulo=[]
mmensaje=[]
MiRepartoCabecera=[]
MiRepartoReporte=[]

colorx=[]

class Miusuario:
    def __init__(self,loginx,clavex):
        self.login=loginx
        self.ok=False
        log=Usuario.objects.filter(login=loginx,clave=clavex)    
        if (len(log)>0):
            self.login=loginx
            self.ok=True

milogin=''#Miusuario('anonimo','xxx')            


class Pagina:
    def __init__(self,id,activa):
        self.id=id
        self.activo=activa

class Periodoelec:
    def __init__(self,per):
        self.per=per
        self.seleccionado=False

class Opcion:
    def __init__(self,id,opcion):
        self.id=id
        self.opcion=opcion
        self.seleccionado=False
        self.ver=True

class TablaIzq:
    def __init__(self,valor,izq):  #izq: True a la izquierda, izq=False a la derecha
        self.valor=valor
        self.izq=izq
class Auxiliar:
    def __init__(self,id):
        self.id=id

class TipoExcel:
    def __init__(self,tipo,cad):
        self.tipo=tipo
        self.cad=cad
    

def CreaRegistro():
    y=[]
    y.append(0)
    for i in range(2976):
        y.append(0)
    return y    
def SumaRegistro(y1,y2):
    y=[]
    y.append(0)
    for i in range(2976):
        y.append(y1[i+1]+y2[i+1])
    return y    

def SeleccionaOpcion(vector,n):
    for v in vector: 
        if (v.id==n):
            v.seleccionado=True
        else:
            v.seleccionado=False    
    return vector

#***************************************************************************************************
# Reparto
#***************************************************************************************************
def BarraenContrato(cont,barra):

    #ver si la barra coincide con la que figura en el contrato
    if (cont.barra.id==barra.id):
        return True
    if (cont.area.clase==0):
        return False
    if (cont.area.clase==2):
        return True
    #ver si la barra coincide con lo que estas que estan en el Area        
    if (cont.area.clase==1):
        esta=False        
        if (cont.area.barra00.id==barra.id):
            esta=True
        if (cont.area.barra01.id==barra.id):
            esta=True
        if (cont.area.barra02.id==barra.id):
            esta=True
        if (cont.area.barra03.id==barra.id):
            esta=True
        if (cont.area.barra04.id==barra.id):
            esta=True
        if (cont.area.barra05.id==barra.id):
            esta=True
        if (cont.area.barra06.id==barra.id):
            esta=True
        if (cont.area.barra07.id==barra.id):
            esta=True
        if (cont.area.barra08.id==barra.id):
            esta=True
        if (cont.area.barra09.id==barra.id):
            esta=True
        if (cont.area.barra10.id==barra.id):
            esta=True
        if (cont.area.barra11.id==barra.id):
            esta=True
        if (cont.area.barra12.id==barra.id):
            esta=True
        if (cont.area.barra13.id==barra.id):
            esta=True
        if (cont.area.barra14.id==barra.id):
            esta=True
        if (cont.area.barra15.id==barra.id):
            esta=True
    return esta



def repartoBuscarCodigos(modelo_id,b, registro,merclibre):
    # registro: True busca de codigos , False busca de contratos libres 3eros
    # merclibre: si es registro (codigos), True medicion total, False mercado libre distribuidora
    codigos  =Codigo.objects.filter(modelo_id=modelo_id)   
    contrato =Contrato.objects.filter(modelo_id=modelo_id,tipo=2)  #contratos 3eros

    subcodigos=[]
    if (registro): #Busca en codigos
        for c in codigos:
            if (b.barra.id==c.barra_id and c.signo==merclibre): #True registros total, False mercado libre distribuidora
                subcodigos.append(c)
    if (not registro):  #busca en contratos libres 3eros
        for c in contrato:
            if (b.barra.id==c.barra_id): # cliente libre 3ero 
                subcodigos.append(c)
    return subcodigos     

def repartoBuscarBarras(modelo_id):
    #   inspeccionar todas las barras del modelo, solo de registros
    #   si hay clientes libres (contratos 3eros) que no estan en estas barras, no tienen que afectar
    codigos  =Codigo.objects.filter(modelo_id=modelo_id)  
    bb=[]
    for c in codigos:
        esta=False
        for b in bb:
            if (b.barra.id==c.barra_id): 
                esta=True
        if (not esta):
            barra=Barra.objects.get(pk=c.barra_id)
            bb.append(RepartoBar(modelo_id,barra))    

    return bb    

class InformacionFactura:
    def __init__(self,fija,variable,fijafp,variablefp,iniciomes,fechaini,fechafin):
        self.fija      =fija
        self.variable  =variable
        self.fijafp    =fijafp
        self.variablefp=variablefp
        self.coincidente=0
        self.energiahp=0
        self.energiafp=0
        self.porcentaje=[]
        self.porcentajefp=[]
        self.vigencia=[]

        for i in range(31):
            self.porcentaje.append(0)
            self.porcentajefp.append(0)
            self.vigencia.append(False)
        #inpeccionar la vigencia del contrato por cada dia del mes
        diasmes=mdays[iniciomes.month]
        for i in range(diasmes):
            dia=iniciomes+timedelta(days=i)
            self.vigencia[i]=True if (fechaini<=dia and  fechafin>dia) else False                

class RepartoBar:
    def __init__(self,modeloid,barra):
        self.modeloid=modeloid
        self.barra=barra

        self.registro=[]
        self.energiahp=[]
        self.energiafp=[]
        self.conmes=[]
        self.factura=[]

        self.porcentaje=[0,0] #regulado y merclibre        
        
        for i in range(3): # 0=regulado 1:merclibre 2:libres 3ros
            vector=[]
            self.registro.append(vector) 
            self.registro[i].append(0) #el 1er reg es la potencia coincidente
            for j in range(2976):
                self.registro[i].append(0)
               
        for i in range(2): #0=regulado 1:merclibre    
            vector=[]             
            self.conmes.append(vector)
            self.factura.append(vector)

        self.pfacturada=[0,0]
        self.pfacturadafp=[0,0]
    
    def RepartoIngresaRegistro(self,tipo,datos,potencia):   #tipo=0:regul tipo=1:libre tipo=2:clibre3eros 
        
        self.registro[tipo][0]+=potencia
        for i in range(2976):  
            self.registro[tipo][i+1]+=datos[i+1]
        if (tipo==1 or tipo==2):   #Bajo 0 ingreso total, para determinar regulado en 0, se resta libre y clibre3eros
            self.registro[0][0]   -=potencia
            for i in range(2976):
                self.registro[0][i+1] -=datos[i+1]
    
    def RepartoHPFP(self,periodo):
        
        for tipo in range(2):
            vec1=[]
            self.energiahp.append(vec1)  #[0] [1] Reg Libre
            vec2=[]
            self.energiafp.append(vec2)  #[0] [1] Reg Libre 

        for tipo in range(2):
            for i in range(31):
                self.energiahp[tipo].append(0)  #[0][0..30] Reg [1][0..30] Libre
                self.energiafp[tipo].append(0)  #[0][0..30] Reg [1][0..30] Libre
        
        for tipo in range(2):

            for d in range(31):
                for h in range(96):
                    i=d*96 + h    
                    if (periodo[i]==1): #HP
                        self.energiahp[tipo][d]+=self.registro[tipo][i+1]
                    if (periodo[i]==0): #HFP
                        self.energiafp[tipo][d]+=self.registro[tipo][i+1]

class MiReparto:
    def __init__(self,log,modeloid,per,mimaximademanda):
        self.fechaini=Periodo.objects.get(pk=per).mesano
        self.fechafin=self.fechaini+timedelta(mdays[self.fechaini.month]-1)
        self.ndias=mdays[self.fechaini.month]
        self.modeloid=modeloid
        self.per=per
        self.mimaximademanda=mimaximademanda
        self.periodo=[]
        self.fechas=[]
        self.contrato=[]
        self.Bar=[]
        self.msg=[]
        self.ok=True

        self.login=log.login

    def Inspeccion(self):
        #Buscar Dias
        self.msg.append('--------------------------------------------------------------------------------------')
        self.msg.append(' Reporte de inspección para determinar reparto')
        self.msg.append('--------------------------------------------------------------------------------------')
        self.ok=True
        bd=Dias.objects.filter(dia__gte=self.fechaini, dia__lte=self.fechafin)
        if (len(bd)>=28):
            self.msg.append('Se encontraton '+ format(len(bd),'4.0f')+ " días del mes")
        else:
            self.msg.append("No se encontraron días del mes completos")
            self.ok=False

        #Buscar codigos de registros
        codigos  =Codigo.objects.filter(modelo_id=self.modeloid)        
        if (len(codigos)>0):
            self.msg.append("Se encontraron "+ format(len(codigos),'4.0f') +" códigos de registros asociadas al modelo")
            self.msg.append(' ')
            #Buscar si hay registros en los codigos
            dia=int(self.mimaximademanda/96)+1
            per=(mimaximademanda%96)
            nenergia=0
            npotencia=0
            msgaux1='     '
            msgaux2='     '
            for c in codigos:
                try:
                    energia1=Registro.objects.get(mesano=self.per,dia=1,codigo=c.id,tipo=1,version=0,potencia=False) 
                except Registro.DoesNotExist:
                    nenergia+=1                    
                    msgaux1+=" " +c.nombre+','
                try:    
                    potencia=Registro.objects.get(mesano=self.per,dia=dia,codigo=c.id,tipo=1,version=0,potencia=True) #jalar todos los datos
                except Registro.DoesNotExist:    
                    npotencia+=1
                    msgaux2+=" " +c.nombre+','
            if (nenergia>0):
                self.msg.append(' ')
                self.msg.append("   Sin datos de energía: ")
                self.msg.append(msgaux1)
                self.ok=False
            if (npotencia>0):
                self.msg.append(' ')
                self.msg.append("   Sin datos de potencia para el intervalo de demanda simultánea: ")
                self.msg.append(msgaux2)
                self.ok=False
        else:
            self.msg.append(' ')
            self.msg.append("No se encontraron códigos de registros asociadas al modelo")
            self.ok=False
        #Buscar barras
        self.msg.append(' ')
        bb=repartoBuscarBarras(self.modeloid)
        if (len(bb)>0):
            self.msg.append('Se encontraron '+format(len(bb),'4.0f')+' barras asociadas')
        else:
            self.msg.append("No se encontraron barras asociadas")
            self.ok=False    

        #Buscar contratos vigentes
        self.msg.append(' ')
        model=Modelo.objects.get(pk=self.modeloid)
        con  = Contrato.objects.filter(modelo_id=self.modeloid,cliente_id=model.cliente_id,fechaini__lte=self.fechaini, fechafin__gt=self.fechafin)
        if (len(con)>0):
            cont=0
            for c in con:
                conmes=ContratoMes.objects.filter(contrato_id=c.id,fechaini__lte=self.fechaini, fechafin__gt=self.fechafin)          
                for cm in conmes:
                    #self.msg.append(cm.contrato.codigo+'  '+cm.generador.nombre+'  '+format(cm.codid,'4.0f'))
                    cont+=1
            self.msg.append('Se encontraron '+format(cont,'4.0f')+' contratos aplicables vigentes')
        else:
            self.msg.append("No se encontraron contratos aplicables vigentes")
            self.ok=False


        self.msg.append(" ")
        if (self.ok):            
            self.msg.append('--------------------------------------------------------------------------------------')
            self.msg.append("Detalles del cálculo")
            self.msg.append('--------------------------------------------------------------------------------------')
        else:    
            self.msg.append(" ............ No se continua el cálculo de repartos ................")

    def CreaPeriodo(self): #crea fechas y hp/hfp
        self.fechas=Dias.objects.filter(dia__gte=self.fechaini, dia__lte=self.fechafin)
        self.periodo=CreaPeriodoHPFP(self.per)

    def BuscaBarras(self): 
        self.msg.append("Lectura de registros de barras")        
        #barras
        self.Bar=repartoBuscarBarras(self.modeloid)
        #  Obtener la energía por barras y por mercado regulado, mercado libre y contratos libres 3eros
        for b in self.Bar:
            cont1=0
            cont2=0
            cont3=0
            for tipo in range(3): #0:regulado, 1:libre 2:libre3eros
                if (tipo==0):
                    subcodigos =repartoBuscarCodigos(self.modeloid,b,True,True)
                if (tipo==1):
                    subcodigos =repartoBuscarCodigos(self.modeloid,b,True,False)
                if (tipo==2):    
                    subcodigos=repartoBuscarCodigos(self.modeloid,b,False,True)           

                if (tipo==0 or tipo==1):# 1 es codigos (registro) (total y merc.libre)
                    energia  = BDobtieneregistro(self.per,subcodigos ,1,False)    
                    potencia = BDobtieneregistroPot(self.per,self.mimaximademanda,subcodigos,1,True)  

                    if (tipo==0):
                        cont1=len(energia)
                    if (tipo==1):
                        cont2=len(energia)    

                if (tipo==2):# 2 es contratos con clientes libres 3eros
                    energia  = BDobtieneregistro(self.per,subcodigos,2,False)    
                    potencia = BDobtieneregistroPot(self.per,self.mimaximademanda,subcodigos,2,True)    
                    cont3=len(energia)

                for e  in energia:  
                    #Si es Total, buscar modo para ver si suma o resta
                    if (tipo==0):
                        cod=Codigo.objects.get(pk=e[0])

                        if (not cod.modo): #resta
                            p[1]=p[1]*-1.0
                            for z in range(1,len(e)):
                                e[z]=e[z]*-1.0
                            

                    for p in potencia:
                        if (e[0]==p[0]):
                            pot=p[1]
                    b.RepartoIngresaRegistro(tipo,e,pot)
                
            b.RepartoHPFP(self.periodo)

            txt="-----"+FormatoNombre(25,b.barra.nombre)+":" 
            txt+=' Registros:'+format(cont1,'4.0f') + ' Mercado libre:'+format(cont2,'4.0f') + ' Clientes libres:' +format(cont3,'4.0f') 
            self.msg.append(txt)
            
    def BuscaContratos(self):
        #Contratos  mediante campo   tipo se puede identificar tipo=0: licitacion  tipo=1:bilateral 
        #                            tiene campo libre:True y False
        self.contrato  = Contrato.objects.filter(modelo_id=self.modeloid,fechaini__lte=self.fechaini, fechafin__gt=self.fechafin)


    def PorcentajeenContrato(self,cont,tipo):
        #Sumar todos los porcentajes de las barras que estan comprendidas en el contrato
        suma=0

        for b in self.Bar: 
            #buscar si esta barra esta en el contrato
            barrabx=b.barra.id
            porcebx=b.porcentaje[tipo]

            if cont.barra.id==barrabx:
                suma+=porcebx
            if cont.area.clase==0: #no hay mas barras
                return suma    
            if cont.area.clase==2: #todas las barras
                suma+=porcebx
            if (cont.area.clase==1):   #Barras seleccionadas
                if (cont.area.barra00.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra01.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra02.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra03.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra04.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra05.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra06.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra07.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra08.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra09.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra10.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra11.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra12.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra13.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra14.id==barrabx):    
                    suma+=porcebx
                if (cont.area.barra15.id==barrabx):    
                    suma+=porcebx

        return suma

    def BuscaPotenciasContratadas(self):
        # porcentajes de potencia de cada barra (coincidente con la maxima demanda,
        # sirve para identificar Pot.Contratada cuando la P.Contratada es en todas las barras
        self.msg.append('--------------------------------------------------------------------------------------')    
        self.msg.append("Lectura de Contratos aplibables a barras") 
        sumpotencia=0
        for tipo in range(2):
            for b in self.Bar: sumpotencia+=b.registro[tipo][0]
            if (sumpotencia==0):
                sumpotencia=100
            for b in self.Bar: b.porcentaje[tipo]=b.registro[tipo][0]/sumpotencia
        
        for b in self.Bar: #inicializar contratosmes regulados y libres
            b.conmes[0]=[]           
            b.conmes[1]=[]
        
        model=Modelo.objects.get(pk=self.modeloid)
        for c in self.contrato:
            if (c.modelo_id==self.modeloid and c.cliente_id==model.cliente_id):
                tipo=1 if c.libre else 0

                for b in self.Bar:

                    #Ver si la barra esta incluida en el contrato
                    incluida=BarraenContrato(c,b.barra)

                    if (incluida): # Suma de Porcentajes de las barras que estan incluidas en el contrato
                        porcentajebarrasencontrato=self.PorcentajeenContrato(c,tipo)

                        listadocontratosmes=ContratoMes.objects.filter(contrato_id=c.id,fechaini__lte=self.fechaini, fechafin__gt=self.fechafin)                
                        for lc in listadocontratosmes:
                            cont=lc
                            #Porcentajes parciales del contrato
                            if porcentajebarrasencontrato!=0: # El contrato participa en la barra 
                                cont.fija      =b.porcentaje[tipo] /porcentajebarrasencontrato * cont.fija   
                                cont.variable  =b.porcentaje[tipo] /porcentajebarrasencontrato * cont.variable
                                cont.fijafp    =b.porcentaje[tipo] /porcentajebarrasencontrato * cont.fijafp
                                cont.variablefp=b.porcentaje[tipo] /porcentajebarrasencontrato * cont.variablefp
                                b.conmes[tipo].append(cont)
                        
                                fac=InformacionFactura(cont.fija,cont.variable,
                                                   cont.fijafp,cont.variablefp,
                                                   self.fechaini,cont.fechaini,cont.fechafin)
                                b.factura[tipo].append(fac)
        
        for b in self.Bar:
            txt="-----"+FormatoNombre(25,b.barra.nombre)+":" 
            txt+=" Regulados:"+ format(len(b.conmes[0]),'3.0f') +" Mercado libre " + format(len(b.conmes[1]),'3.0f') +"\n" 
            self.msg.append(txt)

    def CalculaPotenciasFacturadas(self):
        # Determinar Potencias Variables: ver cantidad de potencia por barra y remantente de las fijas
        cont=0
        for tipo in range(2): #0: regulado 1:libre
            for b in self.Bar:
                potencia=b.registro[tipo][0]

                #  Determinacion de las Potencias Facturadas Variables por barras 
                sumFtotal=0
                sumFtotalfp=0
                sumVtotal=0
                sumVtotalfp=0

                for c in b.conmes[tipo]:   
                    sumFtotal   +=c.fija
                    sumFtotalfp +=c.fijafp
                    sumVtotal   +=c.variable
                    sumVtotalfp +=c.variablefp
               
                sumV  = 0  if sumFtotal  >potencia else potencia-sumFtotal
                sumVfp= 0  if sumFtotalfp>potencia else potencia-sumFtotalfp

                for f in b.factura[tipo]: 
                    f.variable  =0 if sumVtotal  ==0 else f.variable  *sumV  /sumVtotal
                    f.variablefp=0 if sumVtotalfp==0 else f.variablefp*sumVfp/sumVtotalfp
  
                b.pfacturada[tipo]     =sumFtotal   + sumV
                b.pfacturadafp[tipo]   =sumFtotalfp + sumVfp

                pfacturadat= b.pfacturada[tipo] if (self.periodo[mimaximademanda]==1) else b.pfacturadafp[tipo]    

                for f in b.factura[tipo]:
                    pfacturada = f.fija+c.variable if (self.periodo[mimaximademanda]==1) else f.fijafp+f.variablefp
                    f.coincidente=0 if (pfacturadat==0) else potencia * pfacturada / pfacturadat 

                    #determinar los porcentajes de participación sobre la barra para los 31 dias segun HP y HFP
                    fac  = 0 if (b.pfacturada[tipo]  ==0) else (f.fija  +f.variable  ) /b.pfacturada[tipo]
                    facfp =0 if (b.pfacturadafp[tipo]==0) else (f.fijafp+f.variablefp) /b.pfacturadafp[tipo]

                    dia=0
                    for d in self.fechas:
                        #Ver si la fecha del conmes tiene vigencia por cada dia    
                        if f.vigencia[dia]:                         
                            if d.habil:
                               f.porcentaje[dia]  =fac
                               f.porcentajefp[dia]=facfp
                            if not d.habil:
                               f.porcentaje[dia]  =facfp  #con esto ya no se necesita diferenciar entre dia laborable o no
                               f.porcentajefp[dia]=facfp
                        dia+=1
                    cont+=1
        self.msg.append('--------------------------------------------------------------------------------------')    
        self.msg.append("Potencias Facturadas exitosas:"+format(cont,'4.0f')) 


    def CalculaEnergia(self):
        # Determinar de energias
        # b.barra.nombre, b.energiahp[0],b.energiafp[0], b.energiahp[1],b.energiafp[1]  Regulado, Libre
        cont=0
        for b in self.Bar:
            for tipo in range(2):
                for f in b.factura[tipo]:
                    f.energiahp=0
                    f.energiafp=0

                    for d in range(31):
                        f.energiahp+=b.energiahp[tipo][d] * f.porcentaje[d]
                        f.energiafp+=b.energiafp[tipo][d] * f.porcentajefp[d]

                    cont+=1
        
        self.msg.append("Repartos de energías exitosas:"+format(cont,'4.0f')) 
                     

    def GrabaBaseDatos(self,miperiodoid): 

        cont=0
        reg=Reparto.objects.filter(modelo_id  = self.modeloid,mesano_id=miperiodoid)
        reg.delete()

        for b in self.Bar:
            for tipo in range(2): #0: regulado 1:libre
                for i in range(len(b.conmes[tipo])):
                    c=b.conmes[tipo][i] 
                    f=b.factura[tipo][i]
                    contrato=Contrato.objects.get(pk=c.contrato_id)

                    reg=Reparto()
                    reg.modelo_id    = self.modeloid
                    reg.mesano_id   = miperiodoid
                    reg.libre       = False    if (tipo==0) else True
                    reg.barra_id    = b.barra.id               
                    reg.contrato_id = contrato.id
                    reg.tipo        = contrato.tipo #0:Licitacion  1:Bilateral 
                    reg.generador_id = c.generador.id  
                    reg.codid       = c.codid
                    reg.fija        = c.fija     
                    reg.variable    = c.variable 
                    reg.fijafp      = c.fijafp  
                    reg.variablefp  = c.variablefp      
                    reg.fijafact        = f.fija
                    reg.variablefact    = f.variable   
                    reg.fijafptact      = f.fijafp    
                    reg.variablefpfact  = f.variablefp     
                    reg.coincidente     = f.coincidente      
                    reg.energiahp       = f.energiahp
                    reg.energiafp       = f.energiafp     
                    reg.porcentaje01     = f.porcentaje[ 0]
                    reg.porcentaje02     = f.porcentaje[ 1]
                    reg.porcentaje03     = f.porcentaje[ 2]
                    reg.porcentaje04     = f.porcentaje[ 3]
                    reg.porcentaje05     = f.porcentaje[ 4]
                    reg.porcentaje06     = f.porcentaje[ 5]
                    reg.porcentaje07     = f.porcentaje[ 6]
                    reg.porcentaje08     = f.porcentaje[ 7]
                    reg.porcentaje09     = f.porcentaje[ 8]
                    reg.porcentaje10     = f.porcentaje[ 9]
                    reg.porcentaje11     = f.porcentaje[10]
                    reg.porcentaje12     = f.porcentaje[11]
                    reg.porcentaje13     = f.porcentaje[12]
                    reg.porcentaje14     = f.porcentaje[13]
                    reg.porcentaje15     = f.porcentaje[14]
                    reg.porcentaje16     = f.porcentaje[15]
                    reg.porcentaje17     = f.porcentaje[16]
                    reg.porcentaje18     = f.porcentaje[17]
                    reg.porcentaje19     = f.porcentaje[18]
                    reg.porcentaje20     = f.porcentaje[19]
                    reg.porcentaje21     = f.porcentaje[20]
                    reg.porcentaje22     = f.porcentaje[21]
                    reg.porcentaje23     = f.porcentaje[22]
                    reg.porcentaje24     = f.porcentaje[23]
                    reg.porcentaje25     = f.porcentaje[24]
                    reg.porcentaje26     = f.porcentaje[25]
                    reg.porcentaje27     = f.porcentaje[26]
                    reg.porcentaje28     = f.porcentaje[27]
                    reg.porcentaje29     = f.porcentaje[28]
                    reg.porcentaje30     = f.porcentaje[29]
                    reg.porcentaje31     = f.porcentaje[30]

                    reg.porcentajefp01     = f.porcentaje[ 0]
                    reg.porcentajefp02     = f.porcentaje[ 1]
                    reg.porcentajefp03     = f.porcentaje[ 2]
                    reg.porcentajefp04     = f.porcentaje[ 3]
                    reg.porcentajefp05     = f.porcentaje[ 4]
                    reg.porcentajefp06     = f.porcentaje[ 5]
                    reg.porcentajefp07     = f.porcentaje[ 6]
                    reg.porcentajefp08     = f.porcentaje[ 7]
                    reg.porcentajefp09     = f.porcentaje[ 8]
                    reg.porcentajefp10     = f.porcentaje[ 9]
                    reg.porcentajefp11     = f.porcentaje[10]
                    reg.porcentajefp12     = f.porcentaje[11]
                    reg.porcentajefp13     = f.porcentaje[12]
                    reg.porcentajefp14     = f.porcentaje[13]
                    reg.porcentajefp15     = f.porcentaje[14]
                    reg.porcentajefp16     = f.porcentaje[15]
                    reg.porcentajefp17     = f.porcentaje[16]
                    reg.porcentajefp18     = f.porcentaje[17]
                    reg.porcentajefp19     = f.porcentaje[18]
                    reg.porcentajefp20     = f.porcentaje[19]
                    reg.porcentajefp21     = f.porcentaje[20]
                    reg.porcentajefp22     = f.porcentaje[21]
                    reg.porcentajefp23     = f.porcentaje[22]
                    reg.porcentajefp24     = f.porcentaje[23]
                    reg.porcentajefp25     = f.porcentaje[24]
                    reg.porcentajefp26     = f.porcentaje[25]
                    reg.porcentajefp27     = f.porcentaje[26]
                    reg.porcentajefp28     = f.porcentaje[27]
                    reg.porcentajefp29     = f.porcentaje[28]
                    reg.porcentajefp30     = f.porcentaje[29]
                    reg.porcentajefp31     = f.porcentaje[30]
                    
                    reg.usuario0=self.login
                    reg.fecha0  =datetime.now()                          
                    reg.save()  
                    cont+=1

        for b in self.Bar:
            for tipo in range(2): #0: regulado 1:libre
                b.registro[tipo][0]="Rep"+str(self.modeloid)
                BDgrabaregistro(self.login,self.per,
                            tipo, #cod,  0:regulado 1:libre
                            3,# tipo=1: Registro  tipo=2: Con.Libre3eros  tipo=3: Reparto
                            b.barra,#barra 
                            False, #Potencia
                            b.registro[tipo])

                  
        self.msg.append("Registros en la Base de Datos:"+format(cont,'4.0f')) 

class RepartoTabla():
    def __init__(self,reporte,mercado,agrupacion,tipo,valor):
        self.cabecera=[]
        self.reporte=[]

        largo=len(reporte)

        if (largo==0):
            self.cabecera=[]
            self.reporte=[] 
        if (largo>0):
            miindex=["Merc.","Barra","Contrato","Generador","Tipo","Coincidente","Facturada",
                     "Cont.Fija","Cont.Var","Cont.Fija Fact.","Cont.Var Fact." ]
            mivalues=["Coincidente","Facturada","Cont.Fija","Cont.Var","Cont.Fija Fact.","Cont.Var Fact.",
                     "Energia HP","Energia FP","Energia Total"]
                        
            xmercado=[]
            xbarra=[]
            xcontrato=[]
            xgenerador=[]
            xcodid=[]
            xtipo=[]                
            xcoincidente=[]                    
            xfacturada=[]
            xcontfija=[]
            xcontvar=[]
            xcontfijafact=[]
            xcontvarfact=[]
            xenergiahp=[]
            xenergiafp=[]
            xenergiat=[]
        
            for i in range(largo):
                mmerc="Libre" if (reporte[i].libre) else "Regul."
                xmercado.append(mmerc)
                xbarra.append(reporte[i].barra.nombre)
                xcontrato.append(reporte[i].contrato.codigo)
                xgenerador.append(reporte[i].generador.nombre)
                xcodid.append(reporte[i].codid)
                mtipo="Lic." if (reporte[i].tipo==0) else "Bil."
                xtipo.append(mtipo)
                xcoincidente.append(reporte[i].coincidente)
                xfacturada.append(reporte[i].fijafact+reporte[i].variablefact)                        
                xcontfija.append(reporte[i].fija)                        
                xcontvar.append(reporte[i].variable)                        
                xcontfijafact.append(reporte[i].fijafact)                        
                xcontvarfact.append(reporte[i].variablefact)                        
                xenergiahp.append(reporte[i].energiahp)                        
                xenergiafp.append(reporte[i].energiafp) 
                xenergiat.append(reporte[i].energiahp+reporte[i].energiafp) 
        
            df = pd.DataFrame({
              "Mercado":xmercado,"Barra": xbarra,"Contrato": xcontrato, 
              "Generador": xgenerador, "ID":xcodid,
              "Tipo":xtipo,
              "Coincidente": xcoincidente,"Facturada": xfacturada,
              "Cont.Fija": xcontfija,"Cont.Var": xcontvar,
              "Cont.Fija Fact.": xcontfijafact,"Cont.Var Fact.": xcontvarfact,
              "Energia HP":xenergiahp,"Energia FP":xenergiafp,"Energia Total":xenergiat})
        
            val=mivalues[valor-1]
        
            miindex=[]
            if((mercado==3) or (agrupacion==4 and tipo==4)):    #Mercado   Ambos 
                miindex.append("Mercado")
            if(tipo!=4):    #Tipo  total
                miindex.append("Tipo")
            if(agrupacion==1): #Contrato 
                miindex.append("Contrato")
            if(agrupacion==2 ): #Generador  
                miindex.append("Generador")
            if (agrupacion==3): # Contrato / Generador
                miindex.append("Contrato")                
                miindex.append("Generador")                
                miindex.append("ID")
        
            mireporte=pd.pivot_table(df,values=val,index=miindex,columns=["Barra"],aggfunc=np.sum,fill_value=0,margins =True)
        
        
            self.cabecera=[]
            self.reporte=[] 
        
            for col in mireporte.index.names: self.cabecera.append(col)
            for col in mireporte.columns:
                val=col if (col!='All') else 'Total'
                self.cabecera.append(val)
                
            for row in range(len(mireporte.index)):
                vector=[]
                if (isinstance(mireporte.index[row], tuple)):
                    for col in mireporte.index[row]:  
                        val=col if (col!='All') else 'Total'
                        vector.append(TablaIzq(val,True))
                else:
                    vector.append(TablaIzq(mireporte.index[row],True))    
        
                for col in mireporte.values[row]:
                    vector.append(TablaIzq(format(col,'9.3f'),False))
               
                self.reporte.append(vector)    

