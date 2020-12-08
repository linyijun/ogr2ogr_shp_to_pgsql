import os

from common_db import create_table_obj, drop_table, DB_USERNAME, DB_NAME
from osm_models import OsmPoint, OsmMultiPolygon, OsmMultiLine, OsmBuildings


POINT_OSM = ['natural', 'places', 'pois', 'pofw', 'traffic', 'transport']
LINE_OSM = ['railways', 'roads', 'waterways']
POLYGON_OSM = ['landuse_a', 'natural_a', 'places_a', 'pois_a', 'pofw_a', 'traffic_a', 'transport_a', 'water_a']


def ogr2ogr_from_local(file_path, schema, table_name):

    table_obj = None

    if 'buildings_a' in table_name:
        table_obj = create_table_obj(table_name, OsmBuildings)

    for osm in POINT_OSM:
        if osm in table_name and '_a' not in table_name:
            table_obj = create_table_obj(table_name, OsmPoint)

    for osm in LINE_OSM:
        if osm in table_name:
            table_obj = create_table_obj(table_name, OsmMultiLine)

    for osm in POLYGON_OSM:
        if osm in table_name:
            table_obj = create_table_obj(table_name, OsmMultiPolygon)

    drop_table(table_obj)
    print(f'ogr2ogr -f PostgreSQL PG:"dbname = {DB_NAME} user={DB_USERNAME}" -nlt PROMOTE_TO_MULTI '
          f'{file_path} -nln {table_name}')

    os.system(f'ogr2ogr -f PostgreSQL PG:"dbname = {DB_NAME} user={DB_USERNAME}" -nlt PROMOTE_TO_MULTI '
              f'{file_path} -nln {schema}.{table_name}')


if __name__ == '__main__':

    path = './illinois-latest-free.shp'
    state_name = 'illinois'
    schema = 'openstreetmap2021'

    for r, d, f in os.walk(path):

        for file in f:
            if file.endswith('.shp'):

                file_path = os.path.join(r, file)
                feature_name = file.split('_')[1: -2]
                table_name = '_'.join([state_name] + feature_name)
                ogr2ogr_from_local(file_path, schema, table_name)
