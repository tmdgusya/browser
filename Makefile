test-1:
	uv run -m src.browser https://browser.engineering/examples/example1-simple.html

test-2:
	uv run -m src.url file://1.txt

test-3:
	uv run -m src.url view-source:http://browser.engineering/examples/example1-simple.html

test-4:
	uv run -m src.browser http://browser.engineering/history.html