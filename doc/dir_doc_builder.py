from . import class_doc_builder
import os

class DirDocBuilder:
	def __init__(self):
		self.files = list()
		self.root_dir = list()
		self.dirs = list()

	def generate_classed_doc(self, path):
		for filename in os.listdir(path):
			if filename.endswith(".kt"):
				new_file_doc = class_doc_builder.ClassDocBuilder(os.path.join(path + '\\', filename))
				new_file_doc.build_doucumentation()
				new_file_doc.print_classes()
				self.files.append(new_file_doc)
			elif os.path.isdir(os.path.join(path + '\\', filename)):
				new_dir_doc = DirDocBuilder()
				new_dir_doc.generate_classed_doc(os.path.join(path + '\\', filename))
				self.dirs.append(new_dir_doc)

	def print_tree(self):
		for file in self.files:
			print("class------------------")
			file.print_classes()
		for dir in self.dirs:
			print("dir------------------")
			dir.print_tree()