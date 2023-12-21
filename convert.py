from os.path import splitext
from sys import argv
from re import split

output = lambda a: print(a, file=output_file)

FILE_START = '{"cells":\n['
FILE_END = '\n],\n"metadata": {"colab": {},"kernelspec": {"display_name": "Python", "language": "python", "name": "python3"}}, "nbformat": 4, "nbformat_minor": 1}'

CELL = '	{"cell_type": "%s", "metadata": {"id": "c%0d"}, %s"source": ["%s"]}'


name, extension = splitext(argv[1])

output_file = open(name + '.ipynb', 'w')

output(FILE_START)

with open(name + extension) as file:
	text = ''.join(line for line in file)

text = text.replace('\\', r'\\').replace('\t', r'\t').replace('\n', r'\n').replace('"', r'\"')



a = split(r'(## |### |#@title )', text)

cell_id = 0
t = ''
for i in range(1, len(a), 2):
	t += '\n'
	if a[i] == '#@title ':
		t += CELL % ('code', cell_id, '"execution_count": 0, "outputs":[], ', a[i] + a[i+1])
	else:
		t += CELL % ('markdown', cell_id, '', a[i] + a[i+1])
	if i + 2 != len(a):
		t += ','
	cell_id += 1

with open(name + '.ipynb', 'w') as file:
	print(FILE_START + t + FILE_END, file=file)
