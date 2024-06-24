from apscheduler.schedulers.asyncio import AsyncIOScheduler
import subprocess


scheduler = AsyncIOScheduler()


def delete_old_files():
    for dir in ['img/', 'video/', 'users_video/', 'audio/']:
        directory = 'creation/' + dir
        try:
            command = f'find {directory} -type f -mtime +1 -exec rm {{}} \\;'
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Файлы старше 24 часов в директории {directory} успешно удалены.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def start_scheduler():
    scheduler.add_job(delete_old_files, 'interval', hours=24) 
    scheduler.start()
