# Swaprum airdrop claimer
Claims swaprum.finance/free-tokens airdrop!

### Запуск под Ubuntu
- Обновите систему:
```bash
sudo apt update && sudo apt upgrade -y
```
- Установите [git](https://git-scm.com/download/linux) и screen:
```bash
sudo apt install screen git -y
```
- Установите Python 3.11 и зависимости для библиотеки web3:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-dev build-essential libssl-dev libffi-dev -y
ln -s /usr/bin/python3.11/usr/bin/python
```
- Установите [Poetry](https://python-poetry.org/docs/):
```bash
curl -sSL https://install.python-poetry.org | python -
export PATH="/root/.local/bin:$PATH"
```
- Склонируйте этот репозиторий, после чего перейдите в него:
```bash
git clone https://github.com/AlenKimov/swaprum_claimer.git
cd swaprum_claimer
```
- Следующие команды установят требуемые библиотеки и запустят скрипт:
```bash
poetry update                
poetry run python start.py
```