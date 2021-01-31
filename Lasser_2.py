import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
from sklearn.metrics import r2_score

def laser(nom,landa,dl,rango,n_p):
	arc = open(nom,'r+')
	todo = arc.readlines()
	#constantes
	l = 0
	X = []
	Y = []
	u = 0
	j = 0
	max_y = []
	max_x = []
	#Separar letras de valores
	for i in range (len(todo)):
		if todo[i].find('>') != -1:#Cuando encuentra la letra 
			l=i+1
			break
	#Agrego las listas en dos vectores
	for x in todo[l:]:
		X.append(float(x.split()[0]))#split se usa para columnas
		Y.append(float(x.split()[1]))
	arc.close()
	#Encuentro Maximos
	for u in range (len(landa)):
		for i in range (0,len(X)):
			if all([X[i]>=(landa[u]-dl), X[i]<=(landa[u]+dl)]):#if all varias condiciones
				if j==0:
					maxd_y = Y[i]
					maxd_x = X[i]
					j=1
				elif  Y[i]>maxd_y:
					maxd_y = Y[i]
					maxd_x = X[i]			
		max_y.append(maxd_y)
		max_x.append(maxd_x)
		j = 0
	
	#------------------Dfinir rango-----------
	Xaux = []
	Yaux = []
	Yaux_ = []
	X_ = np.linspace(540,600,100)
	T = 0
	#----------------hecho en clase--------
	i = 0
	Xaux2 = []
	Yaux2 = []
	U = 0
	while U < len(X):
		if X[U] < rango[1] and X[U] > rango[0]:
			miny = max(Y)
			while X[U] < rango[0] + (i+1)*5 and X[U] > rango[0]+i*5:
				if miny > Y[U]:
					miny = Y[U]
					minx = X[U]
				U += 1
			Xaux2.append(minx)
			Yaux2.append(miny)
			i += 1
		U += 1
	ajuste2 = np.poly1d(np.polyfit(Xaux2,Yaux2,n_p))
	while T < len(X):
		if X[T] > rango[0] and X[T] < rango[1]:
			Xaux.append(X[T])
			Yaux.append(Y[T])
			Yaux_.append(Y[T]-ajuste2(X[T]))
		T += 1
	print("r^2 = " + str(r2_score(Yaux2, ajuste2(Xaux2))))
	#--------------------Hacer ajuste---------
	ajuste = np.poly1d(np.polyfit(Xaux,Yaux,n_p))
	#------------------Calcular Area
	minT = np.amin(Yaux_)
	max_y_a = []
	for r in range (0,len(max_x)):
		auxa = max_y[r]-ajuste2(max_x[r])-minT
		max_y_a.append(auxa)
	Yaux_2 = []
	for r in range(0,len(Yaux_)):
		Yaux_2.append(Yaux_[r]-minT)

	Ap = Area_P(max_x,max_y,Xaux,Yaux)
	#Imprimir picos
	print("-------------------------",nom,"-----------------------------")
	print("Longitud Propuesta ","Longitud Real ","Intensidad","Area",sep="\t")
	for i in range (len(max_y)):
		print("",landa[i],"|",max_x[i],"|",max_y[i],"|",Ap[0][i],sep="\t")
		print("----------------------------------------------------------------------------------------")
	#--------------Graficar----------
	g = plt.subplot(2,1,1)
	g = plt.plot(Xaux,Yaux,'b',max_x,max_y,'k*',X_,ajuste(X_),'m',X_,ajuste2(X_),'r')
	g = plt.title(nom)
	g = plt.ylabel("intensidad")
	g = plt.legend(('Espectro', 'Maximos Locales', 'Ajuste Polinomial','Ajuste sin minimos'), prop = {'size': 9}, loc='upper right')#Pongo recuadro con indormacion
	g = plt.axvline(x = rango[0],color='c',linestyle = '-')
	for e in range(len(max_x)):
		g = plt.annotate(str("{0:.2f}".format(max_y[e])),xy=(max_x[e],max_y[e]))
	g3 = plt.subplot(2,1,2)
	g3 = plt.plot(Xaux,Yaux_2,'b',X_,ajuste2(X_),'r')
	g3 = plt.xlabel("Lambda")
	g3 = plt.ylabel("intensidad")
	for i in range(0,len(Ap[1])):
		g3 = plt.axvline(x = Ap[1][i],color='k',linestyle = '-')
		g3 = plt.axvline(x = Ap[2][i],color='k',linestyle = '-')
	g3 = plt.legend(('Espectro','Ajuste sin minimos'), prop = {'size': 9}, loc='upper right')#Pongo recuadro con indormacion
	g3 = plt.axhline(y = 0,color ='c',linestyle = '-')
	g3 = plt.axvline(x = rango[0],color='c',linestyle = '-')
	g3 = plt.show()
	return max_y
#--------------------------Funcion que calcula el promedio
def promedio(numarc,nump,prom_p):
	aux_p = []
	aux = 0
	prom_f = []

	for j in range (nump):
		for i in range (numarc):
			aux_p.append(prom_p[i][j])
			aux += aux_p[i]
		aux = aux / numarc
		prom_f.append(aux)
		aux_p = []
		aux = 0 
	print("-------------------------Promedio---------------------------")
	for j in range (nump):
		print("Promedio de picos ",j+1,": ",prom_f[j])
