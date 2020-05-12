from django.db import models
import datetime
from django.utils import timezone
from datetime import datetime

TIPOCONTRATO = [
    (0, 'Licitación'),
    (1, 'Bilateral'),
    (2, 'C.Libres'),
]

CLASEAREA = [
    (0, 'Ninguna'),
    (1, 'Selección'),
    (2, 'Todas'),    
]

MODO = [
    (True, '+'),
    (False, '-'),
]
class Dias(models.Model):
    dia=models.DateField('Dia')
    habil=models.BooleanField(default=True)
    ddmmyyyy=models.CharField(max_length=10)    
    def __str__(self):
        return self.ddmmyyyy

#**************************************************************
class Usuario(models.Model):
    nombre   = models.CharField(max_length=50)    
    apellido = models.CharField(max_length=50)    
    empresa  = models.CharField(max_length=50)    
    correo   = models.EmailField()    
    telefono = models.CharField(max_length=50)  
    login    = models.CharField(max_length=50)    
    clave    = models.CharField(max_length=50)  
    clave2   = models.CharField(max_length=50)  
    modelos  = models.CharField(max_length=200)   #tres caracteres para cada id de modelo, con esto se identifica a cual tiene acceso
    modo     = models.CharField(max_length=200)   #tres caracteres para cada id de modelo, con esto se identifica modo de acceso
    fecha  = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.nombre+' '+self.apellido

class Login(models.Model):
    login   = models.CharField(max_length=50)    
    clave = models.CharField(max_length=50)    
    def __str__(self):
        return self.login

class Periodo(models.Model):
    mesano = models.DateField('Vigencia')
    descripcion = models.CharField(max_length=40)    
    activo = models.IntegerField(default=0)
    fecha  = models.DateField('date published') 
    maxdemandadia  = models.IntegerField(default=1)
    maxdemandahora = models.IntegerField(default=0)

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.descripcion

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)    
    descripcion = models.CharField(max_length=200)    

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.nombre

class Generador(models.Model):
    nombre = models.CharField(max_length=200)    
    descripcion = models.CharField(max_length=200)    

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha  = models.DateTimeField('date published')
    visualizar = models.BooleanField(default=True)

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField('fecha actualizado') 
    def __str__(self):
        return self.nombre


class FactorPerdidas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    factor  = models.FloatField(default=1) 

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField('fecha actualizado') 

    def __str__(self):
        return self.nombre

class BarraTransferencia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField('fecha actualizado') 

    def __str__(self):
        return self.nombre

class Barra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    barratransferencia = models.ForeignKey(BarraTransferencia, on_delete=models.CASCADE)   
    factorperdidas = models.ForeignKey(FactorPerdidas, on_delete=models.CASCADE)         

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.descripcion

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    cliente      = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    clase        = models.IntegerField(default=1,choices=CLASEAREA) #0:Ninguna 1:Seleccion 2:Todas
    barra00 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra00')   
    barra01 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra01')   
    barra02 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra02')   
    barra03 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra03')   
    barra04 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra04')   
    barra05 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra05')   
    barra06 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra06')   
    barra07 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra07')   
    barra08 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra08')   
    barra09 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra09')   
    barra10 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra10')   
    barra11 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra11')   
    barra12 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra12')   
    barra13 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra13')   
    barra14 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra14')   
    barra15 = models.ForeignKey(Barra, on_delete=models.CASCADE,related_name='barra15')   

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.descripcion

class Codigo(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    barra = models.ForeignKey(Barra, on_delete=models.CASCADE)    
    
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)    
    fechaini  = models.DateField('Fecha inicio')
    fechafin  = models.DateField('Fecha fin')
    signo = models.BooleanField(default=True)
    modo  = models.BooleanField(default=True,choices=MODO)  #True:Suma False:Resta
    auxiliar1 = models.IntegerField(default=0)
    auxiliar2 = models.IntegerField(default=0)

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return str(self.modelo_id)+"-"+ self.nombre

