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


	def generate_html(self, tree, path, main_path, origin_main_dir):

		for file in tree.files:
			self.generate_html_for_file(file, path, main_path, origin_main_dir)
		else:
			for dir_item in tree.dirs:
				
				new_doc_path = os.path.dirname(main_path)
				rel_path = os.path.relpath(dir_item.root_dir, new_doc_path)
				rel_path_doc = os.path.sep.join(rel_path.strip(os.path.sep).split(os.path.sep)[1:])
				sub_dir_path = os.path.join(main_path, rel_path_doc)
				os.mkdir(os.path.join(main_path, rel_path_doc))
				self.generate_html(dir_item, sub_dir_path, main_path, origin_main_dir)
	def generate_html_for_file(self, file, path, main_path, origin_main_dir):
		with codecs.open(os.path.join(path, file.filename).strip() + ".html", "w", "utf-8") as stream_file:
			for class_item in file.classes:
				if class_item is None:
					continue
				stream_file.write(self.head)
				stream_file.write(self.class_name.format(class_item.class_name, class_item.full_class_name, \
					class_item.description))
				stream_file.write(self.header.format("Constructors"))
				if class_item.primary_constructor != "":
					stream_file.write(self.attr.format("primary", class_item.primary_constructor, "", ""))
				for constructor in class_item.constructors:
					stream_file.write(self.attr.format("secondary", constructor, "", ""))

				stream_file.write(self.header.format("Properties"))
				for prop in class_item.props:
					stream_file.write( \
					self.attr.format(class_doc_builder.ClassDocBuilder.get_prop_name(prop), prop, \
					class_item.props_description[prop] if prop in class_item.props_description else "", ""))

				stream_file.write(self.header.format("Functions"))
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
						os.path.join(os.path.dirname(main_path), origin_main_dir))
						relpath = os.path.join(relpath, filename)
						import_functions += self.import_a.format(relpath + ".html", \
						imp_class_name + "." + func_name)
					if import_functions != "":
						import_functions = "<b>Imported:</b><br>" + import_functions
					stream_file.write( \
					self.attr.format(class_doc_builder.ClassDocBuilder.get_fun_name(func), func, \
					class_item.functions_description[func] if func in class_item.functions_description else "", \
					import_functions))
				stream_file.write(self.end)
