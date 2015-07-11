# coding=utf-8
from convert import convert
import os
from ttk2.formats import POStore
from ttk2.formats.xliff import XLIFFStore


def test_convert_xliff_to_po():
	xliff = "data/example1.xliff"
	output = "data/tmp.po"
	convert([xliff], output, None)
	po_store = POStore()
	po_store.read(open(output, "r"), None, None)
	os.remove(output)
	xliff_store = XLIFFStore()
	xliff_store.read(open(xliff, "r"))
	xliff_units = xliff_store.units
	assert po_store.units == xliff_units

if __name__ == "__main__":
	test_convert_xliff_to_po()
