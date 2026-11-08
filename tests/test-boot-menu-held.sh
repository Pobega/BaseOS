#!/bin/sh
set -eu

HERE="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$HERE/overlay/usr/sbin/boot-menu-held"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

# The vendor H700 gpio-key driver does not maintain EVIOCGKEY state, so the
# active-low debugfs line is the authoritative cold-boot source.
printf '%s\n' \
	' gpio-131 (                    |GPIO Key Menu       ) in  lo' \
	> "$TMP/gpio-held"
BASEOS_GPIO_DEBUG="$TMP/gpio-held" sh "$SCRIPT"

printf '%s\n' \
	' gpio-131 (                    |GPIO Key Menu       ) in  hi' \
	> "$TMP/gpio-released"
if BASEOS_GPIO_DEBUG="$TMP/gpio-released" sh "$SCRIPT"; then
	echo "released MENU reported held" >&2
	exit 1
fi

# Missing state and similarly named consumers must fail closed into normal boot.
if BASEOS_GPIO_DEBUG="$TMP/missing" sh "$SCRIPT"; then
	echo "missing GPIO state reported held" >&2
	exit 1
fi
printf '%s\n' \
	' gpio-99  (                    |GPIO Key Menu LED   ) in  lo' \
	> "$TMP/gpio-other"
if BASEOS_GPIO_DEBUG="$TMP/gpio-other" sh "$SCRIPT"; then
	echo "non-MENU GPIO reported held" >&2
	exit 1
fi

# On V90S (a133p), button@17 (BTN_MODE on PD13 = gpio-109) has `lable = "Mode"`
# in the vendor DTB, so debugfs shows `?` as the consumer label.
printf '%s\n' 'BASEOS_PLATFORM=a133p' > "$TMP/release-a133p"
printf '%s\n' \
	' gpio-109 (                    |?                   ) in  lo    ' \
	> "$TMP/gpio-v90s-held"
BASEOS_RELEASE_FILE="$TMP/release-a133p" BASEOS_GPIO_DEBUG="$TMP/gpio-v90s-held" sh "$SCRIPT"

printf '%s\n' \
	' gpio-109 (                    |?                   ) in  hi    ' \
	> "$TMP/gpio-v90s-released"
if BASEOS_RELEASE_FILE="$TMP/release-a133p" BASEOS_GPIO_DEBUG="$TMP/gpio-v90s-released" sh "$SCRIPT"; then
	echo "released V90S MENU reported held" >&2
	exit 1
fi

echo "boot-menu-held structural tests passed"
