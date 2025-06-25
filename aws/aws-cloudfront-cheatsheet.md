# AWS Cloudfront Cheatsheet

<!-- tl;dr starts -->

CloudFront is my most favorable cloud solution given by AWS Free-tier. However, it's not easy to learn.

<!-- tl;dr ends -->

## Free Tier quotas 

| Resource                  | Quota                |
| ------------------------- | -------------------- |
| Egress                    | 1 TiB/month  [^0]    |
| # of requests + responses | 10M/month            |
| CloudFront Functions      | 2M invocations/month |
| CloudFront KeyValueStore  | 2M reads/month, NOTE: write operations are NOT FREE [(1$/1000 write)](https://www.reddit.com/r/aws/comments/180vodz/comment/lqax3vf) |

[^0]: So good that make me crawl through its nightmare documentation.

## CloudFront distribution

### TWO types of istribution

You can either create:

- **Standard distribution:** one distribution per website. A standard distribution contains all the settings that you enable for you website/application:

  - Origin settings.
  - Cache behaviors.
  - Security settings.

- **Multi-tenent distribution:** one distribution per multiple websites. For each new website, create a "distribution tenent" that automatically inherits the defined values of its "source distribution":

  - Customize shared settings at source distribution.
  - Customize website-specific settings at distribution tenent.

  > Not appropriate for small scale application.

The following settings are for **standard distribution**:

## Origin settings

> AWS Free tier gives me 1 million requests to Elastic Load Balancing, but charges me for the amount of data associated with those requests. Not cool.

For example, my setup is a custom origin pointing to the Nginx instance running inside my AWS EC2 instance.

> [!CAUTION]
>
> If CloudFront is configured to connect to your origin over HTTPS, make sure one of the domain names in the certificate match the Origin Domain Name. Since my domain is managed by Cloudflare, I hope they do this automatically.

**Q: What will happen when you update the distribution, more specifically, changing the Origin domain?**

CloudFront immediately begins replicating the change to CloudFront edge locations. Until the config is updated, CloudFront continues to forward requests to the **previous origin**.

CloudFront will not repopulate cached objects on the new origin, but for the same requests, CloudFront continues to serve objects that are already in an edge cache until the TTL on each object expires, or until seldom-requested objects are evicted

> The time objects live in edge cache is independent of TTL, therefore you will need to warm your cache frequently, or just let it fetch new objects from your new custom origin.

<!-- prettier-ignore -->
| Setting | Description | Values | Free Tier quota |
| --- | --- | --- | --- |
| **Origin Domain Name** | DNS domain name of the origins where CloudFront will get objects from | - Amazon S3 bucket DNS<br>  - MediaStore container<br>  - MediaPackage endpoint<br>  - Amazon EC2 instance (**best choice**)<br>  - Elastic Load Balancing load balancer<br>  - Your own HTTP web server | - CloudFront: 100 domains/distribution[^1]<br/>ELB: 1M requests/month, **not free for compute and data resource usage**[^2] |
| **Protocol (custom only)** | The protocol that CloudFront uses when it establishes connections to origin servers | - HTTP only<br/>- HTTPS only<br/>- Match viewer: depend on viewer's protocol | Yes |
| **HTTP port (custom only)** | The HTTP port on which the custom origin listens | 80 (def), 443, 1024-65535 | Yes |
| **HTTPS port (custom only)** | The HTTPS port on which the custom origin listens | 80, 443 (default), 1024-65535 | Yes |
| **Minimum Origin SSL Protocol (custom only)** | The minimum TLS/SSL protocol that CloudFront uses when it establishes an HTTPS connection to your origin | Choose the latest TLS protocol that your origin supports (best practice) | Yes |
| **Origin path** | Request your content from a directory in origin server | - Origin domain: `example.com`<br/>- Origin path: `/production` (NO TRAILING SLASH)<br/>- CNAME: `www.example.com`<br/><br/>Example:<br/>- URL: `www.example.com/index.html`<br/>=> CloudFront: `example.com/production/index.html`<br/>- URL: `www.example.com/acme/index.html`<br/>=> CloudFront: `example.com/production/acme/index.html` | Yes |
| **Name** | A string uniquely identified the origin in this distribution<br/>When a custom cache behavior in addition to the default cache behavior is created, this name can be used to identify the origin that CloudFront will route request to when the request matches the path pattern for that cache behavior. | `my-server`, `remotelab`, ... | Yes |
| **Origin access (S3 only)** | Restrict access to an S3 bucket origin to only specific CloudFront distributions. | - Public<br/> - ... | Yes |
| **Custom header** | Add custom headers to request to origins. | `<header-name>=<header-value>` | - 30 custom headers/request<br/>- Max len header name: 256<br/>- Max len header value: 1783<br/>- Max len ALL headers name + value: 10240 |
| **Origin Shield** | It's an additional caching layer:<br>- Better cache hit ratio.<br>- Reduce origin's load => Reduce operation cost.<br>- Better network performance. | Enabled/Disabled | **No** |
| **Connection attempts** | The no. of times that CloudFront attempts to connect to the origin | 1, 2, 3 (default) | Yes |
| **Connection timeout** | The no. of seconds that CloudFront waits when trying to establish a connection to the origin | 1, 2, 3, ... 10 (default) | Yes |
| **Response timeout (custom/VPC-origin only)** | - # of s waiting for a response after forwarding a packet to the origin<br/>- # of s waiting after receiving a packet of a response from the origin and before receiving the next packet. | 1-60, 30 seconds (default) | Yes |
| **Keep-alive timeout (custom/VPC origin only)** | - # of s maintaining a connection to origin after CloudFront gets the last packet of a response. [^4] | 1-60, 5 seconds (default) | Yes |

Note for **Response timeout**:

- `GET`, `HEAD`: if origins no respond within this timeframe, drop the connection and try again (until Connection attempts run out)
- Other HTTP methods: if origins no respond within read's timeframe, drops the connection, doesn't try again.

Note for both **Response timeout** and **Keep-alive timeout**: **Update your origins so they reflects the distribution's timeout values.**

[^1]: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html#limits-web-distributions:~:text=Origins%20per%20distribution
[^2]: https://aws.amazon.com/elasticloadbalancing/pricing/

### Cache behavior settings

1 cache behavior = 1 rule/origin to process a given URL path pattern for files on your origins.

More origins = more cache behavior specifying explicit origin name.

<!-- prettier-ignore -->
| Settings | Description | Values |
| --- | --- | --- |
| Path pattern | The cache behavior applies to which request's URI | - `images/*.jpg`: JPG files inside direct or nested `images` directory<br/>- `images/*`: all files inside direct or nested `images` directory<br/>- `*.gif`: all GIF files<br/>- `a??.jpg`: All JPG files for which the file begins with `a` and is followed by exactly 2 other characters.<br/><br/>**NOTE:**<br/>- No trailing slash<br/>- Case sensitive<br/>- Accept alphanumeric and some characters `_ - . * $ / ~ " ' @ : +`, `&` returned as `&amp`<br/>- Caution when there are more than 1 cache behaviors pointing to the same file. 1 URI can match multiple cache behaviors via overlapped path patterns, lighter cache behaviors can bypass restriction imposed by stricter cache behaviors. | 
| Path normalization | Special characters (e.g. `//`, `..` ) are normalized | - `/a/b?c=1` => `/a/b*`<br/>- `/a/b/..c?=1` => `/a*` | 
| Origin/Origin group | The origin to which you want CloudFront to forward your requests (if distribution configures multiple origins) | `my-machine`, `remotelab`, ... | 
| Viewer protocol policy | Specify the protocol policy that viewers use to access your content in CloudFront edge locations | - HTTP and HTTPS<br/>- Redirect HTTP to HTTPS<br/>- HTTPS only | 
| Allowed HTTP methods | Specify the HTTPS methods that CloudFront will process and forward to origin servers | - GET, HEAD<br/>-GET, HEAD, OPTIONS<br/>- Others | 
| Field-level encryption | Some data fields can be encrypted | ... | 
| Cache HTTP methods | Cache request with HTTP method `OPTIONS` ? | Enabled | 
| Allow gRPC requests over HTTP/2 | Distribution can accept gRPC requests | Disabled | 
| Caching based on request headers | Fine-grained caching strategy based on the values of request headers| - None (no cache based on header, improve caching)<br/>- Allowlist and Allowlist Headers (only cache requests based **only** on the values of the specified headers)<br/>- All (no cache, send every request to origin) |
| Object caching and TTLs | Config different TTL settings | - Honor the origin header `Cache-Control`: Use Origin Cache Headers.<br/>- Minimum TTL.<br/>- Maximum TTL (used if origin **DOES ADD** `Cache-Control max-age`, `Cache-Control s-maxage` or `Expires` header)<br/>- Default TTL (used if origin **DOES NOT ADD** `Cache-Control max-age`, `Cache-Control s-maxage` or `Expires` header). [^3] | 
| Cookies forwarding | Fine-grained control of how cookies from viewers flows to origin server | - Don't forward cookies (S3 origin can't process cookies)<br/>- Allowlist (exact match or wildcards `*, ?`)<br/>- All<br/> | 
| Query string forwarding and caching | Fine-grained caching strategy based on the values of query string parameters | - **None:** Only 1 object is created for all different combinations of parameters<br/>- **Forward all, cached based on allowlist**: Only 1 or more parameters are honored in creating different cached objects<br/>- **Forward all, cache based on all:** Each unique combination of parameters create an unique cached object. | 
| Smooth Streaming | Whether to distribute media files in the MS Smooth Streaming format | No | 
| Restrict viewer access | Requests for objects matching the path pattern for a cache behavior must be sent via signed URLs or signed cookies created from a custom policy, issued by a trusted signer | Yes + choose AWS accounts as trusted signers (self, other accounts) [^4] | 
| Compress objects automatically | Auto compressed files of certain types (if viewers support them) | Yes |
| CloudFront event + Lambda function | Run a Lambda function when 1 or more CloudFront events occur. | - After CloudFront receives a request from a viewer<br/>- Before CloudFront forward a request to the origin<br/>- After CloudFront receives a response from the origin<br/>- Before CloudFront returns the response to the viewer |

