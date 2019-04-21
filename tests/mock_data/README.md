# Explanations of mock data

### General:
1) `basic.json` - A basic title and test 2 rows.
2) `three_pages.json` - A stripped down version just to check that we separate 3 pages
3) `markdown.json` - A more rich markdown example
4) `picture.json` - An inline picture example
5) `md_basic.json` - Basic markdown of text

### Invalid
3) `empty.json` - An empty json file
4) `invalid.json` - A malformed json file (JSONDecode Error)
5) `bad_sane_json_1.json` - An invalid sane json file (not a list)
   - `bad_sane_json_2.json` - missing layout
   - `bad_sane_json_3.json` - missing columnPos
   - `bad_sane_json_4.json` - missing rowPos
   - `bad_sane_json_5.json` - missing w
   - `bad_sane_json_6.json` - missing h
   - `bad_sane_json_7.json` - missing missing rowPos and h in second section 
6) `invalid_layout_keys.json` - an empty invalid empty keys in layout

### Grid Checks
1) `fullgrid` - a page with a full 12x12 grid.
7) `onecellgrid.json` - only one cell.
8) `mergegrid.json` - a full page grid with strange merged cells.

