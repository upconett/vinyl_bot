### Запуск бота

Разархивируйте `res.zip` в директорию `creation/res/`!

Создайте виртуальное окружение, активируйте его
```bash
# Linux
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости
```bash
pip install -r requirements.txt
apt install ffmpeg
```

Создайте `config.yaml`, запишите туда:
```yaml
token: 'токен-вашего-бота'
logdir: 'путь-для-логов'
dbfile: 'название-файла-для-базы-данных.db'

admins:
  - тг-айди-админа (цифры)
  - тг-айди-другого-админа
```

Запустите бота
```bash
# Linux
source start.sh 

# Windows
.\start.ps1
```