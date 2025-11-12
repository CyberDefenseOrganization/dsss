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

## Getting Started

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

## Screenshots
![image](https://github.com/user-attachments/assets/a409f146-c2b5-46f2-aae6-2007e7216910)
