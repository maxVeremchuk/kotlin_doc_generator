import re 

class ClassDocBuilder:
	class ClassDoc:
		def __init__(self):
			self.description = ""
			self.class_name = ""
			self.full_class_name = ""
			self.primary_constructor = ""
			self.constructors = list()
			self.functions = list()
			self.functions_description = list()
			self.functions_body = list()
			self.props = list()
			self.props_description = list()
			self.is_inside_fun = False
		

		#def __str__(self):
		#params = ""
		#base_classes = list()


	def __init__(self, filename):
		print(filename)
		self.init_content = list()
		self.comment = ""
		self.is_full_comment = True	
		self.iter_input = iter("")
		self.classes = list()
		self.new_class = None
		with open(filename, "r") as file:
			self.init_content = file.readlines()
			
	def next_input(self):
		for line in self.init_content:
			yield line

	def build_doucumentation(self):
		self.iter_input = iter(self.next_input())
		for line in self.iter_input:
			self.parse_line(line)
		self.classes.append(self.new_class)

	def parse_line(self, line):
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
			if "class" in line:	
				if self.new_class is not None:
					self.classes.append(self.new_class)
				self.new_class = self.ClassDoc()
				if self.comment != "":
					self.new_class.description = self.comment
					self.comment = ""
				if "constructor" in line:
					line.replace("constructor", "")
					line.replace("private", "")
					line.replace("public", "")
					line.replace("@Inject", "")
					" ".join(line.split())
				splitted_line = line.split(' ')
				class_name = ""
				for i, item in enumerate(splitted_line):
					if item == "class":
						class_name = splitted_line[i + 1]
						class_name = class_name.split('<')[0].split('>')[0].split('(')[0].split(')')[0]
				finded_brace = re.search(r'\([^\)]+\)', line)
				colon = line.find(":")
				if finded_brace is not None:
					self.new_class.full_class_name = line[:finded_brace.start()] + line[finded_brace.end():]
					if finded_brace.start() < colon or colon == 0:
						self.new_class.primary_constructor = class_name + finded_brace.group()
				self.new_class.class_name = class_name
			elif "constructor" in line:
				line = self.new_class.class_name + line.split("constructor")[1]
				if line.strrp()[-1] == "{":
					line = line[:-1]
				line = line.strip()	
				self.new_class.constructors.append(line)
			elif line.strip().startswith("fun ") or line.strip().startswith("override fun ") \
			or line.strip().startswith("private fun ") or line.strip().startswith("internal fun ") \
			or line.strip().startswith("protected open fun ") or line.strip().startswith("protected fun "):
				
				if line.strip()[-1] == "{":
					line = line[:-1]
				self.new_class.functions.append(line.strip())
				if self.comment != "":
					self.new_class.functions_description.append(self.comment)
					self.comment = ""

				bracket_stack = ['{']
				open_list = ["[","{","(","<"] 
				close_list = ["]","}",")",">"] 
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
								print("ERROR")
				self.new_class.functions_body.append(fun_body)

			elif line.strip().startswith("val ") or line.strip().startswith("override val ") \
			or line.strip().startswith("private val ") or line.strip().startswith("internal val ") \
			or line.strip().startswith("protected open val ") or line.strip().startswith("protected val ") \
			or line.strip().startswith("var ") or line.strip().startswith("override var ") \
			or line.strip().startswith("private var ") or line.strip().startswith("internal var ") \
			or line.strip().startswith("protected open var ") or line.strip().startswith("protected var "):
				self.new_class.props.append(line.strip())
				if self.comment != "":
					self.new_class.props_description.append(self.comment)
					self.comment = ""

	def handle_imports(self):
		for class_item in self.classes:
			for function_body in class_item.functions_body
				pass
	def parse_line_import(self, line):
		pass



	def print_classes(self):
		for class_item in self.classes:
			if class_item is not None:
				print(class_item.description)
				print(class_item.class_name)
				print(class_item.primary_constructor)
				print(class_item.constructors)
				print("prop---------------")
				print(class_item.props)
				print("props desc---------------")
				print(class_item.props_description)
				print("fun---------------")
				print(class_item.functions)
				print("fun body---------------")
				print(class_item.functions_body)
			else:
				print("None")