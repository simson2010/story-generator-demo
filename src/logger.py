import logging
import sys
import os
from typing import Optional

class Logger:
    def __init__(
        self,
        name: str = "root",
        log_file: str = "./log/app.log",
        level: int = logging.INFO,
        fmt: Optional[str] = None,
        console: bool = True
    ):
        """
        初始化日志记录器
        :param name: 日志记录器名称
        :param log_file: 日志文件路径
        :param level: 日志级别 (logging.DEBUG/INFO/WARNING/ERROR/CRITICAL)
        :param fmt: 日志格式字符串
        :param console: 是否输出到控制台
        """

        # 在__init__方法中添加目录创建逻辑
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加handler
        if self.logger.handlers:
            return

        # 设置默认格式
        if not fmt:
            fmt = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

        formatter = logging.Formatter(fmt)

        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # 控制台处理器
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    @staticmethod
    def debug(msg: str):
        logging.debug(msg)

    @staticmethod
    def info(msg: str):
        logging.info(msg)

    @staticmethod
    def warn(msg: str):
        logging.warning(msg)

    @staticmethod
    def error(msg: str):
        logging.error(msg)

# 默认日志记录器实例
LOG = Logger().logger