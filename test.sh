coverage erase \
&& coverage run -m unittest discover -s src/tests \
&& coverage report -m \
&& coverage html
