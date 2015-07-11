#!/usr/bin/env python
from argparse import ArgumentParser
from ttk2.formats import guess_format


def convert(input_files, output_file, template):
	instores = []
	for path in input_files:
		cls = guess_format(path)
		store = cls()
		with open(path, "r") as f:
			store.read(f, lang="todo")
		instores.append(store)

	# Create the outgoing store
	outstore = guess_format(output_file)()
	for store in instores:
		for unit in store.units:
			outstore.units.append(unit)
	if template:
		tunits = []
		for unit in template.units:
			unit.propkey = unit.key
			unit.key = unit.value
			unit.value = ""
			tunits.append(unit)

		for unit in outstore.units:
			for tunit in tunits:
				if unit.key == tunit.propkey:
					tunit.value = unit.value

		outstore.units = tunits
	with open(output_file, "w") as f:
		f.write(outstore.serialize())


def main():
	import sys

	arguments = ArgumentParser(prog="ttk convert")
	arguments.add_argument("--template", type=str, dest="template",
		help="Template for bilingual conversion", nargs=1)
	arguments.add_argument("outfile", nargs=1)
	arguments.add_argument("infile", nargs="+")
	args = arguments.parse_args(sys.argv[1:])
	output_file = args.outfile[0]
	input_files = args.infile

	if args.template:
		path = args.template[0]
		cls = guess_format(path)
		template = cls()
		with open(path, "r") as f:
			template.read(f, lang="todo")
	else:
		template = None

	convert(input_files, output_file, template)


if __name__ == "__main__":
	main()
