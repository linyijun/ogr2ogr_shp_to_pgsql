from sqlalchemy import Column, Integer, String, Numeric
from geoalchemy2 import Geometry


class OsmTemplate(object):
    __table_args__ = {'schema': 'openstreetmap2021'}

    ogc_fid = Column(Integer, nullable=False, primary_key=True)
    osm_id = Column(String(10), nullable=True)
    code = Column(Numeric(4), nullable=True)
    fclass = Column(String(20), nullable=True)
    name = Column(String(100), nullable=True)


class OsmBuildings(OsmTemplate, object):
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)
    type = Column(String(20), nullable=True)


class OsmPoint(OsmTemplate, object):
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class OsmMultiPolygon(OsmTemplate, object):
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class OsmMultiLine(OsmTemplate, object):
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)
