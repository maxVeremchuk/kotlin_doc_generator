from . import class_doc_builder
import os

class DirDocBuilder:
	def __init__(self):
		self.files = list()
		self.root_dir = ""
		self.dirs = list()
		self.index = list()

	def generate_classed_doc(self, path):
		self.root_dir = path
		for filename in os.listdir(path):
			if filename.endswith(".kt"):
				new_file_doc = class_doc_builder.ClassDocBuilder(filename, path)
				new_file_doc.build_doucumentation()
				#new_file_doc.print_classes()
				self.files.append(new_file_doc)
			elif os.path.isdir(os.path.join(path, filename)):
				new_dir_doc = DirDocBuilder()
				new_dir_doc.generate_classed_doc(os.path.join(path, filename))
				self.dirs.append(new_dir_doc)
			elif filename.endswith(".md"):
				with open(os.path.join(path, filename), "r", encoding='utf-8') as file:
					self.index = file.readlines()
				

	def generate_imports(self, main_tree):
		for file in self.files:
			file.handle_imports(main_tree)
		for dir_item in self.dirs:
			dir_item.generate_imports(main_tree)

	def return_file(self, class_path, filename):
		if self.root_dir == class_path:
			for file in self.files:
				if file.filename == filename:
					return file
		else:
			find_path = os.path.relpath(class_path, self.root_dir)
			find_dir = os.path.join(self.root_dir, find_path.split(os.path.sep)[0])

			for dir_item in self.dirs:
				if dir_item.root_dir == find_dir:
					return dir_item.return_file(class_path, filename)
		return None

				
	def print_tree(self):
		for file in self.files:
			print("class------------------")
			file.print_classes()
		for dir in self.dirs:
			print("dir------------------")
			dir.print_tree()