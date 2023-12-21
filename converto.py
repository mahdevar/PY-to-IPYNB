from os.path import splitext
from sys import argv

output = lambda a: print(a, file=output_file)

FILE_START = '{"cells":\n['
FILE_END = '],\n"metadata": {"colab": {},"kernelspec": {"display_name": "Python", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 1}'

CELL = '	{"cell_type": "%s", "metadata": {"id": "c%0d"}, %s"source": ["%s"]}'


def text_to_cell(text, id):
	if text.startswith('#@title '):
		return CELL % ('code', id, '"execution_count": 0, "outputs":[], ', text)
	else:
		return CELL % ('markdown', id, '', text)


name, extension = splitext(argv[1])

output_file = open(name + '.ipynb', 'w')

output(FILE_START)

current_cell = ''
cell_id = 0
with open(name + extension) as file:
	for line in file:
		if any(line.startswith(prefix) for prefix in ['## ', '### ', '#@title ']) and current_cell:
			output(text_to_cell(current_cell, cell_id) + ',')
			current_cell = ''
			cell_id += 1
		current_cell += line.replace('\\', r'\\').replace('\t', r'\t').replace('\n', r'\n').replace('"', r'\"')

output(text_to_cell(current_cell, cell_id))
output(FILE_END)

output_file.close()
exit()
