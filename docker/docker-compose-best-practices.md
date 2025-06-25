# Docker Compose Best Practice

<!-- tl;dr starts -->

<!-- tl;dr ends -->

## Dockerfile Naming Convention

1. **Environment-specific:** `Dockerfile.dev`, `Dockerfile.prod`, `Dockerfile.test`
2. **Base image variations:** `Dockerfile.alpine`, `Dockerfile.debian`
3. **Architecture-specific:** `Dockerfile.arm64`, `Dockerfile.amd64`
4. **Service-specific:** `Dockerfile.web`, `Dockerfile.api`

## Services Naming Convention

1. Name based on **Functional Role** rather than **Technology**.
2. Use consistent naming patterns across services
3. Choose names that make sense in application context.

This creates better abstraction - if you change from application A to application B, the service function remains the same even though the implementation changes.

## References

- [Docker Docs's "Compose file reference"](https://docs.docker.com/reference/compose-file/)
