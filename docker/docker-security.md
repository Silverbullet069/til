# Docker Security

<!-- tl;dr starts -->

Container is fast and convienent. An image has malicious code embedded or run with root privilege can cause destruction to CI/CD pipeline.

<!-- tl;dr ends -->

## Attack vectors

Common:

- Unknown base images come from untrustworthy sources.
- Root privilege
- Sensitive information are included in one of the image layers.

## Security features

### User Namespace

Mapping root user inside container to non-root user on host system.

`/etc/docker/daemon.json`

```json
{
  "userns-remap": "default"
}
```

```sh
sudo systemctl restart docker
```

### Image scanning

Using static analysis tools such as: [aquasecurity/trivy](https://github.com/aquasecurity/trivy), [snyk](https://www.snyk.io), Docker Scan (only available in Docker Desktop) ...

These tools work best within CI/CD pipeline. They can fail the pipeline if happens a critical error.

### Security Profiles

Without security profiles:

- Dangerous syscall (e.g. `ptrace`) can be used to extract sensitive data inside process.
- Container escape.

Docker provides several security profiles and features to help harden containers. Docker enforce a default Seccomp profile.

- **Seccomp:** Restricts the system calls a container can make. Pass `unconfined` to run a container without default profile.
- **AppArmor:** Restricts file accessing capabilities.
- **SELinux:** Provides mandatory access controls.
- **Capabilities:** If the container must run as root, limit the capabilities using `--cap-drop=ALL`, on the contrary, if the container run as user requiring a capability (e.g. pinging port < 1024), use `--cap-add`.
- **No new privileges:** Prevents processes from gaining additional privileges, even if binaries have setuid/setgid. Use this when container is run as non-root.
- **User namespaces:** Remap container user IDs to non-root host users for isolation.
- **Read-only root filesystem:** Run containers with a read-only root filesystem using `--read-only`.
- **Resource limits:** Limit CPU, memory, and other resources to reduce attack surface.

```sh
docker run \
  --security-opt seccomp=profile.json \
  --security-opt apparmor=profile_name \
  --security-opt <label>:<type>:<label> \
  --security-opt no-new-privileges:true \
  --read-only \
  --cap-drop=ALL \
  --user 1000:1000 \
  --memory="512m" \
  --cpus="0.5" \
  ...
```

## References

[Trần Phước Huỳnh, 2024-12-19, Bài 7. Docker Security: Bảo Mật Container Hiệu Quả](https://devops.vn/posts/docker-security-bao-mat-container-hieu-qua/)
