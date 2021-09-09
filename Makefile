.PHONY: help verify ls-links ls-img-size

help:
	@echo 'available commands: verify, ls-links, ls-img-size'

verify:
	@echo 'checking broken links...'
	@sh tools/check-broken-links.sh
	@echo 'done.'
	@echo
	@echo 'checking wrong quotes...'
	@find ./content -type f -name contents.lr -exec grep "´" {} + || echo 'done.'

ls-links:
	@sh tools/list-all-links.sh

ls-img-size:
	@echo 'checking custom set image size...'
	@find ./content -type f -name contents.lr -exec grep --color=auto "^\(width\|height\): [^0]" {} + || echo 'done.'
