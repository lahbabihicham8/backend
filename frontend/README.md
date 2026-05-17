# Khafeefa Frontend

## EasyPanel Deployment

Use the Dockerfile in this folder.

- Repository: `lahbabihicham8/frontend`
- Branch: `main`
- Build method: Dockerfile
- Dockerfile path: `Dockerfile`
- Exposed port: `3000`

The Docker image builds a static export and serves it with Nginx on port `3000`.

If you use EasyPanel auto-detect/Nixpacks instead of Dockerfile, this repo also includes `nixpacks.toml`.

- Install command: `npm ci`
- Build command: `npm run build`
- Start command: `npm run start`
- Node version: `22+`

Environment variables:

```env
NEXT_PUBLIC_SITE_URL=https://getkhafeefa.shop
NEXT_PUBLIC_API_BASE_URL=https://api.getkhafeefa.shop
NEXT_PUBLIC_META_PIXEL_ID=
NEXT_PUBLIC_TIKTOK_PIXEL_ID=
NEXT_PUBLIC_SNAP_PIXEL_ID=
NEXT_PUBLIC_ENABLE_PIXELS=true
NEXT_PUBLIC_ENVIRONMENT=production
```
