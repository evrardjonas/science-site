# Architecture

## Rôle du dépôt

Ce dépôt contient le site-portail. Les applications importantes peuvent rester dans des dépôts indépendants et être publiées séparément. Une petite application autonome peut aussi être placée dans `public/apps/`.

## Principes

1. Astro génère un site statique compatible avec GitHub Pages.
2. Le contenu éditorial et les applications interactives restent séparés.
3. Les styles réutilisent exclusivement les variables de `src/styles/tokens.css`.
4. L’accueil et les rubriques thématiques restent en français. La page Scienteens Lab est en anglais.
5. Le JavaScript côté client est ajouté uniquement lorsqu’une interaction l’exige.

## Intégration d’une application HTML

Utiliser `InteractiveFrame.astro` afin de conserver le même cadre, la même accessibilité et le lien d’ouverture séparée sur toutes les pages.

## Déploiement

La branche `main` est construite puis publiée par `.github/workflows/deploy.yml`. Les pull requests exécutent la vérification et la compilation via `.github/workflows/check.yml`.

## Parcours principal

Le menu conserve les cinq rubriques d’origine : `Accueil`, `Ressources`, `Simulations`, `Jeux` et `Projets`. `Scienteens Lab` est une page supplémentaire, accessible depuis un sixième onglet. Son ajout ne remplace ni l’accueil ni le design d’origine.

La page `Scienteens Lab` reste volontairement limitée à deux sections : `Interview`, consacrée à l’atelier du tube de Kundt, et `Other`, réservée à de futurs compléments. Les autres projets et ressources sont publiés dans les rubriques générales afin de préserver une navigation lisible.
