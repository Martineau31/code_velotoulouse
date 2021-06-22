les codes decallge_2020.py, decallage_p5.py, decallage_p5_jour.py, decallage_prec.py ont la même fonction. ils permettent de calculer le decallage, degré de ressemblance entre 2019 et 2020 et certain fit les différent signaux.
ils ont cependant pas les même paramètre: 
	decallge_2020.py permet de comparer tout les jour entre eux sans distinction sur une années, c'est a dire chaque jour d'une année est comparer a chaque jour de cette même année
	decallage_p5.py permet de comparer les jour de 2019 et 2020 en vis a vis ( lundi de la semaine 2 2019 avec le lundi de semaine 2 de 2020, etc...)
	decallage_p5.py permet de comparer les semaines de 2019 et 2020 en vis a vis ( semaine 2 2019 avec semaine 2, 2020 etc...)
	decallage_prec.py fonctionne comme le précédent mais découpe la semaine en 3, du lundi au jeudi, le vendredi et le samedi, dimanche. on a donc 3 point par semaine au lieu de 1 précédement
pour faire fonctionné ses code il faut: les deux fichier de log de 2019 et 2020, le fichier calculer des distance entre station, le fichier de position des station
ces scrite retourne: un fichier avec les valeur calculé, les différent tracer des période étudié

le code comp_distribut.py fais les même calcul que les code présenté au dessus mais sur les distribution de vitesse, temps, distance

le code presen_prec.py permet d'affiché les resultat de decallage_prec.py

le code presentation.py permet d'affiché les resultat de decallge_2020.py, decallage_p5.py, decallage_p5_jour.py

le code pres_distribut.py permet d'affiché les resultat de comp_distribut.py

le script distance.py permet de calculer la distance entre chaque station.
il a besoin du fichier des position des station
il retourne un tableau de 289 sur 289 qui représente la distance entre les station. les ligne sont les station de départ, les colones les station d'arriver.

test-fit-distrib.py utilise les donnée calculé par decallge_2020.py, decallage_p5.py, decallage_p5_jour.py, decallage_prec.py pour testé les ajustement de courbe sur ses signaux de fréquentation

test-fit-distrib.py utilise les donnée calculé par  pour testé les ajustement de courbe sur ses signaux de fréquentation


le codes import_export est un ensemble de fonction qui permettent de lire les fichier de log. les fonction sont documenter dans le code grâce a la commande "nom de la fonction.__doc__".
il y a: *lecture_n_n(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='00:00',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',annee='2019')
		renvoye des matrice 289 par 289 par pas de temps entre les dates et heures indiqué des trajet effectué.
	*enregistrement_n_n(fichier_enregistrement,tableau,val)
		Enregistre dans un tableau '.csv' le les tableau de lecture_n_n
	*matrice_n_n(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',annee='2019')
		permet de faire les deux fonction au dessus en même temps
	*matrice_n_n_dif(debut_1='01/01',debut_2='01/01',heure_debut='00:00',fin_1='31/12',fin_2='31/12',heure_fin='23:59',pas=24*60,fichier_lecture_1='TOULOUSE TRAJETS 2019',fichier_lecture_2='TOULOUSE TRAJETS 2019',fichier_enregistrer='test',norme=True)
		permet de faire les deux fonction au dessus en même temps mais en faissant la différence entre la période entré en 1 et la période entré en 2
	*position()
		retourne les position x et y de chaque station
	*distance(fichier='distance_dijkstra')
		détermine la distance entre chaque station, retourne une matrice carré
	*lecture_chro(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_distance='distance_dijkstra',annee='2019')
		permet de renvoyer le traitement statistique des vitesse, distance et temps sur l'interval donnée avec le pas de temps
		renvoie les matrice de distribution de vitesse, temps et distance pour chaque pas de temps		
	*enregistrement_chro(station,parcourt,temps,vitesse,val,fichier_enregistrer='test_distance')
		Enregistre dans un tableau '.csv' le les tableau de lecture_chro
	*depl_chro(debut='01/01',heure_debut='00:00',fin='31/12',heure_fin='23:59',pas=24*60,fichier_lecture='TOULOUSE TRAJETS 2019',fichier_enregistrer='test_distance',fichier_distance='distance_dijkstra',annee='2019')
		permet de faire les deux fonction au dessus en même temps
	*depl_chro_dif(debut_1='01/01',debut_2='01/01',heure_debut='00:00',fin_1='31/12',fin_2='31/12',heure_fin='23:59',pas=24*60,fichier_lecture_1='TOULOUSE TRAJETS 2019',fichier_lecture_2='TOULOUSE TRAJETS 2019',fichier_enregistrer='test_distance',fichier_distance='distance_dijkstra')
		permet de faire les deux fonction au dessus en même temps mais en faissant la différence entre la période entré en 1 et la période entré en 2
	*utilisation_lecture(fichier=['test'])
		permet de lire la matrice d'utilisation du temps en fonction du nombre d'usager
	*depl_crenau_lecture(fichier='test_distance',pas_vitesse=1,pas_distance=100,pas_temps=1,pas_temps_graph=60*24)
		lis la répartition des vitesse,temps et distance sur l'interval moyenner sur un longtemps avec crenau

le code outil_calcul.py apporte des outils qui ont servit dans quasiment tout les code.
	*conv_minute(date,horaire,annee)
		convertie une date en minute depuis le debut de l'année
	*conv_date(minute,annee)
		convertie des minutes en date
	*comparaison_numpy(tabi_1,tabi_2)
		effectue la correlation croisée entre tabi_1 et tabi_2

le code graph_perso est la pour l'affichage des graphique. il est lui aussi composé de fonction différente.
	* utilisation_graph(fichier=['test'])
		prend un matrice de matrice_n_n pour en affiché la fréquentation calculé par se dernier
	*reseau(fichier='test')
		affiche le réseau prétraité par matrice_n_n
	*degree_reseau(fichier='test')
		affiche le degré des point prétraité par matrice_n_n
	* degree_in_out_reseau(fichier='test')
		affiche le degre entrant et sortant de chaque point prétraité par matrice_n_n
	*clustering_reseau(fichier='test')
		affiche le clustering de chaque point prétraité par matrice_n_n
	*centrality_clo_reseau(fichier='test')
		affiche le centrality closeness de chaque point prétraité par matrice_n_n
	*depl_crenau_graph(fichier='test_distance',pas_vitesse=1,pas_distance=100,pas_temps=1,pas_temps_graph=60*24)
		permet de tracer la distribution des vitesse, temps, distance sur l'intervalle pas_temps_graph prétraité par depl_chro
	*freq_graph(fichier='test_distance')
		permet de tracer la vitesse,distance et temps de trajet moyen et leur espérance en fonction du temps\nEn entrer le tableau des distance, temps et vitesse prétraité par depl_chro
	*trajet_vitesse_graph(fichier='test_distance',choix_station=[],trier_anormal=None,trier_normal=None)
		affiche les graphique baton des arriver au station en fonction des vitesse prétraité par depl_chro