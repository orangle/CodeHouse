.PHONY: clean build

clean:
	find . -name '*.log' -exec rm -f {} +

build: clean
	dd if=/dev/zero of=test.log bs=1M count=1000