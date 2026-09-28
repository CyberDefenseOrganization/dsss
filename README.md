<div align="center">
  
<div>
  <img height=200 src="logo.png" alt="CDO Logo" />
</div>

# DSSS
**Damiens' Simple Scoring Suite**\
*A minimalist scoring engine for Red-Blue cyber competitions.*

[About](#about) •
[Deploying](#deploying) •
[Creating Checks](#creating-checks) •
[Screenshots](#screenshots)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


</div>

## About
**DSSS** is a bare-bones scoring engine for Red-Blue cyber competitions, [with a focus on simplicity, clarity, and frugality](https://suckless.org/). It intends to be as minimal and focused as possible, while being easy to configure and deploy.

## Deploying

### Local development dependencies
To deploy DSSS, it is required that both NodeJS and Python are installed and available in your system path, alongside both [npm](https://www.npmjs.com/) and [PDM](https://pdm-project.org/). This can be accomplished through the following on Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install nodejs npm pdm
```

Now it's time to clone the repo:
```bash
git clone https://github.com/CyberDefenseOrganization/dsss
cd dsss
```

Next, install the required frontend dependencies, and build the frontend:
```bash
cd frontend
npm install
npm run build
cd ..
```

Finally, you can install the dependencies for the backend and launch it:
```bash
pdm install
pdm run start --config "config.toml"
```

## Configuration

All competition settings and team/service definitions live in `config.toml`.

All paths resolved in the config are relative to the location of the TOML file.

An example config may look like:
```toml
[branding]
event_name_long = "Great Dane Defense Competition"
event_name_short = "GDDC"
organization_name_long = "Cyber Defense Organization"
organization_name_short = "CDO"
logo_path = "dsss/assets/shield.png"

[engine]
host = "0.0.0.0"
port = 8080
target_round_time = 35
num_worker_processes = 32
database_path = "rounds.db"

[admin]
username = "${DSSS_ADMIN_USERNAME:-admin}" # you can use environment variables in your configs!
password = "${DSSS_ADMIN_PASSWORD}"

[defaults]
timeout_seconds = 20
username = "${DSSS_SCORING_USERNAME:-scoring}"
password = "${DSSS_SCORING_PASSWORD}"

[[services]]
name = "Router SSH"
points = 10

[services.check]
type = "ssh"
host = "172.16.{subnet}.1"

[[teams]]
name = "Team1"
variables = { subnet = 21 }

[[teams]]
name = "Team2"
variables = { subnet = 22 }
```

The `[[services]]` definition is shared between all teams, though each team is given it's own unique instance of the check object. In practice this means that teams do not have to be uniform:

```toml
[[teams]]
name = Team3

[[teams.services]]
name = "Router SSH"
points = 15

[teams.services.check]
port = 2222
```

## Creating Checks
Checks are simply classes that inherit from either the `AsyncCheck`, or `SyncCheck` base classes, and implement a `check()` method that returns: `(success: bool, message: str)`.

Checks can be added under `/dsss/checks/`, and are automatically discovered. The check TOML schema is automatically derived from signature of the checks `__init__` method, and validated using Pydantic.

Below is an example of what a check may look like:
```python
from typing import Annotated
from pydantic import Field

from dsss.checks.base import AsyncCheck, Host, Port, Timeout

class MyCheck(AsyncCheck):
    def __init__(
        self,
        host: Host,
        port: Port = 1234,
        timeout_seconds: Timeout = 10,
        retries: Annotated[int, Field(ge=0)] = 2,
    ) -> None:
        super().__init__(host, port, timeout_seconds)
        self.retries = retries

    async def check(self) -> tuple[bool, str | None]:
        return (True, None)
```

## Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/726908e5-5600-4361-9de8-874728fee03e" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3076084c-a1bb-4597-84bb-fd183df9d2d0" />
