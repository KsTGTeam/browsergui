import os
from browsergui import *

click_counter = 0
def note_click():
  global click_counter
  click_counter += 1
  button.text = 'Button ({} clicks)'.format(click_counter)
button = Button('Button (0 clicks)', callback=note_click)

reversed_text_field_contents = Text(''.join(reversed('Reversed')))
def note_text_field_change():
  reversed_text_field_contents.text = ''.join(reversed(text_field.value))
text_field = TextField(value='Reversed', change_callback=note_text_field_change)

selected_dropdown_item = Text('')
def note_dropdown_change():
  selected_dropdown_item.text = dropdown.value
dropdown = Dropdown(['Dr', 'op', 'do', 'wn'], change_callback=note_dropdown_change)
selected_dropdown_item.text = dropdown.value

number_field_contents = Text('')
def note_number_change():
  number_field_contents.text = number_field.value
number_field = NumberField(value=12, change_callback=note_number_change)
number_field_contents.text = str(number_field.value)

colored_text = Text('colored')
def note_color_change():
  colored_text.set_styles(color=color_field.value_to_xml_string(color_field.value))
color_field = ColorField(change_callback=note_color_change)

elements = (
  Text("Plain text."),
  CodeSnippet("Inline code."),
  Paragraph("A paragraph of text."),
  CodeBlock("A block of code."),
  button,
  Container(text_field, reversed_text_field_contents),
  Container(dropdown, Text('Selected: '), selected_dropdown_item),
  Container(number_field, Text('You entered: '), number_field_contents),
  Container(color_field, colored_text),
  Link("A link.", url="http://google.com"),
  Image(os.path.join(os.path.dirname(__file__), 'tour-image.png')),
  Viewport(Paragraph('viewport '*1000, styling={'width': 1000}), width=400, height=200),
  List(items=(Text("lists"), CodeSnippet("lists"), List(items=(Text("sublists"),)))),
  Grid([[None, Text('browsergui', styling={'font-weight':'600'}), Text('tkinter', styling={'font-weight':'600'})],
        [Text('has grids', styling={'font-weight':'600'}), Text('yes'), Text('yes')],
        [Text('made by me', styling={'font-weight':'600'}), Text('yes'), Text('no')]]))

gui = GUI(Paragraph("Here are all the elements available to you:"), title="Browser GUI tour")
for element in elements:
  gui.append(Container(element, styling={'margin': '1em', 'border': '1px solid black'}))

def main():
  run(gui)

if __name__ == '__main__':
  main()
