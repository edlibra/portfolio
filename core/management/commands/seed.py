"""
core/management/commands/seed.py

Commande de peuplement de la base de données.
Ajoute projets, compétences, liens sociaux et sections CV.
Passe silencieusement sur les enregistrements déjà existants.

Usage:
    python manage.py seed
    python manage.py seed --clear   ← efface tout avant de repeupler
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Peuple la base de données avec les données initiales du portfolio'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Efface les données existantes avant de repeupler',
        )

    def handle(self, *args, **options):
        from portfolio.models import SkillCategory, Skill, ProjectTag, Project
        from core.models import SocialLink, ResumeSection, ResumeItem

        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠ Suppression des données existantes...'))
            Project.objects.all().delete()
            Skill.objects.all().delete()
            SkillCategory.objects.all().delete()
            ProjectTag.objects.all().delete()
            SocialLink.objects.all().delete()
            ResumeItem.objects.all().delete()
            ResumeSection.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Données effacées.\n'))

        self.stdout.write(self.style.HTTP_INFO('\n── Catégories de compétences & compétences ──'))
        self._seed_skills(SkillCategory, Skill)

        self.stdout.write(self.style.HTTP_INFO('\n── Projets ──'))
        self._seed_projects(Project, ProjectTag)

        self.stdout.write(self.style.HTTP_INFO('\n── Liens sociaux ──'))
        self._seed_social_links(SocialLink)

        self.stdout.write(self.style.HTTP_INFO('\n── Sections CV ──'))
        self._seed_resume(ResumeSection, ResumeItem)

        self.stdout.write(self.style.SUCCESS(
            '\n══════════════════════════════════════\n'
            '✓ Base de données peuplée avec succès !\n'
            '══════════════════════════════════════\n'
            '\nProchaines étapes :\n'
            '  python manage.py createsuperuser\n'
            '  python manage.py runserver\n'
            '\nRemplace ensuite :\n'
            '  static/images/profile.jpg        ← ta photo\n'
            '  static/files/edlyn-exavier-cv.pdf ← ton CV\n'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # COMPÉTENCES
    # ─────────────────────────────────────────────────────────────────────────

    def _seed_skills(self, SkillCategory, Skill):
        categories = [
            {
                'name': 'Développement backend',
                'icon_class': 'bi-server',
                'order': 1,
                'skills': [
                    ('Python',           4, 85),
                    ('Django',           4, 82),
                    ('REST API Design',  3, 72),
                    ('PostgreSQL',       3, 70),
                    ('SQLite',           3, 75),
                ],
            },
            {
                'name': 'Développement frontend',
                'icon_class': 'bi-window',
                'order': 2,
                'skills': [
                    ('HTML5 / CSS3',        4, 88),
                    ('Bootstrap 5',         4, 86),
                    ('JavaScript (ES6+)',   3, 70),
                ],
            },
            {
                'name': 'Outils & DevOps',
                'icon_class': 'bi-tools',
                'order': 3,
                'skills': [
                    ('Git & GitHub',    4, 85),
                    ('Linux / Bash',    3, 74),
                    ('Docker (bases)',  2, 48),
                    ('Nginx / Gunicorn', 3, 65),
                ],
            },
            {
                'name': 'Électronique & Systèmes',
                'icon_class': 'bi-cpu',
                'order': 4,
                'skills': [
                    ('Conception de circuits', 3, 73),
                    ('Arduino / C embarqué',   3, 68),
                    ('Support IT & Réseaux',   4, 80),
                ],
            },
        ]

        total_cats = 0
        total_skills = 0

        for cat_data in categories:
            skills_list = cat_data.pop('skills')
            cat, created = SkillCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data,
            )
            if created:
                total_cats += 1
                self.stdout.write(f'  + Catégorie : {cat.name}')
            else:
                self.stdout.write(f'  · Existe déjà : {cat.name}')

            for order, (name, level, percent) in enumerate(skills_list, start=1):
                skill, created = Skill.objects.get_or_create(
                    name=name,
                    category=cat,
                    defaults={
                        'level': level,
                        'level_percent': percent,
                        'order': order,
                        'is_active': True,
                    },
                )
                if created:
                    total_skills += 1
                    self.stdout.write(f'      ↳ {name} ({percent}%)')

        self.stdout.write(self.style.SUCCESS(
            f'  → {total_cats} catégorie(s) créée(s), {total_skills} compétence(s) créée(s)'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # PROJETS
    # ─────────────────────────────────────────────────────────────────────────

    def _seed_projects(self, Project, ProjectTag):

        # Créer les tags d'abord
        tag_names = [
            'Python', 'Django', 'Bootstrap 5', 'REST API',
            'PostgreSQL', 'Arduino', 'JavaScript', 'HTML/CSS',
            'SQLite', 'Flask', 'Linux',
        ]
        tags = {}
        for name in tag_names:
            tag, _ = ProjectTag.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name},
            )
            tags[name] = tag

        projects_data = [
            {
                'title': 'Portfolio Personnel — edlynexavier.com',
                'slug': 'edlynexavier-portfolio',
                'tagline': 'Mon site web professionnel personnel, construit avec Django + Bootstrap 5.',
                'description': (
                    'Site portfolio full-stack construit de zéro avec Django, Bootstrap 5 et PostgreSQL. '
                    'Ce projet reflète mes capacités en développement web complet.\n\n'
                    'Fonctionnalités principales : gestion dynamique des projets via l\'admin Django, '
                    'pages SEO-optimisées avec données structurées JSON-LD (Person, WebSite, '
                    'SoftwareSourceCode), formulaire de contact avec protection anti-spam honeypot, '
                    'sitemap.xml, robots.txt, site bilingue FR/EN avec Django i18n.\n\n'
                    'Le frontend utilise un système de design personnalisé en CSS avec variables, '
                    'typographie Syne + DM Sans, animations CSS fluides et layout entièrement responsive.'
                ),
                'status': 'completed',
                'github_url': 'https://github.com/edlynexavier/portfolio',
                'live_url': 'https://edlynexavier.com',
                'is_featured': True,
                'order': 1,
                'tags': ['Python', 'Django', 'Bootstrap 5', 'PostgreSQL'],
                'meta_description': 'Portfolio personnel d\'Edlyn Exavier — Django, Bootstrap 5, PostgreSQL.',
            },
            {
                'title': 'Système de Gestion d\'Inventaire',
                'slug': 'systeme-gestion-inventaire',
                'tagline': 'Application web de suivi de stock et d\'inventaire pour petites entreprises.',
                'description': (
                    'Application de gestion d\'inventaire full-stack construite avec Django et PostgreSQL. '
                    'Conçue pour les petites entreprises ayant besoin de suivre leur stock, '
                    'leurs fournisseurs et leurs commandes.\n\n'
                    'Fonctionnalités : accès multi-utilisateurs avec permissions par rôle (admin, '
                    'staff, lecteur), suivi des niveaux de stock en temps réel, alertes de stock bas '
                    'configurables, gestion des catégories de produits, gestion des fournisseurs, '
                    'export CSV et tableau de bord avec graphiques Chart.js.\n\n'
                    'Implémentation technique : vues basées sur les classes Django, managers de modèles '
                    'personnalisés, signaux Django pour les alertes, Bootstrap 5 pour l\'interface responsive.'
                ),
                'status': 'completed',
                'github_url': 'https://github.com/edlynexavier/inventory-system',
                'live_url': '',
                'is_featured': True,
                'order': 2,
                'tags': ['Python', 'Django', 'PostgreSQL', 'JavaScript'],
                'meta_description': 'Système de gestion de stock Django + PostgreSQL pour petites entreprises.',
            },
            {
                'title': 'Moniteur IoT de Température',
                'slug': 'moniteur-iot-temperature',
                'tagline': 'Système de surveillance ambiante Arduino avec tableau de bord web en temps réel.',
                'description': (
                    'Projet matériel + logiciel combinant un microcontrôleur Arduino Uno avec '
                    'des capteurs DHT22 de température et d\'humidité pour surveiller l\'environnement '
                    'en temps réel.\n\n'
                    'L\'Arduino lit les données des capteurs toutes les 30 secondes et les transmet '
                    'par USB série à un serveur Python léger. Le backend stocke les relevés dans '
                    'SQLite et expose une API REST. Un tableau de bord web minimal affiche les '
                    'données en direct et l\'historique avec seuils d\'alerte configurables.\n\n'
                    'Composants techniques : firmware Arduino en C++, listener série Python avec '
                    'pyserial, API REST Flask, SQLite pour les séries temporelles, graphiques '
                    'Chart.js avec auto-rafraîchissement, alertes email via smtplib.'
                ),
                'status': 'completed',
                'github_url': 'https://github.com/edlynexavier/iot-temp-monitor',
                'live_url': '',
                'is_featured': True,
                'order': 3,
                'tags': ['Arduino', 'Python', 'SQLite', 'Flask'],
                'meta_description': 'Système IoT de surveillance température Arduino avec dashboard Python.',
            },
            {
                'title': 'Gestionnaire de Tâches CLI',
                'slug': 'gestionnaire-taches-cli',
                'tagline': 'Outil de gestion de tâches en ligne de commande rapide, construit en Python.',
                'description': (
                    'Outil de productivité en ligne de commande pour gérer les tâches quotidiennes, '
                    'entièrement en Python avec une interface interactive utilisant la bibliothèque '
                    'Rich pour un rendu terminal stylisé.\n\n'
                    'Supporte la création, le listage, le filtrage, la mise à jour et la suppression '
                    'des tâches. Les tâches sont stockées localement dans un fichier JSON pour '
                    'la portabilité. Fonctionnalités : niveaux de priorité (faible, moyen, '
                    'élevé, urgent), dates d\'échéance avec mise en évidence des retards, '
                    'filtrage par catégorie et vue tableau de bord récapitulatif.'
                ),
                'status': 'completed',
                'github_url': 'https://github.com/edlynexavier/task-cli',
                'live_url': '',
                'is_featured': False,
                'order': 4,
                'tags': ['Python', 'Linux'],
                'meta_description': 'Gestionnaire de tâches CLI Python avec interface terminal Rich.',
            },
        ]

        total = 0
        for pdata in projects_data:
            tag_names_for_project = pdata.pop('tags')
            slug = pdata.get('slug', slugify(pdata['title']))

            project, created = Project.objects.get_or_create(
                slug=slug,
                defaults={**pdata, 'status': pdata.get('status', 'completed')},
            )

            if created:
                # Assign tags via the M2M manager — this always works
                project_tags = [tags[t] for t in tag_names_for_project if t in tags]
                project.tags.set(project_tags)
                total += 1
                tag_labels = ', '.join(tag_names_for_project)
                self.stdout.write(f'  + Projet : {project.title}')
                self.stdout.write(f'      ↳ Tags : {tag_labels}')
                self.stdout.write(f'      ↳ Vedette : {"Oui" if project.is_featured else "Non"}')
            else:
                self.stdout.write(f'  · Existe déjà : {project.title}')

        self.stdout.write(self.style.SUCCESS(f'  → {total} projet(s) créé(s)'))

    # ─────────────────────────────────────────────────────────────────────────
    # LIENS SOCIAUX
    # ─────────────────────────────────────────────────────────────────────────

    def _seed_social_links(self, SocialLink):
        links = [
            ('github',   'GitHub',   'https://github.com/edlynexavier',         'bi-github',       1),
            ('linkedin', 'LinkedIn', 'https://linkedin.com/in/edlynexavier',     'bi-linkedin',     2),
            ('email',    'Email',    'mailto:hello@edlynexavier.com',            'bi-envelope-fill', 3),
        ]
        total = 0
        for platform, label, url, icon, order in links:
            link, created = SocialLink.objects.get_or_create(
                platform=platform,
                defaults={
                    'label': label,
                    'url': url,
                    'icon_class': icon,
                    'order': order,
                    'is_active': True,
                },
            )
            if created:
                total += 1
                self.stdout.write(f'  + {label} : {url}')
            else:
                self.stdout.write(f'  · Existe déjà : {label}')
        self.stdout.write(self.style.SUCCESS(f'  → {total} lien(s) créé(s)'))

    # ─────────────────────────────────────────────────────────────────────────
    # CV / RÉSUMÉ
    # ─────────────────────────────────────────────────────────────────────────

    def _seed_resume(self, ResumeSection, ResumeItem):
        sections_data = [
            {
                'title': 'Formation',
                'order': 1,
                'items': [
                    {
                        'title': 'Diplôme en Technologie du Génie Électronique',
                        'subtitle': 'Établissement d\'enseignement, Canada',
                        'location': 'Canada',
                        'date_start': 'Sept. 2022',
                        'date_end': 'Présent',
                        'description': (
                            'Programme complet couvrant la conception et l\'analyse de circuits, '
                            'la programmation de systèmes embarqués, l\'électronique de puissance, '
                            'les signaux et systèmes, l\'automatisation industrielle et la gestion '
                            'de projets techniques. Solide performance académique avec forte orientation pratique.'
                        ),
                        'order': 1,
                    },
                ],
            },
            {
                'title': 'Expérience',
                'order': 2,
                'items': [
                    {
                        'title': 'Développeur Web Full-Stack',
                        'subtitle': 'Freelance / Projets indépendants',
                        'location': 'Télétravail',
                        'date_start': '2021',
                        'date_end': 'Présent',
                        'description': (
                            'Conception et développement de plusieurs applications web full-stack '
                            'from scratch avec Python et Django. Implémentation d\'APIs REST, '
                            'schémas de base de données relationnelles, systèmes d\'authentification, '
                            'interfaces d\'administration et déploiements en production sur VPS.'
                        ),
                        'order': 1,
                    },
                    {
                        'title': 'Technicien Support IT',
                        'subtitle': 'Clients indépendants',
                        'location': 'Canada',
                        'date_start': '2020',
                        'date_end': '2022',
                        'description': (
                            'Support technique complet pour infrastructure matérielle, logicielle '
                            'et réseau. Configuration de routeurs et commutateurs réseau, '
                            'administration de serveurs Linux, résolution de problèmes systèmes '
                            'complexes et déploiements de postes de travail.'
                        ),
                        'order': 2,
                    },
                ],
            },
            {
                'title': 'Certifications',
                'order': 3,
                'items': [
                    {
                        'title': 'Python for Everybody Specialization',
                        'subtitle': 'Coursera / Université du Michigan',
                        'location': '',
                        'date_start': '2021',
                        'date_end': '2021',
                        'description': (
                            'Spécialisation de 5 cours couvrant les fondamentaux Python, '
                            'les structures de données, le web scraping, les bases de données '
                            'et la visualisation de données.'
                        ),
                        'order': 1,
                    },
                ],
            },
        ]

        total_sections = 0
        total_items = 0

        for sdata in sections_data:
            items = sdata.pop('items')
            section, created = ResumeSection.objects.get_or_create(
                title=sdata['title'],
                defaults=sdata,
            )
            if created:
                total_sections += 1
                self.stdout.write(f'  + Section : {section.title}')
            else:
                self.stdout.write(f'  · Existe déjà : {section.title}')

            for idata in items:
                item, created = ResumeItem.objects.get_or_create(
                    section=section,
                    title=idata['title'],
                    defaults=idata,
                )
                if created:
                    total_items += 1
                    self.stdout.write(f'      ↳ {item.title}')

        self.stdout.write(self.style.SUCCESS(
            f'  → {total_sections} section(s) créée(s), {total_items} entrée(s) créée(s)'
        ))
