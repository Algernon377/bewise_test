import logging
from logging.handlers import RotatingFileHandler

name = 'bewise_back'
debug_mode = False

logger = logging.getLogger(name)
logger.setLevel(logging.DEBUG)

# Создание объекта обработчика, который будет записывать логи в файл с ограничением по размеру
log_file = "logs/log_bewise_back_info.log"
backup_count_info = 10
max_log_size_info = 1024*1024*2
file_handler_info = RotatingFileHandler(log_file, maxBytes=max_log_size_info, backupCount=backup_count_info, encoding='utf-8')

log_file = "logs/log_bewise_back_error.log"
backup_count_error = 3
max_log_size_error = 1024*1024*3
file_handler_error = RotatingFileHandler(log_file, maxBytes=max_log_size_error, backupCount=backup_count_error, encoding='utf-8')

# Установка уровней логирования для обработчиков
file_handler_info.setLevel(logging.INFO)
file_handler_error.setLevel(logging.ERROR)
# Создание форматтера, определяющего, как будут выглядеть записи логов
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler_info.setFormatter(formatter)
file_handler_error.setFormatter(formatter)


# Добавление обработчика к логгеру
logger.addHandler(file_handler_info)
logger.addHandler(file_handler_error)
if debug_mode:
    cons_handler = logging.StreamHandler()
    cons_handler.setLevel(logging.DEBUG)
    cons_handler.setFormatter(formatter)
    logger.addHandler(cons_handler)