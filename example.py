#!/usr/bin/env python

import sys
from osgeo import ogr
import mapcode

themap = mapcode.Map('ZA', 1000000, (-785420, -710582, 832443, 695214))
conn = ogr.Open("PG: dbname=wikimaps")
select = ' ST_Multi(ST_Intersection(ST_Transform(geom, 60001), ST_MakeEnvelope(%f, %f, %f, %f, 60001))) ' % (themap.west - 20000, themap.south - 20000, themap.east + 20000, themap.north + 20000)
select_simp = select.replace("geom", "geom_simp")

themap.print_header()

layer = conn.ExecuteSQL("SELECT " + select + " FROM neighbour_land")
themap.render_multipolygon(layer, "neighbour", None, "fill:#e0e0e0;stroke:none")

layer = conn.ExecuteSQL("SELECT code, " + select_simp + " FROM muni")
themap.render_multipolygon(layer, "muni", "code", "stroke:#646464;stroke-width:1;stroke-linecap:butt;stroke-linejoin:bevel;")

layer = conn.ExecuteSQL("SELECT " + select_simp + " FROM prov_border")
themap.render_multiline(layer, "provborder", "fill:none;stroke:#646464;stroke-width:1.5;stroke-linejoin:bevel;stroke-linecap:round")

layer = conn.ExecuteSQL("SELECT " + select + " FROM country_border")
themap.render_multiline(layer, "nationborder", "fill:none;stroke:#646464;stroke-width:2.5;stroke-linejoin:bevel;stroke-linecap:round")

layer = conn.ExecuteSQL("SELECT " + select + " FROM coast")
themap.render_multiline(layer, "coastline", "fill:none;stroke:#0978ab;stroke-width:1.5;stroke-linejoin:bevel;stroke-linecap:round")

themap.print_footer()
