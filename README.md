svg-map-draw
============

This respository contains assorted Python scripts that I use to make SVG maps from [OGR](http://www.gdal.org/ogr/) data sources - principally [PostGIS](http://postgis.net/) databases.

mapcode.py
----------
This is a module that generates SVG maps. You initialise a `Map` object with two parameters: the first the number of pixels you want the map to contain; the second a tuple of the bounds (west, south, east, north) of the map in whatever projection you're using. You then call various methods, which all print to standard output, to generate the SVG.

* `print_header` must be called before any other methods.
* `render_multipolygon` draws shapes from a multipolygon OGR layer. It takes four parameters: the OGR layer, a string to use as the group ID in the SVG output, the name of a field in the OGR field to use to label the individual shapes that are drawn (may be `None`), and a string which is used as the `style` attribute for the shapes that are drawn.
* `render_multiline` draws lines from a multiline OGR layer. It takes three parameters: the OGR layer, a string to use as the group ID in the SVG output, and a string which is used as the `style` attribute for the lines that are drawn.
* `print_footer` must be called after all other methods.

example.py
----------
This is an example of how `mapcode.py` can be used.

apply-colors.py
---------------
This program changes the colour of elements in an SVG file based on the IDs of the elements and a CSV file supplied. The CSV file must contain two column, the first containing SVG element IDs, and the second containing six-character hex RGB codes. You pass the program the name of the CSV on the command line, and an SVG file as standard input. It then changes the colours of any elements in the SVG file that have an ID listed in the CSV file to the colour indicated for that ID in the CSV file, and writes the resulting SVG file to standard output.
