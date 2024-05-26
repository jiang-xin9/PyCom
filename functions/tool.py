import csv


class Tool:

    def read_csv_by_command(self, file_path):
        """
        读取 CSV 文件，并按列返回数据。

        :return: 一个字典，键为列名，值为对应列的数据列表
        """
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row for row in reader]

    def clear_widget(self, widget):
        """传入控件，清空内容"""
        widget.clear()

# 使用示例
# if __name__ == '__main__':
#     csv_reader = Tool()
#     result = csv_reader.read_csv_by_command('../config/instruction_config.csv')
