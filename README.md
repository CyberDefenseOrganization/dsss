<div align="center">
  
<div>
  <img height=200 src="logo.png" alt="DSSS Logo" />
</div>

# DSSS
**Damiens' Simple Scoring Suite**


[About](#about) •
[Deploying](#deploying) •
[Creating Checks](#creating-checks) •
[Supported Platforms](#supported-platforms) •
[Demo](#demo)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


</div>

## About
**DSSS** is a bare-bones scoring engine for Red-Blue cyber competitions, [with a focus on simplicity, clarity, and frugality](https://suckless.org/). It intends to be as minimal and focused as possible, while being easy to configure and deploy.


## Components

```
dsss/
├── dsss/       # python backend
└── frontend/   # react frontend
```

## Deploying

### Dependencies 
To deploy DSSS, it is required that both NodeJS and Python are installed and available in your system path, alongside both [npm](https://www.npmjs.com/) and [PDM](https://pdm-project.org/). This can be accomplished through the following on Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install nodejs npm pdm
```

### Backend
```bash
gt clone https://github.com/CyberDefenseOrganization/dsss
cd dsss
pdm install
pdm run start
```

### Frontend
```bash
gt clone https://github.com/CyberDefenseOrganization/dsss
cd dsss/
npm install
npm run dev
```

## Creating Checks
All checks in DSSS are simply subclasses of the `BaseCheck` class, implementing the constructor as well as an asynchronous `check` method.

Below is an example of what the **Random** check looks like.
```python
class RandomCheck(BaseCheck):
  liklihood: float

  def __init__(self, liklihood: float = 0.5) -> None:
    self.liklihood = liklihood
    super().__init__("0.0.0.0", None, 10)

  @override
  async def check(self) -> tuple[bool, str | None]:
    if random.random() > 1 - self.liklihood:
      return (True, "lucky")
    else:
      return (False, "unlucky")
```
To extend DSSS with your own custom checks, simply create a file in `./dsss/checks/` containing a class that inherits from `BaseCheck`. Worth noting is that all checks are ran concurrently, so try to avoid blocking if possible.

## Screenshots
![image](https://github.com/user-attachments/assets/a409f146-c2b5-46f2-aae6-2007e7216910)
