
import xlsxwriter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import io
import urllib, base64
from datetime import datetime, timedelta
import date_converter
from calendar import mdays
import random
import numpy as np
import xlsxwriter

from .models import *


def FormatoNombre(n,nombre):
    ll=len(nombre)
    for i in range(n-ll):
      nombre=nombre+'_'
    return nombre

def round_up(total,partes):
    val=int(total/partes)+(total%partes>0)
    return int(val)    

class InspeccionaModelo:
    def __init__(self,modeloid,per):
        
        modelo=Modelo.objects.get(pk=modeloid)

        fechaini=Periodo.objects.get(pk=per).mesano
        fechafin=fechaini+timedelta(mdays[fechaini.month])

        fechas=Dias.objects.filter(dia__gte=fechaini, dia__lte=fechafin)
        self.contrato = Contrato.objects.filter(modelo_id=modeloid,tipo__in=[0,1],
                                 fechaini__lte=fechaini, fechafin__gt=fechafin)   
        self.generador=[]
        for c in self.contrato:
            listadocontratosmes=ContratoMes.objects.filter(contrato_id=c.id,fechaini__lte=fechaini, fechafin__gt=fechafin)                
            for cm in listadocontratosmes:
                self.generador.append(cm.generador)
        self.generador=list(set(self.generador))         #se eliminan duplicados

        bar=Barra.objects.filter(cliente=modelo.cliente)
        self.barra=[]
        for b in bar:
            if (b.nombre!="Todas"):
                self.barra.append(b)

    
def CreaPeriodoHPFP(per): #crea fechas y hp/hfp
    fechaini=Periodo.objects.get(pk=per).mesano
    fechafin=fechaini+timedelta(mdays[fechaini.month])
    fechas=Dias.objects.filter(dia__gte=fechaini, dia__lte=fechafin)
    cont=0
    periodo=[]
    for f in fechas:
        for i in range(96):
            tipo=1 if (72<=i and i<=91 and f.habil) else 0
            periodo.append(tipo)
            cont+=1
    #completar para los 31 dias
    largo=len(periodo)
    for i in range(largo,2976):
        periodo.append(0)

    return periodo

def Creagrafico(tipo,nombres,y,colorx):
    n=len(nombres)

    if (tipo=='1' or tipo=='6'): #cada 15
        x2=[]                    
        for d in range(2976):  x2.append(d/96)
        y2=[]
        for i in range(len(nombres)):
            val=[]
            y2.append(val)
            for j in range(2976):  y2[i].append(y[i][j+1]*4)

    if (tipo=='2' or tipo=='3' or tipo=='5'): 
        x2=nombres
        y2=[]
        for i in range(len(nombres)):
            suma=0
            for j in range(2976):  suma+=y[i][j+1]
            y2.append(suma*0.001)

    if (tipo=='4'  or tipo=='10' ):
        x2=[]
        for d in range(31): x2.append(d+1)
        y2=[]
        for i in range(len(nombres)):
            vec=[]
            for d in range(31): vec.append(0)
            y2.append(vec)                        

            pos=0
            for d in range(31):
                suma=0
                for t in range(96):
                    pos=d*96+t
                    suma+=y[i][pos+1]
                y2[i][d]=suma*0.001
        
    plt.rcParams.update({'figure.max_open_warning': 0})    

    f = plt.figure()

    if (tipo=='1' or tipo=='6'):  # cada 15 minutos todos los dias
        f, axes = plt.subplots(3)
        f.suptitle('Potencia (MW)')

        if (tipo=='1'): # independientes
            for i in range(n):  axes[0].plot( x2[0:1056], y2[i][0:1056],label=nombres[i])        
            for i in range(n):  axes[1].plot( x2[1056:2112], y2[i][1056:2112])
            for i in range(n):  axes[2].plot( x2[2112:2976], y2[i][2112:2976])
        if (tipo=='6'): # acumulados    
            ygraf=[]
            for i in range(n): ygraf.append(y2[i][0:1056])
            axes[0].stackplot(x2[0:1056],ygraf,labels=nombres)

            ygraf=[]
            for i in range(n): ygraf.append(y2[i][1056:2112])
            axes[1].stackplot(x2[1056:2112],ygraf)

            ygraf=[]
            for i in range(n): ygraf.append(y2[i][2112:2976])
            axes[2].stackplot(x2[2112:2976],ygraf)


        axes[0].set(xlim=(0,11))
        axes[1].set(xlim=(11,22))
        axes[2].set(xlim=(22,33))
        for i in range(3):
            axes[i].grid(b=True, which='major', color='red', linestyle='-')
            axes[i].minorticks_on()
            axes[i].grid(b=True, which='minor', color='black', linestyle='-', alpha=0.2)

        f.legend(prop = {'size': 5}, loc='upper right')
        

    if (tipo=='2'):  #barras energia mensual vertical
        h=plt.bar(x2,y2,align='center', label=nombres,  color=colorx)
        #plt.xticks(x, nombres,rotation=20)
        plt.xticks([])
        plt.title('Energía mensual (GW.h)')
        plt.legend(h,nombres,prop = {'size': 5}, loc='upper right')

    if (tipo=='3'):  #barras energia mensual horizontal
        h = plt.barh(x2, y2,  align='center', label=nombres,  color=colorx )
        plt.yticks([])
        plt.title('Energía mensual (GW.h)')
        plt.legend(h, nombres,prop = {'size': 5}, loc='upper right')
        

    if (tipo=='4'): #barras energia por dias
        axes = f.add_axes([0.05,0.05,0.9,0.9])

        for i in range(n):
            xaux=[]
            for j in range(len(x2)): xaux.append(x2[j]+0.1*i)
            axes.bar(xaux , y2[i], width = 0.25)
        axes.set_title('Energía diaria (GW.h)')
        axes.legend(labels=nombres,prop = {'size': 5}, loc='upper right')
        axes.yaxis.set_tick_params(labelsize=8)
        

    if (tipo=='5'): #pie por energia
        axes = f.add_axes([0.05,0.05,0.9,0.9])
        patches, texts, autotexts = axes.pie(y2, labels=nombres, autopct='%1.1f%%', startangle=90)
        for i in range(len(texts)): texts[i].set_fontsize(6)
        for i in range(len(texts)): autotexts[i].set_fontsize(7)
        axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.        
        axes.legend(prop = {'size': 5}, loc='upper right')

    if (tipo=='10'): #3d
        if (len(y)==0):
            return
        data=np.array([y2[0]])
        for i in range(1,len(nombres)):
            data=np.append(data,[y2[i]],axis=0)
        column_names=[]
        for i in range(31): column_names.append(str(i+1))
        row_names=nombres

       
        f = plt.figure()
        axes = Axes3D(f)
        
        lx= len(data[0])            # Work out matrix dimensions
        ly= len(data[:,0])

        xpos = np.arange(0,lx,1)    # Set up a mesh of positions
        ypos = np.arange(0,ly,1)
        xpos, ypos = np.meshgrid(xpos+0.1, ypos+0.2)
        
        xpos = xpos.flatten()   # Convert positions to 1D array
        ypos = ypos.flatten()
        zpos = np.zeros(lx*ly)
        
        dx = 0.1 * np.ones_like(zpos)
        dy = dx.copy()
        dz = data.flatten()

        axes.bar3d(xpos,ypos,zpos, dx, dy, dz,  alpha=0.5)

       
        ticksx = np.arange(0.5, 31, 1)
        plt.xticks(ticksx, column_names)
        ticksy = np.arange(0.6, len(nombres), 1)
        plt.yticks(ticksy, row_names)

        axes.set_xlabel('dia')
        #axes.set_ylabel('Day')
        axes.set_zlabel('Energía (GW.h)')
        axes.yaxis.set_tick_params(labelsize=5)
        axes.xaxis.set_tick_params(labelsize=5)

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    f.savefig(buf,format='png')
    buf.seek(0)
    string=base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    return uri    



