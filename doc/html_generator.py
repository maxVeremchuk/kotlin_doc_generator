import os 
from . import class_doc_builder
import codecs
import pathlib

class HTMLGenerator:
	head = \
	"""
	<html>
		<head>
			<!-- Latest compiled and minified CSS -->
			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

			<!-- Optional theme -->
			<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">

			<!-- Latest compiled and minified JavaScript -->
			<script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
		</head>
		<body style="background-color: #FFFEDF">
	"""

	end = \
	"""
		</body>
	<html>
	"""

	class_name = \
	"""
	<div style="overflow:auto; margin: 15px">
		<h1>{}</h1>
		<div style=""> <span><code>{}</code></span> <br> <span>{}</span></div>
	</div>
	"""

	header = \
	"""
	<div style="overflow:auto; margin: 15px">
		<h3>{}</h3>
	</div>
	"""

	attr = \
	"""
	<div style="overflow:auto; margin: 15px">
		<div style="width: 30%; float: left"> <span><h4 style="position:absolute; margin-top:-0px; margin-left:10px">{}</h4></span> </div>
		<div style="width: 70%; float: right"> <span><code>{}</code></span> <br> <span>{}</span> <span>{}</span> </div>
	</div>
	"""
	import_a = \
	"""
	<a href = "{}">{}</a><br>
	"""

	indent_const = "        "


	def generate_html(self, tree, path, main_path, origin_main_dir, build_index = True):

		if build_index:
			self.build_index_from_md(path, tree, main_path, origin_main_dir)
		for file in tree.files:
			self.generate_html_for_file(file, path, main_path, origin_main_dir)
		else:
			for dir_item in tree.dirs:
				
				new_doc_path = os.path.dirname(main_path)
				rel_path = os.path.relpath(dir_item.root_dir, new_doc_path)
				rel_path_doc = os.path.sep.join(rel_path.strip(os.path.sep).split(os.path.sep)[1:])
				sub_dir_path = os.path.join(main_path, rel_path_doc)
				os.mkdir(os.path.join(main_path, rel_path_doc))
				self.generate_html(dir_item, sub_dir_path, main_path, origin_main_dir, False)
	def generate_html_for_file(self, file, path, main_path, origin_main_dir):
		with codecs.open(os.path.join(path, file.filename).strip() + ".html", "w", "utf-8") as stream_file:
			for class_item in file.classes:
				if class_item is None:
					continue
				self.write_class_info_to_file(class_item, stream_file, 0, file.class_path)

				if len(class_item.nested_classes) > 0:
					stream_file.write(self.header.format("Nested Classes"))
					for nested_class in class_item.nested_classes:
						self.write_class_info_to_file(nested_class, stream_file, 1, file.class_path)


	def write_class_info_to_file(self, class_item, stream_file, indent, class_item_class_path):
		filler = "<span style=\"margin-left:" + str(indent * 20) +"px\"></span>"
		if indent == 0:
			stream_file.write(self.head)
		stream_file.write(self.class_name.format(filler + class_item.class_name, filler + class_item.full_class_name, \
			filler + class_item.description))
		stream_file.write(self.header.format(filler + "Constructors"))
		if class_item.primary_constructor != "":
			stream_file.write(self.attr.format(filler + "primary", filler + class_item.primary_constructor, "", ""))
		for constructor in class_item.constructors:
			stream_file.write(self.attr.format(filler + "secondary", filler + constructor, "", ""))

		stream_file.write(self.header.format(filler + "Properties"))
		for prop in class_item.props:
			stream_file.write( \
			self.attr.format(filler + class_doc_builder.ClassDocBuilder.get_prop_name(prop), filler + prop, \
			filler + class_item.props_description[prop] if prop in class_item.props_description else "", ""))

		stream_file.write(self.header.format(filler + "Functions"))
		for func in class_item.functions:
			import_functions = ""
			for imported_func in class_item.imports[func]:
				params = imported_func.split(' ')
				class_path = ""
				for path in params[:-3]:
					class_path += path + " "
				class_path.strip()
				filename = params[-3]
				func_name = params[-2]
				imp_class_name = params[-1]
				relpath = os.path.relpath(class_path, \
				class_item_class_path)
				relpath = os.path.join(relpath, filename)
				import_functions += self.import_a.format(relpath + ".html", \
				imp_class_name + "." + func_name)
			if import_functions != "":
				import_functions = "<b>Imported:</b><br>" + import_functions
			stream_file.write( \
			self.attr.format(filler + class_doc_builder.ClassDocBuilder.get_fun_name(func), filler +  func, \
			filler + class_item.functions_description[func] if func in class_item.functions_description else "", \
			filler + import_functions))		

	def build_index_from_md(self, path, tree, main_path, origin_main_dir):
		with codecs.open(os.path.join(path, "index").strip() + ".html", "w", "utf-8") as stream_file:
			stream_file.write(self.head)
			for line in tree.index:
				hashtags = line.count("#")
				if hashtags > 0:
					line = "<h" + str(hashtags) + ">" + line.split('#')[-1] + "</h" + str(hashtags) + ">"
				stream_file.write(line)
			stream_file.write(self.header.format("Classes:"))
			self.print_classes(tree, stream_file, main_path, origin_main_dir)

	def print_classes(self, tree, stream_file, main_path, origin_main_dir):
		for file in tree.files:
			for class_item in file.classes:
				relpath = os.path.relpath(file.class_path, \
				os.path.join(os.path.dirname(main_path), origin_main_dir))
				relpath = os.path.join(relpath, file.filename)
				stream_file.write(self.import_a.format(relpath + ".html", class_item.class_name))
		else:
			for dir_item in tree.dirs:
				self.print_classes(dir_item, stream_file, main_path, origin_main_dir)
