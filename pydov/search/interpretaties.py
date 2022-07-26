# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV interpretations."""

from pydov.search.abstract import AbstractSearch
from pydov.types.interpretaties import (FormeleStratigrafie,
                                        GecodeerdeLithologie,
                                        GeotechnischeCodering,
                                        HydrogeologischeStratigrafie,
                                        InformeleHydrogeologischeStratigrafie,
                                        InformeleStratigrafie,
                                        LithologischeBeschrijvingen,
                                        QuartairStratigrafie)


class InformeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about 'informele stratigrafie'."""

    def __init__(self, objecttype=InformeleStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the InformeleStratigrafie type.
            Optional: defaults to the InformeleStratigrafie type
            containing the fields described in the documentation.

        """
        super(InformeleStratigrafieSearch, self).__init__(
            'interpretaties:informele_stratigrafie', objecttype)


class FormeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve the interpretation for Formele
    stratigrafie"""

    def __init__(self, objecttype=FormeleStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the FormeleStratigrafie type.
            Optional: defaults to the FormeleStratigrafie type containing the
            fields described in the documentation.

        """
        super(FormeleStratigrafieSearch, self).__init__(
            'interpretaties:formele_stratigrafie', objecttype)


class HydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve hydrogeological interpretations """

    def __init__(self, objecttype=HydrogeologischeStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the HydrogeologischeStratigrafie
            type. Optional: defaults to the HydrogeologischeStratigrafie type
            containing the fields described in the documentation.

        """
        super(HydrogeologischeStratigrafieSearch, self).__init__(
            'interpretaties:hydrogeologische_stratigrafie',
            objecttype)


class LithologischeBeschrijvingenSearch(AbstractSearch):
    """Search class to retrieve lithologische beschrijvingen """

    def __init__(self, objecttype=LithologischeBeschrijvingen):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the LithologischeBeschrijvingen
            type. Optional: defaults to the LithologischeBeschrijvingen type
            containing the fields described in the documentation.

        """
        super(LithologischeBeschrijvingenSearch, self).__init__(
            'interpretaties:lithologische_beschrijvingen',
            objecttype)


class GecodeerdeLithologieSearch(AbstractSearch):
    """Search class to retrieve gecodeerde lithologie """

    def __init__(self, objecttype=GecodeerdeLithologie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GecodeerdeLithologie type.
            Optional: defaults to the GecodeerdeLithologie type containing
            the fields described in the documentation.

        """
        super(GecodeerdeLithologieSearch, self).__init__(
            'interpretaties:gecodeerde_lithologie',
            objecttype)


class GeotechnischeCoderingSearch(AbstractSearch):
    """Search class to retrieve geotechnische codering """

    def __init__(self, objecttype=GeotechnischeCodering):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GeotechnischeCodering type.
            Optional: defaults to the GeotechnischeCodering type containing
            the fields described in the documentation.

        """
        super(GeotechnischeCoderingSearch, self).__init__(
            'interpretaties:geotechnische_coderingen',
            objecttype)


class QuartairStratigrafieSearch(AbstractSearch):
    """Search class to retrieve the interpretation for Quartair
    stratigrafie"""

    def __init__(self, objecttype=QuartairStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the QuartairStratigrafie type.
            Optional: defaults to the QuartairStratigrafie type containing
            the fields described in the documentation.

        """
        super(QuartairStratigrafieSearch, self).__init__(
            'interpretaties:quartaire_stratigrafie', objecttype)


class InformeleHydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about informele
    hydrogeologische stratigrafie.

    Parameters
    ----------
    objecttype : subclass of pydov.types.abstract.AbstractDovType
        Reference to a class representing the
        InformeleHydrogeologischeStratigrafie type.
        Optional: defaults to the InformeleHydrogeologischeStratigrafie type
        containing the fields described in the documentation.

    """

    def __init__(self, objecttype=InformeleHydrogeologischeStratigrafie):
        """Initialisation."""
        super(InformeleHydrogeologischeStratigrafieSearch, self).__init__(
            'interpretaties:informele_hydrogeologische_stratigrafie',
            objecttype)
