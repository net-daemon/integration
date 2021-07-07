# NetDaemon integration

This is a helper integration for NetDaemon, this is not NetDeamon it self, for that you want [net-daemon/netdaemon](https://github.com/net-daemon/netdaemon), this is not required to run NetDaemon.

## Features

- Service to create a persistent entity
- Service to update a persistent entity
- Service to remove a persistent entity
- Service to register custom services to use in NetDaemon
- Service to force a reload of NetDaemon

For now only the following platforms are supported:

- `binary_sensor`
- `sensor`
- `switch`
- `select`

## Installation

1. Add `https://github.com/net-daemon/integration` with the category "integration" as a custom repository in [HACS](https://hacs.xyz/docs/faq/custom_repositories)
2. Install it in HACS
3. Clear browser cache (no need to restart Home Assistant)
4. Go to Configuration -> Integrations -> + -> Search for "NetDaemon"
