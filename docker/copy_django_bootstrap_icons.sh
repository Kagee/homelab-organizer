#! /bin/bash
set -euxo pipefail
cd "$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/.."

rm -r static/django_bootstrap_icons/{bs,md}_icon || true

echo "INFO: Copying bootstrap icons to static"
#  Path(BS_ICONS_BASE_PATH, "icons", f"{icon_name}.svg")
mkdir -p static/django_bootstrap_icons/bs_icon/icons/
cp node_modules/bootstrap/LICENSE static/django_bootstrap_icons/bs_icon/
git grep -h -i -P "bs_icon"  | \
    awk "match(\$0, /(bs_icon[ (]['\"]([^'\"]*))/, a){print a[2]}" | \
    sort -u | while read -r NAME; do
        cp node_modules/bootstrap-icons/icons/$NAME.svg \
           static/django_bootstrap_icons/bs_icon/icons/;
    done;

echo "INFO: Copying mdi icons to static"

# Path(MD_ICONS_BASE_PATH, "svg", f"{icon_name}.svg")
mkdir -p static/django_bootstrap_icons/md_icon/svg/
cp node_modules/@mdi/svg/LICENSE static/django_bootstrap_icons/md_icon/

git grep -h -i -P "md_icon"  | \
    awk "match(\$0, /(md_icon[ (]['\"]([^'\"]*))/, a){print a[2]}" | \
    sort -u | while read -r NAME; do
        cp node_modules/@mdi/svg/svg/$NAME.svg \
           static/django_bootstrap_icons/md_icon/svg/; 
    done;