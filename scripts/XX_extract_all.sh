#!/usr/bin/env sh

./scripts/00_download_last_wikipedia_dump.sh en
poetry run python ./scripts/01_extract_nodes_to_json.py
poetry run python ./scripts/02_extract_redirections_to_json.py
# poetry run python ./scripts/03_extract_infobox_to_json.py
poetry run python ./scripts/04_extract_categories_to_json.py
poetry run python ./scripts/05_extract_portals_to_json.py
poetry run python ./scripts/06_extract_links_to_json.py
poetry run python ./scripts/07_alim_duckdb_except_links.py
poetry run python ./scripts/08_alim_duckdb_links.py
# poetry run python ./scripts/09_extract_danker_file.py
# poetry run python ./scripts/10_compute_danker_rank.sh
# poetry run python ./scripts/11_alim_danker.py