#-------------------Funcion que calcula el Area
def Area_P(Xmax,Ymax,X,Y):
	U = 0
	c = 1
	c2 = -1
	Ymas = []
	Ymast = []
	Xmas = [] 
	Ymenos = []
	Ymenost = []
	Xmenos = []
	for i in range(len(X)):
		if Xmax[U] == X[i]:
			aux_y = Ymax[U]
			while Y[i+c] < aux_y:
				aux_y = Y[i+c]
				Ymas.append(Y[i+c])
				c += 1
			Xmas.append(X[i+c-1])
			Ymast.append(Ymas)
			Ymas = []
			aux_y2 = Ymax[U]
			while Y[i+c2] < aux_y2:
				aux_y2 = Y[i+c2]
				Ymenos.append(Y[i+c2])
				c2 -= 1
			Xmenos.append(X[i+c2+1])
			Ymenost.append(Ymenos)
			Ymenos = []
			if U < len(Xmax)-1:
				U += 1
				c = 1
				c2 = -1
	Area = []
	Cambiox = []
	Sumad = []
	Sumai = []
	Sumat = []
	for v in range(len(Ymast)):#Me da el numero de filas de la matriz 5 en este caso
		auxX = Xmas[v]-Xmenos[v]
		Cambiox.append(auxX)
		sd = sum(Ymast[v])#Suma los elementos de la fila
		Sumad.append(sd)
		si = sum(Ymenost[v])
		Sumai.append(si)
		auxSuma = (Sumai[v]+Sumad[v])/(len(Ymast[v])+len(Ymenost[v]))#Columnas de que fila
		Sumat.append(auxSuma)
		auxArea = Sumat[v]*Cambiox[v]
		Area.append(auxArea)
	return Area, Xmas, Xmenos
#-------------Funcion que llama a las otras dos-----
def todo(num_arc,dl,picos, rango, n_p):
	prom_t = []
	for i in range(1,num_arc+1):
		if i < 10:
			nom = "0_340_Subt2_0"+str(i)+".txt"
			prom = laser(nom,picos,dl,rango,n_p)
			print("\n")
			prom_t.append(prom)
		else:
			nom = "0_340_Subt2_"+str(i)+".txt"
			print("\n")
			prom = laser(nom,picos,dl,rango,n_p)
			prom_t.append(prom)
	print("\n")
	promedio(num_arc,len(picos),prom_t)
#-----------------------Funcion para separar------------
def separar(cadena):
	separador = ', '
	cad_sep = cadena.split(separador)
	cad_f = []
	for i in range (len(cad_sep)):
		aux = float(cad_sep[i])
		cad_f.append(aux)
	return cad_f
def borrar():
	num_arc.set("")
	dl.set("")
	picos.set("")
	rango.set("")
	
#Interfaz Grafica--------------------------------------------------------
raiz=Tk()
miFrame=Frame(raiz) 
#miFrame.config(background = "blue") #Poner color a la ventana
miFrame.pack()
#Constantes
picos = StringVar()
dl = StringVar()
num_arc = StringVar()
rango = StringVar()
Ajt_poln = StringVar()
picos.set("550.91, 561.289, 568.153, 573.301, 580.701")
rango.set("540, 600")
dl.set("1.5")
num_arc.set("3")
Ajt_poln.set("9")
#Texto---------------------------------------------------------------------
Titulo = Label(miFrame,text = "Proyecto Laser").grid(row = 0)
T_N_arc = Label(miFrame,text = "Inserte el número de archivos:").grid(row = 1)
T_dl = Label(miFrame,text = "Inserte rango de error:").grid(row = 2)
T_Picos = Label(miFrame,text = "Inserte los picos:").grid(row = 3)
T_Rango = Label(miFrame,text = "Inserte Rango:").grid(row=4)
T_Ajus = Label(miFrame,text = "Inserte Ajuste del Polinomio").grid(row=5)
#Pantallas---------------------------------------------------------------------
pt=Entry(miFrame,textvariable=num_arc)
pt.grid(row = 1,column = 1)
pt.config(background = "black",fg = "#03f943",justify = "left")

pt_2 = Entry(miFrame,textvariable=dl)
pt_2.grid(row = 2,column = 1)
pt_2.config(background = "black",fg = "#03f943",justify = "left")

pt_3 = Entry(miFrame,textvariable=picos)
pt_3.grid(row = 3,column = 1)
pt_3.config(background = "black",fg = "#03f943",justify = "left")

pt_3 = Entry(miFrame,textvariable=rango)
pt_3.grid(row = 4,column = 1)
pt_3.config(background = "black",fg = "#03f943",justify = "left")

pt_4 = Entry(miFrame,textvariable = Ajt_poln)
pt_4.grid(row = 5,column = 1)
pt_4.config(background = "black",fg = "#03f943",justify = "left")
#Botones--------------------------------------------------------------------
bt_1 = Button(miFrame,text = "Calcular", width = 6,command=lambda:todo(int(num_arc.get()),float(dl.get()),separar(picos.get()),separar(rango.get()),int(Ajt_poln.get())))
bt_1.grid(row = 6,column = 0)

bt_2 = Button(miFrame,text = "Borrar", width = 6,command=borrar)
bt_2.grid(row = 6,column = 1)

raiz.mainloop()
#------------------------------------------------------------


#picos1 = [541, 544.2, 545.8, 550.1, 558.2]
