# Design REST API Best Practices

<!-- tl;dr starts -->

One of the best design decisions that you will make is having a strong and consistent REST resource naming strategy.

<!-- tl;dr ends -->

## The THREE characteristics of REST resource

1. **A resource can be a Singleton or a Collection**
1. **A resource may contain Sub-collection resources, a Sub-collection resource can also have Singleton resources**
1. **Using URI to address REST resource**

```
/customers                                        # collection resource
/customers/{customer-id}/accounts                 # sub-collection resource
/customers/{customer-id}/accounts/{account-id}    # singleton resource
```

REST API designers should create URIs that convey a **REST API resource model** to clients of the API.

## THREE archetypes of a resource

- Document: **object instance, database record**. Use the "object" or "row" as the resource in **singular** form, use "object field" or "database column" as GET filter.
- Collection: **server-managed**. Client propose new resource to add, Collection choose whether to create a new resouce (a new URI as well) or not. Each collection can be in two forms:
  - Primary collection.
  - Secondary collection: it's a sub-collection of Primary collection.
- Store: **client-managed directory**. Store resource put resources in, get them back out, decide when to delete them. A store **never** generate new URIs, instead each stored resource has a URI and this URI is chosen by the client.

> **NOTE:** The store resource archetype is rarely observed in practice.

```txt
/users                            # collection
/customers                        # collection
/users/{id}/posts                 # collection
/customers/{id}/accounts          # collection

/about-us                         # document
/contact-us                       # document
/users/{id}/status                # document
/users/{id}/profile               # document

/users/{id}/playlists             # store
```

## FOUR-step process of REST API Design Enginerring

Or "how to apply REST principles in the application design process?"

### Step 1: Object Modeling

_Definition:_ Identify the object that will be presented as resources. Identify the unique identifier for each object.

```
# network-based application
devices
routers
modems
switches
...

# 2 categories: devices and configurations
# A config can be A sub-collection of A device.
# ONE device can have MANY configuration.

# `id` integer/UUID as unique identifier
```

### Step 2: Create Model URIs

_Definition:_ Focus on the relationship between resources and their sub-resources.

> **TERM:** A resource URI can be called an **API endpoint**.

```
# network-based application

# A device is a top-level resource
# A configuration is a sub-resource under the device

/devices
/devices/{id}

/configurations
/configurations/{id}

/devices/{id}/configurations
/devices/{id}/configurations/{id}
```

### Step 3: Determine resource represenations

_Definition:_ What's the MIME type of your HTTP Response Body? Nowadays, most representations are defined in **JSON**.

> **XML** used to be in the game but not anymore.

#### 3.1. `/devices` - A Collection resource of Device

```json
{
  "devices": {
    "size": "2",
    "link": {
      "rel": "self",
      "href": "/devices"
    },
    "device": [
      {
        "id": "12345",
        "link": {
          "rel": "self",
          "href": "/devices/12345"
        },
        "deviceFamily": "apple-es",
        "OSVersion": "10.3R2.11",
        "platform": "SRX100B",
        "serialNumber": "32423457",
        "connectionStatus": "up",
        "ipAddr": "192.168.21.9",
        "name": "apple-srx_200",
        "status": "active"
      },
      {
        "id": "556677",
        "link": {
          "rel": "self",
          "href": "/devices/556677"
        },
        "deviceFamily": "apple-es",
        "OSVersion": "10.3R2.11",
        "platform": "SRX100B",
        "serialNumber": "6453534",
        "connectionStatus": "up",
        "ipAddr": "192.168.20.23",
        "name": "apple-srx_200",
        "status": "active"
      }
    ]
  }
}
```

Collection resource only contains the most important information about its Singular resources.

This will keep the size of the HTTP Response Body (payload) small, therefore improve the performance of the API.

#### 3.2. `/devices/{id}`: a Singular resource of Device

