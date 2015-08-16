from browsergui import Dropdown, Text
from . import BrowserGUITestCase

def dropdown_xml(*options):
  return '<select oninput="notify_server({{target_id: this.getAttribute(&quot;id&quot;), type_name: event.type, value: this.value}})">{}</select>'.format(''.join('<option value="{s}">{s}</option>'.format(s=s) for s in options))

class DropdownTest(BrowserGUITestCase):

  def test_construction(self):
    self.assertEqual([], list(Dropdown()))
    self.assertEqual(['a', 'b'], list(Dropdown(['a', 'b'])))

  def test_options_must_be_strings(self):
    with self.assertRaises(TypeError):
      Dropdown([()])

    d = Dropdown(['a'])
    with self.assertRaises(TypeError):
      d[0] = ()
    with self.assertRaises(TypeError):
      d.insert(0, ())

  def test_getitem(self):
    d = Dropdown(['a', 'b'])
    self.assertEqual(['a', 'b'], d[:])
    self.assertEqual('a', d[0])
    with self.assertRaises(IndexError):
      d[2]

  def test_delitem(self):
    d = Dropdown(['a', 'b'])

    del d[0]
    self.assertEqual('b', d[0])
    with self.assertRaises(IndexError):
      d[1]

    self.assertHTMLLike(dropdown_xml('b'), d)

  def test_setitem(self):
    d = Dropdown(['a', 'b'])

    d[0] = 'c'
    self.assertEqual(d[0], 'c')
    self.assertEqual(2, len(d))

    self.assertHTMLLike(dropdown_xml('c', 'b'), d)

  def test_insert(self):
    d = Dropdown()

    d.insert(0, 'b')
    d.insert(0, 'a')
    d.insert(99, 'd')
    d.insert(-1, 'c')
    self.assertEqual(['a', 'b', 'c', 'd'], list(d))
    self.assertHTMLLike(dropdown_xml('a', 'b', 'c', 'd'), d)

  def test_tag(self):
    self.assertHTMLLike(dropdown_xml(), Dropdown())
