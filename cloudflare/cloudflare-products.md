# Cloudflare Products

<!-- tl;dr starts -->

There are a lot of products on Cloudflare Developer Platform. Cloud engineers will need to consider and pick a subset of services for their use cases.

<!-- tl;dr ends -->

## Overview

Cloudflare, is a company that provides services on its global network of servers. It's one of the largest networks on the Internet.

Cloudflare's services are categorized into 4 product lines:

- SASE and SSE services.
- Application services.
- Infrastructure services.
- Developer Platform.

Three first services are for private and public organizations, businesses, governments, individual consumers. In general, non tech-savvy clients that need technological consultance from Cloudflare.

Cloudflare Developer Platform is the product line that we, cloud engineer, care about. It includes Cloudflare Workers, which allows engineers to deploy serverless code globally.

### Cloud Computing

In the early days of the web, we have on-premise infrastructure. Basically anyone who wanted to build a web application had to buy their own physical hardware and install and configure web server program into them. It requires painstakingly time and money.

Then came Cloud Computing. It is defined as hosting computing resources (virtual machines, storage, databases, networking services) on 3rd-party servers. There are several major vendors: AWS, MS Azure, Google Cloud Platform (GCP), Cloudflare.

Cloud computing allows organizations to rent a fixed number of servers or server space. To prepare for seasonal or unplanned traffic spikes, organizations have to overpurchase server space to ensure their applications do not go down because of high request volume from end users or customers.

### Serverless Computing (Serverless)

_Definition:_ It's a subset of cloud computing, a method of providing backend services on an pay-as-you-go basis. Cloud's customers aren't required to calculate how much server space or machines they need to rent.

Despite the name "serverless", physical servers are still existed, but engineers do not need to be aware of them.

_Characteristics:_

- **Abstracted:** Unlike traditional hosting providers, a serverless computing provider take card or server management, provisioning, allowing developers and organizations to focus on writing and deploying logic.
- **Pay-for-value:** or usage model paradigm. Instead of paying for fixed amount of computing resources that may be underutilized or exceeded, users pay as much as users are charged based on their computation usage. However, usage is defined differently per serverless computing provider so make sure you've done thorough research.
- **Auto-scaling:** The service is responsible for the scalability of your application. It scales automatically to handle both low points and surges in request traffic.
- **Event-driven execution model:** when an event (HTTP request, Worker Cron Trigger, ...) invokes a Worker, the Worker code will execute.

_Ideal for:_ Event-driven applications, Microservices, Workloads with unpredictable traffic patterns.

_Limitations:_

- **Cold starts:** There are initial startup time when a function hasn't been used recently. Not a problem for functions that are used often.
- **Resource constraints:** There might be time, memory, CPU constraints that are set up by cloud vendors:
  - The total amount of time from the start to end of an invocation of a Worker is known as duration.
  - The amount of time the CPU actually spends doing work during a given request is known as CPU time.
- **Statelessness:** Functions don't maintain state between executions.
- **Vendor Lock-in:** Code might be tied to specific provider services

## Products Overview

> Browse all Cloudflare's products here: https://developers.cloudflare.com/products/

Here are some of the most popular products:

<!-- prettier-ignore -->
| Groups | Product | Use Case | Ideal for |
| --- | --- | --- | --- |
| Consumer services | Registrar | Buy a new domain | Secure, performance DNS query from [Cloudflare DNS](https://developers.cloudflare.com/dns/) |
| Developer platform | Pages and Pages Functions | Configure and deploy a static sites with minimal dynamic functionality | Landing Pages, Blogs, Simple e-commerce website for local business, Pet projects, Online CVs, ... |
| Developer platform | Workers | Full-stack applications | Front-end applications, Back-end applications, Serverless AI inference, Background jobs, ... |
| Storage | Workers KV | Key-value storage | API Gateway Configuration (or Service Routing), Feature Flags, Personalization (A/B Testing) |
| Storage | R2 | No egress object storage | Web assets (images, videos, ...), Large object (Machine Learning model's datasets, Analytics datasets, Log and event data), Strong consistency per object application |
| Storage | D1 | SQLite-based database | Relational data (user profiles, e-commerce product listings and orders, ...), Ad-hoc query, High ratio of reads to writes workloads |
| Storage | Durable Objects | Special kind of Worker which uniquely combines compute and storage | Real-time Collaborative application (Chat application, Game server), Consistent, transactional storage, Data Locality |
| Storage | Hyperdrive | Service which accelerates queries users make to existing database | Scale web application that is built on top of on-premise databases |
| Media | Images | Store, transform, optimize, deliver images at scale | Image hosting platforms, e-commerce platforms, ... |

Built-in products: no manual set up, no configuration

- Application Performance CDN, Load Balancing, ...
- Application Security: DDoS protection, WAF, ...
- Artificial Intelligence: Workers AI, AI Gateway, Vectorize, ...

## Built with Cloudflare

Here's how you can build one application using Cloudflare:

- Workers deployed the code.
- Storage group's products hosted the assets.
- Enhance the application performance by speeding up content delivery using CDN.
- Protect the application from malicious activity such as DDoS by configuring Web Application Firewall (WAF).
- Route traffic (Load Balancing, Waiting Room). These are paid products.

## Free tier limit

### Developer Platform group

<!-- TODO -->

### Storage group

<!-- prettier-ignore -->
| Feature | [Workers KV](https://developers.cloudflare.com/kv/platform/limits/) | [R2](https://developers.cloudflare.com/r2/platform/limits/) | [Durable Objects](https://developers.cloudflare.com/durable-objects/platform/limits/) | [D1](https://developers.cloudflare.com/d1/platform/limits/) |
| --- | --- | --- | --- | --- |
| Maximum storage per account | 1 GiB | 10 GiB | 5 GiB (SQLite-backed) + 50 GiB (KV-backed) | 5 GiB |
| Maximum size per value | 25 MiB/value | 5 TiB/object | 128 KiB/object | 500 MiB/database |
| Storage grouping name | Namespace | Bucket | Durable Object | Database |
| Consistency model | Eventual updates (~60s to be reflected) | Strong (read-after-write) | Serializable (with transactions) | Serializable (no replicas) / Causal (with replicas) |
| Supported APIs | Workers, HTTP/REST API | Workers, S3-compatible | Workers | Workers, HTTP/REST API |

## Source of truth

There are 2 source of truth when building your Worker. If you're building your project using Web UI, consider [Cloudflare dashboard](https://dash.cloudflare.com). If you're building your application programmatically, use C3 and Wrangler:

- C3, also known as NPM package `create-cloudflare` , is a CLI tool designed to help users set up and deploy applications to Cloudflare
- Wrangler, is a CLI tool to develop Worker locally and remotely, configure and delete projects. C3 install Wrangler when creating your project. Wrangler comes with a configuration file to manage your environment variables, bindings, routes, ...

> Remember to update Wrangler in your project, it doesn't update itself: `npm install wrangler@latest`

## Reference

- [Cloudflare's Docs "Choose a data or storage product"](https://developers.cloudflare.com/workers/platform/storage-options/)
- [2025-04-08, Cloudflare Blog's "Your frontend, backend, and database — now in one Cloudflare Worker"](https://blog.cloudflare.com/full-stack-development-on-cloudflare-workers/)