```json
{
  "id": "12345",
  "link": {
    "rel": "self",
    "href": "/devices/12345"
  },
  "deviceFamily": "apple-es",
  "OSVersion": "10.0R2.10",
  "platform": "SRX100-LM",
  "serialNumber": "32423457",
  "name": "apple-srx_100_lehar",
  "hostName": "apple-srx_100_lehar",
  "ipAddr": "192.168.21.9",
  "status": "active",
  "configurations": {
    "size": "2",
    "link": {
      "rel": "self",
      "href": "/configurations"
    },
    "configuration": [
      {
        "id": "42342",
        "link": {
          "rel": "self",
          "href": "/configurations/42342"
        }
      },
      {
        "id": "675675",
        "link": {
          "rel": "self",
          "href": "/configurations/675675"
        }
      }
    ]
  },
  "method": [
    {
      "href": "/devices/12345/exec-rpc",
      "rel": "rpc"
    },
    {
      "href": "/devices/12345/synch-config",
      "rel": "synch device configuration"
    }
  ]
}
```

Each resource, be that a Singular or a Collection, should contain at least one link (i.e. to itself `"href": "/configurations"`). A primary collection can have extra links to its secondary collection (configurations, methods).

> You can say this REST API is HATEOAS-driven. A REST API that return a HTML file with anchor tags is also HATEOAS-driven.

#### 3.3. `/configurations`: a Collection resouce of Configuration

```json
{
  "configurations": {
    "size": "20",
    "link": {
      "rel": "self",
      "href": "/configurations"
    },
    "configuration": [
      {
        "id": "42342",
        "link": {
          "rel": "self",
          "href": "/configurations/42342"
        }
      },
      {
        "id": "675675",
        "link": {
          "rel": "self",
          "href": "/configurations/675675"
        }
      }
      // ... more configurations would follow
    ]
  }
}
```

As you can see, there are 20 configurations for various devices. But there are only 2 configurations for each device.

#### 3.4. `/configurations/{id}`: a Singular resource of Configuration

```json
{
  "id": "42342",
  "link": {
    "rel": "self",
    "href": "/configurations/42342"
  },
  "content": "…",
  "status": "active",
  "links": [
    {
      "rel": "very big raw configuration script",
      "href": "/configurations/42342/raw"
    }
  ]
}
```

It includes all possible information about a Configuration, including a link relevant links. It is also called the resource from the _primary collection_.

#### 3.5. `/devices/{id}/configurations`: a Collection resource of Configuration under a Singular collection of Device

```json
{
  "configurations": {
    "size": "2",
    "link": {
      "rel": "self",
      "href": "/devices/12345/configurations"
    },
    "configuration": [
      {
        "id": "53324",
        "links": [
          {
            "rel": "self",
            "href": "/devices/12345/configurations/53324"
          },
          {
            "rel": "detail",
            "href": "/configurations/53324"
          }
        ]
      },
      {
        "id": "333443",
        "links": [
          {
            "rel": "self",
            "href": "/devices/12345/configurations/333443"
          },
          {
            "rel": "detail",
            "href": "/configurations/333443"
          }
        ]
      }
    ]
  }
}
```

Representations can have extra links:

- one acts as its direct representation inside sub-collection: `/devices/12345/configurations/53324`
- one acts as its location in the primary collection: `/configurations/53324`

#### 3.6. `/devices/{id}/configurations/{id}`: a Singular resource of Configuration under a Singular resource of Device

```json
{
  "id": "11223344",
  "link": {
    "rel": "self",
    "href": "/devices/12345/configurations/11223344"
  },
  "content": "…",
  "status": "active",
  "links": [
    {
      "rel": "detail",
      "href": "/configurations/11223344"
    },
    {
      "rel": "raw configuration content",
      "href": "/configurations/11223344/raw"
    }
  ]
}
```

