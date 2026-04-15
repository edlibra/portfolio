# Guide de peuplement — Seed

## La bonne méthode : `python manage.py seed`

C'est la commande à utiliser. Elle est fiable, affiche ce qu'elle fait,
et gère correctement les relations M2M (tags des projets).

```bash
# Première installation (base vide)
python manage.py seed

# Si tu veux repartir de zéro (efface tout et recrée)
python manage.py seed --clear
```

### Ce que seed crée :

**4 catégories de compétences** avec 15 compétences :
- Développement backend : Python (85%), Django (82%), REST API (72%), PostgreSQL (70%), SQLite (75%)
- Développement frontend : HTML5/CSS3 (88%), Bootstrap 5 (86%), JavaScript (70%)
- Outils & DevOps : Git (85%), Linux (74%), Docker (48%), Nginx (65%)
- Électronique & Systèmes : Circuits (73%), Arduino (68%), Support IT (80%)

**4 projets** (3 vedettes + 1) avec tags :
- Portfolio edlynexavier.com [Python, Django, Bootstrap 5, PostgreSQL] ⭐
- Système de Gestion d'Inventaire [Python, Django, PostgreSQL, JavaScript] ⭐
- Moniteur IoT de Température [Arduino, Python, SQLite, Flask] ⭐
- Gestionnaire de Tâches CLI [Python, Linux]

**3 liens sociaux** : GitHub, LinkedIn, Email

**3 sections CV** avec 4 entrées :
- Formation : Diplôme Génie Électronique
- Expérience : Dev Web Freelance + Technicien IT
- Certifications : Python for Everybody

---

## Méthode alternative : `loaddata` (compétences + CV seulement)

```bash
python manage.py loaddata fixtures/initial_data.json
```

⚠ Cette commande charge compétences, sections CV et liens sociaux,
mais **ne lie pas les tags aux projets** (limitation Django fixtures M2M).
Préfère `seed` qui gère tout correctement.

---

## Séquence complète d'installation

```bash
# 1. Migrations
python manage.py migrate

# 2. Seed (tout le contenu)
python manage.py seed

# 3. Superuser admin
python manage.py createsuperuser

# 4. Lancer le serveur
python manage.py runserver
```

Accès admin : http://localhost:8000/fr/admin/
