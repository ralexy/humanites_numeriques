from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import json
import requests
import locale
import datetime


bp = Blueprint('recherche', __name__)

########### VARIABLES A MODIFIER ###########
url = "http://localhost:8984/rest/Nuremberg"
headers = {'Authorization': 'Basic YWRtaW46YWRtaW4='}
############################################



def regexify(mot):

    liste = mot

    for index, car in enumerate(mot):
        new_mot = mot[:index]+"."+mot[index+1:]
        liste += "|" + new_mot
    
    return liste

def checkForAliases(intervenant):
    
    f = open("C:\\Users\\manil\\Humanités numériques - Moteur de recherche\\flaskr\\levenstein\\intervenants.json", encoding="utf8")

    data = json.load(f)

    liste_intervenants = intervenant

    for num in data:
        if intervenant in data[num]["représentant"]["nom"]:
            for alias in data[num]["alias"]:
                liste_intervenants += "|" + alias["nom"][:-1]


    f.close()

    return liste_intervenants
        
def inputExists(inputName) :
    return inputName in request.form.keys()

def getFormValue(key) :
    if(inputExists(key)) :
        return request.form[key]
    
    return ""

@bp.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        propos = getFormValue('propos')
        intervenant = getFormValue('monIntervenant')
        check_propos = getFormValue('exactTerm')
        check_intervenant = getFormValue('exactIntervenant')
        startDate = getFormValue('startDate')
        endDate = getFormValue('endDate')

        print(" check box :", check_propos)

        

        if startDate != "":
            print(startDate)
            
            from datetime import datetime

            dateFormatter = "%Y-%m-%d"
            d = datetime.strptime(startDate, dateFormatter)
            print(d.strftime("%d %B %Y"))

        if 'on' in check_propos: #recherche précise du propos

            if intervenant == "":
                query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$paragraphes%20:=%20$i//*:text//*:p%20for%20$paragraphe%20in%20$paragraphes%20where(matches($paragraphe,%20'"+ propos +"',%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$paragraphe/../..//*:head/text()}</audience>%20<intervenant>{$paragraphe/..//*:speaker/text()}</intervenant>%20<texte>{$paragraphe/text()}</texte>%20</instance>}%20</query>&method=json&json=format=jsonml"
            else:
                if 'on' in check_intervenant: #recherche précise de l'intervenant
                    query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$terme%20:=%20'"+ propos +"'%20let%20$terme_intervenant%20:=%20'" + intervenant +"'%20let%20$sp%20:=%20$i//*:sp%20let%20$intervenants%20:=%20$sp//*:speaker%20for%20$intervenant%20in%20$intervenants%20where(matches($intervenant,%20$terme_intervenant,%20'i'))%20let%20$interventions%20:=%20$intervenant/../*:p%20for%20$intervention%20in%20$interventions%20where(matches($intervention,%20$terme,%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$intervention/../..//*:head/text()}</audience>%20<intervenant>{$intervenant//text()}</intervenant>%20<texte>{$intervention/text()}</texte>%20</instance>%20}</query>&method=json&json=format=jsonml"

                else: #recherche étendue de l'intervenant

                    liste_intervenants = checkForAliases(intervenant)
                    print(liste_intervenants)

                    query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$terme%20:=%20'"+ propos +"'%20let%20$terme_intervenant%20:=%20'" + liste_intervenants +"'%20let%20$sp%20:=%20$i//*:sp%20let%20$intervenants%20:=%20$sp//*:speaker%20for%20$intervenant%20in%20$intervenants%20where(matches($intervenant,%20$terme_intervenant,%20'i'))%20let%20$interventions%20:=%20$intervenant/../*:p%20for%20$intervention%20in%20$interventions%20where(matches($intervention,%20$terme,%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$intervention/../..//*:head/text()}</audience>%20<intervenant>{$intervenant//text()}</intervenant>%20<texte>{$intervention/text()}</texte>%20</instance>%20}</query>&method=json&json=format=jsonml"



        else:#recherche étendue du propos

            liste_propos = regexify(propos)
            print(liste_propos)

            if intervenant == "":
                query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$paragraphes%20:=%20$i//*:text//*:p%20for%20$paragraphe%20in%20$paragraphes%20where(matches($paragraphe,%20'"+ liste_propos +"',%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$paragraphe/../..//*:head/text()}</audience>%20<intervenant>{$paragraphe/..//*:speaker/text()}</intervenant>%20<texte>{$paragraphe/text()}</texte>%20</instance>}%20</query>&method=json&json=format=jsonml"
            else:
                if 'on' in check_intervenant:#recherche précise de l'intervenant
                    query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$terme%20:=%20'"+ liste_propos +"'%20let%20$terme_intervenant%20:=%20'" + intervenant +"'%20let%20$sp%20:=%20$i//*:sp%20let%20$intervenants%20:=%20$sp//*:speaker%20for%20$intervenant%20in%20$intervenants%20where(matches($intervenant,%20$terme_intervenant,%20'i'))%20let%20$interventions%20:=%20$intervenant/../*:p%20for%20$intervention%20in%20$interventions%20where(matches($intervention,%20$terme,%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$intervention/../..//*:head/text()}</audience>%20<intervenant>{$intervenant//text()}</intervenant>%20<texte>{$intervention/text()}</texte>%20</instance>%20}</query>&method=json&json=format=jsonml"
                
                else:#recherche étendue de l'intervenant

                    print(" mon intervenant :",len(intervenant))

                    liste_intervenants = checkForAliases(intervenant)
                    print(liste_intervenants)

                    query = "query=<query>{%20for%20$i%20in%20//*:TEI%20let%20$terme%20:=%20'"+ liste_propos +"'%20let%20$terme_intervenant%20:=%20'" + liste_intervenants +"'%20let%20$sp%20:=%20$i//*:sp%20let%20$intervenants%20:=%20$sp//*:speaker%20for%20$intervenant%20in%20$intervenants%20where(matches($intervenant,%20$terme_intervenant,%20'i'))%20let%20$interventions%20:=%20$intervenant/../*:p%20for%20$intervention%20in%20$interventions%20where(matches($intervention,%20$terme,%20'i'))%20return%20<instance>%20<date>{($i//*:head)[1]/text()}</date>%20<audience>{$intervention/../..//*:head/text()}</audience>%20<intervenant>{$intervenant//text()}</intervenant>%20<texte>{$intervention/text()}</texte>%20</instance>%20}</query>&method=json&json=format=jsonml"

        error = None

        if propos is None:
            error = 'Veuillez entrer un terme'

        try:
            print(url + "?" + query)
            r = requests.get(url + "?" + query, headers=headers)
            r = json.loads(r.text)
        
        except requests.Timeout as err:
            print({"Pas de réponse ": err.message})
            exit()
        except requests.RequestException as err:
            print({"Erreur requête :": err.message})
            exit() 
    
        flash(error)
        return render_template('index.html', msg=r, length=len(r), intervenant=intervenant)

    if request.method == "GET" :

        r=""    
        return render_template('index.html', msg=r, length=len(r), intervenant="")


    