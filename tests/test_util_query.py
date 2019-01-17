"""Module grouping tests for the pydov.util.query module."""
import pandas as pd
import pytest

from pydov.util.query import (
    PropertyInList,
    Join,
)


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

    def test_tooshort(self):
        """Test the PropertyInList expression with a list containing
        a single item.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = ['a']
            PropertyInList('methode', l)

    def test_tooshort_duplicate(self):
        """Test the PropertyInList expression with a list containing
        a two identical items.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = ['a', 'a']
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
        l = ['https://www.dov.vlaanderen.be/data/boring/1986-068853',
             'https://www.dov.vlaanderen.be/data/boring/1986-068843',
             'https://www.dov.vlaanderen.be/data/boring/1980-068861']

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
        l = ['https://www.dov.vlaanderen.be/data/boring/1986-068853',
             'https://www.dov.vlaanderen.be/data/boring/1986-068853',
             'https://www.dov.vlaanderen.be/data/boring/1980-068861']

        l_output = ['https://www.dov.vlaanderen.be/data/boring/1986-068853',
                    'https://www.dov.vlaanderen.be/data/boring/1980-068861']

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
            l = ['https://www.dov.vlaanderen.be/data/boring/1986-068853',
                 'https://www.dov.vlaanderen.be/data/boring/1986-068843',
                 'https://www.dov.vlaanderen.be/data/boring/1980-068861']

            df = pd.DataFrame({
                'pkey_boring': pd.Series(l),
                'diepte_tot_m': pd.Series([10, 20, 30])
            })

            Join(df, 'pkey_sondering')

    def test_tooshort(self):
        """Test the Join expression with a dataframe containing a single row.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = ['https://www.dov.vlaanderen.be/data/boring/1986-068853']

            df = pd.DataFrame({
                'pkey_boring': pd.Series(l),
                'diepte_tot_m': pd.Series([10])
            })

            Join(df, 'pkey_boring')

    def test_tooshort_duplicate(self):
        """Test the Join expression with a dataframe containing two
        identical keys.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = ['https://www.dov.vlaanderen.be/data/boring/1986-068853',
                 'https://www.dov.vlaanderen.be/data/boring/1986-068853']

            df = pd.DataFrame({
                'pkey_boring': pd.Series(l),
                'diepte_tot_m': pd.Series([10, 20])
            })

            Join(df, 'pkey_boring')
