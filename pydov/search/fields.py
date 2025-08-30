
from pydov.util.notebook import HtmlFormatter
from pydov.util.wrappers import AbstractDictLike


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


class FieldMetadataList(AbstractDictLike):
    """List of FieldMetadata objects. """

    def add(self, field_metadata):
        """Add a FieldMetadata object to this list.

        Parameters
        ----------
        field_metadata : FieldMetadata
            The FieldMetadata object to add.
        """
        self.base_dict[field_metadata.name] = field_metadata

    def _repr_html_(self):
        """HTML representation for Jupyter notebooks.

        Returns
        -------
        str
            The HTML representation.
        """
        s = ''.join(i._repr_html_() for i in self.base_dict.values())
        return f'<div>{s}</div>'


class FieldMetadata(AbstractDictLike, HtmlFormatter):
    """Class holding metadata for a field."""

    def _repr_html_(self):
        """HTML representation for Jupyter notebooks.

        Returns
        -------
        str
            The HTML representation.
        """
        html = (f"<p><b>{self.base_dict['name']}</b>"
                f" - {self.base_dict['definition']}</p>")

        html += '<ul>'
        html += f'<li>type: <span class="code small">{self.type}</span></li>'
        html += (f'<li>notnull: <span class="code small">{self.notnull}'
                 '</span></li>')
        html += f'<li>query: <span class="code small">{self.query}</span></li>'
        html += f'<li>cost: <span class="code small">{self.cost}</span></li>'
        html += f'<li>list: <span class="code small">{self.list}</span></li>'

        if self.base_dict.get('codelist') is not None:
            html += '<li>codelist:</li>'
            html += self.base_dict.get('codelist')._repr_html_()
        html += '</ul>'

        return super()._repr_html_(html, with_header=False)
