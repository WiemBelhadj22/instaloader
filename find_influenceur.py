#!pip install instaloader
#!pip install instagram-explore

import instaloader
import pandas as pd
from itertools import islice
from math import ceil
from datetime import datetime
from itertools import dropwhile, takewhile
from instaloader import Instaloader, Profile
from instaloader import Instaloader, Profile , Post ,InstaloaderContext
from instaloader import Story , StoryItem , Hashtag, FrozenNodeIterator
import matplotlib.pyplot as plt
import re
import sys
import csv
import os
import pandas as pd
import numpy as np
import json
import latlon as LatLon
from latlon import *
from langdetect import *

#Prétraitement
context=instaloader.InstaloaderContext(sleep=True, quiet=False, user_agent=None, max_connection_attempts=3, request_timeout=300.0, rate_controller=None, fatal_status_codes=None, iphone_support=True)
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
                #finding frensh valid phone number using regex
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
                        else:
                            pass
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
                path=['C:/Users/User/Desktop/orthlane/data_initial/']
                ext=['.csv']
                a=path[0]+mots[0]+ext[0]
                df=pd.DataFrame(liste_1,columns = ['Username','User ID','Picture','Number of posts','Followers','Followees','bio','Location','email','Phone','url externe','isPrivate','isBusiness','BusinessType'])
                
                #Effacer les redendances
                df.drop_duplicates(subset="Username",inplace=True)
                
                #Ajouter une colone de langue et appender les résultats
                df['langue']=''
                from langdetect import detect
                def langue(x):
                    try:
                        lang = detect(x)
                    except:
                        lang = 'Other'
                    return lang
                for i in df.index:
                    a=langue(df['bio'][i])
                    df['langue'][i]=a


                df['Engagement Rate']=0
                df['AVG Likes']=0
                df['AVG Comments']=0
                df['Nomber of Sponsors']=0
                df['AVG Video Viewers']=0
                df['Taux Appartenance Géographique']=0.
                
                #Enregistrement des données initiales
                df.to_csv(a, index=False)

                #Extraction des données liées au postes des profiles trouvés
                for i in df['Username']:
                    user=i
                    users=[]
                    users.append(user)
                    #!curl -k --proxy E1JzH9Wia52-zNyqhbT3hQ@smartproxy.proxycrawl.com:8012 "https://httpbin.org/ip"
                    
                    #Informations de profile
                    _username=profile.username
                    _mediacount=(profile.mediacount)
                    _followers=(profile.followers)
                    _followees=(profile.followees)
                    #Informations de poste
                    posts =profile.get_posts()
                    _postsliste=[]
                    _postsliste=list(posts)
                    nombre_de_postes=len(_postsliste)
                    shortcode=[]
                    for i in _postsliste :
                        a=(str(i)[6:-1])
                        shortcode.append(a)
                    print(shortcode)
                    liste_P=[]
                    for i in (shortcode) :
                        Liste_p=[]
                        Liste_p.append(_username)
                        Liste_p.append(_followers)
                        Liste_p.append(_followees)
                        Liste_p.append(_mediacount)

                        post=Post.from_shortcode(loader.context,i)
                        #Likes
                        likes=post.likes
                        Liste_p.append(likes)
                        #Comments
                        comments=(post.comments)
                        Liste_p.append(comments)
                        #Location
                        distance =''
                        place=''
                        location=post.location
                        print(location)
                        corrd=[]
                        if ((location)==None):
                            distance='Nul'        
                        else:
                            for i in (location) :
                                a=(str(i))
                                corrd.append(a)
                                print(corrd)
                            lat=corrd[-2]
                            lng=corrd[-1]
                            location_name=corrd[1]
                            if ((lat!='')&(lng!='')&(lat!='None')&(lng!='None')):
                                loc_found=LatLon(Latitude(lat), Longitude(lng))
                                ile_de_France = LatLon(Latitude(48.8499), Longitude( 2.6370))   
                                if ((ile_de_France.distance(loc_found))<=50):
                                    distance='In Zone'
                                        
                                else:
                                    distance='Off Zone'
                            if(location_name!=''):
                                place=location_name
                            else:
                                distance='Nul'
                                place='Nul'
                        Liste_p.append(distance)    
                        Liste_p.append(place)
                        #Caption
                        caption=post.caption
                        Liste_p.append(caption)
                        try:
                            print(caption)
                            #Caption langue
                            langue_caption=detect((caption))
                        except :
                            langue_caption = 'undefined'
                        Liste_p.append(langue_caption)
                        print(langue_caption)

                        #Title
                        title=post.title
                        Liste_p.append(title)
                        #URL
                        url=post.url
                        Liste.append(url)
                        #Date
                        date=post.date_local
                        Liste_p.append(date)
                        #Liste des Likes
                        L= post.get_likes()
                        Liste_p.append(L)
                        #Liste des Commentaires
                        C=post.get_comments()
                        Liste_p.append(C)
                        #Tagged users
                        tagged_users=post.tagged_users
                        Liste_p.append(tagged_users)
                        #Sponsorisée
                        sponsored=post.is_sponsored
                        Liste_p.append(sponsored)
                        #The Post’s sponsors
                        sponsor_users=post.sponsor_users
                        Liste_p.append(sponsor_users)
                        #Number of sponsors
                        taille=len(sponsor_users)
                        Liste_p.append(taille)
                        #Video viewers
                        video_view_count=post.video_view_count
                        Liste_p.append(video_view_count)
                        #Engagement Rate
                        engagement_rate=(post.likes/_followers)*100
                        Liste_p.append(engagement_rate)
                        #Ajout dans la liste principale
                        liste_P.append(Liste_p)
                    df_p=pd.DataFrame(liste_P,columns=['user','Followers','Followees','mediacount','Likes','Comments','Distance','place','Caption','langue','Title','URL','Date','Liste des Likes','Liste des Commentaires','Tagged users','Sponsorisée','The Posts sponsors','Number of sponsors','Video viewers','Engagement Rate'])
                    #Création d'un fichier csv pour stocker les données
                    path=['C:/Users/User/Desktop/orthlane/user_post/']
                    ext=['.csv']
                    b=path[0]+users[0]+ext[0]
                    df_p.to_csv(b, index=False)

                    nombre_de_postes=len(_postsliste)

                    #Likes
                    avg_likes=0
                    Likes_total=0
                    for i in df_p['Likes']:
                        Likes_total+=i
                    if(nombre_de_postes!=0):
                        avg_likes=Likes_total/nombre_de_postes
                    df.loc[df['Username']==i, 'AVG Likes'] = avg_likes

                    #Comments
                    avg_comments=0
                    Comments_total=0
                    for i in df_p['Comments']:
                        Comments_total+=i
                    if(nombre_de_postes!=0):
                        avg_comments=Comments_total/nombre_de_postes
                    df.loc[df['Username']==i, 'AVG Comments'] = avg_comments
                    print(avg_comments)
                    #Engagement
                    avg_engagement=0
                    Engagement_total=0
                    for i in df_p['Engagement Rate']:
                        Engagement_total+=i
                    if(nombre_de_postes!=0): 
                        avg_engagement=Engagement_total/nombre_de_postes
                    df.loc[df['Username']==i, 'Engagement Rate'] = avg_engagement
                    print(avg_engagement)
                    

                    #Sponsors
                    Sponsors_total=0
                    for i in df_p['Number of sponsors']:
                        Sponsors_total+=i
                    df.loc[df['Username']==i, 'Nomber of Sponsors'] = Sponsors_total

                    #Video Viewers
                    nombre_video=0
                    video_viewers_total=0
                    avg_video_viewers=0
                    for i in df_p['Video viewers']:
                        try:
                            a=int(i)
                            nombre_video+=1
                            video_viewers_total+=a
                            if(nombre_video!=0): 
                                avg_video_viewers=video_viewers_total/nombre_video
                            df.loc[df['Username']==i,'AVG Video Viewers'] = avg_video_viewers
                        except:
                            pass 

                    
                    
                    #Appartenance géographique
                    nombre_distance_existante=0
                    nombre_distance_cible=0
                    Taux_appartenance=0
                    for i in df_p['Distance']:
                        if (i!='Nul'):
                            nombre_distance_existante+=1
                            if(i=='In Zone'):
                                nombre_distance_cible+=1
                    if(nombre_distance_existante!=0):
                        Taux_appartenance=nombre_distance_cible/nombre_distance_existante
                    df.loc[df['Username']==i,'Taux Appartenance Géographique'] = Taux_appartenance
                
                #Choisir le path
                path=['C:/Users/User/Desktop/orthlane/data_final/']
                ext=['.csv']
                c=path[0]+mots[0]+ext[0]
                df.to_csv(c, index=False)

            except :
                pass

#Exécuter la fonction
influenceur_instagram(mot)

#Concatenation des fichiers de postes
user_post_file_folder = ('C:/Users/User/Desktop/orthlane/user_post')
df = []
for file in os.listdir(user_post_file_folder):
    if file.endswith('.csv'):
        print('Loading file {0}...'.format(file))
        df.append(pd.read_csv(os.path.join(user_post_file_folder, file)))
        
df_master = pd.concat(df, axis=0)
df_master.to_csv(r'C:\Users\User\Desktop\orthlane\user_post\final_data_user.csv', index=False)

#Concatenation des fichiers finaux 
data_final_file_folder = ('C:/Users/User/Desktop/orthlane/data_final')
df = []
for file in os.listdir(data_final_file_folder):
    if file.endswith('.csv'):
        print('Loading file {0}...'.format(file))
        df.append(pd.read_csv(os.path.join(data_final_file_folder, file)))
        
df_master = pd.concat(df, axis=0)
df_master.to_csv(r'C:\Users\User\Desktop\orthlane\data_final\final_data.csv', index=False)