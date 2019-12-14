from doc import class_doc_builder
from doc import dir_doc_builder
from doc import html_generator
import os
import shutil
import sys


if __name__ == '__main__':
	if len(sys.argv) == 2 and sys.argv[1] == "-h":
		print(
"""
Enter path to dir wtih -d flag(-d path) or to file with -f flag(-f path).
In case of dir: new folder will be created with [your dir name]_documentation name with html files.
In case of file: will be created html file
""")
	elif len(sys.argv) < 3:
		print("write -h flag for help")
	elif sys.argv[1] == "-d":
		path = ""
		for item in sys.argv[2:]:
			path += item + " "
		path = path.strip()
		if path[-1] == "\\":
			path = path[:-1]
		if path[-1] == "/":
			path = path[:-1]
		dir_doc = dir_doc_builder.DirDocBuilder()
		dir_doc.generate_classed_doc(path)
		dir_doc.generate_imports(dir_doc)
		dir_name = os.path.basename(path)
		doc_dir = os.path.join(os.path.dirname(path), dir_name + "_documentation")
		if os.path.exists(doc_dir):
			shutil.rmtree(doc_dir)
		os.mkdir(doc_dir)
		html_generator.HTMLGenerator().generate_html(dir_doc, doc_dir, doc_dir, os.path.basename(path))
	elif sys.argv[1] == "-f":
		path = ""
		for item in sys.argv[2:]:
			path += item + " "
		class_doc = class_doc_builder.ClassDocBuilder(os.path.basename(path), os.path.dirname(path))
		class_doc.build_doucumentation()
		html_generator.HTMLGenerator().generate_html_for_file(class_doc, os.path.dirname(path), os.path.dirname(path), os.path.basename(path))