import csv

ligne = 0
clefs =[]

class Dico:
    def getData(self):
    
        with open('temperature-quotidienne-departementale.csv', newline='') as csvfile:
            
            reader = csv.reader(csvfile,delimiter=';')
            dico = {}
            for row in reader:
                if ligne == 0:
                    for cle in row:
                        cle = cle.strip('\ufeff')
                        dico[cle]=[]
                        clefs.append(cle)
                else:
                    for i in range(len(row)):
                        dico[clefs[i]].append(row[i])
                ligne +=1
        self.date = dico['Date']
        self.codePostale = dico['Code_INSEE_departement']
        self.nomDepartement = dico['Departement']
        self.tempMin = dico['TMin_(°C)']
        self.tempMax = dico['TMax_(°C)']
        self.tempMoy = dico['TMoy_(°C)']
        self.correctData = []
        self.annee = input('Donne une année')
        self.mois = input('Donne un mois')
        self.jour = input('Donne un jour')
    
    def getCertainDate(self):           #Obtient les valeurs 
        j = 0
        indices = []
        for i in self.date:
            if str(i).startswith(self.annee+'-'+self.mois+'-'+self.jour):
                indices.append(j)
            j += 1
        for indice in indices:
            self.correctData.append(self.codePostale[indice],self.tempMoy[indice])

    

        

    def createDico(self,):           #Créer un nouveau dictionnaire avec les valeurs à utiliser 
        data = self.getCertainDate()
        dicoCorrect = {}
        for cle, valeur in data:
            dicoCorrect[cle] = valeur

