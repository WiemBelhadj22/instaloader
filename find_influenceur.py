import instaloader
import pandas as pd
from itertools import islice
from math import ceil
from datetime import datetime
from itertools import dropwhile, takewhile
from instaloader import Instaloader, Profile
import matplotlib.pyplot as plt
import re
import sys
loader = instaloader.Instaloader()

#Connexion
NOM=sys.argv[1]
MDP=sys.argv[2]
loader.login(NOM,passwd=MDP)

#Mot clé à chercher
mot=sys.argv[3]

#Fonction
def influenceur_instagram(key) :
    mot=key
    #Ajouter le mot choisi dans une liste
    mots=[]
    mots.append(mot)
    
    #Extraction des profiles liés au mots clés 
    profil_mots={}
    for i in (mots):
        s=instaloader.TopSearchResults(loader.context,i).get_profiles()
        l=[profile.username for profile in s]
        profil_mots[i]=l

    #Extraction des informations liés au profile
    for valeur in profil_mots.values()  :
        liste_1=[]
        for k in valeur :
            try:
                profile = instaloader.Profile.from_username(loader.context,k)
                _followers=(profile.followers)
                _username=profile.username
                _userid=(profile.userid)
                _profile_pic=(profile.profile_pic_url)
                _mediacount=(profile.mediacount)
                _followees=(profile.followees)
                _biography=(profile.biography)
                _external_url=(profile.external_url)
                _private=(profile.is_private)
                _business_account=(profile.is_business_account)
                _business_category_name=(profile.business_category_name)
                #finding all valid emails using regex
                email = re.findall(r"[A-Za-z0-9_%+-.]+"
                                r"@[A-Za-z0-9.-]+"
                                r"\.[A-Za-z]{2,5}",_biography,flags=re.IGNORECASE)
                
                phone_pattern = re.compile(r'((?:\+\d{2}[-.\s]?(?:\(0\)|0)*?[-.\s]?|00[-.\s]?\d{2}[-.\s]?(?:\(0\)|0)*?[-.\s]?|0)\d?[-.\s]?(?:\d{2}[-.\s]?){3,4})(?:$|\D)')
                phone = re.findall(phone_pattern,_biography)

                #localisation 
                Localisations = ['parisian','France', 'france', 'française', 'Française', 'French','Île-de-France','Cannes','cannes' ,'Paris', 'paris', 'Lyon', 'lyon','Brussels','Nantes', 'bruxelles', 'Marseille', 'marseille', 'Nice', 'nice', 'Toulouse', 'toulouse', 'Bordeaux', 'bordeaux', 'Caen', 'caen', 'Lille', 'lille']
                liste_de_chaine = [] #split la chaine en mots
                loc_cherchée = " " #final
                _localisation = []
                liste_de_chaine = _biography.split()
                for e in liste_de_chaine:
                    for k in Localisations:
                        if (e == k):
                            loc_cherchée = e
                            _localisation.append(loc_cherchée)
                if (loc_cherchée == " "):
                    _localisation.append(" ")
                loc_cherchée = " "
                
                if (_followers>=3000):
                    Liste=[]
                    Liste.append(_username)
                    Liste.append(_userid)
                    Liste.append(_profile_pic)
                    Liste.append(_mediacount)
                    Liste.append(_followers) 
                    Liste.append(_followees)
                    Liste.append(_biography)
                    Liste.append(_localisation)
                    Liste.append(email)
                    Liste.append(phone)
                    Liste.append(_external_url)
                    Liste.append(_private)
                    Liste.append(_business_account)
                    Liste.append(_business_category_name)
                    liste_1.append(Liste)
                else:
                    pass
                #Création d'un fichier csv pour stocker les données
                #Choisir le path
                path=['C:/Users/User/Desktop/orthlane/data_final/']
                ext=['.csv']
                a=path[0]+mots[0]+ext[0]
                df=pd.DataFrame(liste_1,columns = ['Username','User ID','Picture','Number of posts','Followers','Followees','bio','Location','email','Phone','url externe','isPrivate','isBusiness','BusinessType'])
                df.to_csv(a, index=False)
            except :
                pass

#Exécuter la fonction
influenceur_instagram(mot)