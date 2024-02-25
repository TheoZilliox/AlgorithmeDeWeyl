import math
import matplotlib.pyplot as plt
import numpy as np

#Partie 2 : Complexes et polynômes en Python

#Q1) Addition et multiplication de complexes

def Addition(z1, z2):
    a1, b1 = z1 #Extraction des valeurs des couples
    a2, b2 = z2

    resultat = (a1+a2, b1+b2)
    return resultat

def Multiplication(z1, z2):
    a1, b1 = z1 #Extraction des valeurs des couples
    a2, b2 = z2

    resultat = (a1*a2-b1*b2, a1*b2+b1*a2)
    return resultat

#Q2) Complexe à la puissance n

def Puissance(z, n):
    a, b = z
    resultat = (1, 0)
    #On commence par l'élement neutre pour la mutliplication, 1
    
    for _ in range(n):
        resultat = (
            resultat[0] * a - resultat[1] * b,
            resultat[0] * b + resultat[1] * a)
    # On multiplie le resultat (initialement égal à 1, puis celui obtenu) par z

    return resultat

#Q3) Module d'un nombre complexe

def Module(z):
    a, b = z
    module = (a **2 + b ** 2) ** 0.5
    return module

#Q4) Evaluation d'un polynôme en z

def Eval(P, z):
    #P = [5,1,2] -> 2x^2 + 1x + 5
    longueur = len(P)   
    resultat = (0, 0)
    #On commence par l'élement neutre pour l'addition, 0

    for i in range(longueur):
        MonomeSansCoeff = Puissance(z, i)
        a, b = MonomeSansCoeff
        Monome = (a*P[i] ,b *P[i])
        resultat = Addition(resultat, Monome)
    
    return resultat

#Q5) Dérivée n-ième de P

def deriv(P, n):
    longueur = len(P)
    DériP = [0] * longueur 
    if n == 0:
        return P    
    if n >= len(P):
        return DériP   
    else :
        for i in range(0 , len(P)-n):
            DériP[i] = (P[i+n]*math.factorial(i+n))/math.factorial(i)
        for i in range(len(P)-n+1 ,len(P)):
            DériP[i] = 0
        return DériP
    
#Partie 3 : Algorithme 
#Utilisons les méthodes établies dans la partie 2 pour réaliser l'aglorithme
#de Weil, et trouver les racines complexes de polynomes.

#Q1) Test de l'inégalité (1), pour un polynome P, un complexe z et un réel r

def Test(P, r, z):
    longueur = len(P)   
    Somme = 0
    for i in range(1 ,longueur):
        Pdéri = deriv(P, i)
        PdériEvalué = Eval(Pdéri, z)
        RePdériEvalué , ImPdériEvalué = PdériEvalué
        Module = (RePdériEvalué**2 + ImPdériEvalué**2)**0.5
        x = Module*(r**i)/math.factorial(i)
        Somme = Somme + x
    Pz1 = Eval(P, z)
    RePz1, ImPz1 = Pz1
    NormePz1 = (RePz1**2 + ImPz1**2)**0.5
    if NormePz1 > Somme :
        #print("Pas de racine dans le disque de centre z et de rayon r")
        return 0
    else :
        #print("Il y a peut être une racine")
        return 1
    
#Q2) Test de l'inégalité (1) sur quatre sous-carrés pour ne garder que les non-exclus

def TestCarres(P,c,a):
    ReC, ImC = c
    ListeDesCarrés = []
    Point0 = (ReC - a/4 , ImC + a/4)
    Point1 = (ReC + a/4 , ImC + a/4)
    Point2 = (ReC - a/4 , ImC - a/4)
    Point3 = (ReC + a/4 , ImC - a/4)
    r = (2**0.5)*a/4
    
    if Test(P, r, Point0):
        ListeDesCarrés.append([Point0 ,a/2])
        
    if Test(P, r, Point1):
        ListeDesCarrés.append([Point1 ,a/2])
        
    if Test(P, r, Point2):
        ListeDesCarrés.append([Point2 ,a/2])
        
    if Test(P, r, Point3):
        ListeDesCarrés.append([Point3 ,a/2])
    
    return ListeDesCarrés

#Q3) Algorithme de Weyl : n étapes de découpage pour renvoyer 
#la liste des petits carrés restant à la fin 

def Weyl(P,n):
    Amax = abs(max ((P[:-1]), key=abs))
    An = abs(P[len(P)-1])
    r = (1+Amax/An)
    coté = 2*r
    if Test(P, r , (0,0)) == 0:
        print("Pas de racines !")
        return 0
    else : 
        L = TestCarres(P,(0,0) ,coté) 
        M=[]
        for i in range(0, n-1):
            for j in range(len(L)):
                Carréj = L[j]
                CentreCarréj = Carréj[0]
                CotéCarréj = Carréj[1]
                K = TestCarres(P,CentreCarréj,CotéCarréj)
                for k in range(len(K)):
                    M.append(K[k])
            L = M
            M = []
        return L
        
#Q4) Représentation du carré de centre c (nombre complexe) et de coté a, à l'aide
# de la bibliotheque matplotlib.pyplot

def Carre(c, a):
        ReC, ImC = c
        CoinsCarrés = np.array([
            [ReC - a/2, ImC - a/2],
            [ReC + a/2, ImC - a/2],
            [ReC + a/2, ImC + a/2],
            [ReC - a/2, ImC + a/2],
            [ReC - a/2, ImC - a/2] ])
        plt.plot(CoinsCarrés[:, 0], CoinsCarrés[:, 1], 'g-') 
        #Le "g-" indique la couleur et
        #que l'on souhaite utiliser un trait rempli pour le contour
        plt.axis('equal')  
        plt.title('Carré de Centre {} et Côté {}'.format(c, a))
        plt.xlabel('Axe Réel')
        plt.ylabel('Axe Imaginaire')
        plt.grid(True)
        plt.show()
            
#Q5) Visualisation du fonctionnement de l'algorithme de Weyl

def CarreWeyl(P, n):
        Amax = abs(max ((P[:-1]), key=abs))
        An = abs(P[len(P)-1])
        r = (1+Amax/An)
        coté = 2*r
        L =  Weyl(P,n)
        
        for i in range(len(L)):
            Carréi = L[i]
            Xcentre, Ycentre = Carréi[0]
            l = Carréi[1]/2
            CoinsCarrés = [
                (Xcentre - l, Ycentre - l),
                (Xcentre + l, Ycentre - l),
                (Xcentre + l, Ycentre + l),
                (Xcentre - l, Ycentre + l),
                (Xcentre - l, Ycentre - l)
                ]
            CooX = [point[0] for point in CoinsCarrés]  
            CooY = [point[1] for point in CoinsCarrés]
            plt.fill(CooX, CooY, 'red' ,0.5)
        Carre((0,0), coté)
              
def FilmWeyl(P,n):
    for i in range(n):
        CarreWeyl(P, i)
        plt.pause(0.1)
