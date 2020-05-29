"""Module grouping tests for the pydov.util.query module."""
from itertools import permutations

import numpy as np
import pandas as pd
import pytest
from owslib.etree import etree

from pydov.util.dovutil import build_dov_url
from pydov.util.query import Join, PropertyInList
from tests.abstract import clean_xml


class TestPropertyInList(object):
    """Test the PropertyInList query expression."""
    def test(self):
        """Test the PropertyInList expression with a standard list.

        Test whether the generated query is correct.

        """
        l = ['a', 'b', 'c']

        query = PropertyInList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'methode'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l.remove(literal.text)

        assert len(l) == 0

    def test_stable(self):
        """Test the PropertyInList expression with a standard list.

        Test whether the generated query is correct and stable.

        """
        l = ['a', 'b', 'c']

        for p in permutations(l):
            query = PropertyInList('methode', list(p))
            xml = query.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<ogc:Or><ogc:PropertyIsEqualTo><ogc:PropertyName>methode</ogc'
                ':PropertyName><ogc:Literal>a</ogc:Literal></ogc'
                ':PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName'
                '>methode</ogc:PropertyName><ogc:Literal>b</ogc:Literal></ogc'
                ':PropertyIsEqualTo><ogc:PropertyIsEqualTo><ogc:PropertyName'
                '>methode</ogc:PropertyName><ogc:Literal>c</ogc:Literal></ogc'
                ':PropertyIsEqualTo></ogc:Or>')

    def test_duplicate(self):
        """Test the PropertyInList expression with a list containing
        duplicates.

        Test whether the generated query is correct and does not contain the
        duplicate entry twice.

        """
        l = ['a', 'a', 'b', 'c']
        l_output = ['a', 'b', 'c']

        query = PropertyInList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'methode'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l_output.remove(literal.text)

        assert len(l_output) == 0

    def test_list_single(self):
        """Test the PropertyInList expression with a list containing
        a single item.

        Test whether the generated query is correct and does contain only a
        single PropertyIsEqualTo.

        """
        l = ['a']

        query = PropertyInList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

        propertyname = xml.find('./{http://www.opengis.net/ogc}PropertyName')
        assert propertyname.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/ogc}Literal')
        assert literal.text in l

        l.remove(literal.text)
        assert len(l) == 0

    def test_list_single_duplicate(self):
        """Test the PropertyInList expression with a list containing
        a single duplicated item.

        Test whether the generated query is correct and does contain only a
        single PropertyIsEqualTo.

        """
        l = ['a', 'a']
        l_output = ['a']

        query = PropertyInList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

        propertyname = xml.find('./{http://www.opengis.net/ogc}PropertyName')
        assert propertyname.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/ogc}Literal')
        assert literal.text in l_output

        l_output.remove(literal.text)
        assert len(l_output) == 0

    def test_emptylist(self):
        """Test the PropertyInList expression with an empty list.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = []
            PropertyInList('methode', l)

    def test_nolist(self):
        """Test the PropertyInList expression with a string instead of a list.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = 'goed'
            PropertyInList('betrouwbaarheid', l)


class TestJoin(object):
    """Test the Join query expression."""
    def test(self):
        """Test the Join expression with a standard dataframe.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = Join(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l.remove(literal.text)

        assert len(l) == 0

    def test_duplicate(self):
        """Test the Join expression with a column containing
        duplicates.

        Test whether the generated query is correct and does not contain the
        duplicate entry twice.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1980-068861')]

        l_output = [build_dov_url('data/boring/1986-068853'),
                    build_dov_url('data/boring/1980-068861')]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = Join(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 2

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l_output.remove(literal.text)

        assert len(l_output) == 0

    def test_wrongcolumn(self):
        """Test the Join expression with a join_column not available in the
        dataframe.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = [build_dov_url('data/boring/1986-068853'),
                 build_dov_url('data/boring/1986-068843'),
                 build_dov_url('data/boring/1980-068861')]

            df = pd.DataFrame({
                'pkey_boring': pd.Series(l),
                'diepte_tot_m': pd.Series([10, 20, 30])
            })

            Join(df, 'pkey_sondering')

    def test_single(self):
        """Test the Join expression with a dataframe containing a single row.

        Test whether the generated query is correct and does contain only a
        single PropertyIsEqualTo.

        """
        l = [build_dov_url('data/boring/1986-068853')]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10])
        })

        query = Join(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

        propertyname = xml.find('./{http://www.opengis.net/ogc}PropertyName')
        assert propertyname.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/ogc}Literal')
        assert literal.text in l

        l.remove(literal.text)
        assert len(l) == 0

    def test_single_duplicate(self):
        """Test the Join expression with a dataframe containing two
        identical keys.

        Test whether the generated query is correct and does contain only a
        single PropertyIsEqualTo.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068853')]
        l_output = [build_dov_url('data/boring/1986-068853')]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20])
        })

        query = Join(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

        propertyname = xml.find('./{http://www.opengis.net/ogc}PropertyName')
        assert propertyname.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/ogc}Literal')
        assert literal.text in l_output

        l_output.remove(literal.text)
        assert len(l_output) == 0

    def test_empty(self):
        """Test the Join expression with an empty dataframe.

        Test whether a ValueError is raised

        """
        df = pd.DataFrame({
            'pkey_boring': [np.nan, np.nan],
            'diepte_tot_m': pd.Series([10, 20])
        })

        with pytest.raises(ValueError):
            Join(df, 'pkey_boring')

    def test_on(self):
        """Test the Join expression with a standard dataframe and 'on'.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = Join(df, on='pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l.remove(literal.text)

        assert len(l) == 0

    def test_using(self):
        """Test the Join expression with a standard dataframe and 'on' and
        'using'.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        df = pd.DataFrame({
            'boringfiche': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = Join(df, on='pkey_boring', using='boringfiche')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/ogc}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/ogc}PropertyIsEqualTo'

            propertyname = f.find('./{http://www.opengis.net/ogc}PropertyName')
            assert propertyname.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/ogc}Literal')
            assert literal.text in l

            l.remove(literal.text)

        assert len(l) == 0