def WriteToExcel(workbook,tipo,descripcion,nombre,miperiodo,tit,y):

    title = workbook.add_format({ 'bold': True,  'font_size': 14,  'align': 'center',  'valign': 'vcenter'})
    header = workbook.add_format({'bg_color': '#F7F7F7', 'color': 'black',  'align': 'center',  'valign': 'top',  'border': 1})

    if (tipo==1):
                worksheet = workbook.add_worksheet(nombre)
                worksheet.merge_range('B1:H1', descripcion, title)

                for i in range(len(tit)):
                    for col in range(len(tit[i])):
                        if (tit[i][col].tipo=='t'):
                            worksheet.write_string(i+1, col, tit[i][col].cad,header)
                        if (tit[i][col].tipo=='f'):
                            worksheet.write_formula(i+1, col, tit[i][col].cad,header)
                        if (tit[i][col].tipo=='n'):
                            worksheet.write_number(i+1, col, tit[i][col].cad,header)

                fechaini=Periodo.objects.get(pk=miperiodo).mesano
                fecha0 = date_converter.date_to_datetime(fechaini)
                
                pos=len(tit)             

                delta=timedelta(minutes=15)
                for fil in range(2976):
                    fecha0=fecha0+delta
                    worksheet.write(fil+pos+1,0, fecha0.strftime('%x %X'))

                for fil in range(1,len(y[0])):
                    for col in range(len(y)):
                        worksheet.write_number(fil+pos,col+1,y[col][fil])             
                        
                        

class MensajesTxt():
    def __init__(self,tipo):
        titulo=''    
        ss=[]
        if (tipo=='Menu'):
            titulo='Menu de Modelos'
            ss.append('Contratos        : Información de contratos de Licitaciones, Bilaterales y Clientes libres')        
            ss.append('Punto de medición: Parámetros de medición')     
            ss.append('Registros        : Puntos de medición')     
            ss.append('Reparto          : Reparto de energía y potencia de la Distribuidora entre Generadores')     
        if (tipo=='Contrato'):
            titulo='Contratos'
            ss.append('Información de contratos de Licitaciones, Bilaterales y Clientes libres')
            ss.append('Licitaciones: contratos de Generadoras con la Distribuidora llevados a cabo por Osinergmin')
            ss.append('Bilaterales: contratos de Generadoras con la Distribuidora llevados a cabo directamente')
            ss.append('Clientes Libres: contratos de Generadoras con clientes libres dentro de la zona de Distribución')
        if (tipo=='Medicion'):
            titulo='Registros'
            ss.append('Parámetros de medición')
            ss.append(' Modo:')
            ss.append('      (+): Consumo de distribuidora   (-) Consumo externo a la distribuidora')
        if (tipo=='Registro'):
            titulo='Puntos de medición'
            ss.append('Gestión de contadores de registros de medidores')
        if (tipo=='Reparto'):
            titulo='Reparto'
            ss.append('Gestión de reparto de energía y potencia de la Distribuidora entre Generadores')
            ss.append('Cálculo: a ser utilizado para determinar los repartos de energía y potencia. Si ya han sido determinados no es necesario lo vuelva a hacer')
        self.titulo=titulo
        self.msg=ss