[^3]: In my use case, I set everything to 10 year `315360000`.
[^4]: Very good if you want distributed private objects

### Distribution settings

<!-- prettier-ignore -->
| Settings | Description | Values | Free Tier Quota |
| --- | --- | --- |
| Price class | Reduce delivary price by excluding CloudFront's more expensive edge locations from distribution | Price Class 200 [^5] / Price Class All [^6] | Yes |
| AWS Web Application Firewall | Secure your web applications and APIs, block requests before reaching your origins | Enabled | Yes |
| CNAMEs + Custom SSL Certificate + Custom SSL client support | Replace the ugly-looking assigned DNS that CloudFront assigned to you with your custom domain | Add a CNAME for your custom domain in your authoritative nameservers (mine was Cloudflare's standard nameservers [^7]) | 100 CNAMEs/distribution [^8] |
| Security policy | - The minimum SSL/TLS protocol<br/>- THe ciphers that CloudFront use to encrypt the content that it returns to viewers | - Latest TLS version and use a cipher | Yes |
| Supported HTTP versions | - HTTP/2 ? => Viewers must support TLSv1.2 + SNI<br/>- HTTP/3 ? => Viewers must support TLSv1.3 + SNI | Try to use HTTP/3 and TLSv1.3 | Yes |
| Default root object | The object that will be returned when viewers accessing the root of your distribution<br/>E.g. `https://www.example.com/index.html`<br/>Optional, but it avoids exposing the content of your distribution<br/> | `index.html` (**DO NOT ADD LEADING FORWARD SLASH**)  | Yes |
| Logging + Log prefix + Cookie logging | CloudFront can log information about each request for an object and store the log files (keep in mind S3 doesn't process cookies) | Enabled all settings | Log if free, storing and accessing the log is NOT FREE |
| Enable IPv6 | CloudFront can respond to requests from IPv4 and IPv6 addresses | Disabled (can't use it if using signed URLs/signed cookies) | Yes |
| Distribution state | Indicating whether the distribution is enabled or disabled | - Enabled (It takes time for the changes to propagate to all CloudFront edge locations)<br/>- Disabled | Yes |
| Custom error pages + error caching | CloudFront return an object to the viewer (e.g. `404.html`, `50x.html`) when the custom origin returns an HTTP 4xx or 5xx status code to CloudFront. This object is cachable and have dedicated TTL | Better to set up a few simple HTML files | Yes |
| Geographic restrictions | Prevent users in selected countries from accessing your content | - Allowlist<br/>- Blocklist | Yes |

[^5]: https://aws.amazon.com/cloudfront/pricing/#:~:text=Price%20Class%20200
[^6]: https://aws.amazon.com/cloudfront/pricing/#:~:text=Price%20Class%20All
[^7]: https://developers.cloudflare.com/dns/nameservers/#standard-nameservers
[^8]: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-limits.html#limits-web-distributions:~:text=Alternate%20domain%20names%20%28CNAMEs%29%20per%20distribution

## CloudFront Functions

It's a serverless computing service using lightweight JS to handle high-scale, latency-sensitive CDN customization.

Here are some use cases and pros:

- Manipulate request/response header.
- Limited manipulation request/response body.
- Perform basic authentication and authorization.
- Generate HTTP Response at the edge location.
- Sub-ms startup times.
- Scalable to millions of reqs/second.
- Highly secure.
- Build, test, deploy code.

## CloudFront KeyValueStore

IT's a serverless key-value store specifically targeting CloudFront Functions, designed to meet the high-performance requirement.

Here are some use cases and pros:

- Global, low-latency.
- Secure: encryption at rest and during transit when calling API operations. Decryption in-memory.
- URL rewrites or redirects.
- A/B testing.
- Feature flags.
- Access authorization: no need to learn WAF, implement access control to allow/deny requests using data stored inside the store.
- Data source can be S3.

Data types:

- String.
- Byte-encoded string.
- JSON.

## FAQ

**Q: Does CloudFront fetch and cache new content from origin server?**

A:

- Pull-based caching: CloudFront doesn't automatically fetch and cache content from origin servers. Content is cached only when requested by real users.
- Per-edge caching: Each edge location caches independently.
- Cache key driven: Different URLs, query parameters, headers, create different cache entries.

**Q: How can I manipulate the request and responses that flow through CloudFront?**

A: Use **CloudFront Functions** associating with a CloudFront distribution to intercept requests/responses at CloudFront edge location.

## Reference

- [Distribution settings reference](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html)
