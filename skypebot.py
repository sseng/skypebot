# -*- coding: UTF8 -*-
#verified working with python 2.7.8

import Skype4Py
import time
import re
import subprocess
import os

class SkypeBot:
	def __init__(self):
		self.skype = Skype4Py.Skype(Events=self)	
		self.skype.Attach()
    
	def MessageStatus(self, message, status):
		if status == Skype4Py.cmsReceived or status == Skype4Py.cmsSent:
			splitMessage = message.Body.split()
			for command, function in self.commands.items():
				if command in splitMessage[0]:
					function(self, message)
					break

	def command_open_notepad(self, message):
		notepad = os.path.join( 'c:\\', 'windows', 'system32', 'notepad.exe')
		subprocess.check_output(notepad)
	
	def command_test(self, message):
		message.Chat.SendMessage('test from {0}' .format(message.FromDisplayName))

	def command_say(self, message):
		splitMessage = message.Body.split(' ',1)
		messageText = splitMessage[1]
		message.Chat.SendMessage(' '+messageText)	
	
	def command_check_uin(self, message):
		msg = message.Body.encode('utf-8').lower()		
		parameter = msg.split()
		parameter_length = len(parameter)
		parameter_max = 3
		
		if is_valid_param_size(parameter_length, parameter_max, message):			
			server = parameter[1]
			uin = parameter[2]
			
			if is_valid_int(uin):
				uin = int(uin)
			
				if is_valid_server(server, message) and is_valid_uin(server, uin, message):					
					message.Chat.SendMessage('{0} is a valid UIN' .format(uin))
			else:
				send_message('Error: invalid uin value: {0}' .format(uin), message)
	
	def command_level_exp(self, message):
		msg = message.Body.encode('utf-8').lower()
		parameter = msg.split()
		
		level = parameter[1]
		print '\nlevel : %s' % level
		
		if is_valid_level(level, message):		
			exp = level_xp_info['level %s' %level]
			print '\nexp : %s' % exp
			send_message('level {0} requires {1} experience' .format(level, exp), message)
	
	def command_set_currency(self, message):
		msg = message.Body.encode('utf-8').lower()		
		parameter = msg.split()
		parameter_length = len(parameter)
		parameter_max = 4
		
		if is_valid_param_size(parameter_length, parameter_max, message):			
			server = parameter[1]
			uin = parameter[2]
			currency = parameter[3]
			
			if is_valid_int(currency):
				currency = int(currency)			
		
				if is_valid_server(server, message) and is_valid_uin(server, uin, message) and is_valid_currency(currency):
					apitool_ban_user(server, uin)
					apitool_set_userinfo_by_id(server, uin, currency)
					apitool_unban_user(server, uin)
					send_message('Currency command completed.', message)				
			else:
				send_message('Error: Invalid currency value: {0}' .format(currency), message)	
	
	def command_set_level(self, message):
		msg = message.Body.encode('utf-8').lower()		
		parameter = msg.split()
		parameter_length = len(parameter)
		parameter_max = 4
		
		if is_valid_param_size(parameter_length, parameter_max, message):			
			server = parameter[1]
			uin = parameter[2]
			arg1 = parameter[3]
			
			if is_valid_level(arg1, message):
				arg1 = int(arg1)			
		
				if is_valid_server(server, message) and is_valid_uin(server, uin, message):
					apitool_ban_user(server, uin)
					
					apitool_unban_user(server, uin)
					send_message('set level command Completed', message)				
			else:
				send_message('Error: Invalid level value: {0}' .format(currency), message)

	def boba(self, message):
		message.Chat.SendMessage('Sorry no Boba!')
	
	def command_cmds(self, message):
		message.Chat.SendMessage(
			'\ncommands start with !\n Current commands:\n'
			'\ntest'
			'\nuin #'
			'\ncurrency server uin #'
			'\nsay <string>'
			'\nlevelexp #1-60'
		)
		
	commands = {
		'!test!' : command_test,
		'!say' : command_say,
		'!currency' : command_set_currency,		
		'!levelexp' : command_level_exp,
		'!commands' : command_cmds
	}

level_xp_info = {
	'level 1' : 0,
	'level 2' : 65,
	'level 3' : 140,
	'level 4' : 231,
	'level 5' : 330,
	'level 6' : 422,
	'level 7' : 542,
	'level 8' : 702,
	'level 9' : 916,
	'level 10' : 1199,
	'level 11' : 1567,
	'level 12' : 2038,
	'level 13' : 2606,
	'level 14' : 3315,
	'level 15' : 4237,
	'level 16' : 5401,
	'level 17' : 6839,
	'level 18' : 8586,
	'level 19' : 10680,
	'level 20' : 13162,
	'level 21' : 16077,
	'level 22' : 19474,
	'level 23' : 23406,
	'level 24' : 27931,
	'level 25' : 33113,
	'level 26' : 39021,
	'level 27' : 45730,
	'level 28' : 53322,
	'level 29' : 61887,
	'level 30' : 71522,
	'level 31' : 82334,
	'level 32' : 94439,
	'level 33' : 107963,
	'level 34' : 123044,
	'level 35' : 139832,
	'level 36' : 158490,
	'level 37' : 179197,
	'level 38' : 202147,
	'level 39' : 227552,
	'level 40' : 255643,
	'level 41' : 286672,
	'level 42' : 320913,
	'level 43' : 358665,
	'level 44' : 400254,
	'level 45' : 446036,
	'level 46' : 496398,
	'level 47' : 551762,
	'level 48' : 612588,
	'level 49' : 679378,
	'level 50' : 752679,
	'level 51' : 833087,
	'level 52' : 921251,
	'level 53' : 1017879,
	'level 54' : 1123743,
	'level 55' : 1239684,
	'level 56' : 1366619,
	'level 57' : 1505548,
	'level 58' : 1657560,
	'level 59' : 1823843,
	'level 60' : 2005691
}

