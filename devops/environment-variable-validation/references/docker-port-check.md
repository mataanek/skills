# Quick Guide: Reading docker ps for Port Mapping

When you run `docker ps`, the PORTS column shows how container ports are mapped to the host.

## Format
`HOST_IP:HOST_PORT->CONTAINER_PORT/PROTOCOL`

## Examples from the session
```
0.0.0.0:8081->80/tcp
```
- Host port: 8081 (this is what you use in URLs from the host or WSL)
- Container port: 80 (internal to the container)
- Protocol: tcp

```
0.0.0.0:8899->8899/tcp
```
- Same port on host and container (8899)

## Common Patterns
- `0.0.0.0:HOST->CONTAINER/tcp` - accessible from all interfaces
- `127.0.0.1:HOST->CONTAINER/tcp` - only accessible from localhost
- `[::]:HOST->CONTAINER/tcp` - IPv6 version

## How to Use
1. Find your service in the `docker ps` output (look at the IMAGE or NAMES column)
2. Locate the PORTS column for that row
3. Extract the HOST_PORT (the number before the `->`)
4. Use `http://localhost:HOST_PORT` or `http://127.0.0.1:HOST_PORT` in your configuration

## Verification
After extracting the host port, test with:
```bash
curl -s http://localhost:<HOST_PORT>/<expected-endpoint>
```
Should return a successful response (not 404 Not Found).