Either it have the exactly representation as of [the top-level Singular resource of Configuration](#34-configurationsid-a-singular-resource-of-configuration) or you may mask a few fields,

### Step 4: Assigning HTTP Methods

After deciding [all resource URIs](#step-2-create-model-uris) and [their representation](#step-3-determine-resource-represenations), let's decide the application's possible operation and map those operations to the resource URIs.

E.g. A user can make CRUD operations on devices from the network, on configurations on each device

```md
# browse all devices or configurations

HTTP GET /devices
HTTP GET /configurations

HTTP GET /devices?size=10&page=1 # pagination, filtering
HTTP GET /configurations?size=5?page=2 # pagination, filtering

# browse a single device or a single configuration

HTTP GET /devices/{id}
HTTP GET /configurations/{id}

# browse all configurations under a single device

HTTP GET /devices/{id}/configurations

# browse a single configuration under a single device

HTTP GET /devices/{id}/configurations/{id}

# create a device or configuration

HTTP POST /devices
HTTP POST /configurations

NOTE: The HTTP POST Request Body payload should not contain `id` attribute, that's for server to decide

A successful response should be `201 Created`

# update a device or configuration based on its unique identifier

HTTP PUT /devices/{id}
HTTP PUT /configurations/{id}

A successful response should be `200 OK`

# apply a configuration under a device

HTTP PUT /devices/{id}/configurations

# remove a configuration from a device

HTTP DELETE /devices/{id}/configurations/{id}

# remove a device or configuration

HTTP DELETE /devices/{id}
HTTP DELETE /configurations/{id}

If the deletion operation is asynchronous:

- The server acknowledge the delete request but places it in a queue for later processing.
- The deletion hasn't actually occured yet when the response is sent.
- The status code `202 Accepted` indicates "I've received your request and will process it later", usually the response body will include a task id that can be tracked for success/failure status.
- The resource may continue to exist for some time after the response.

If the deletion operation is synchronous:

- The server completes the deletion before sending the response.
- The resource has been deleted permanently.
- There are 2 appropriate status codes:
  - `200 OK` if the response body includes information about the deleted resource.
  - `204 No Content` if there is no response body.
```

## SIX real-life example practices in consistency

1. Use forward slash `/` to indicate hierarchical relationships. DO NOT use trailing forward slash `/`:

   ```
   /users/                           # bad! no trailing forward slash

   /users                            # good
   /users/{id}                       # good
   /users/{id}/comments              # good
   ```

1. Use hyphens `-` to improve readability. DO NOT use underscores `_` .

   ```
   /devicemanagement/manageddevices    # bad
   /deviceManagement/managedDevices    # bad

   /device-management/managed-devices  # good
   ```

1. Use ALL lowercase letters. DO NOT use `UPPERCASE`. `Capitalize` or `camelCase`.

   ```
   /My-Folder/My-Doc               # bad
   /MY-FOLDER/MY-DOC               # bad
   /myFolder/myDoc                 # bad

   /my-folder/my-doc               # good
   ```

1. Use query components to filter Collection resource. DO NOT create new URI.

   ```
   /device-management/managed-devices/usa-region     # bad

   /device-management/managed-devices?region=USA     # good
   ```

1. DO NOT use file extensions

   ```
   /device-management/managed-devices.xml            # bad

   /device-management/managed-devices                # good
   ```

1. Use a noun with an implicit associated action. DO NOT use CRUD function name, or in general, **DO NOT use verbs in the URI**.

   ```
   /device-management/managed-devices/{id}/scripts/{id}/execute      # bad

   /device-management/managed-devices/{id}/scripts/{id}/status       # good
   ```

   > **NOTE:** Google Cloud introduces an API design that use colon `:` which is called custom method.

1. There are people designing REST API using OO concept for more granularity

   ```
   /domain/resource/operation/qualifier/parameter
   ```

## My experience

1. Think about your use cases carefully before designing. What is the insight/analysis that can be derived from data that you want to show to your users?

## References

- [2023-11-04, Lokesh Gupta's "REST API URI Naming Conventions and Best Practices"](https://restfulapi.net/resource-naming/)
- [2023-11-06, Lokesh Gupta's "How to Design a REST API"](https://restfulapi.net/rest-api-design-tutorial-with-example/)
