# NetDaemon integration

This is a helper integration for NetDaemon, this is not NetDeamon it self, for that you want [net-daemon/netdaemon](https://github.com/net-daemon/netdaemon), this is not required to run NetDaemon.

## Features

- Service to create a persistent entity
- Service to update a persistent entity
- Service to remove a persistent entity
- Service to register custom services to use in NetDaemon
- Service to force a reload of NetDaemon

For now only the folowing platforms are supported:

- `binary_sensor`
- `sensor`
- `switch`
- `climate`

## Installation

1. Add `https://github.com/net-daemon/integration` with the category "integration" as a custom repository in [HACS](https://hacs.xyz/docs/faq/custom_repositories)
2. Install it in HACS
3. Clear browser cache (no need to restart Home Assistant)
4. Go to Configuration -> Integrations -> + -> Search for "NetDaemon"

## Use

Within your netdaemon app call into `ha.CallService` with one of the methods defined in [services.yaml](custom_components/netdaemon/services.yaml) - you can specify the appropriate fields via anonymous parameters as in the example below, noting that the domain should be set to "netdaemon":

```csharp
public MyApp(IHaContext ha, ILogger<HelloWorldApp> logger)
{
     ha.CallService("netdaemon", "entity_create", data: new {entity_id ="sensor.scott", state = "present", description = "My sensor"});
...
}
```

