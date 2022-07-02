# lint
.PHONY: lint
lint:
	poetry run pysen run lint

# format
.PHONY: format
format:
	poetry run pysen run format

# test
.PHONY: test
test:
	poetry run pytest -s -vv ./tests


# get mnist image
.PHONY: get_mnist
get_mnist:
	poetry run python -m conv_animation.get_mnist_image