#class TipoContrato(models.Model):
#    nombre      = models.CharField(max_length=200)        
#    descripcion = models.CharField(max_length=200)
#    licitacion  = models.BooleanField(default=True)
#    regulado    = models.BooleanField(default=True)
#    def __str__(self):
#        return self.nombre

class Contrato(models.Model):
    descripcion  = models.CharField(max_length=200)
    codigo       = models.CharField(max_length=200)       
    cliente      = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    modelo       = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    tipo         = models.IntegerField(default=1,choices=TIPOCONTRATO)  #0:Licitacion  1:Bilateral 2:C.Libres
    libre        = models.BooleanField(default=True)                    #True:Libre False:Regulado
    barra        = models.ForeignKey(Barra, on_delete=models.CASCADE)
    area         = models.ForeignKey(Area, on_delete=models.CASCADE)
    fechaini     = models.DateField('Fecha inicio', blank=True)
    fechafin     = models.DateField('Fecha fin', blank=True)     

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return self.codigo
class ContratoMes(models.Model):
    contrato     = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    generador    = models.ForeignKey(Generador, on_delete=models.CASCADE)  
    codid        = models.IntegerField(default=1) 
    fechaini     = models.DateField('Fecha inicio')
    fechafin     = models.DateField('Fecha fin')    
    fija        = models.FloatField(default=0)      
    variable    = models.FloatField(default=0)     
    fijafp      = models.FloatField(default=0)      
    variablefp  = models.FloatField(default=0)      

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return str(self.contrato)+"-"+str(self.generador)

