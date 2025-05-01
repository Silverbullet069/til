# My Ultimate Web Tech Stack

<!-- tl;dr starts -->

I've found a solid web tech stack for all of my projects from now on.

<!-- tl;dr ends -->

## Overview

<!-- prettier-ignore -->
| Use Case | Product | Short description |
| --- | --- | --- |
| Static Site Generator (SSG) | [11ty](https://github.com/11ty/eleventy) | <ul><li>Simple yet mature, Production-ready</li><li>No component-based template by default</li><li>[Small `node_modules`, fast installation](https://www.11ty.dev/docs/performance/#installation-performance)</li><li>[Fast build](https://www.11ty.dev/docs/performance/#build-performance)</li><li>[Support partial hydration](https://www.11ty.dev/docs/plugins/is-land/) like Astro</li><li>[Optimize image on-request](https://www.11ty.dev/docs/performance/#performance-tips)</li><li>[Support incremental builds](https://www.11ty.dev/docs/performance/#performance-tips)</li></ul> |
| Content Management System (CMS) | [Decap CMS](https://github.com/decaporg/decap-cms?tab=readme-ov-file) | <ul><li>Git-based CMS, hosted content on GitHub</li><li>Admin panel hosted on Netlify</li></ul> |
| Cloud provider and their products | [Cloudflare Developer Platform](https://developers.cloudflare.com) - Zero Trust, Workers, Workers KV, R2, D1 | <ul><li><a href="https://free-for.dev/#/?id=major-cloud-providers">Most generous Free tier</a></li><li><a href="https://www.cloudflare.com/network/">Three data centers in Vietnam (HN, DN, HCM)</a></li><li>Steep learning curve</li></ul> |
| CI/CD platform that works with cloud provider | [GitHub Actions](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/) | <ul><li><a href="https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions">1GB of storage, 3000 minutes per month for Pro users</a></li><li>Deeply integrate with Git and GitHub</li></ul> |

This is a non-exhaustive list, I will include/update more tech in the current stack.
