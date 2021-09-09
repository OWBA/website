#!/bin/sh
# shellcheck disable=SC1091

cd "${0%/*}/.." || exit 1
. tools/lib.sh

enum_links | while read -r link; do
	dir=${link##*	}
	link=${link%	*}
	name=${link%	*}
	target=${link#*	}
	echo "[$name]($target)  --  $dir"
	echo
done
