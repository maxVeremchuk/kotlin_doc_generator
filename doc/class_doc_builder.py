import re 
import os
from collections import defaultdict

class ClassDocBuilder:
	class ClassDoc:
		def __init__(self):
			self.description = ""
			self.class_name = ""
			self.full_class_name = ""
			self.primary_constructor = ""
			self.constructors = list()
			self.constructors_ann = list(list())
			self.class_ann = list()
			self.functions = list()
			self.functions_description = dict()
			self.functions_body = list()
			self.functions_ann = list(list())
			self.props = list()
			self.props_description = dict()
			self.props_ann = list(list())
			self.imports = defaultdict(list)
			self.nested_classes = list()
			#self.is_inside_fun = False



	def __init__(self, filename, class_path):
		self.init_content = list()
		self.comment = ""
		self.is_full_comment = True	
		self.iter_input = iter("")
		self.classes = list()
		self.new_class = None
		self.class_path = class_path
		self.filename = filename
		self.imports = list()
		self.imports_alias = list()
		self.is_outer_class = False
		self.annotation = list()
		self.memory = list()
		self.skip = False
		self.skip_line = ""
		self.functions = list()
		self.functions_description = dict()
		self.functions_body = list()
		self.functions_ann = list(list())
		self.file_comment = ""
		self.first_comment = True
		try:
			with open(os.path.join(class_path, filename), "r") as file:
				self.init_content = file.readlines()
			self.init_content.append("")
			temp_init_content = "`".join(self.init_content)
			finded_line = re.findall(r'"([^"]*)"', temp_init_content)
			if finded_line is not None:
				for line in finded_line:
					temp_init_content = temp_init_content.replace("\"" + line  + "\"", "")
			self.init_content = temp_init_content.split("`")
		except:
			print("error in reading file")
			
	def next_input(self):
		for line in self.init_content:
			yield line

	def build_doucumentation(self):
		try:
			print(self.class_path)
			print(self.filename)
			self.iter_input = iter(self.next_input())
			for line in self.iter_input:
				self.parse_line(line)
		except:
			print("Some error in formating")

	def parse_line(self, line):
		#print("parse_line",line)	
		if "/**" in line:
			self.is_full_comment = False
		elif not self.is_full_comment:
			if "*/" in line:
				#self.comment += line[:-2]
				self.is_full_comment = True
				if self.first_comment:
					self.first_comment = False
					self.file_comment = self.comment
					self.comment = ""
			# elif "/**" in line or self.comment != "":
			# 	self.comment += line[3:]
			else:
				self.comment += line.strip()[1:].strip()
		else: 
			self.first_comment = False
			line = self.handle_annotation(line)
			if line.strip().startswith("//"):
				return
			elif line.strip().startswith("class ") or " class " in line \
			or line.strip().startswith("object ") or " object " in line:
				if not "= object" in line and not "object :" in line:
					self.classes.append(self.build_class(line))
			elif line.strip().startswith("interface ") or " interface " in line:
				self.classes.append(self.build_class(line, True))
			elif line.strip().startswith("import "):
				if " as " in line:
					imp, alias = line.split(" as ")
					self.imports.append(imp.split(" ")[1])
					self.imports_alias.append(imp.split(" ")[1] +  " " + alias.strip())
				else:
					self.imports.append(line.split(" ")[1])
			elif line.strip().startswith("fun ") or " fun " in line:
				bracket_stack = []
				open_list = ["[","{","("] 
				close_list = ["]","}",")"] 
				first = True
				last = False
				temp_line = line
				while(len(bracket_stack) != 0) or first:
					first = False
					#print(line)	
					#print(bracket_stack)
					for j, letter in enumerate(line):
						if letter in open_list:
							last = False
							bracket_stack.append(letter)
						elif letter in close_list:
							pos = close_list.index(letter)
							if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
								bracket_stack.pop()
								if len(bracket_stack) == 0:
									last = True
							else:
								print("ERROR FUN")
								return
					if not last:
						line = next(self.iter_input)
						temp_line += line.strip()
				line = temp_line
				#print(line)
				if line.strip()[-1] == "{":
					line = line.strip()[:-1]
				elif line.strip().endswith("{}"):
					line = line.strip()[:-2]

				line = line[:line.find('{')]
				
				self.functions.append(line.strip())
				if self.comment != "":
					self.functions_description[line.strip()] = self.comment
					self.comment = ""
				#print(line)
				fun_body = list()
				self.functions_body.append(" ".join(fun_body))
				self.functions_ann.append(self.annotation)
				self.annotation = list()
				
			if len(self.memory) > 0:
				self.parse_line(self.memory.pop())
				#self.imports.append(line.split(" ")[1])

	def handle_annotation(self, line):

		while line.strip().startswith('@'):
			full_annotation = ""

			if re.findall(r'@[A-Za-z0-9]+\(', line) != []:
				annotation_name, line_without_name = line.split('(', 1)
				#print(annotation_name, line_without_name)
				bracket_stack = ['(']
				open_list = ["("] 
				close_list = [")"]
				end_of_annotation = 0
				first = True
				full_annotation += annotation_name + "("
				stop = False
				while(len(bracket_stack) != 0):
					if not first:
						full_annotation += line_without_name
						line_without_name = next(self.iter_input)

					first = False
					for j, letter in enumerate(line_without_name):
						if letter in open_list:
							bracket_stack.append(letter)
						elif letter in close_list:
							pos = close_list.index(letter)
							if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
								bracket_stack.pop()
								full_annotation += line_without_name[:j + 1]
								line_without_name = line_without_name[j + 1:]
								if len(bracket_stack) == 0:
									stop = True
									break
							else:
								print("ERROR ANNOTAION")
								return line
					if stop:
						break
				if line_without_name == "":
					line = next(self.iter_input)
				else:
					line = line_without_name.strip()
			else:
				if line.strip().count(' ') > 0:
					full_annotation, line = line.split(' ', 1)
				else:
					full_annotation = line.strip()
					line = next(self.iter_input)
					if line.strip() == "}":
						self.skip = True
						self.skip_line = line
			self.annotation.append(full_annotation.strip())
		return line

	def build_class(self, line, is_interface = False):
		new_class = self.ClassDoc()
		new_class.class_ann.extend(self.annotation)
		self.annotation = list()
		if self.comment != "":
			new_class.description = self.comment
			self.comment = ""

		bracket_stack_class = ["{"]
		if not line.strip().endswith('{'):
			next_line =  next(self.iter_input)
			if next_line.strip().startswith('{'):
				line = line.strip() + " " + next_line.strip()
			else:
				bracket_stack_class = []
				self.memory.append(next_line)	


		if "constructor" in line:
			line.replace("constructor", "")
			line.replace("private", "")
			line.replace("public", "")
			line.replace("@Inject", "")
			" ".join(line.split())
		splitted_line = line.strip().split(' ')
		class_name = ""
		for i, item in enumerate(splitted_line):
			if item == "class" or item == "interface" or item == "object":
				class_name = splitted_line[i + 1]
				class_name = class_name.split('<')[0].split('>')[0].split('(')[0].split(')')[0]
				if not re.compile("[A-Za-z0-9]+").fullmatch(class_name):
					class_name = "anonymous"
				break
		if line.strip()[-1] == "{":		
			new_class.full_class_name = line.strip()[:-1]
		else:
			new_class.full_class_name = line.strip()

		finded_brace = re.search(r'\([^\)]+\)', line)
		colon = line.find(":")
		if finded_brace is not None:
			#new_class.full_class_name = line.strip()[:-1]
			#new_class.full_class_name = line[:finded_brace.start()] + line[finded_brace.end():]
			if finded_brace.start() < colon or colon == 0:
				new_class.primary_constructor = class_name + finded_brace.group()
		new_class.class_name = class_name


		#print("0", line)

		open_list = ["{"] 
		close_list = ["}"] 
		if(len(bracket_stack_class) == 0):
			for j, letter in enumerate(line):
					if letter in open_list:
						bracket_stack_class.append(letter)
					elif letter in close_list:
						pos = close_list.index(letter)
						if ((len(bracket_stack_class) > 0) and (open_list[pos] == bracket_stack_class[-1])): 
							bracket_stack_class.pop()
						else:
							print("ERROR CLASS")
							return new_class
		#print("00", line)
		while(len(bracket_stack_class) != 0):
			# if len(self.memory) > 0:
			# 	line = self.memory.pop()
			# else:
			
			if not self.skip:
				line = next(self.iter_input)
				#print(line)
				if line.strip().startswith("//"):
					continue
			else:
				line = self.skip_line
				self.skip = False
			#print("1", line)
			open_list = ["{"] 
			close_list = ["}"] 
			for j, letter in enumerate(line):
				if letter in open_list:
					bracket_stack_class.append(letter)
					
				elif letter in close_list:
					pos = close_list.index(letter)
					if ((len(bracket_stack_class) > 0) and (open_list[pos] == bracket_stack_class[-1])): 
						bracket_stack_class.pop()
					else:
						print("ERROR CLASS")
						return new_class
			
		
			#print("END",bracket_stack_class)
			line = self.handle_annotation(line)
			#print("2", line)
			if line.strip().startswith("class ") or " class " in line \
			or line.strip().startswith("object ") or " object " in line:
				new_class.nested_classes.append(self.build_class(line))	
				bracket_stack_class.pop()
			elif line.strip().startswith("constructor"):
				if line.strip().endswith("{"):
					bracket_stack_class.pop()

				bracket_stack = []
				open_list = ["[","("] 
				close_list = ["]",")"] 
				first = True
				last = False
				temp_line = line
				while(len(bracket_stack) != 0) or first:
					first = False
					#print("con", line)
					for j, letter in enumerate(line):
						if letter in open_list:
							last = False
							bracket_stack.append(letter)
						elif letter in close_list:
							pos = close_list.index(letter)
							if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
								bracket_stack.pop()
								if len(bracket_stack) == 0:
									last = True
							else:
								print("ERROR CONSTRUCTOR")
								return new_class
					if not last:
						line = next(self.iter_input)
						temp_line += line.strip()
				line = temp_line
				#print("temp", line)
				if line.strip()[-1] == "}":
					line = line.strip()[:-1]
				elif line.strip()[-1] == "{":
					last = False
					bracket_stack = ["{"]
					open_list = ["[", "{", "("] 
					close_list = ["]", "}", ")"] 
					temp_line = line
					while(len(bracket_stack) != 0) :
						#print("con br", bracket_stack)
						line = next(self.iter_input)
						#print(line)
						for j, letter in enumerate(line):
							if letter in open_list:
								last = False
								bracket_stack.append(letter)
							elif letter in close_list:
								pos = close_list.index(letter)
								if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
									bracket_stack.pop()
									if len(bracket_stack) == 0:
										last = True
								else:
									print("ERROR CONSTRUCTOR")
									return new_class
						#if not last:				
					line = temp_line.strip()[:-1]
				else:
					line = line.strip()

				line = new_class.class_name + line.split("constructor")[1]
				 
				

				
				#bracket_stack_class.pop()

				new_class.constructors.append(line)
				new_class.constructors_ann.append(self.annotation)
				self.annotation = list()



			elif line.strip().startswith("fun ") or " fun " in line:
				#print("fun decl", line)
				has_body = True
				#print("interface", is_interface)
				if line.strip().endswith("{"):
					bracket_stack_class.pop()
				if not is_interface:
					#print("here")
					if line.strip().startswith("abstract ") or " abstract " in line:
						has_body = False
						bracket_stack = []
						open_list = ["[","{","("] 
						close_list = ["]","}",")"] 
						first = True
						last = False
						temp_line = line
						while(len(bracket_stack) != 0) or first:
							#print("else", line)
							first = False
							for j, letter in enumerate(line):
								if letter in open_list:
									bracket_stack.append(letter)
									last = False
									#print("else append", bracket_stack)
								elif letter in close_list:
									pos = close_list.index(letter)
									#print(letter)
									if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
										bracket_stack.pop()
										#print("else pop ", bracket_stack)
										if len(bracket_stack) == 0:
											#print("break",line)
											last = True
									else:
										print("ERROR FUN BODY ABS")
										return new_class
							if not last:
								line = next(self.iter_input)
								temp_line = temp_line.strip() + " " + line
						line = temp_line
						#print("abstract",line)
					else:
						#print("here2")
						if "=" not in line:
							#print("here3")
							while line.strip()[-1] != "{" and not line.strip().endswith("{}"):
								
								if '=' in line:
									break
								temp_line = next(self.iter_input)
								if temp_line.strip() == "" or temp_line.strip() == "}" \
								or temp_line.strip().startswith("fun ") or " fun " in temp_line \
								or temp_line.strip().startswith("class ") or " class " in temp_line \
								or temp_line.strip().startswith("interface ") or " interface " in temp_line \
								or temp_line.strip().startswith("object ") or " object " in temp_line \
								or temp_line.strip().startswith("val ") or " val " in temp_line \
								or temp_line.strip().startswith("var ") or " var " in temp_line:
									has_body = False 
									self.skip = True
									self.skip_line = temp_line
									break
									#line = temp_line
								else:
									line = line.strip() + " " + temp_line
								#print("loop", line)
								 


						if line.strip().endswith("="):
							line = line.strip()[:-1]
							has_body = False
				
					# while line.strip().endswith('(') or line.strip().endswith(','):
					# 	line = line.strip() + " " + next(self.iter_input).strip()
					# if line.strip().endswith("="):
					# 	line = line.strip() + " " + next(self.iter_input)
					# 	if "||" in line or "&&" in line:
					# 		while line.strip().endswith("||") or line.strip().endswith("&&"):
					# 			line = line.strip() + " " + next(self.iter_input).strip()
					# 	else:
					# 		while not line.strip().endswith(')') and not line.strip().endswith('}'):
					# 			line = line.strip() + " " + next(self.iter_input)
				else:
					# while line.strip()[-1] != ")" and "):" not in line:
					# 	if line.strip().endswith('{'):
					# 		has_body = True
					# 		break
					# 	line = line.strip() + " " + next(self.iter_input).strip()
					# if line.strip().endswith("="):
					# 	while not line.strip().endswith(')') or "):" in line:
					# 		line = line.strip() + " " + next(self.iter_input)
					# while line.strip().endswith("||") or line.strip().endswith("&&"):
					# 	line = line.strip() + " " + next(self.iter_input).strip()
					if line.strip().endswith("="):
						line = line.strip()[:-1]
						has_body = False
					else:
						bracket_stack = []
						open_list = ["[","("] 
						close_list = ["]",")"] 
						first = True
						last = False
						temp_line = line
						while(len(bracket_stack) != 0) or first:
							first = False
							#print("con", line)
							for j, letter in enumerate(line):
								if letter in open_list:
									last = False
									bracket_stack.append(letter)
								elif letter in close_list:
									pos = close_list.index(letter)
									if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
										bracket_stack.pop()
										if len(bracket_stack) == 0:
											last = True
									else:
										print("ERROR FUN")
										return new_class
							if not last:
								line = next(self.iter_input)
								temp_line += line.strip()
						line = temp_line




				if line.strip()[-1] == "{":
					line = line.strip()[:-1]
				elif line.strip().endswith("{}"):
					line = line.strip()[:-2]
				else:
					line = line.strip()
					has_body = False
				
				new_class.functions.append(line.strip())
				if self.comment != "":
					new_class.functions_description[line.strip()] = self.comment
					self.comment = ""
				#print("fun body",line)
				fun_body = list()
				if has_body:
					bracket_stack = ["{"]
					open_list = ["[","{","("] 
					close_list = ["]","}",")"] 
					while(len(bracket_stack) != 0):
						#print("funnn", line)
						line = next(self.iter_input)
						#print("funnn after", line)
						fun_body.append(line)
						for j, letter in enumerate(line):
							if letter in open_list:
								bracket_stack.append(letter)
							elif letter in close_list:
								pos = close_list.index(letter)
								if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
									bracket_stack.pop()
								else:
									print("ERROR FUN")
									return new_class
					#bracket_stack_class.pop()
					#print("funn",bracket_stack_class)

				new_class.functions_body.append(" ".join(fun_body))
				new_class.functions_ann.append(self.annotation)
				self.annotation = list()
				


			elif line.strip().startswith("val ") or " val " in line \
			or line.strip().startswith("var ") or " var " in line:
				new_class.props.append(line.strip())
				if self.comment != "":
					self.new_class.props_description[line.strip()] = self.comment
					self.comment = ""
				new_class.props_ann.append(self.annotation)
				self.annotation = list()
			else:
				#print("fun body", line)

				bracket_stack = []
				open_list = ["{"] 
				close_list = ["}"]
				is_pop = True
				for j, letter in enumerate(line):
					#print("linelien",line, letter) 
					if letter in open_list:
						bracket_stack.append(letter)

					elif letter in close_list:
						pos = close_list.index(letter)
						#print("123456765432",bracket_stack)
						if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
							bracket_stack.pop()
						else:
							is_pop = False
				#print("bra ",bracket_stack)
				if is_pop:
					for i in bracket_stack:
						bracket_stack_class.pop()
				if '{' in line:
					bracket_stack = []
					open_list = ["[","{","("] 
					close_list = ["]","}",")"]
					first = True
					last = False
					while(len(bracket_stack) != 0) or first:
						#print("else", line)
						first = False
						for j, letter in enumerate(line):
							if letter in open_list:
								bracket_stack.append(letter)
								last = False
								#print("else append", bracket_stack)
							elif letter in close_list:
								pos = close_list.index(letter)
								#print(letter)
								if ((len(bracket_stack) > 0) and (open_list[pos] == bracket_stack[-1])): 
									bracket_stack.pop()
									#print("else pop ", bracket_stack)
									if len(bracket_stack) == 0:
										#print("break",line)
										last = True
								else:
									print("ERROR FUN BODY")
									return new_class
						if not last:
							line = next(self.iter_input)
					#print("else last", line)
					#bracket_stack_class.pop()
					#print("else",bracket_stack_class)
		#print("created clss")
		return new_class

	def handle_imports(self, main_tree):
		imports_to_find = list()
		for import_item in self.imports:
			import_item = import_item.replace(".", os.path.sep)
			from_class_path = os.path.join(self.class_path, import_item).strip() + ".kt"
			from_full_path = os.path.join(main_tree.root_dir, import_item).strip() + ".kt"
			if from_class_path == from_full_path:
				imports_to_find.append(from_class_path)
			else:
				imports_to_find.append(from_class_path)
				imports_to_find.append(from_full_path)
		imported_files = list()
		for import_item in imports_to_find: 
			imported_file = main_tree.return_file(os.path.dirname(import_item), os.path.basename(import_item))
			if imported_file is not None:
				imported_files.append(imported_file)

		for class_item in self.classes:
			if class_item is None:
				continue
			for func_idx, function_body in enumerate(class_item.functions_body):
				for alias in self.imports_alias:
					function_body = function_body.replace(alias.split(" ")[1] + ")", alias.split(" ")[0] + ")")
					function_body = function_body.replace(alias.split(" ")[1] + ".", alias.split(" ")[0] + ".")
					function_body = function_body.replace(alias.split(" ")[1] + "(", alias.split(" ")[0] + "(")

				for imported_file in imported_files:
					for imported_file_class in imported_file.classes:
						regex_to_find_val = r'val\s.* = {}\(\)'.format(imported_file_class.class_name)
						regex_to_find_var = r'var\s.* = {}\(\)'.format(imported_file_class.class_name)
						finded_variables = re.findall(regex_to_find_val, function_body)
						finded_variables += re.findall(regex_to_find_var, function_body)
						if finded_variables is not None:
							for new_obj in finded_variables:
								new_obj_name = new_obj.split(" ")[1] + "."
								function_body = \
								 function_body.replace(new_obj_name[:-1], imported_file_class.class_name)
						for imp_func in imported_file_class.functions:
							imp_func_name = ClassDocBuilder.get_fun_name(imp_func)
							if imported_file_class.class_name + "." + imp_func_name in function_body:
								class_item.imports[class_item.functions[func_idx]].append((imported_file.class_path \
								+ ' ' + imported_file.filename + ' ' + imp_func_name + ' ' + \
								imported_file_class.class_name).strip())
							elif " " + imported_file_class.class_name + ")" in function_body or \
							" " + imported_file_class.class_name + " " in function_body or \
							"(" + imported_file_class.class_name + " " in function_body or\
							"(" + imported_file_class.class_name + "(" in function_body or\
							"." + imported_file_class.class_name + "(" in function_body or\
							"." + imported_file_class.class_name + " " in function_body or\
							"." + imported_file_class.class_name + ")" in function_body:
								class_item.imports[class_item.functions[func_idx]].append((imported_file.class_path \
								+ ' ' + imported_file.filename + ' ' + 'constructor' + ' ' + \
								imported_file_class.class_name).strip())

	@staticmethod
	def get_fun_name(fun):
		decl = fun.split(" ")
		for i, item in enumerate(decl):
			if item == "fun":
				while i < len(decl) - 1:
					if re.compile("[A-Za-z0-9]+").fullmatch(decl[i + 1].split('(')[0]):
						return decl[i + 1].split('(')[0]
					i += 1
				return "anonymous"
				#return decl[i + 1].split('(')[0]
		return None

	@staticmethod
	def get_prop_name(prop):
		decl = prop.split(" ")
		for i, item in enumerate(decl):
			if item == "val" or item == "var":
				if decl[i + 1].endswith(':'):
					return decl[i + 1][:-1]
				return decl[i + 1]
		return None

	def print_classes(self):
		for class_item in self.classes:
			if class_item is not None:
				print(class_item.description)
				print(class_item.class_name)
				print(class_item.full_class_name)
				print(class_item.primary_constructor)
				print(class_item.constructors)
				print("prop---------------")
				print(class_item.props)
				print("props desc---------------")
				print(class_item.props_description)
				print("fun---------------")
				print(class_item.functions)
				print("fun desc---------------")
				print(class_item.functions_description)
				print("fun body---------------")
				print(class_item.functions_body)
				print("imp func---------------")
				print(class_item.imports)
			else:
				print("None")