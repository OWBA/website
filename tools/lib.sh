#!/bin/sh

cd "${0%/*}/.." || exit 1

enum_links() {
	find . -type f -name 'contents.lr' | while read -r file; do
		dir="${file%contents\.lr}"
		sed -n 's/^.*\[\([^]]*\)\](\([^)]*\)).*$/\1	\2/p' "$file" | while read -r match; do
			echo "$match	$dir"
		done
	done
}
