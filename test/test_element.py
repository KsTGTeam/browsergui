import json
from browsergui import Element, Container, CLICK, KEYDOWN, KEYUP
from browsergui.elements import NoSuchCallbackError, arg_to_js

from . import BrowserGUITestCase

class ElementTest(BrowserGUITestCase):

  def test_construction(self):
    Element(tag_name="a")

  def test_callbacks(self):

    e = Element(tag_name="a")
    e.add_callback(CLICK, self.set_last_event)
    e.add_callback(KEYDOWN, self.set_last_event)

    e.handle_event({'type': CLICK, 'id': e.id})
    self.assertEqual(self.last_event, {'type': CLICK, 'id': e.id})

    e.handle_event({'type': KEYDOWN, 'id': e.id, 'key': 'a'})
    self.assertEqual(self.last_event, {'type': KEYDOWN, 'id': e.id, 'key': 'a'})

    e.remove_callback(CLICK, self.set_last_event)
    with self.assertRaises(NoSuchCallbackError):
      e.remove_callback(CLICK, self.set_last_event)

    self.assertEqual(list(e.callbacks[CLICK]), [])
    self.assertEqual(list(e.callbacks[KEYDOWN]), [self.set_last_event])
    self.assertEqual(list(e.callbacks[KEYUP]), [])

  def test_toggle_visibility(self):
    e = Element(tag_name='a')
    e.toggle_visibility()
    self.assertEqual('none', e.get_style('display'))
    e.toggle_visibility()
    self.assertIsNone(e.get_style('display'))

  def test_arg_to_js(self):
    self.assertEqual("0", arg_to_js(0))
    self.assertEqual("[1, 2]", arg_to_js([1, 2]))

    element = Element(tag_name="a")
    self.assertEqual("document.getElementById({})".format(json.dumps(element.id)), arg_to_js(element))
    self.assertEqual("document.getElementById({})".format(json.dumps(element.id)), arg_to_js(element.tag))


class ContainerTest(BrowserGUITestCase):
  def test_constructor(self):
    Container()
    Container(Container())
    Container(inline=False)

  def test_children_must_be_elements(self):
    with self.assertRaises(TypeError):
      Container(0)

  def test_children(self):
    container = Container()
    first = Container()
    second = Container()

    self.assertEqual(list(container.children), [])

    container.append(first)
    self.assertEqual(list(container.children), [first])

    container.insert_after(second, reference_child=first)
    self.assertEqual(list(container.children), [first, second])

    container.disown(first)
    self.assertEqual(list(container.children), [second])

    container.disown(second)
    self.assertEqual(list(container.children), [])

  def test_hash_static(self):
    c = Container()
    h = hash(c)

    self.assertEqual(h, hash(c))

    c.append(Element(tag_name="b"))
    self.assertEqual(h, hash(c))

    c.add_callback("blahblahtrigger", self.set_last_event)
    self.assertEqual(h, hash(c))