class Reparto(models.Model):
    modelo       = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    mesano       = models.ForeignKey(Periodo, on_delete=models.CASCADE)    
    libre        = models.BooleanField(default=True)                    #True:Libre False:Regulado    
    barra        = models.ForeignKey(Barra, on_delete=models.CASCADE)
    contrato     = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    tipo         = models.IntegerField(default=1,choices=TIPOCONTRATO)  #0:Licitacion  1:Bilateral 2:C.Libres    
    generador    = models.ForeignKey(Generador, on_delete=models.CASCADE)    
    codid        = models.IntegerField(default=1)
    fija        = models.FloatField(default=0)      #Pot.Cont.Fija HP
    variable    = models.FloatField(default=0)      #Pot.Cont.Var  HP
    fijafp      = models.FloatField(default=0)      #Pot.Cont.Fija FP 
    variablefp  = models.FloatField(default=0)      #Pot.Cont Var  FP
    fijafact        = models.FloatField(default=0)  #Pot.Fact.Fija HP    
    variablefact    = models.FloatField(default=0)  #Pot.Fact.Var  HP   
    fijafptact      = models.FloatField(default=0)  #Pot.Fact.Fija FP    
    variablefpfact  = models.FloatField(default=0)  #Pot.Fact.Var  FP    
    coincidente     = models.FloatField(default=0)  #Pot.Coincidente 
    energiahp       = models.FloatField(default=0)  #Energia HP 
    energiafp       = models.FloatField(default=0)  #Energia FP

    # Para determinar la energia de c/15:
    # Obtener registros energia de la barra (Regulado o Libre) c/15
    # aplicar el porcentaje por bloques horarios (hp se aplica a 18-23), no importa si es dia laborable o no,
    # esto ya se incorporo en el calculo previo
    # Si no esta vigente  el contrato para ese dia es 0 y 0
    # el bloque de punta esta en el periodo   72<=i and i<=91 
    porcentaje01      = models.FloatField(default=0)  
    porcentaje02      = models.FloatField(default=0)  
    porcentaje03      = models.FloatField(default=0)  
    porcentaje04      = models.FloatField(default=0)  
    porcentaje05      = models.FloatField(default=0)  
    porcentaje06      = models.FloatField(default=0)  
    porcentaje07      = models.FloatField(default=0)  
    porcentaje08      = models.FloatField(default=0)  
    porcentaje09      = models.FloatField(default=0)  
    porcentaje10      = models.FloatField(default=0)  
    porcentaje11      = models.FloatField(default=0)  
    porcentaje12      = models.FloatField(default=0)  
    porcentaje13      = models.FloatField(default=0)  
    porcentaje14      = models.FloatField(default=0)  
    porcentaje15      = models.FloatField(default=0)  
    porcentaje16      = models.FloatField(default=0)  
    porcentaje17      = models.FloatField(default=0)  
    porcentaje18      = models.FloatField(default=0)  
    porcentaje19      = models.FloatField(default=0)  
    porcentaje20      = models.FloatField(default=0)  
    porcentaje21      = models.FloatField(default=0)  
    porcentaje22      = models.FloatField(default=0)  
    porcentaje23      = models.FloatField(default=0)  
    porcentaje24      = models.FloatField(default=0)  
    porcentaje25      = models.FloatField(default=0)  
    porcentaje26      = models.FloatField(default=0)  
    porcentaje27      = models.FloatField(default=0)  
    porcentaje28      = models.FloatField(default=0)  
    porcentaje29      = models.FloatField(default=0)  
    porcentaje30      = models.FloatField(default=0)                      
    porcentaje31      = models.FloatField(default=0)                          
    porcentajefp01      = models.FloatField(default=0)  
    porcentajefp02      = models.FloatField(default=0)  
    porcentajefp03      = models.FloatField(default=0)  
    porcentajefp04      = models.FloatField(default=0)  
    porcentajefp05      = models.FloatField(default=0)  
    porcentajefp06      = models.FloatField(default=0)  
    porcentajefp07      = models.FloatField(default=0)  
    porcentajefp08      = models.FloatField(default=0)  
    porcentajefp09      = models.FloatField(default=0)  
    porcentajefp10      = models.FloatField(default=0)  
    porcentajefp11      = models.FloatField(default=0)  
    porcentajefp12      = models.FloatField(default=0)  
    porcentajefp13      = models.FloatField(default=0)  
    porcentajefp14      = models.FloatField(default=0)  
    porcentajefp15      = models.FloatField(default=0)  
    porcentajefp16      = models.FloatField(default=0)  
    porcentajefp17      = models.FloatField(default=0)  
    porcentajefp18      = models.FloatField(default=0)  
    porcentajefp19      = models.FloatField(default=0)  
    porcentajefp20      = models.FloatField(default=0)  
    porcentajefp21      = models.FloatField(default=0)  
    porcentajefp22      = models.FloatField(default=0)  
    porcentajefp23      = models.FloatField(default=0)  
    porcentajefp24      = models.FloatField(default=0)  
    porcentajefp25      = models.FloatField(default=0)  
    porcentajefp26      = models.FloatField(default=0)  
    porcentajefp27      = models.FloatField(default=0)  
    porcentajefp28      = models.FloatField(default=0)  
    porcentajefp29      = models.FloatField(default=0)  
    porcentajefp30      = models.FloatField(default=0)                      
    porcentajefp31      = models.FloatField(default=0)                          
    
    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 

    def __str__(self):
        return str(self.modelo)+"-"+str(self.mesano)

