from xml.etree import ElementTree
from ttk2.formats import XMLStore, Unit


def _find_children(element, tag_name):
	return element.findall("ns:" + tag_name, {"ns": "urn:oasis:names:tc:xliff:document:2.0"})

class _XLIFFItem:
	def __init__(self, xml=None):
		if xml:
			children = _find_children(xml, self._children_class._node_name)
			self.children = list()
			for c in children:
				pass
			self.children.append(self._children_class(c))
		else:
			self.children = None

	def to_element(self):
		e = ElementTree.Element(self._node_name)
		for c in self.children:
			e.append(c.to_element())
		return e


class _Segment():
	_node_name = "segment"

	def __init__(self, xml=None, unit=None):
		if xml:
			s = _find_children(xml, "source")
			if not s:
				raise SyntaxError("Source element not found in xml content")
			self.source = s[0].text
			ts = _find_children(xml, "target")
			# self.translations = dict()
			self.translations = list()
			for t in ts:
				# lang = ts.attrib("trgLang")
				# self.translations[lang] = t.text
				self.translations.append(t.text)
		elif unit:
			self.source = unit.key
			self.translations = [unit.value]
		else:
			raise ValueError("Either xml or unit argument must be provided.")

	def to_element(self):
		base = ElementTree.Element(self._node_name)
		base.append(ElementTree.Element("source", text=self.source))
		# todo targets
		return base

	def to_unit(self):
		return Unit(self.source, self.translations[0])


class _Unit(_XLIFFItem):
	_node_name = "unit"
	_children_class = _Segment


class _File(_XLIFFItem):
	_node_name = "file"
	_children_class = _Unit


class XLIFFStore(XMLStore):
	GLOBS = ["*.xliff", "*.xlf"]

	def __init__(self):
		XMLStore.__init__(self)
		self._files = list()
		self.srcLang = None
		self.trgLang = None

	@property
	def units(self):
		def read_unit():
			for f in self._files:
				for u in f.children:
					for s in u.children:
						yield s.to_unit()
		return list(read_unit())

	@units.setter
	def units(self, x):
		f = _File()
		u = _Unit()
		u.children = [_Segment(u) for u in x]
		f.children = [u]
		self._files = f

	def read(self, file, lang=None):
		xliff = ElementTree.parse(file).getroot()
		self.srcLang = xliff.attrib["srcLang"]
		self.trgLang = xliff.attrib["trgLang"]
		files = _find_children(xliff, "file")
		self._files = list()
		for f in files:
			self._files.append(_File(f))

	def serialize(self):
		root = ElementTree.Element("xliff")
		if self.srcLang:
			root.attrib["srcLang"] = self.srcLang
		if self.trgLang:
			root.attrib["trgLang"] = self.trgLang
		for f in self._files:
			root.append(f.to_element())
		return self._pretty_print(ElementTree.tostring(root))