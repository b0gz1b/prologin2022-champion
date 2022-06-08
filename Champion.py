from api import *
import math, random

nids = []
papys = []
trous = []
objo = []
hist = []
cptNids = []
tony = [False]
# Fonction appelée au début de la partie.
def partie_init():
    for i in range(HAUTEUR):
        for j in range(LARGEUR):
            tc = info_case((i, j, 0)).contenu
            if tc == type_case.PAPY:
                papys.append((i,j,0))
            elif tc == type_case.NID:
                nids.append((i,j,0))
            elif tc == type_case.TROU:
                trous.append((i, j, 0))

    for num_troupe in range(NB_TROUPES):
        objo.append(math.inf)


# Fonction appelée à chaque tour.
def jouer_tour():
    # La stratégie tourne autour de plusieurs axes: Bloquer l'ennemi, lui laisser faire un travail pénible de creusage
    # (quoique gratuit), avoir des nids, stacker les miches et éventuellement gagner mais ça bof.
    # Pour les nids on envoie chaque troupe au plus proche, on aurait pu optimiser j'ai essayé assez longtemps
    # Pour l'aggrandissment on le fait si on est à distance d'un objo autrement dit on accelera
    # Pour le pain on prend les miches à plus forte rentabilité gain/cases à parcourir
    # Pour le retour au nid c'est si on a un inventaire plein

    # hist.append(historique())
    tms = troupes_joueur(moi())
    tas = troupes_joueur(adversaire())
    # On gère chaque troupe selon le même algo
    for num_troupe in range(NB_TROUPES):
        # Il faut qu'lle puisse se déplacer
        if troupes_joueur(moi())[num_troupe].pts_action > 0:
            toNids = []
            # print("Calcul des distances de",troupes_joueur(moi())[num_troupe].id,"aux nids")
            for nid in nids:
                if info_nid(nid) == 0:
                    toNid = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, nid)
                    if len(toNid) > 0:
                        toNids.append((len(toNid), toNid))
            if toNids != []:
                toNids = sorted(toNids)
                d,shortestNid = toNids[0]
                # print("Le nid le plus proche de", troupes_joueur(moi())[num_troupe].id, "est à",d,"cases en empruntant",shortestNid)
                i = 0

                while troupes_joueur(moi())[num_troupe].pts_action > 0 and (len(cptNids) < min(math.ceil(len(nids)/4),2)):
                    if i == d:
                        # print("La troupe",troupes_joueur(moi())[num_troupe].id,"est arrivée au nid")
                        cptNids.append(troupes_joueur(moi())[num_troupe].maman)
                        toNids == []
                        for nid in nids:
                            if info_nid(nid) == etat_nid.LIBRE:
                                toNid = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, nid)
                                if len(toNid) > 0:
                                    toNids.append((len(toNid), toNid))
                        if toNids == []:
                            # print("Plus de nid libre !")
                            break
                        else:
                            toNids = sorted(toNids)
                            d, shortestNid = toNids[0]
                            i = 0
                            # print("Le nid le plus proche de", troupes_joueur(moi())[num_troupe].id, "est à", d, "cases en empruntant", shortestNid)
                            continue
                    if toNids == []:
                        break
                    # print("La troupe",troupes_joueur(moi())[num_troupe].id,"avance depuis",troupes_joueur(moi())[num_troupe].maman,"vers",shortestNid[i])
                    er = avancer(troupes_joueur(moi())[num_troupe].id, shortestNid[i])
                    # if er == erreur.OK:
                    #     # print("Déplacement réussi il reste",troupes_joueur(moi())[num_troupe].pts_action,"points d'action")
                    # else:
                    #     # print("Oh nyoo")
                    #     # print(er)
                    i += 1
            goPapy = False
            while grandir(troupes_joueur(moi())[num_troupe].id) == erreur.OK and objo[num_troupe] > PTS_ACTION:
                pass
                # print("Troupe",troupes_joueur(moi())[num_troupe].id,"grandit, il reste",troupes_joueur(moi())[num_troupe].pts_action,"points d'action")
            # print("Troupe", troupes_joueur(moi())[num_troupe].id, "ne peux plus grandir")
            prev = math.inf
            while troupes_joueur(moi())[num_troupe].pts_action > 0 and troupes_joueur(moi())[num_troupe].pts_action < prev :
                prev = troupes_joueur(moi())[num_troupe].pts_action
                toPains = []
                # print("Calcul des interêt de", troupes_joueur(moi())[num_troupe].id, "aux pains")
                p = sorted([(info_case(pain).nb_pains, pain) for pain in pains() if all([pain not in t.canards for t in troupes_joueur(moi())]) and all([pain not in t.canards for t in troupes_joueur(adversaire())])], reverse=True)
                for pain in p:
                    toPain = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, pain[1])
                    if len(toPain) > 0:
                        toPains.append((pain[0]/len(toPain), toPain))
                if toPains == []:
                    # print("Pas de pain")
                    goPapy = True # Go faire les papys
                else:
                    _,nicePain = toPains[0]
                    d = len(nicePain)
                    objo[num_troupe] = d
                    i = 0
                    # print("Le pain le plus intéressant pour", troupes_joueur(moi())[num_troupe].id, "est à", d, "cases en empruntant", nicePain)
                    while troupes_joueur(moi())[num_troupe].pts_action > 0 and troupes_joueur(moi())[num_troupe].inventaire < troupes_joueur(moi())[num_troupe].taille // 3 and not tony[0]:

                        if i == d:
                            # print("La troupe", troupes_joueur(moi())[num_troupe].id, "est arrivée au pain")
                            p = sorted([(info_case(pain).nb_pains, pain) for pain in pains() if all([pain not in t.canards for t in troupes_joueur(moi())]) and all([pain not in t.canards for t in troupes_joueur(adversaire())])], reverse=True)
                            for pain in p:
                                toPain = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, pain[1])
                                if len(toPain) > 0:
                                    toPains.append((pain[0] / len(toPain), toPain))
                            if toPains == []:
                                # print("Plus de pain !")
                                goPapy = True
                                break
                            else:
                                toPains = sorted(toPains,reverse=True)
                                _, nicePain = toPains[0]
                                d = len(nicePain)
                                objo[num_troupe] = d
                                i = 0
                                # print("Le pain le plus intéressant pour", troupes_joueur(moi())[num_troupe].id, "est à", d, "cases en empruntant", nicePain)
                                continue
                        if toPains == []:
                            break
                        # print("La troupe", troupes_joueur(moi())[num_troupe].id, "avance depuis", troupes_joueur(moi())[num_troupe].maman, "vers", nicePain[i])
                        er = avancer(troupes_joueur(moi())[num_troupe].id, nicePain[i])
                        # if er == erreur.OK:
                        #     # print("Déplacement réussi il reste",troupes_joueur(moi())[num_troupe].pts_action,"points d'action")
                        # else:
                        #     # print("Oh nyoo")
                        #     # print(er)
                        i += 1
                        objo[num_troupe] = d - i
                if troupes_joueur(moi())[num_troupe].pts_action > 0 and (not goPapy or tony[0]):

                    tony[0]=True
                    toNids = []
                    # print("Calcul des distances de", troupes_joueur(moi())[num_troupe].id, "aux nids alliés")
                    for nid in nids:
                        if (info_nid(nid) == etat_nid.JOUEUR_0 and moi() == 0) or (info_nid(nid) == etat_nid.JOUEUR_1 and moi() == 1):
                            toNid = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, nid)
                            if len(toNid) > 0:
                                toNids.append((len(toNid), toNid))
                    if toNids != []:
                        toNids = sorted(toNids)
                        d, shortestNid = toNids[0]
                        objo[num_troupe] = d
                        # print("Le nid allié le plus proche de", troupes_joueur(moi())[num_troupe].id, "est à", d,"cases en empruntant", shortestNid)
                        i = 0
                        while troupes_joueur(moi())[num_troupe].pts_action > 0 and i != d:
                            pass
                            # print("La troupe", troupes_joueur(moi())[num_troupe].id, "avance depuis",troupes_joueur(moi())[num_troupe].maman, "vers", shortestNid[i])
                            er = avancer(troupes_joueur(moi())[num_troupe].id, shortestNid[i])
                            # if er == erreur.OK:
                            #     # print("Déplacement réussi il reste", troupes_joueur(moi())[num_troupe].pts_action,"points d'action")
                            # else:
                            #     # print("Oh nyoo")
                            #     # print(er)
                            i += 1
                            objo[num_troupe] = d - i
                        if i==d:
                            tony[0] = False
                    gobuissonmode(nids)

                if troupes_joueur(moi())[num_troupe].pts_action > 0:
                    goPapy = False
                    toPapys = []
                    # print("Calcul des distances de", troupes_joueur(moi())[num_troupe].id, "aux papys qui khalass")
                    for papy in papys:
                            toPapy = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, papy)
                            if len(toPapy) > 0:
                                toPapys.append((len(toPapy)+max(0,len(toPapy)-papy_tours_restants(papy)), toPapy))
                    print(toPapys,papys)
                    if toPapys != []:
                        toPapys = sorted(toPapys)
                        _, shortestPapy = toPapys[0]
                        d = len(shortestPapy)
                        objo[num_troupe] = d
                        # print("Le papy le plus proche de", troupes_joueur(moi())[num_troupe].id, "est à", d,"cases en empruntant", shortestPapy)
                        i = 0
                        while troupes_joueur(moi())[num_troupe].pts_action > 0:
                            if i == d:
                                # print("La troupe", troupes_joueur(moi())[num_troupe].id, "est arrivée au papy")
                                toPapys == []
                                for papy in papys:
                                    toPapy = trouver_chemin(troupes_joueur(moi())[num_troupe].maman, papy)
                                    if len(toPapy) > 0 and len(toPapy) - papy_tours_restants(papy) >= 0:
                                        toPapys.append((len(toPapy)+max(0,len(toPapy) - papy_tours_restants(papy)), toPapy))
                                if toPapys == []:
                                    # print("Plus de papy :/ !")
                                    break
                                else:
                                    toPapys = sorted(toPapys)
                                    _, shortestPapy = toPapys[0]
                                    d = len(shortestPapy)
                                    objo[num_troupe] = d
                                    i = 0
                                    # print("Le papy le plus intéressant pour", troupes_joueur(moi())[num_troupe].id,"est à", d, "cases en empruntant", shortestPapy)
                                    continue
                            if toPapys == []:
                                break
                            er = avancer(troupes_joueur(moi())[num_troupe].id, shortestPapy[i])
                            # if er == erreur.OK:
                            #     # print("Déplacement réussi il reste", troupes_joueur(moi())[num_troupe].pts_action,
                            #           "points d'action")
                            # else:
                            #     # print("Oh nyoo")
                            #     # print(er)
                            i += 1
                            objo[num_troupe] = d - i
                    else:
                        break
            c = []
            while troupes_joueur(moi())[num_troupe].pts_action > 0:
                while len(c) == 0:
                    c = trouver_chemin(troupes_joueur(moi())[num_troupe].maman,(random.randint(0,HAUTEUR-1),random.randint(0,LARGEUR-1),troupes_joueur(moi())[num_troupe].maman[2]))
                for d in c:
                    if avancer(troupes_joueur(moi())[num_troupe].id,d) == erreur.MOUVEMENTS_INSUFFISANTS:
                        break