class Registro(models.Model):
    #codigo = models.ForeignKey(Codigo, on_delete=models.CASCADE)
    codigo  = models.IntegerField(default=1)  
    mesano = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    version = models.IntegerField(default=0)    
    barra   = models.ForeignKey(Barra, on_delete=models.CASCADE)
    tipo    = models.IntegerField(default=1)    #1: registro 2:contrato cliente libre 3eros
    potencia= models.BooleanField(default=False)
    descripcion = models.CharField(max_length=200)        
    dia     = models.IntegerField(default=0)  
    energia = models.FloatField(default=0)        
    reg00    = models.FloatField(default=0)    
    reg01    = models.FloatField(default=0)    
    reg02    = models.FloatField(default=0)    
    reg03    = models.FloatField(default=0)    
    reg04    = models.FloatField(default=0)    
    reg05    = models.FloatField(default=0)    
    reg06    = models.FloatField(default=0)    
    reg07    = models.FloatField(default=0)    
    reg08    = models.FloatField(default=0)    
    reg09    = models.FloatField(default=0)                                    
    reg10    = models.FloatField(default=0)    
    reg11    = models.FloatField(default=0)    
    reg12    = models.FloatField(default=0)    
    reg13    = models.FloatField(default=0)    
    reg14    = models.FloatField(default=0)    
    reg15    = models.FloatField(default=0)    
    reg16    = models.FloatField(default=0)    
    reg17    = models.FloatField(default=0)    
    reg18    = models.FloatField(default=0)    
    reg19    = models.FloatField(default=0)                                    
    reg20    = models.FloatField(default=0)    
    reg21    = models.FloatField(default=0)    
    reg22    = models.FloatField(default=0)    
    reg23    = models.FloatField(default=0)    
    reg24    = models.FloatField(default=0)    
    reg25    = models.FloatField(default=0)    
    reg26    = models.FloatField(default=0)    
    reg27    = models.FloatField(default=0)    
    reg28    = models.FloatField(default=0)    
    reg29    = models.FloatField(default=0)                                    
    reg30    = models.FloatField(default=0)    
    reg31    = models.FloatField(default=0)    
    reg32    = models.FloatField(default=0)    
    reg33    = models.FloatField(default=0)    
    reg34    = models.FloatField(default=0)    
    reg35    = models.FloatField(default=0)    
    reg36    = models.FloatField(default=0)    
    reg37    = models.FloatField(default=0)    
    reg38    = models.FloatField(default=0)    
    reg39    = models.FloatField(default=0)                                    
    reg40    = models.FloatField(default=0)    
    reg41    = models.FloatField(default=0)    
    reg42    = models.FloatField(default=0)    
    reg43    = models.FloatField(default=0)    
    reg44    = models.FloatField(default=0)    
    reg45    = models.FloatField(default=0)    
    reg46    = models.FloatField(default=0)    
    reg47    = models.FloatField(default=0)    
    reg48    = models.FloatField(default=0)    
    reg49    = models.FloatField(default=0)                                    
    reg50    = models.FloatField(default=0)    
    reg51    = models.FloatField(default=0)    
    reg52    = models.FloatField(default=0)    
    reg53    = models.FloatField(default=0)    
    reg54    = models.FloatField(default=0)    
    reg55    = models.FloatField(default=0)    
    reg56    = models.FloatField(default=0)    
    reg57    = models.FloatField(default=0)    
    reg58    = models.FloatField(default=0)    
    reg59    = models.FloatField(default=0)                                    
    reg60    = models.FloatField(default=0)    
    reg61    = models.FloatField(default=0)    
    reg62    = models.FloatField(default=0)    
    reg63    = models.FloatField(default=0)    
    reg64    = models.FloatField(default=0)    
    reg65    = models.FloatField(default=0)    
    reg66    = models.FloatField(default=0)    
    reg67    = models.FloatField(default=0)    
    reg68    = models.FloatField(default=0)    
    reg69    = models.FloatField(default=0)                                    
    reg70    = models.FloatField(default=0)    
    reg71    = models.FloatField(default=0)    
    reg72    = models.FloatField(default=0)    
    reg73    = models.FloatField(default=0)    
    reg74    = models.FloatField(default=0)    
    reg75    = models.FloatField(default=0)    
    reg76    = models.FloatField(default=0)    
    reg77    = models.FloatField(default=0)    
    reg78    = models.FloatField(default=0)    
    reg79    = models.FloatField(default=0)                                    
    reg80    = models.FloatField(default=0)    
    reg81    = models.FloatField(default=0)    
    reg82    = models.FloatField(default=0)    
    reg83    = models.FloatField(default=0)    
    reg84    = models.FloatField(default=0)    
    reg85    = models.FloatField(default=0)    
    reg86    = models.FloatField(default=0)    
    reg87    = models.FloatField(default=0)    
    reg88    = models.FloatField(default=0)    
    reg89    = models.FloatField(default=0)                                    
    reg90    = models.FloatField(default=0)    
    reg91    = models.FloatField(default=0)    
    reg92    = models.FloatField(default=0)    
    reg93    = models.FloatField(default=0)    
    reg94    = models.FloatField(default=0)    
    reg95    = models.FloatField(default=0)    

    usuario0 = models.CharField(max_length=200)
    fecha0   = models.DateTimeField(default=datetime.today) 
                                                  
    def __str__(self):
        return self.descripcion

