# Instructions pour Codex

## Objectif

Construire un site pédagogique de physique destiné principalement aux élèves de 12 à 18 ans. Le site doit soutenir l’exploration, la prédiction et l’expérimentation.

## Contraintes techniques

- Conserver Astro et la génération statique tant qu’aucun besoin serveur précis n’est démontré.
- Ne pas introduire React, Vue ou une nouvelle dépendance sans justification explicite.
- Réutiliser les tokens de `src/styles/tokens.css`. Ne pas inventer de couleur, police, rayon ou largeur directement dans un nouveau composant.
- Préserver le fonctionnement sous le chemin GitHub Pages `/science-site/`.
- Vérifier le mobile, le clavier et `prefers-reduced-motion`.
- Exécuter `npm run check` et `npm run build` avant de terminer.

## Contraintes pédagogiques

- Favoriser « prédire → expérimenter → expliquer ».
- Ne pas révéler une réponse avant l’expérimentation lorsque l’activité repose sur une découverte.
- Préférer un retour visuel direct à une accumulation de fenêtres explicatives.

## Organisation

- Site et contenu éditorial : ce dépôt.
- Gros jeux et simulations : dépôts autonomes, intégrés par URL.
- Petites applications autonomes : `public/apps/<nom>/`.
