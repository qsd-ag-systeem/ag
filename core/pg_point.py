from sqlalchemy import func
import sqlalchemy.types as types


class Point(types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self):
        return "POINT"

    def bind_expression(self, bindvalue):
        return func.POINT(bindvalue, type_=self)

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            return "%s, %s" % (value[1], value[0])
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None

            if value.startswith('('):
                value = value[1:]
            if value.endswith(')'):
                value = value[:-1]

            lng, lat = value.split(',')
            lng = lng.strip()
            lat = lat.strip()
            
            return (float(lat), float(lng))
        return process
