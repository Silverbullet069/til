# Tailscale Cheatsheet

<!-- tl;dr starts -->

My cheatsheet is comprised of every CLI commands I run, every configuration files I wrote, stem from performance or security best practices to create reliable, performant, secure Tailscale set ups on various type of infrastructure. It is made from official documentation and personal experience.

<!-- tl;dr ends -->

## Install Tailscale on Rootless Docker

Create an Auth key and write it into `tailscale.env`:

```env
TS_AUTHKEY=tskey-auth-caution-thisIsNotARealAuthKeyLoremIpsumDolarSitAmet
```

On my laptop, instead of using Rootful Docker, **I'm using Rootless Docker**, therefore there is a lot of workaround inside my `/opt/servarr/docker-compose.yml`.

Safely create and start container (remove orphans, force recreate and force rebuild):

```sh
$ docker compose up -d --remove-orphans --force-recreate --build tailscale
```

(Optional) If you've turned on newly added devices need to be approved, go into admin panel and approve it. Disable key expiry if you don't want your node to go down after 90 days.

Check if IPv6 is enabling and the latency to Hong Kong DERP server is the lowest:

```sh
$ docker exec tailscale tailscale netcheck
```

([After you've set up Tailscale on AWS EC2](tailscale-playbook.md#aws)) Check for direct connection establishment between on-premise and AWS EC2:

```sh
$ docker exec tailscale tailscale ping -c 0 <aws-ec2-hostname>
```

> I was wondering why the ping command suddenly stopped execution when one packet managed to traverse via direct connection. Turn out, [it's Tailscale default behavior](https://tailscale.com/kb/1023/troubleshooting#derp-traffic-route-checking). IMO, there should have been a message that print the reason why it aborts the ping.

([After you've set up Tailscale on AWS EC2](tailscale-playbook.md#aws)) Try to use Tailscale SSH

```sh
$ docker exec -it tailscale tailscale ssh ec2-user@<aws-ec2-hostname>
```

## Install Tailscale on AWS EC2

- Choose the region that's closest to you (for me it's Hong Kong) and create an AWS EC2 compute engine there.

> I'm using this tool: [CloudPing.cloud](https://www.cloudping.cloud/aws) to test latency.

- SSH into AWS EC2:

```sh
$ ssh -i path/to/primary/key.pem ec2-user@ec2-ip-X-X-X-X.region.compute.amazonaws.com
# Tips: it's better to use password manager such as GNOME Libsecret or KeePassXC
```

- [Manually install Tailscale on AWS EC2](https://tailscale.com/kb/1449/quick-guide-aws#install-manually):

```sh
curl -fsSL https://tailscale.com/install.sh | sh
```

- (optional) Turn on IP forwarding:

```sh
$ echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
$ echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
$ sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

- Turn on Tailscale and Tailscale SSH (and optional exit node mode):

```sh
$ sudo tailscale up --operator=ec2-user --ssh

# if IP forwarding is enabled
$ sudo tailscale up --advertise-exit-node --operator=ec2-user --ssh
```

- Authenticate web login portal with SSO. If you've turned on newly added devices need to be approved, go into admin panel and approve it. Disable key expiry if you don't want your node to go down after 90 days.

- [Enable auto-update manually](https://tailscale.com/kb/1067/update?tab=linux#enable-auto-updates-on-devices):

```sh
$ sudo tailscale set --auto-update
```

- Manual update:

```sh
$ tailscale update
$ sudo yum update tailscale   # Amazon Linux
```

- Check for Endpoints and Client Connectivity information on Tailscale admin panel, if there is no info, you will have to reboot EC2 instance.

## Azure

> **NOTE:** only because I have free Azure resources provided by GitHub Student Developer Pack.

## Performance practices

- Increase the likelihood of a direct connection by:
  - Enable IPv6 on both nodes.
  - Expose a public IP address for Tailnet devices.
  - Open a firewall port.
  - Troubleshoot why a device use a relayed connection using [device connectivity guide](https://tailscale.com/kb/1411/device-connectivity) and understanding logic behind [connections types](https://tailscale.com/kb/1257/connection-types)

## Security practices

> **NOTE:** most of them are team-based security practices. Individual security practices which I'm using are written in bold text.

### General

- **Write ACL tests to ensure ACLs work as you wanted.**
- Require users to rotate keys by re-authenticating their devices to the Tailnet regularly.
- Remove unused OAuth client/API keys/Auth keys. Especially during offboarding process.

### The principle of least privileges

- Using groups to manage users. Control identities based on job function. If someone leaves organization/changes roles, adjust group membership rather than update all of their ACL.
- Using tags to manage devices. Define access to devices based on purpose instead of owner. If someone leaves organization/changes role, devices they have set up will not be reconfigured.

- Beside implementing RBAC using custom group, Tailscale has a built-in RBAC system. Assign these roles to users based on their job function: _Admin, Network admin, IT admin, Billing admin, Auditor._
- Use just-in-time access requests to manage temporary access to resources on Tailscale node.

### SSH-related

- Using `"accept": "check"` mode for Tailscale SSH can force connections to privilege user (such as `root`) must be re-authenticate for the next 12 hours (customizable).
- Set up session recording for Tailscale SSH to log the contents of SSH sessions. Ain't nobody messing up your Tailnet device that's gone unnoticed anymore. The recordings can be stored in AWS S3 / AWS EBS. (this practice is also included in [Monitoring-related section](tailscale-playbook.md#monitoring-related))

### Monitoring-related

- Review who did what, and when, in your tailnet using Configuration Audit Logs.
- Get notified about events in your tailnet using Webhooks to subscribe to events.

### External tools-related

- **Obtain TLS certs from a public CA for internal web tools.**
- If you're using HTTP, you must **Prevent DNS rebinding attacks by ensuring a Host headeer is present for HTTP services.**

### Networking-related

- Using Tailscale with firewall. Install Tailscale in Docker can save you some trouble. Depending on the setup of each machines, some [firewall ports need to be opened to achive P2P direct connection](https://tailscale.com/kb/1082/firewall-ports).
- Use _Network flow logs_ to determine how nodes are connecting on your Tailscale network. These logs can be exported for long-term storage.

### Repository management

- **Use GitOps for Tailscale with GitHub Actions to manage your Tailnet policy file in a code repository.** That includes:

  - No need to use Tailscale admin dashboard.
  - Version control.
  - Collaborative code audit.

- **Setup Tailscale with IaC via Terraform by interacting with Tailscale API**. Features:

  - Define Tailnet policy file.
  - Set DNS settings.
  - Generate Auth keys/OAuth clients.
  - Manage device properties. <!-- TODO: find out about Tailscale device properties -->

  > IaC need to be restricted access as well.

## Deployment

Check the status of all Tailscale's systems: https://status.tailscale.com/

### [Hardening Tailscale node](https://tailscale.com/kb/1279/security-node-hardening#suggested-hardening-configuration-based-on-systemd) and [Best practices to secure your tailnet](https://tailscale.com/kb/1196/security-hardening)

### [SSH into AWS VM](https://tailscale.com/kb/1308/quick-guide-ssh-linux-vm#configure-tailscale-ssh)

### [Turning AWS EC2 into a Tailscale Exit node](https://tailscale.com/kb/1103/exit-nodes#how-it-works)

## Performance best practices

I've two Tailscale clients, one is my physical laptop installed as a Docker container, one is my AWS EC2 that I got as a free-tier service.

## Reference

- [Performance Best Practices, Tailscale Docs, 2025-05-23](https://tailscale.com/kb/1320/performance-best-practices)
- [Best practices to secure your Tailnet, Tailscale Docs, 2025-05-07](https://tailscale.com/kb/1196/security-hardening)
- [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh)
- [Manage permissions using ACLs](https://tailscale.com/kb/1018/acls)
- [Syntax reference for the tailnet policy file](https://tailscale.com/kb/1337/policy-syntax)
- [ACL policy samples](https://tailscale.com/kb/1192/acl-samples)
- [Troubleshooting guide, Tailscale Docs, 2025-05-07](https://tailscale.com/kb/1023/troubleshooting)

## Tailnet policy file syntax

> **NOTE:** Only Admin or Network admin can modify the Tailnet policy file.

```jsonc
{
  // Define custom groups to implement RBAC
  // NOTE: Check if autogroup: aligns with your use case
  // TIPS: best practice is to use tag to manage users' role
  // TIPS: Refrain from using name that's overlapped with autogroups, such as "owner", "admin", ... If you must, write a prefix/suffix to the name (e.g. `admin-1", ...)
  // Docs: https://tailscale.com/kb/1337/policy-syntax#groups
  "groups": {
    // NOTE: "admin" is just a name. These accounts are not assigned with Admin role on the current Tailnet
    "group:dev": ["johndoe@example.com"],
    "group:engineering": ["dave@example.com", "laura@example.com"],
    "group:sales": ["brad@example.com", "alice@example.com"]
  },

  // Define the tags which can be applied to devices and by which users.
  // CAUTION: once you have add a tag to a TS node, that node is owned by tag and not a user anymore. Therefore render Taildrop useless. To revert this action, remove the node and re-auth it
  // TIPS: best practice is to use tag to manage devices' environment
  "tagOwners": {
    "tag:prod": ["autogroup:admin"],
    "tag:ci": ["group:dev"],
    "tag:dev": ["autogroup:admin", "group:dev"],
    "tag:container": ["autogroup:admin"]
  },

  // Define access control lists (ACL) to govern how and where data can flow within a Tailnet.
  // - Deny-by-default model
  // - Explicit direction flow (unidirectional or bidirectional)
  // - Enforced locally
  // - Does not affect local network access
  "acls": [
    {
      // IMO, no rule = deny, rule = accept. No need "action" property
      // Must be the result of early design decisions and backward-compability
      "action": "accept",

      // - an autogroup ().
      "src": [
        "*", // all TS devices + approved subnets + autogroup:shared
        "johndoe@example.com", // an email
        "johndoe@github", // a GitHub account
        "johndoe@passkey", // a passkey
        "100.xxx.xxx.xxx", // a Tailscale IPv4
        "192.168.1.0/24", // a subnet or a CIDR notation
        "my-host", // a hostname assigns to a Tailscale IP or subnet
        "tag:production", // a tag, best used for managing environments
        "autogroup:shared", // users, destinations, usernames with the same roles/property. Docs: https://tailscale.com/kb/1337/policy-syntax#autogroups
        "autogroup:danger-all" // a special autogroup, all sources including outside tailnet
      ],

      // <host>:<ports>
      // <host>=most of them are similar to "src", there are "tag:<tag-name>"
      // <ports>
      // * = any
      // 22 = single
      // 80,443 = multiple
      // 1000-2000 = range
      "dst": [
        "*:*", // any destination
        "johndoe@example.com:*", // an email
        "johndoe@github:*", // a GitHub account
        "johndoe@passkey:*", // a passkey
        "100.xxx.xxx.xxx:*", // a Tailscale IPv4
        "192.168.1.0/24:*", // a subnet or a CIDR notation
        "my-host:*", // a hostname assigns to a Tailscale IP or subnet
        "tag:production:*", // a tag, best used for managing environments

        // Dst-specific autogroups
        "autogroup:internet:*", // devices with access to the Internet routed through exit nodes // NOTE: this rule is crucial for devices who want to use other devices as exit nodes
        "autogroup:self:*", // devices where the same user is auth on both src and dst. // NOTE: tag is not supported, only works with autogroup:member
        "autogroup:member:*", // devices where the user is a direct member
        "autogroup:admin:*", // the user is Admin
        "autogroup:network-admin:*", // the user is a Network admin
        "autogroup:it-admin:*", // the user is an IT admin
        "autogroup:billing-admin:*", // the user is a Billing admin
        "autogroup:auditor:*", // the user is an Auditor
        "autogroup:owner:*", // the user is the Tailnet owner.
        "autogroup:tagged" // all devices that are tagged
      ]

      // optional
      // no "proto" = rule applies to all TCP + UDP traffic
      // "proto": "tcp"
      // "proto": "udp"
    }
  ],

  // Define users and services that can use Tailscale SSH
  // NOTE: required both "acl:" and "ssh:" rules to be defined
  // - Tailscale takes over port 22 for incoming SSH connection from Tailnet.
  // - Use Node key to auth and encrypt the connection over WireGuard.
  // - Does not interfere with other SSH connections.
  "ssh": [
    {
      "action": "check", // re-auth every 12 hours
      "action": "accept", // logged in to Tailnet once is enough

      "src": [
        "autogroup:members" // CAUTION: access to external invited users who shared with "dst" is also accessed, even if they have no devices in Tailnet
        // a tag, group, autogroup
      ],

      // dst can be  (no *, no port)
      "dst": [
        "autogroup:self" // NOTE: only works with "autogroup:members"
        // a user, tag, group, autogroup
      ],

      "users": ["root", "autogroup:nonroot"]
    }
  ],

  // Test access rules every time they're saved.
  "tests": [
    {
      "src": "johndoe@gmail.com", // a host, an email, a group, a tag
      "srcPostureAttrs": {}, // NOTE: best to omit
      "proto": "tcp", // NOTE: best to omit

      // NOTE: tests require IP address, these values are translated to IP address later
      // "accept" now acts as "dst"
      "accept": [
        // port must be single, numeric number
        "100.xxx.xxx.xxx:22", // Tailscale IPv4
        "my-host", // a host in `hosts:` section
        "[1:2:3::4]:80", // Tailscale IPv6
        "johndoe@example.com:8080", // an email
        "group:security@example.com:1234", // a group
        "tag:production:443" // a tag
      ],

      "deny": [
        // same as "accept"
      ]
    }
  ],

  // Test Tailscale SSH rules specifically
  // Similar to "tests:" whose rule's "accept" port is 22
  // Docs: https://tailscale.com/kb/1337/policy-syntax#ssh-tests
  "sshTests": [
    {
      "src": "dave@example.com", // an email, a tag, a group, a host

      "dst": [
        "johndoe@gmail.com", // an email
        "example-host-1", // a host
        "tag:production", // a tag
        "group:dev" // a group
      ],

      // allow connection
      "accept": [
        "dave" // username
      ],

      // allow connection if fulfilled an additional re-auth
      "check": [
        "admin" // username
      ],

      // disallow connection
      "deny": [
        "root" // username, tend to be "root"
      ]
    }
  ]
}
```

## Tailscale Docker Compose syntax

```yml
services:
  tailscale-nginx:
    image: tailscale/tailscale:latest
    hostname: tailscale-nginx
    # Parameters: https://tailscale.com/kb/1282/docker#ts_auth_once
    environment:
      - TS_ACCEPT_DNS=true # accept DNS configuration from the admin console
      - TS_AUTH_ONCE=true # attempt to log in ONLY if not already logged in, set to false to forcibly log in every time the container starts
      # Option 1: use auth key, similar to run `tailscale login --auth-key=`
      # Option 2: use OAuth client (with "Auth key: write" scope, prevent modifying ACLs or DNS on clients), but the associated tag must be provided using `TS_EXTRA_ARGS=--advertise-tags=tag:owner`
      - TS_AUTHKEY=tskey-client-notAReal-OAuthClientSecret1Atawk?ephemeral=false # TS node auth via OAuth Client will NOT be removed from Tailnet if specified ?ephemeral=false at the end of OAuth client secret
      - TS_DEST_IP= # proxy incoming Tailscale traffic to an IP
      - TS_LOCAL_ADDR_PORT= # def=[::]:9002, customize the address:port on which will serve local metrics and health check HTTP endpoints
      - TS_ENABLE_HEALTH_CHECK=true # enable unauth /healthz endpoint at the address specified by TS_LOCAL_ADDR_PORT
      - TS_ENABLE_METRICS=true # enable unauth /metrics endpoint at the address specified by TS_LOCAL_ADDR_PORT
      - TS_HOSTNAME=johndoe # specifiy custom hostname
      - TS_ROUTES= # advertise subnet routes
      - TS_EXTRA_ARGS=--advertise-tags=tag:owner # flags for `tailscale set` cmd
      - TS_TAILSCALED_EXTRA_ARGS= # flags for `tailscaled` cmd
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_SERVE_CONFIG=/config/mealie.json
      - TS_USERSPACE=false # def=true, use kernel networking
    volumes:
      - ${PWD}/tailscale-nginx/state:/var/lib/tailscale
    devices:
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - net_admin
    restart: unless-stopped
  nginx:
    image: nginx
    depends_on:
      - tailscale-nginx
    network_mode: service:tailscale-nginx
```
