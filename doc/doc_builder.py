import re 

class ClassDocBuilder:
	init_content = list()
	comment = ""
	is_full_comment = False	
	iter_input = iter("")
	classes = list()
	new_class = None
	class ClassDoc:
		description = ""
		class_name = ""
		full_class_name = ""
		primary_constructor = ""
		constructors = list()
		functions = list()
		functions_description = list()
		props = list()
		props_description = list()
		

		#def __str__(self):
		#params = ""
		#base_classes = list()


	def __init__(self, filename):
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
					classes.append(self.new_class)
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
				self.new_class.full_class_name = line[:finded_brace.start()] + line[finded_brace.end():]
				if finded_brace.start() < colon or colon == 0:
					self.new_class.primary_constructor = class_name + finded_brace.group()
				self.new_class.class_name = class_name
			elif "constructor" in line:
				line = self.new_class.class_name + line.split("constructor")[1]
				if line[-1] == "{":
					line = line[:-1]
				line = line.strip()	
				self.new_class.constructors.append(line)
			elif line.strip().startswith("fun"):
				if line[-1] == "{":
					line = line[:-1]
				self.new_class.constructors.append(line.strip())
				if self.comment != "":
					self.new_class.function_description.append(self.comment)
					self.comment = ""
			elif line.strip().startswith("var"):
				self.new_class.props.append(line.strip())
				if self.comment != "":
					self.new_class.props_description.append(self.comment)
					self.comment = ""
	def print_classes(self):
		for class_item in self.classes:
			print(class_item.description)
			print(class_item.class_name)
			print(class_item.primary_constructor)
			print(class_item.constructors)
			print("---------------")
			print(class_item.props)
			print("---------------")
			print(class_item.props_description)
