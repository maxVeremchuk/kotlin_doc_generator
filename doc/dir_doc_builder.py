from . import class_doc_builder
import os

class DirDocBuilder:
	def __init__(self):
		self.files = list()
		self.root_dir = ""
		self.dirs = list()

	def generate_classed_doc(self, path):
		root_dir = path
		for filename in os.listdir(path):
			if filename.endswith(".kt"):
				new_file_doc = class_doc_builder.ClassDocBuilder(os.path.join(path + '\\', filename),)
				new_file_doc.build_doucumentation()
				new_file_doc.print_classes()
				self.files.append(new_file_doc)
			elif os.path.isdir(os.path.join(path + '\\', filename)):
				new_dir_doc = DirDocBuilder()
				new_dir_doc.generate_classed_doc(os.path.join(path + '\\', filename))
				self.dirs.append(new_dir_doc)

	def return_file(self, class_path, filename):
		if self.root_dir == class_path:
			for file in self.files:
				if file.filename == filename:
					return file
		else:
			find_path = os.path.relpath(class_path, self.root_dir)
			find_dir = os.path.join(self.root_dir, find_path.split(os.path.sep)[0])

			for dir_item in dirs:
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