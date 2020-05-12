from django import forms
from django.utils import timezone
from .models import  *

class LoginForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (LoginForm,self ).__init__(*args,**kwargs) # populates the post
    class Meta:
        model=Login
        fields=[ 'login','clave']
        labels={
            'login':'Login',
            'clave':'clave',
            }
        widgets={
            'login':forms.TextInput(attrs={'class':'form-control'}),            
            'clave':forms.PasswordInput(),            
            }

class ContratoMesForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (ContratoMesForm,self ).__init__(*args,**kwargs) # populates the post
    class Meta:
        model=ContratoMes
        fields=[ 'generador','codid','fechaini','fechafin','fija','variable','fijafp','variablefp']

        labels={
            'generador':'Generador',
            'codid':'Identificador',
            'fechaini':'Fecha ini',
            'fechafin':'Fecha fin',
            'fija':'Pot.Fija HP (MW)',
            'variable':'Pot.Variable HP (MW)',
            'fijafp':'Pot.Fija HFP (MW)',
            'variablefp':'Pot.Variable HFP (MW)',            
            }
        help_texts = { 'fechaini': ('mm/dd/yyyy'), 'fechafin': ('mm/dd/yyyy'),} 
        widgets={
            'generador':forms.Select(attrs={'class':'form-control'}),            
            'codid':forms.NumberInput(attrs={'class':'form-control'}),          
            'fechaini':forms.DateInput(format=('%m/%d/%Y'),  attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            'fechafin':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            'fija':       forms.NumberInput(attrs={'class':'form-control'}),
            'variable':   forms.NumberInput(attrs={'class':'form-control'}),
            'fijafp':       forms.NumberInput(attrs={'class':'form-control'}),
            'variablefp':   forms.NumberInput(attrs={'class':'form-control'}),
          
            }
class ContratoForm1(forms.ModelForm): #Para Licitaciones o bilaterales 
    def __init__(self,cliente,*args,**kwargs):
        super (ContratoForm1,self ).__init__(*args,**kwargs) # populates the post
        self.fields['barra'].queryset = Barra.objects.filter(cliente=cliente)
        self.fields['area'].queryset = Area.objects.filter(cliente=cliente)

    class Meta:
        model=Contrato
        fields=[  'descripcion','codigo','area','barra','libre','fechaini','fechafin']

        labels={
            'descripcion':'Descripción',            
            'codigo':'Código',
            'area':'Area',
            'barra':'Barra',
            'libre':'Mercado',
            'fechaini':'fechaini',
            'fechafin':'fechafin',
            }
        widgets={
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),            
            'codigo':     forms.TextInput(attrs={'class':'form-control'}),
            'area' :forms.Select(attrs={'class':'form-control'}),            
            'barra':forms.Select(attrs={'class':'form-control'}),            
            'libre'      :forms.Select(choices=[(True, 'Libre'),  (False, 'Regulado')]),
            'fechaini':forms.DateInput(format=('%m/%d/%Y'),  attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            'fechafin':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            }
        
class ContratoForm2(forms.ModelForm): #para clientes libre 3eros
    def __init__(self,cliente,*args,**kwargs):
        super (ContratoForm2,self ).__init__(*args,**kwargs) # populates the post
        self.fields['barra'].queryset = Barra.objects.filter(cliente=cliente)

    class Meta:
        model=Contrato
        fields=[ 'descripcion','codigo','barra','cliente','fechaini','fechafin']

        labels={
            'descripcion':'Descripción',            
            'codigo':'Código',
            'barra':'Barra',
            'cliente':'Cliente',
            'fechaini':'fechaini',
            'fechafin':'fechafin',            
            }
        widgets={
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'codigo':     forms.TextInput(attrs={'class':'form-control'}),
            'cliente'    :forms.Select(attrs={'class':'form-control'}),   
            'barra':     forms.Select(attrs={'class':'form-control'}),                     
            'fechaini':forms.DateInput(format=('%m/%d/%Y'),  attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            'fechafin':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            }
        
       

class CodigoForm(forms.ModelForm): #Para mediciones
    def __init__(self,cliente,*args,**kwargs):
        super (CodigoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['barra'].queryset = Barra.objects.filter(cliente=cliente)

    class Meta:
        model=Codigo
        fields=[ 'barra','nombre', 'descripcion', 'signo','modo','fechaini','fechafin']

        labels={
            'barra':'Barra',                        
            'nombre':'Código',
            'descripcion':'Descripcion',
            'signo':'Tipo',            
            'modo':'Modo',            
            'fechaini':'Fecha inicio',
            'fechafin':'Fecha fin',
            }
        help_texts = { 'fechaini': ('mm/dd/yyyy'), 'fechafin': ('mm/dd/yyyy'),'modo':('Mercado libre:(-)')} 
        widgets={
            'barra':forms.Select(attrs={'class':'form-control'}),                        
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'signo':   forms.Select(choices=[(True, 'Total'),  (False, 'Mercado Libre')]),       
            'modo':    forms.Select(choices=[(True, '+'),  (False, '-')]),                   
            'fechaini':forms.DateInput(format=('%m/%d/%Y'),  attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            'fechafin':forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'myDateClass', 'placeholder':'Select a date'}),
            }
        

        
