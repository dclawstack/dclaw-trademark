# Troubleshooting

Common issues and solutions for DClaw Trademark.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-trademark

# Check logs
kubectl logs -n dclaw-trademark deployment/dclaw-trademark-backend

# Check database
kubectl get clusters -n dclaw-trademark
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
