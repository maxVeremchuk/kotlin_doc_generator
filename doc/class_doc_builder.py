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
			self.functions = list()
			self.functions_description = dict()
			self.functions_body = list()
			self.props = list()
			self.props_description = dict()
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
		self.is_outer_class = False
		with open(os.path.join(class_path, filename), "r") as file:
			self.init_content = file.readlines()
			
	def next_input(self):
		for line in self.init_content:
			yield line

	def build_doucumentation(self):
		self.iter_input = iter(self.next_input())
		for line in self.iter_input:
			self.parse_line(line)

	def parse_line(self, line):
		#print("parse_line",line)	
		if "/**" in line:
			self.is_full_comment = False
		elif not self.is_full_comment:
			if "*/" in line:
				#self.comment += line[:-2]
				self.is_full_comment = True
			# elif "/**" in line or self.comment != "":
			# 	self.comment += line[3:]
			else:
				self.comment += line.strip()[1:].strip()
		else: 
			if line.strip().startswith("class ") or line.strip().startswith("abstract class ") \
			or line.strip().startswith("open class ") or line.strip().startswith("object "):
				self.classes.append(self.build_class(line))
			elif line.strip().startswith("interface "):
				self.classes.append(self.build_class(line, True))
			elif line.strip().startswith("import "):
				if " as " in line:
					imp, alias = line.split(" as ")
					self.imports.append(imp.split(" ")[1])
					self.imports.append(alias)
				else:
					self.imports.append(line.split(" ")[1])
					print(line.split(" ")[1])

	def build_class(self, line, is_interface = False):
		new_class = self.ClassDoc()
		if self.comment != "":
			new_class.description = self.comment
			self.comment = ""

		while "{" not in line:
			line = line.strip() + " " + next(self.iter_input)

		if "constructor" in line:
			line.replace("constructor", "")
			line.replace("private", "")
			line.replace("public", "")
			line.replace("@Inject", "")
			" ".join(line.split())
		splitted_line = line.strip().split(' ')
		class_name = ""
		for i, item in enumerate(splitted_line):
			if item == "class" or item == "interface":
				class_name = splitted_line[i + 1]
				class_name = class_name.split('<')[0].split('>')[0].split('(')[0].split(')')[0]
				break
		new_class.full_class_name = line.strip()[:-1]

		finded_brace = re.search(r'\([^\)]+\)', line)
		colon = line.find(":")
		if finded_brace is not None:
			#new_class.full_class_name = line.strip()[:-1]
			#new_class.full_class_name = line[:finded_brace.start()] + line[finded_brace.end():]
			if finded_brace.start() < colon or colon == 0:
				new_class.primary_constructor = class_name + finded_brace.group()
		new_class.class_name = class_name


		bracket_stack_class = ["{"]
		open_list = ["{"] 
		close_list = ["}"] 

		while(len(bracket_stack_class) != 0):
			line = next(self.iter_input)
			for j, letter in enumerate(line):
				if letter in open_list:
					bracket_stack_class.append(letter)
				elif letter in close_list:
					pos = close_list.index(letter)
					if ((len(bracket_stack_class) > 0) and (open_list[pos] == bracket_stack_class[-1])): 
						bracket_stack_class.pop()
					else:
						print("ERROR CLASS")
						return None
					
			if (line.strip().startswith("inner class ") or line.strip().startswith("class ")):
				new_class.nested_classes.append(self.build_class(line))	
				bracket_stack_class.pop()
			elif line.strip().startswith("constructor"):

				line = new_class.class_name + line.split("constructor")[1]
				 
				if line.strip()[-1] == "{":
					line = line.strip()[:-1]
				else:
					line = line.strip()

				new_class.constructors.append(line)

			elif line.strip().startswith("fun ") or line.strip().startswith("override fun ") \
			or line.strip().startswith("private fun ") or line.strip().startswith("internal fun ") \
			or line.strip().startswith("protected open fun ") or line.strip().startswith("protected fun "):
				if not is_interface:
					if "=" not in line:
						while line.strip()[-1] != "{":
							line = line.strip() + " " + next(self.iter_input)
				else:
					while line.strip()[-1] != ")":
						line = line.strip() + " " + next(self.iter_input)

				if line.strip()[-1] == "{":
					line = line.strip()[:-1]
				else:
					line = line.strip()
				
				new_class.functions.append(line.strip())
				if self.comment != "":
					new_class.functions_description[line.strip()] = self.comment
					self.comment = ""
				bracket_stack = ['{']
				open_list = ["[","{","("] 
				close_list = ["]","}",")"] 
				fun_body = list()
				while(len(bracket_stack) != 0):
					line = next(self.iter_input)
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
								return None
				new_class.functions_body.append(" ".join(fun_body))
				bracket_stack_class.pop()

			elif line.strip().startswith("val ") or line.strip().startswith("override val ") \
			or line.strip().startswith("private val ") or line.strip().startswith("internal val ") \
			or line.strip().startswith("private lateinit val ") or line.strip().startswith("internal lateinit val ") \
			or line.strip().startswith("protected open val ") or line.strip().startswith("protected val ") \
			or line.strip().startswith("var ") or line.strip().startswith("override var ") \
			or line.strip().startswith("private var ") or line.strip().startswith("internal var ") \
			or line.strip().startswith("private lateinit var ") or line.strip().startswith("internal lateinit var ") \
			or line.strip().startswith("protected open var ") or line.strip().startswith("protected var "):
				new_class.props.append(line.strip())
				if self.comment != "":
					self.new_class.props_description[line.strip()] = self.comment
					self.comment = ""
		return new_class

	def handle_imports(self, main_tree):
		imports_to_find = list()
		for import_item in self.imports:
			import_item = import_item.replace(".", os.path.sep)
			imports_to_find.append(os.path.join(self.class_path, import_item).strip() + ".kt")
			imports_to_find.append(os.path.join(main_tree.root_dir, import_item).strip() + ".kt")
			#print(main_tree.root_dir)
			#print(import_item)
			#print(self.class_path)
			#print(import_item)
		imported_files = list()
		for import_item in imports_to_find: 
			#print(os.path.dirname(import_item))
			#print(os.path.basename(import_item))
			#print(main_tree.dirs[0].files)
			imported_file = main_tree.return_file(os.path.dirname(import_item), os.path.basename(import_item))
			print(imported_file)
			if imported_file is not None:
				imported_files.append(imported_file)

		for class_item in self.classes:
			if class_item is None:
				continue
			for func_idx, function_body in enumerate(class_item.functions_body):
				for imported_file in imported_files:
					for imported_file_class in imported_file.classes:
						#print(imported_file_class)
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
								# if class_item.functions[func_idx] not in class_item.imports:
								# 	class_item.functions[func_idx] = []
								class_item.imports[class_item.functions[func_idx]].append((imported_file.class_path \
								+ ' ' + imported_file.filename + ' ' + imp_func_name + ' ' + \
								imported_file_class.class_name).strip())
							elif " " + imported_file_class.class_name + ")" in function_body or \
							" " + imported_file_class.class_name + " " in function_body or \
							"(" + imported_file_class.class_name + " " in function_body or\
							"(" + imported_file_class.class_name + "(" in function_body:
								class_item.imports[class_item.functions[func_idx]].append((imported_file.class_path \
								+ ' ' + imported_file.filename + ' ' + '-' + ' ' + \
								imported_file_class.class_name).strip())

	@staticmethod
	def get_fun_name(fun):
		decl = fun.split(" ")
		for i, item in enumerate(decl):
			if item == "fun":
				return decl[i + 1].split('(')[0]
		return None

	@staticmethod
	def get_prop_name(prop):
		decl = prop.split(" ")
		for i, item in enumerate(decl):
			if item == "val" or item == "var":
				return decl[i + 1][:-1]
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