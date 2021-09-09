#!/bin/sh
# shellcheck disable=SC1091

cd "${0%/*}/.." || exit 1
. tools/lib.sh

enum_links | while read -r link; do
	dir=${link##*	}
	link=${link%	*}
	name=${link%	*}
	target=${link#*	}
	unset err
	case "$target" in
		http:*|https:*|mailto:*|feed:*|tel:*);;  # ignore
		/*)  # absolute path
			if [ ! -e "./content/$target" ]; then err=1; fi;;
		*)  # probably relative path. If not, add exception above
			if [ ! -e "$dir/$target" ]; then err=1; fi;;
	esac
	if [ $err ]; then
		echo "Link: [$name]($target)"
		echo "File: $dir"
		echo
	fi
done
