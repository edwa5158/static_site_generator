clear && \
uv tool run coverage run --rcfile=pyproject.toml \
&& uv tool run coverage report -m \
&& uv tool run coverage html
