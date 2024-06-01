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

    def _read_config(self):
        """
        读取配置文件。
        """
        try:
            self.config.read(self.file_path)
        except Exception as e:
            # print(f"Failed to read config file: {e}")
            self.signal_emitter.error_signal(f"Failed to file: {e}")

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
            SignalEmitter.error_signal(f"get value Failed")
            return default

    def save_data(self, section, data):
        """
        保存数据到配置文件。

        :param section: 配置段的名称
        :param data: 要保存的数据，列表类型
        """
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)

            # 清除已有的数据
            for key in list(self.config[section]):
                self.config.remove_option(section, key)

            # 保存新的数据
            for i, command in enumerate(data, start=1):
                self.config.set(section, f'command{i}', command)

            with open(self.file_path, 'w') as configfile:
                self.config.write(configfile)
            SignalEmitter.success_signal(f"Configuration saved successfully.")
            # self.signal_emitter.send_signal("Configuration saved successfully.")
        except Exception as e:
            # print(f"Failed to save configuration: {e}")
            SignalEmitter.error_signal(f"Failed to save configuration: {e}")

# if __name__ == '__main__':
#     config_reader = ConfigReader('fast_btn_config.ini')
#     print(config_reader.get_value())
