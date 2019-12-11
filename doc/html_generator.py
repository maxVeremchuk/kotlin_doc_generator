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
			
			<style>
				ul, #myUL {
				  list-style-type: none;
				  font-size:25px;
				}

				#myUL {
				  margin: 0;
				  padding: 0;
				}

				.caret-custom {
				  cursor: pointer;
				  -webkit-user-select: none; 
				  -moz-user-select: none; 
				  -ms-user-select: none;
				  user-select: none;
				}

				.caret-custom::before {
				  content: "\\25B6";
				  color: black;
				  display: inline-block;
				  margin-right: 6px;
				}

				.caret-custom-down::before {
				  -ms-transform: rotate(90deg);
				  -webkit-transform: rotate(90deg); 
				  transform: rotate(90deg);  
				}

				.nested {
				  display: none;
				}

				.active {
				  display: block;
				}
			</style>
		</head>
		<body style="background-color: #FFFEDF">
			
	"""

	end = \
	"""		
			<script>
					var toggler = document.getElementsByClassName("caret-custom");
					var i;

					for (i = 0; i < toggler.length; i++) {
					  toggler[i].addEventListener("click", function() {
					    this.parentElement.querySelector(".nested").classList.toggle("active");
					    this.classList.toggle("caret-custom-down");
					  });
					}
			</script>
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

	file_descript = \
	"""
	<div style="overflow:auto; margin: 15px">
		<h5>{}</h5>
	</div>
	"""

	attr = \
	"""
	<div style="overflow:auto; margin: 15px">
		<div style="width: 30%; float: left"> <span><h4 style="position:absolute; margin-top:-0px; margin-left:10px">{}</h4></span> </div>
		<div style="width: 70%; float: right"> <span style="color:#aa6c39">{}</span> <br> <span><code>{}</code></span> <br> <span>{}</span> <span>{}</span> </div>
	</div>
	"""
	import_a = \
	"""
	<a href = "{}">{}</a><br>
	"""

	indent_const = "        "


	def generate_html(self, tree, path, main_path, origin_main_dir, build_index = True):
		new_doc_path = os.path.dirname(main_path)
		rel_path = os.path.relpath(tree.root_dir, new_doc_path)
		self.build_index_from_md(path, tree, main_path, rel_path, build_index)
		for file in tree.files:
			self.generate_html_for_file(file, path, main_path, origin_main_dir)
		else:
			for dir_item in tree.dirs:
				
				rel_path = os.path.relpath(dir_item.root_dir, new_doc_path)
				rel_path_doc = os.path.sep.join(rel_path.strip(os.path.sep).split(os.path.sep)[1:])
				sub_dir_path = os.path.join(main_path, rel_path_doc)
				os.mkdir(os.path.join(main_path, rel_path_doc))
				self.generate_html(dir_item, sub_dir_path, main_path, origin_main_dir, False)
	def generate_html_for_file(self, file, path, main_path, origin_main_dir):
		with codecs.open(os.path.join(path, file.filename).strip() + ".html", "w", "utf-8") as stream_file:
			stream_file.write(self.head)
			stream_file.write(self.print_top_tree(path, main_path))
			if file.file_comment != "":
				stream_file.write(self.file_descript.format(file.file_comment))
			for class_item in file.classes:
				if class_item is None:
					continue
				self.write_class_info_to_file(class_item, stream_file, 0, file.class_path)
				#print(path)
				#print(class_item.nested_classes)
				if len(class_item.nested_classes) > 0:
					stream_file.write(self.header.format("Nested Classes"))
					for nested_class in class_item.nested_classes:
						if nested_class is None:
							continue
						self.write_class_info_to_file(nested_class, stream_file, 1, file.class_path)
			if len(file.functions) > 0:
				stream_file.write(self.header.format("Functions:"))
			for i, func in enumerate(file.functions):
				annotations = ""
				if len(file.functions_ann[i]) > 0:
					annotations = "<b style=\"color:black\">Annotations:</b><br>"
				for annotation in file.functions_ann[i]:
					annotations += annotation + "<br>"
				func_rep_tags = func.replace('<', "&lt;").replace('>', "&gt;")
				stream_file.write(
				self.attr.format(class_doc_builder.ClassDocBuilder.get_fun_name(func), annotations, func_rep_tags, \
				file.functions_description[func] if func in file.functions_description else "", \
				""))
			stream_file.write(self.end)


	def write_class_info_to_file(self, class_item, stream_file, indent, class_item_class_path):
		filler = "<span style=\"margin-left:" + str(indent * 20) +"px\"></span>"
		stream_file.write(self.class_name.format(filler + class_item.class_name, filler + class_item.full_class_name, \
			filler + class_item.description))
		stream_file.write(self.header.format(filler + "Constructors"))
		if class_item.primary_constructor != "":
			stream_file.write(self.attr.format(filler + "primary", "", filler + class_item.primary_constructor, "", ""))
		for i, constructor in enumerate(class_item.constructors):
			annotations = ""
			if len(class_item.constructors_ann[i]) > 0:
				annotations = "<b style=\"color:black\">Annotations:</b><br>"
			for annotation in class_item.constructors_ann[i]:
				annotations += annotation + "<br>"
			stream_file.write(self.attr.format(filler + "secondary", filler + annotations, filler + constructor, "", ""))

		stream_file.write(self.header.format(filler + "Properties"))
		for i, prop in enumerate(class_item.props):
			annotations = ""
			if len(class_item.props_ann[i]) > 0:
				annotations = "<b style=\"color:black\">Annotations:</b><br>"
			for annotation in class_item.props_ann[i]:
				annotations += annotation + "<br>"
			stream_file.write( \
			self.attr.format(filler + class_doc_builder.ClassDocBuilder.get_prop_name(prop), filler + annotations, filler + prop, \
			filler + class_item.props_description[prop] if prop in class_item.props_description else "", ""))

		stream_file.write(self.header.format(filler + "Functions"))
		for i, func in enumerate(class_item.functions):
			annotations = ""
			if len(class_item.functions_ann) > i:
				if len(class_item.functions_ann[i]) > 0:
					annotations = "<b style=\"color:black\">Annotations:</b><br>"
				for annotation in class_item.functions_ann[i]:
					annotations += annotation + "<br>"

			import_functions = ""
			for imported_func in class_item.imports[func]:
				params = imported_func.split(' ')
				class_path = ""
				for path in params[:-3]:
					class_path += path + " "
				class_path.strip()
				filename = params[-3]
				func_name = params[-2].replace('<', "&lt;").replace('>', "&gt;")
				imp_class_name = params[-1]
				relpath = os.path.relpath(class_path, \
				class_item_class_path)
				relpath = os.path.join(relpath, filename)
				import_functions += self.import_a.format(relpath + ".html", \
				imp_class_name + "." + func_name)
			if import_functions != "":
				import_functions = "<b style=\"color:black\">Imported:</b><br>" + import_functions
			func_rep_tags = func.replace('<', "&lt;").replace('>', "&gt;")
			stream_file.write( \
			self.attr.format(filler + class_doc_builder.ClassDocBuilder.get_fun_name(func), filler + annotations, filler +  func_rep_tags, \
			filler + class_item.functions_description[func] if func in class_item.functions_description else "", \
			filler + import_functions))		

	def build_index_from_md(self, path, tree, main_path, origin_main_dir, build_index):
		with codecs.open(os.path.join(path, "index").strip() + ".html", "w", "utf-8") as stream_file:
			stream_file.write(self.head)
			stream_file.write(self.print_top_tree(path, main_path))
			if build_index:
				for line in tree.index:
					hashtags = line.count("#")
					if hashtags > 0:
						line = "<h" + str(hashtags) + ">" + line.split('#')[-1] + "</h" + str(hashtags) + ">"
					stream_file.write(line)

			stream_file.write(self.header.format("Files tree:"))

			tree_list = ""
			tree_list = self.print_tree(tree, "<ul id=\"myUL\">", main_path, origin_main_dir)
			tree_list += "</ul>"
			stream_file.write(tree_list)
			tree.generate_alphabet(tree)
			#print(tree.alphabet)
			stream_file.write(self.print_alphabet(tree.alphabet, main_path, origin_main_dir))
			
			# stream_file.write(self.header.format("Classes:"))
			# self.print_classes(tree, stream_file, main_path, origin_main_dir)
			# stream_file.write(self.header.format("Files:"))
			# self.print_files(tree, stream_file, main_path, origin_main_dir)
			stream_file.write(self.end)

	def print_top_tree(self, path, main_path):
		top_tree = ""
		relpath = os.path.relpath(path, os.path.dirname(main_path))
		partly_path = ""
		for direrctory in relpath.strip().split(os.path.sep):
			partly_path = os.path.join(partly_path, direrctory)
			inner_relpath =  os.path.relpath(partly_path, relpath)
			top_tree += "<a href = \"{}\">{}</a>".format(os.path.join(inner_relpath, "index.html"), os.path.basename(partly_path)) + ">>"
		top_tree = top_tree[:-2]
		top_tree += "<br>"
		return top_tree

	def print_alphabet(self, alph_dict, main_path, origin_main_dir):
		import operator
		alpha_finder = ""
		alphabet = sorted(alph_dict.items(), key=operator.itemgetter(0))
		for elem in alphabet:
			alpha_finder += "<h2>{}</h2><br>".format(elem[0].upper())
			for line in elem[1]:
				#print(os.path.join(os.path.dirname(line[1]), line[2] + ".html"))
				relpath = os.path.relpath(\
				os.path.join(line[1], line[2] + ".html"),\
				os.path.join(os.path.dirname(main_path), origin_main_dir))
				alpha_finder +=\
				"<a href=\"{}\" style=\"margin-left:20px\">{}</a><br>".format(relpath, line[0])
		return alpha_finder


	def print_tree(self, tree, tree_list, main_path, origin_main_dir):
	
		for file in tree.files:
			relpath = os.path.relpath(tree.root_dir, \
			os.path.join(os.path.dirname(main_path), origin_main_dir))
			relpath = os.path.join(relpath, file.filename + ".html")

			anchor = "<a href = \"{}\">{}</a>".format(relpath, file.filename)
			tree_list += "\n<li>" + anchor + "</li>"
		for dir_item in tree.dirs:
			relpath = os.path.relpath(dir_item.root_dir, \
			os.path.join(os.path.dirname(main_path), origin_main_dir))
			relpath = os.path.join(relpath, "index.html")
			#print(relpath)
			anchor = "<a href = \"{}\">{}</a>".format(relpath, os.path.basename(dir_item.root_dir))
			#print(anchor)
			tree_list += "<li><span class=\"caret-custom\">" + anchor + "</span>"
			tree_list += "<ul class=\"nested\">"
			tree_list = self.print_tree(dir_item, tree_list, main_path, origin_main_dir)
				#os.path.join(origin_main_dir, os.path.basename(dir_item.root_dir)))
			tree_list += "</ul>"
			tree_list += "</li>"
		return tree_list


	def print_classes(self, tree, stream_file, main_path, origin_main_dir):
		for file in tree.files:
			for class_item in file.classes:
				if class_item is not None:
					relpath = os.path.relpath(file.class_path, \
					os.path.join(os.path.dirname(main_path), origin_main_dir))
					relpath = os.path.join(relpath, file.filename)
					stream_file.write(self.import_a.format(relpath + ".html", class_item.class_name))
		for dir_item in tree.dirs:
			self.print_classes(dir_item, stream_file, main_path, origin_main_dir)

	def print_files(self, tree, stream_file, main_path, origin_main_dir):
		for file in tree.files:
				relpath = os.path.relpath(file.class_path, \
				os.path.join(os.path.dirname(main_path), origin_main_dir))
				relpath = os.path.join(relpath, file.filename)
				stream_file.write(self.import_a.format(relpath + ".html", file.filename))
		for dir_item in tree.dirs:
			self.print_files(dir_item, stream_file, main_path, origin_main_dir)

