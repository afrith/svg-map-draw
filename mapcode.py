from math import sqrt

class Map(object):

    def __init__(self, provcode, pixels, bounds):
        (self.west, self.south, self.east, self.north) = map(float, bounds)

        geowidth = self.east - self.west
        geoheight = self.north - self.south

        scale = sqrt(pixels / (geowidth * geoheight))
        self.mapwidth = int(round(scale * geowidth))
        self.mapheight = int(round(scale * geoheight))

        self.horizscale = float(self.mapwidth) / geowidth
        self.vertscale = float(self.mapheight) / geoheight

        self.mapwidth += 50
        self.west -= 25/self.horizscale
        self.east += 25/self.horizscale

        self.mapheight += 50
        self.south -= 25/self.vertscale
        self.north += 25/self.vertscale

    def lon_to_x(self, lon):
        return (lon - self.west) * self.horizscale

    def lat_to_y(self, lat):
        return (self.north - lat) * self.vertscale

    def geo_to_map(self, lon, lat):
        return ((lon - self.west) * self.horizscale, (self.north - lat) * self.vertscale)

    def render_multipolygon(self, layer, svgid, idfield, style):
        layer.SetSpatialFilterRect(self.west, self.south, self.east, self.north)

        print '<g id="%s" style="%s">' % (svgid, style)

        feat = layer.GetNextFeature()
        while feat:
            if idfield:
                print '<g id="%s">' % feat.GetFieldAsString(idfield)
            else:
                print '<g>'
            geom = feat.GetGeometryRef()
            for pidx in range(0, geom.GetGeometryCount()):
                part = geom.GetGeometryRef(pidx)
                path = ""
                for ridx in range(0, part.GetGeometryCount()):
                    ring = part.GetGeometryRef(ridx)
                    path += "M "
                    oldx, oldy = self.geo_to_map(ring.GetX(0), ring.GetY(0))
                    path += "%.2f,%.2f " % (oldx, oldy)
                    for pti in range(1, ring.GetPointCount()):
                        newx, newy = self.geo_to_map(ring.GetX(pti), ring.GetY(pti))
                        path += "L %.2f,%.2f " % (newx, newy)
                        oldx, oldy = newx, newy
                    path += "z "
                print '<path d="%s" />' % path

            print '</g>'
            feat = layer.GetNextFeature()

        print '</g>'

    def render_polygon_color(self, layer, svgid, colfield):
        layer.SetSpatialFilterRect(self.west, self.south, self.east, self.north)

        print '<g id="%s" style="stroke:none">' % (svgid, )

        firstgroup = True
        currentcolor = ''
        feat = layer.GetNextFeature()
        while feat:
            color = feat.GetFieldAsString(colfield)
            if color <> currentcolor:
                currentcolor = color
                if firstgroup:
                    firstgroup = False
                else:
                    print '</g>'
                print '<g id="color-%s" style="fill:#%s">' % (color, color)
            geom = feat.GetGeometryRef()
            path = ""
            for ridx in range(0, geom.GetGeometryCount()):
                ring = geom.GetGeometryRef(ridx)
                path += "M "
                oldx, oldy = self.geo_to_map(ring.GetX(0), ring.GetY(0))
                path += "%.2f,%.2f " % (oldx, oldy)
                for pti in range(1, ring.GetPointCount()):
                    newx, newy = self.geo_to_map(ring.GetX(pti), ring.GetY(pti))
                    path += "L %.2f,%.2f " % (newx, newy)
                    oldx, oldy = newx, newy
                path += "z "
            print '<path d="%s" />' % path
            feat = layer.GetNextFeature()
        print '</g>'
        print '</g>'


    def render_multiline(self, layer, svgid, style):
        layer.SetSpatialFilterRect(self.west, self.south, self.east, self.north)

        print '<g id="%s" style="%s">' % (svgid, style)

        feat = layer.GetNextFeature()
        while feat:
            path = ""
            geom = feat.GetGeometryRef()
            for pidx in range(0, geom.GetGeometryCount()):
                part = geom.GetGeometryRef(pidx)
                path += "M "
                oldx, oldy = self.geo_to_map(part.GetX(0), part.GetY(0))
                path += "%.2f,%.2f " % (oldx, oldy)
                for pti in range(1, part.GetPointCount() - 1):
                    newx, newy = self.geo_to_map(part.GetX(pti), part.GetY(pti))
                    path += "L %.2f,%.2f " % (newx, newy)
                    oldx, oldy = newx, newy
                path += "L %.2f,%.2f " % self.geo_to_map(part.GetX(part.GetPointCount() - 1), part.GetY(part.GetPointCount() - 1))
            print '<path d="%s" />' % path
            feat = layer.GetNextFeature()

        print '</g>'

    def print_header(self):
        print '<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg"'
        print '     version="1.1" width="%d" height="%d" id="doc">' % (self.mapwidth, self.mapheight)

        print '<defs id="defs"><clipPath id="mapclip">'
        print '<rect width="%d" height="%d" x="0" y="0" id="cliprect" />' % (self.mapwidth, self.mapheight)
        print '</clipPath></defs>'

        print '<g id="map" clip-path="url(#mapclip)">'

        print '<rect width="%d" height="%d" x="0" y="0" id="ocean" style="fill:#c6ecff" />' % (self.mapwidth, self.mapheight)

    def print_footer(self):
        print '</g>'
        print '</svg>'
