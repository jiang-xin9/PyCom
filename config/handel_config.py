import os, sys, datetime

Base_Path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '\..')
sys_ = os.path.realpath(os.path.dirname(sys.argv[0]))
LogTime = datetime.datetime.now().strftime("%H_%M_%S")

command_config = os.path.join(Base_Path, 'config', 'fast_btn_config.ini')



