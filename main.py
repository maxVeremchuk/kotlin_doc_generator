from doc import class_doc_builder
from doc import dir_doc_builder

if __name__ == '__main__':
	class_doc = class_doc_builder.ClassDocBuilder(r'C:\Users\maxve\OneDrive\Робочий стіл\4course\mataprograming\kotlin_documentation\test.kt')
	class_doc.build_doucumentation()
	class_doc.print_classes()
	# dir_doc = dir_doc_builder.DirDocBuilder()
	# dir_doc.generate_classed_doc(r'C:\Users\maxve\OneDrive\Робочий стіл\4course\mataprograming\kotlin_documentation\test')
	# dir_doc.print_tree()