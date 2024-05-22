import configparser
from functions.send_singer import SignalEmitter


class ConfigReader:

    def __init__(self, file_path):
        """
        初始化 ConfigReader 对象。

        :param file_path: INI 配置文件的路径
        """
        self.config = configparser.ConfigParser()
        self.file_path = file_path
        self._read_config()
        self.signal_emitter = SignalEmitter()

    def _read_config(self):
        """
        读取配置文件。
        """
        try:
            self.config.read(self.file_path)
        except Exception as e:
            self.signal_emitter.send_signal(f"Failed to file: {e}")

    def get_value(self, default=None):
        """
        获取字符串类型的配置数据。

        :param section: 配置段的名称
        :param option: 配置项的名称
        :param default: 如果配置项不存在，则返回的默认值
        :return: 配置项的值，或者默认值
        """
        try:
            commands = []
            for section in self.config.sections():
                for key in self.config[section]:
                    commands.append(self.config[section][key])
            return commands
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default


# if __name__ == '__main__':
#     config_reader = ConfigReader('fast_btn_config.ini')
#     print(config_reader.get_value())
