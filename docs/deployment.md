# Demo Deployment

Recommended Demo Day setup:

- Frontend: Vercel, rooted at `frontend`
- Backend: Render free web service, using `render.yaml`

## Backend on Render

1. Create a new Render Blueprint from this repository and branch.
2. Select the `oncoreconcile-api` service from `render.yaml`.
3. Leave `ALLOWED_ORIGINS` empty until the Vercel URL exists, then set it to the deployed frontend origin:

```text
https://your-project.vercel.app
```

The backend Docker build uses `backend/Dockerfile.render`, which includes the repo-level `data/` directory required by benchmark and enterprise demo endpoints.

## Frontend on Vercel

1. Import the same repository and branch.
2. Set the project root directory to:

```text
frontend
```

3. Use the default Vite settings:

```text
Build command: npm run build
Output directory: dist
```

4. Add this environment variable:

```text
VITE_API_BASE_URL=https://your-render-service.onrender.com
```

5. Deploy.

After Vercel deploys, return to Render and set `ALLOWED_ORIGINS` to the Vercel URL. Redeploy the Render service.

## Demo Tip

Render free services spin down after idle time. Open the Render backend URL a few minutes before presenting so it wakes up before judges click through the demo.