def gobuissonmode(nids):
    if score(moi()) > COUT_BUISSON:
        for nid in nids:
            if (info_nid(nid) == etat_nid.JOUEUR_1 and moi() == 0) or (info_nid(nid) == etat_nid.JOUEUR_0 and moi() == 1):
                x,y,l = nid
                # print("Enfermons", nid,"!")
                if construire_buisson((x + 1, y, l)) != erreur.SCORE_INSUFFISANT:
                    if construire_buisson((x - 1, y, l)) != erreur.SCORE_INSUFFISANT:
                        if construire_buisson((x, y + 1, l)) != erreur.SCORE_INSUFFISANT:
                            if construire_buisson((x, y - 1, l)) != erreur.SCORE_INSUFFISANT:
                                continue
                break
        for num_troupe in range(len(troupes_joueur(adversaire()))):
            x,y,l = troupes_joueur(adversaire())[num_troupe].maman
            # print("Enfermons", troupes_joueur(adversaire())[num_troupe].maman, "!")
            if construire_buisson((x + 1, y, l)) != erreur.SCORE_INSUFFISANT:
                if construire_buisson((x - 1, y, l)) != erreur.SCORE_INSUFFISANT:
                    if construire_buisson((x, y + 1, l)) != erreur.SCORE_INSUFFISANT:
                        if construire_buisson((x, y - 1, l)) != erreur.SCORE_INSUFFISANT:
                            continue
            break


# def trouver_meilleur_chemin(start,end):
#     tc = trouver_chemin(start,end)
#     cout = lambda p

# Fonction appelée à la fin de la partie.
def partie_fin():
    pass
