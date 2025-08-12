
from pydov.util.notebook import HtmlFormatter


class ReturnFieldList(list):
    """List of return fields used in search methods. """

    def __contains__(self, __key: object):
        """Overwrite the default method. Checks on field name.

        Parameters
        ----------
        __key
            The key to check.

        Returns
        -------
        boolean
            Whether the key is one of the names in the ReturnFieldList.
        """
        return __key in [i.name for i in self]

    def get_names(self):
        """Return a list with all the names of the fields in this
        ReturnFieldList.

        Returns
        -------
        list of str
            List of field names.
        """
        return [f.name for f in self]

    @classmethod
    def from_field_names(self, *return_fields):
        """Initiale a ReturnFieldList from a list of return field names.

        Parameters
        ----------
        return_fields : list or set or tuple of str
            List, set or tuple of return field names.

        Returns
        -------
        ReturnFieldList
            Equivalent ReturnFieldList.

        Raises
        ------
        AttributeError
            If the value of return_fields is not a list, set or tuple.
        """
        if len(return_fields) == 0:
            return None

        if len(return_fields) == 1:
            return_fields = return_fields[0]

        if isinstance(return_fields, str):
            return_fields = (return_fields,)

        if return_fields is None:
            return None

        if not isinstance(return_fields, (list, set, tuple)):
            # FIXME: this should be TypeError instead
            raise AttributeError(
                'return_fields should be a list, set or tuple')

        result = ReturnFieldList()
        for rf in return_fields:
            if isinstance(rf, AbstractReturnField):
                result.append(rf)
            else:
                result.append(ReturnField.from_field_name(rf))
        return result


class AbstractReturnField:
    """Base class of ReturnField and GeometryReturnField."""

    def __init__(self, name):
        """Initialisation.

        Parameters
        ----------
        name : str
            Name of the return field.
        """
        self.name = name

    @classmethod
    def from_field_name(cls, name):
        """Initialise a new instance from a field name.

        Parameters
        ----------
        name : str
            Field name.

        Returns
        -------
        Instance of this class.
            Instance of ReturnField or GeometryReturnField.
        """
        return cls(name)


class ReturnField(AbstractReturnField):
    """Normal (non-geometry) return field."""

    def __init__(self, name):
        """Initialisation.

        Parameters
        ----------
        name : str
            Name of the return field.
        """
        super().__init__(name)


class GeometryReturnField(AbstractReturnField):
    def __init__(self, geometry_field, epsg=None):
        """Initialise a geometry return field.

        Parameters
        ----------
        geometry_field : str
            Name of the geometry field.
        epsg : int, optional
            EPSG code of the CRS of the geometries that will be returned.
            Defaults to None, which means the default CRS of the WFS layer.
        """
        super().__init__(geometry_field)

        if epsg is not None:
            if not isinstance(epsg, int):
                raise TypeError('epsg should be an integer value')

        self.epsg = epsg


class FieldMetadataList:
    def __init__(self):
        self.fields = {}

    def add(self, field_metadata):
        self.fields[field_metadata.name] = field_metadata

    def __dir__(self):
        return list(self.fields.keys())

    def __getitem__(self, name):
        if name in self.fields:
            return self.fields.get(name)
        raise KeyError(f'{name}')

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields.get(name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has not attribute '{name}'")

    def __repr__(self):
        return self.fields.__repr__()
        s = ', '.join(i.__repr__() for i in self.fields.values())

        return f'<pydov.types.fields.FieldMetadataList: {s}>'

    def _repr_html_(self):
        s = ''.join(i._repr_html_() for i in self.fields.values())
        return f'<div>{s}</div>'


class FieldMetadata(HtmlFormatter):
    @staticmethod
    def from_dict(field):
        fm = FieldMetadata()
        fm.__field = field
        return fm

    def __dir__(self):
        return list(self.__field.keys())

    def __getitem__(self, name):
        if name in self.__field:
            return self.__field.get(name)
        raise KeyError(f'{name}')

    def __getattr__(self, name):
        if name in self.__field:
            return self.__field.get(name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has not attribute '{name}'")

    def __repr__(self):
        return self.__field.__repr__()

    def _repr_html_(self):
        html = (f"<p><b>{self.__field['name']}</b>"
                f" - {self.__field['definition']}</p>")

        html += '<ul>'
        html += f'<li>type: {self.type}</li>'
        html += f'<li>notnull: {self.notnull}</li>'
        html += f'<li>query: {self.query}</li>'
        html += f'<li>cost: {self.cost}</li>'
        html += f'<li>list: {self.list}</li>'

        if self.__field.get('values') is not None:
            html += f'<li>values:</li>'
            # html += '<div class="indent">'
            html += self.values._repr_html_()
            # html += '</div>'
        html += '</ul>'

        return super()._repr_html_(html, with_header=False)
