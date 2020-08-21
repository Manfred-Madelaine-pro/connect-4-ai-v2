from conf.global_config import *

import back


class Connect_4_AI:
	def __init__(self, global_conf={}):
		main_args = global_conf['main'].values()
		back_model = back.Model(*main_args)


if __name__ == '__main__':
	config_file = "conf/config.yml"
	global_conf = global_config(config_file)
	
	Connect4_AI(global_conf)