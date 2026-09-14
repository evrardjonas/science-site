# Architecture

## Rôle du dépôt

Ce dépôt contient le site-portail. Les applications importantes peuvent rester dans des dépôts indépendants et être publiées séparément. Une petite application autonome peut aussi être placée dans `public/apps/`.

## Principes

1. Astro génère un site statique compatible avec GitHub Pages.
2. Le contenu éditorial et les applications interactives restent séparés.
3. Les styles réutilisent exclusivement les variables de `src/styles/tokens.css`.
4. Les routes publiques restent en français et utilisent des URL simples.
5. Le JavaScript côté client est ajouté uniquement lorsqu’une interaction l’exige.

## Intégration d’une application HTML

Utiliser `InteractiveFrame.astro` afin de conserver le même cadre, la même accessibilité et le lien d’ouverture séparée sur toutes les pages.

## Déploiement

La branche `main` est construite puis publiée par `.github/workflows/deploy.yml`. Les pull requests exécutent la vérification et la compilation via `.github/workflows/check.yml`.