def main():
	bot = SkypeBot()
	
	#print 'name : ', skype.CurrentUser.FullName
	
	while True:
		print '|--------------------------------------|'
		print '|    Skype Bot is currently Running    |'
		print '|--------------------------------------|'
		raw_input()
		time.sleep(1.0)
		
def is_valid_int(input):
	if input.isdigit():
		return True
	return False
	
def is_valid_currency(amount):
    max = 99999999

    if amount > 0 and amount < max:
        return True
    return false

def is_valid_uin(server, uin, message):
	result_uin = apitool_get_account_by_id_full_info(server, uin)
	error = 'Error: {0} is an invalid UIN' .format(uin)
	
	print result_uin
	print type(result_uin)
	
	if 'no results' in result_uin:
		send_message(error, message)
		return False
	
	print 'uin {0} is valid' .format(uin)
	return True
	
def is_valid_server(server, message):
	valid_servers = ['test1', 'test4', 'test5', 'trunk', 'sean', 'seth']
	error = 'Error: invalid server : {0} ' .format(server)
	
	if str(server) in valid_servers:
		return True

	send_message(error, message)
	return False
	
def is_valid_param_size(size, max, message):
	error = 'Error: command takes {1} arugments. {0} were given.' .format(size, max)
	
	if size == max:
		return True
		
	send_message(error, message)
	return False

def is_valid_level(server, message):
	error = 'Error: invalid Level : {0} ' .format(server)
	level = 'level %s' %str(server)
	
	if level_xp_info.has_key(level):
		return True
	
	send_message(error, message)
	return False
	
def send_message(msg, message):
	name = message.FromDisplayName
	request_msg = ' - requested by {0}' .format(name)
	message.Chat.SendMessage('%s %s' % (msg, request_msg))
	print '%s %s' % (message.Datetime, msg)
	
def param_size_error(size, max, message):
	error = 'Error: command takes {1} arugments. {0} were given.' .format(size, max)
	send_message(error, message)
	
def cstool_server(server):
	if server == 'test1':
		return 'cs_tool_1'
		
	if server == 'test4':
		return 'cs_tool_4'
		
	if server == 'test5' or server == 'trunk':
		return 'cs_tool_5'
	
	return server
	
def run_process(api_env, param):
	return subprocess.check_output(['curl', api_env, '-d', param])
	
def apitool_url():
	return 'http://10.10.9.63/{0}/index.php/apitool/submit'
		
#----------------------- Apitool Functions -----------------------#

def apitool_set_userinfo_by_id(server, uin, currency):	
	print '\nSetting user currency\nRunning.. UserInfo -> set_userinfo_by_id\n'
	cstool = cstool_server(server)
	curl = apitool_url() .format(cstool)
	param = (
		'model_name=UserInfo'
		'&method_name=set_userinfo_by_id'
		'&uin={0}'
		'&changedData=%7B'
		'%22coin%22%3A{1}'
		'%2C%22shard%22%3A{1}'
		'%2C%22uin%22%3A%22{0}'
		'%22%7D' 
		.format(uin, currency)
	)	
	run_process(curl, param)

def apitool_get_account_by_id_full_info(server, uin):
	print '\nRunning.. DDRAccounts -> get_account_by_id_full_info\n'
	cstool = cstool_server(server)
	curl = apitool_url() .format(cstool)
	param = (
		'model_name=DDRAccounts'
		'&method_name=get_account_by_id_full_info'
		'&uin={0}'
		'&desired_columns=uin'
		.format(uin)
	)	
	result = run_process(curl, param)
	return result.lower()
    
def apitool_update_hero_by_hid():
    print '\nRunning.. HeroMap -> update_hero_by_hid\n'

def apitool_ban_user(server, uin):
	print '\nRunning.. DDRAccounts -> ban_user\n'
	cstool = cstool_server(server)
	curl = apitool_url() .format(cstool)
	param = (
		'model_name=DDRAccounts'
		'&method_name=ban_user'
		'&uin={0}'
		'&ban_type=1'
		'&ban_length=0'
		'&time_unit=0'
		.format(uin)
	)
	run_process(curl, param)
	
def apitool_unban_user(server, uin):
	print '\nRunning.. DDRAccounts -> recover_user\n'
	cstool = cstool_server(server)
	curl = apitool_url() .format(cstool)
	param = (
		'model_name=DDRAccounts'
		'&method_name=recover_user'
		'&uin={0}'
		.format(uin)
	)
	run_process(curl, param)
	
if __name__ == '__main__':
	main()