install:
	pip install -r requirements.txt

run:
	cd src && python main.py

prepare:
	cd src && python -c 'import main; main.prepare_data()'

visualize:
	cd src && python -c 'import main; main.show_graphs()'

test:
	cd src && python -c 'import main; main.show_best_apps(3)'
