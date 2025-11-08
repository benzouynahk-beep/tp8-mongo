
#1. Créer les collections : produits, clients et commandes dans une base de données ecommerceDB.
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")  
db = client.ecommerceDB
produits_col = db.produits
clients_col = db.clients
commandes_col = db.commandes
print("connecter avec succes")
from datetime import datetime

def creer_commande():
    nom_client = input("Nom du client: ")
    client = clients_col.find_one({"nom": nom_client})
    if not client:
        print("Client non trouve")
        return

    nom_produit = input("Nom du produit: ")
    produit = produits_col.find_one({"nom": nom_produit})
    if not produit:
        print("Produit non trouve")
        return

    quantite = int(input("Quantite: "))
    total = produit["prix"] * quantite

    commande = {
        "client_id": client["_id"],
        "produits": [{"produit_id": produit["_id"], "nom": produit["nom"], "quantite": quantite, "prix": produit["prix"]}],
        "date_commande": datetime.now(),
        "statut": "en cours",
        "montant_total": total
    }

    commandes_col.insert_one(commande)
    print("Commande creer")
creer_commande()

#2. Affichez tous les produits de la collection produits.
def afficher_produits():
    produits = produits_col.find()  
    for p in produits:
        print(f"Nom: {p['nom']}, Categorie: {p['categorie']}, Prix: {p['prix']}, Stock: {p['stock']}")
afficher_produits()

#3. Recherchez toutes les commandes d’un client spécifique (saisi par l’utilisateur).
def commandes_par_client():
    nom = input("Nom du client: ")
    client = clients_col.find_one({"nom": nom})
    
    if not client:
        print("Client pas trouve")
        return
    
    for cmd in commandes_col.find({"client_id": client["_id"]}):
        print(f"{cmd['date_commande']} - {cmd['statut']} - Total: {cmd['montant_total']}")
        for p in cmd['produits']:
            print(f"  {p['nom']} ")
commandes_par_client()
#4. Recherchez les commandes  ayant le statut : livrée.
def commandes_livrees():
    commandes = commandes_col.find({"statut": "livre"})
    for c in commandes:
        client_doc = clients_col.find_one({"_id": c["client_id"]})
        print(f"Client ayant le statut  livree: {client_doc['nom']}, Date: {c['date_commande']}, Total: {c['montant_total']}")
        for p in c['produits']:
            print(f"  - {p['nom']}")
commandes_livrees()

#5. Mettez à jour un produit choisi par son nom.
def mise_a_jour_produit():
    nom = input("Entrez le nom du produit a modifier: ")
    produit = produits_col.find_one({"nom": nom})
    
    if not produit:
        print("Produit non trouve")
        return
    
    nouveau_prix = float(input(f"Entrez le nouveau prix pour {nom} (actuel: {produit['prix']}): "))
    nouveau_stock = int(input(f"Entrez le nouveau stock pour {nom} (actuel: {produit['stock']}): "))
    
    produits_col.update_one(
        {"_id": produit["_id"]},
        {"$set": {"prix": nouveau_prix, "stock": nouveau_stock}}
    )
    
    print(f"Produit {nom} mis a jour avec succes.")

#6. Ajoutez un nouveau champ disponible pour tous les produits ayant une valeur par défaut true.
def ajouter_champ_disponible():
    result = produits_col.update_many(
        {},{"$set": {"disponible": True}}
    )
ajouter_champ_disponible()
    
#7. Supprimez une commande en fonction du produit et du client.
def supprimer_commande():
    nom_client = input("Entrez le nom du client: ")
    nom_produit = input("Entrez le nom du produit: ")

    client = clients_col.find_one({"nom": nom_client})
    if not client:
        print("Client non trouve")
        return

    result = commandes_col.delete_one({
        "client_id": client["_id"],
        "produits.nom": nom_produit
    })

    if result.deleted_count > 0:
        print("Commande supprimee avec succes ")
    else:
        print("Aucune commande trouvee avec ce client et ce produit ")
supprimer_commande()
#8. Supprimez tous les commandes d’un client donné.
def supprimer_commandes_client():
    nom_client = input("Nom du client: ")  
    client = clients_col.find_one({"nom": nom_client})
    if not client:
        print("Client non trouve")
        return
    result = commandes_col.delete_many({"client_id": client["_id"]})
    if result.deleted_count > 0:
        print(f"{result.deleted_count} commande(s) supprimee")
    else:
        print("Aucune commande trouvee pour ce client ")

#9. Affichez les commandes triées par date de la commande (du plus récent au plus ancien).
def commandes_triees_par_date():
    commandes = commandes_col.find().sort("date_commande", -1)
    for c in commandes:
        client = clients_col.find_one({"_id": c["client_id"]})
        print(f"Client: {client['nom']}, Date: {c['date_commande']}, Statut: {c['statut']}, Total: {c['montant_total']}")
        for p in c['produits']:
            print(f"  - {p['nom']}")
        print("--------------------------------------------------")
commandes_triees_par_date()


#10. Affichez seulement les produits disponibles.
def afficher_produits_disponibles():

    produits = produits_col.find({"disponible": True})
    
    for p in produits:
        print(f"Nom: {p['nom']}, Categorie: {p['categorie']}, Prix: {p['prix']}, Stock: {p['stock']}")
        print("-************************************************")

afficher_produits_disponibles()
#11. Implémentez un menu en console permettant à l’utilisateur de :
def menu():
    while True:
        print("\n=== MENU E-COMMERCE ===")
        print("1. Ajouter une commande")
        print("2. Afficher tous les produits")
        print("3. Afficher tous les produits disponibles")
        print("4. Rechercher une commande par client")
        print("5. Mettre à jour un produit")
        print("6. Supprimer une commande")
        print("7. Supprimer les commandes d’un client donné")
        print("8. Afficher les produits disponibles")
        print("9. Trier les commandes par date de la commande")
        print("10. Quitter")
        
        choix = input("Entrez votre choix (1-10): ")

        if choix == "1":
            creer_commande()  
        elif choix == "2":
            afficher_produits()
        elif choix == "3":
            afficher_produits_disponibles()
        elif choix == "4":
            commandes_par_client()
        elif choix == "5":
            mise_a_jour_produit()
        elif choix == "6":
            supprimer_commande()
        elif choix == "7":
            supprimer_commandes_client()
        elif choix == "8":
            afficher_produits_disponibles()
        elif choix == "9":
            commandes_triees_par_date()
        elif choix == "10":
            print("Au revoir")
            break
        else:
            print("Choix invalide")
menu()
"""
# a. Administrateur
db.command("createUser", "admin",
           pwd="admin123",
           roles=[{"role": "dbAdmin", "db": "ecommerceDB"}])

# b. Utilisateur
db.command("createUser", "user",
           pwd="user123",
           roles=[{"role": "userAdmin", "db": "ecommerceDB"}])

# c. Visiteur
db.command("createUser", "visiteur",
           pwd="visiteur123",
           roles=[{"role": "read", "db": "ecommerceDB"}])

2. Donner la syntaxe de connexion en tant que visiteur
visiteur_client = MongoClient("mongodb://visiteur:visiteur123@localhost:27017/ecommerceDB")
visiteur_db = visiteur_client.ecommerceDB
for produit in visiteur_db.produits.find():
    print(produit)
3. Supprimer les utilisateurs crées

admin_db.command("dropUser", "admin")
admin_db.command("dropUser", "user")
admin_db.command("dropUser", "visiteur")


"""