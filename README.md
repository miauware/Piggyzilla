# Piggyzilla
<p align="center">


[![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)
[![Babel](https://img.shields.io/badge/Babel-F9DC3E?logo=babel&logoColor=000)](#)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-%2338B2AC.svg?logo=tailwind-css&logoColor=white)](#)
[![DaisyUI](https://img.shields.io/badge/DaisyUI-5A0EF8?logo=daisyui&logoColor=fff)](#)



<table>
<tr>
<td>
<img src="https://raw.githubusercontent.com/miauware/miauware/master/assets/poiting.png" width=70>
</td>
<td>
 Piggyzilla: a localhost money manager with multi language support
</td>
</tr>
</table>

> ❗ **ATTENTION**:<br>
>**⚠️ need tailwind cli ,uv, python babel and jinja installed from your  linux distribuition**

on arch based distros :
```bash
sudo pacman -S python-babel  python-jinja
npm install -g tailwindcss @tailwindcss/cli
```

Continue the installation and use with:


```bash
git clone https://github.com/miauware/Piggyzilla.git
cd Piggyzilla
./buildcss.sh
uv run pytest
uv run main.py
```