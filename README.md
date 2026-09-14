# Science Site

Socle technique du site pédagogique de Jonas Evrard.

Le projet utilise Astro et est publié automatiquement sur GitHub Pages. La V0 contient uniquement la structure du site, le design system et les composants nécessaires pour accueillir ensuite des cours, images, vidéos, jeux et simulations HTML.

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
