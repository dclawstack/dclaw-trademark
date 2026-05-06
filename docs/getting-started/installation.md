# Installation

## Via DPanel

1. Open DPanel at `https://panel.yourdomain.com`
2. Find **DClaw Trademark** in the app grid
3. Click **Install**
4. The DClaw Operator will provision:
   - Namespace: `dclaw-trademark`
   - Frontend deployment (Next.js)
   - Backend deployment (FastAPI)
   - PostgreSQL database (CloudNativePG)
   - Ingress with TLS

## Via kubectl

```bash
# Apply the DClawApp CRD
kubectl apply -f - <<EOF
apiVersion: platform.dclaw.io/v1
kind: DClawApp
metadata:
  name: trademark
spec:
  appId: trademark
  appName: DClaw Trademark
  version: 0.1.0
  category: legal
  enabled: true
  frontend:
    image: ghcr.io/dclawstack/dclaw-trademark:latest
    replicas: 2
  backend:
    image: ghcr.io/dclawstack/dclaw-trademark-backend:latest
    replicas: 2
  database:
    enabled: true
    storage: 10Gi
  ingress:
    enabled: true
    host: trademark.yourdomain.com
    tls: true
EOF
```

## Verify

```bash
kubectl get pods -n dclaw-trademark
kubectl get ingress -n dclaw-trademark
```
