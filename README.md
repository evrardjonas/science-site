# Science Site

Socle technique du site pédagogique de Jonas Evrard.

Le projet utilise Astro et est publié automatiquement sur GitHub Pages. La V0 contient uniquement la structure du site, le design system et les composants nécessaires pour accueillir ensuite des cours, images, vidéos, jeux et simulations HTML.

Une page dédiée à Scienteens Lab est disponible en anglais depuis un onglet supplémentaire du menu, sans modifier l’accueil ni les rubriques d’origine.

## Modifier la page Scienteens Lab

Tous les textes de cette page sont regroupés dans `src/content/scienteens.json`. Sur GitHub, ouvrir ce fichier, cliquer sur le crayon, modifier uniquement le texte entre guillemets, puis utiliser **Commit changes**. GitHub Pages republie ensuite automatiquement le site.

Le bloc `interview.steps` contient les cinq parties du parcours Mersenne → Kundt. Dans chaque partie, `title` modifie le titre et `paragraphs` contient les paragraphes affichés. Les emplacements de vidéos et d’animations sont indiqués par `media` ; leur intégration pourra donc se faire sans réécrire le reste de la page.

Le bloc `other` est réservé aux réponses ou documents complémentaires qui seront ajoutés plus tard. Les autres projets ont vocation à rejoindre les rubriques générales du site. Ne pas supprimer les guillemets, virgules ou accolades du fichier JSON.

## Développement local

```bash
npm install
npm run dev
```

Vérifications avant une pull request :

```bash
npm run check
npm run build
```

## Structure

- `src/pages/` : routes du site
- `src/components/` : composants réutilisables
- `src/layouts/` : mise en page commune
- `src/styles/` : design system global
- `public/apps/` : jeux et animations HTML autonomes
- `.github/workflows/` : vérification et publication GitHub Pages

Voir aussi [ARCHITECTURE.md](./ARCHITECTURE.md), [AGENTS.md](./AGENTS.md) et [CLAUDE.md](./CLAUDE.md).
