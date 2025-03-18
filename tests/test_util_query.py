"""Module grouping tests for the pydov.util.query module."""
from itertools import permutations

import numpy as np
import pandas as pd
import pytest
from owslib.etree import etree

from pydov.util.dovutil import build_dov_url
from pydov.util.query import FuzzyJoin, Join, PropertyInList, PropertyLikeList
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'methode'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
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
                '<fes:Or><fes:PropertyIsEqualTo><fes:ValueReference>methode</fes'
                ':ValueReference><ogc:Literal>a</fes:Literal></fes'
                ':PropertyIsEqualTo><fes:PropertyIsEqualTo><fes:ValueReference'
                '>methode</fes:ValueReference><ogc:Literal>b</fes:Literal></fes'
                ':PropertyIsEqualTo><fes:PropertyIsEqualTo><fes:ValueReference'
                '>methode</fes:ValueReference><fes:Literal>c</fes:Literal></fes'
                ':PropertyIsEqualTo></fes:Or>')

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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'methode'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
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


class TestPropertyLikeList(object):
    """Test the PropertyLikeList query expression."""

    def test(self):
        """Test the PropertyLikeList expression with a standard list and modifier.

        Test whether the generated query is correct.

        """
        l = ['a', 'b', 'c']
        l_modified = ['%a%', '%b%', '%c%']

        query = PropertyLikeList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'methode'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0

    def test_modifier(self):
        """Test the PropertyLikeList expression with a standard list and custom modifier.

        Test whether the generated query is correct.

        """
        l = ['a', 'b', 'c']
        l_modified = ['%|a|%', '%|b|%', '%|c|%']

        query = PropertyLikeList('methode', l, modifier='%|{item}|%')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'methode'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0

    def test_stable(self):
        """Test the PropertyLikeList expression with a standard list and modifier.

        Test whether the generated query is correct and stable.

        """
        l = ['a', 'b', 'c']

        for p in permutations(l):
            query = PropertyLikeList('methode', list(p))
            xml = query.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">'
                '<fes:ValueReference>methode</fes:ValueReference><ogc:Literal>%a%</fes:Literal>'
                '</fes:PropertyIsLike><fes:PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">'
                '<fes:ValueReference>methode</fes:ValueReference><ogc:Literal>%b%</fes:Literal>'
                '</fes:PropertyIsLike><fes:PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">'
                '<fes:ValueReference>methode</fes:ValueReference><fes:Literal>%c%</fes:Literal>'
                '</fes:PropertyIsLike></fes:Or>')

    def test_duplicate(self):
        """Test the PropertyLikeList expression with a list containing
        duplicates.

        Test whether the generated query is correct and does not contain the
        duplicate entry twice.

        """
        l = ['a', 'a', 'b', 'c']
        l_modified = ['%a%', '%b%', '%c%']

        query = PropertyLikeList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'methode'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0

    def test_list_single(self):
        """Test the PropertyLikeList expression with a list containing
        a single item.

        Test whether the generated query is correct and does contain only a
        single PropertyIsLike.

        """
        l = ['a']
        l_modified = ['%a%']

        query = PropertyLikeList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
        assert literal.text in l_modified

        l_modified.remove(literal.text)
        assert len(l_modified) == 0

    def test_list_single_duplicate(self):
        """Test the PropertyLikeList expression with a list containing
        a single duplicated item.

        Test whether the generated query is correct and does contain only a
        single PropertyIsLike.

        """
        l = ['a', 'a']
        l_modified = ['%a%']

        query = PropertyLikeList('methode', l)
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'methode'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
        assert literal.text in l_modified

        l_modified.remove(literal.text)
        assert len(l_modified) == 0

    def test_emptylist(self):
        """Test the PropertyLikeList expression with an empty list.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = []
            PropertyLikeList('methode', l)

    def test_nolist(self):
        """Test the PropertyLikeList expression with a string instead of a list.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            l = 'goed'
            PropertyLikeList('betrouwbaarheid', l)


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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
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

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsEqualTo'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l

            l.remove(literal.text)

        assert len(l) == 0


class TestFuzzyJoin(object):
    """Test the FuzzyJoin query expression."""

    def test(self):
        """Test the FuzzyJoin expression with a standard dataframe and modifier.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        l_modified = [f"%|{build_dov_url('data/boring/1986-068853')}|%",
                      f"%|{build_dov_url('data/boring/1986-068843')}|%",
                      f"%|{build_dov_url('data/boring/1980-068861')}|%"]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = FuzzyJoin(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0

    def test_duplicate(self):
        """Test the FuzzyJoin expression with a column containing
        duplicates.

        Test whether the generated query is correct and does not contain the
        duplicate entry twice.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1980-068861')]

        l_output = [f"%|{build_dov_url('data/boring/1986-068853')}|%",
                    f"%|{build_dov_url('data/boring/1980-068861')}|%"]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = FuzzyJoin(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_output

            l_output.remove(literal.text)

        assert len(l_output) == 0

    def test_wrongcolumn(self):
        """Test the FuzzyJoin expression with a join_column not available in the
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

            FuzzyJoin(df, 'pkey_sondering')

    def test_single(self):
        """Test the FuzzyJoin expression with a dataframe containing a single row.

        Test whether the generated query is correct and does contain only a
        single PropertyIsLike.

        """
        l = [build_dov_url('data/boring/1986-068853')]
        l_output = [f"%|{build_dov_url('data/boring/1986-068853')}|%"]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10])
        })

        query = FuzzyJoin(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
        assert literal.text in l_output

        l_output.remove(literal.text)
        assert len(l_output) == 0

    def test_single_duplicate(self):
        """Test the FuzzyJoin expression with a dataframe containing two
        identical keys.

        Test whether the generated query is correct and does contain only a
        single PropertyIsLike.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068853')]

        l_output = [f"%|{build_dov_url('data/boring/1986-068853')}|%"]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20])
        })

        query = FuzzyJoin(df, 'pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

        valuereference = xml.find(
            './{http://www.opengis.net/fes/2.0}ValueReference')
        assert valuereference.text == 'pkey_boring'

        literal = xml.find('./{http://www.opengis.net/fes/2.0}Literal')
        assert literal.text in l_output

        l_output.remove(literal.text)
        assert len(l_output) == 0

    def test_empty(self):
        """Test the FuzzyJoin expression with an empty dataframe.

        Test whether a ValueError is raised

        """
        df = pd.DataFrame({
            'pkey_boring': [np.nan, np.nan],
            'diepte_tot_m': pd.Series([10, 20])
        })

        with pytest.raises(ValueError):
            FuzzyJoin(df, 'pkey_boring')

    def test_on(self):
        """Test the FuzzyJoin expression with a standard dataframe and 'on'.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        l_modified = [f"%|{build_dov_url('data/boring/1986-068853')}|%",
                      f"%|{build_dov_url('data/boring/1986-068843')}|%",
                      f"%|{build_dov_url('data/boring/1980-068861')}|%"]

        df = pd.DataFrame({
            'pkey_boring': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = FuzzyJoin(df, on='pkey_boring')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0

    def test_using(self):
        """Test the Join expression with a standard dataframe and 'on' and
        'using'.

        Test whether the generated query is correct.

        """
        l = [build_dov_url('data/boring/1986-068853'),
             build_dov_url('data/boring/1986-068843'),
             build_dov_url('data/boring/1980-068861')]

        l_modified = [f"%|{build_dov_url('data/boring/1986-068853')}|%",
                      f"%|{build_dov_url('data/boring/1986-068843')}|%",
                      f"%|{build_dov_url('data/boring/1980-068861')}|%"]

        df = pd.DataFrame({
            'boringfiche': pd.Series(l),
            'diepte_tot_m': pd.Series([10, 20, 30])
        })

        query = FuzzyJoin(df, on='pkey_boring', using='boringfiche')
        xml = query.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 3

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}PropertyIsLike'

            valuereference = f.find(
                './{http://www.opengis.net/fes/2.0}ValueReference')
            assert valuereference.text == 'pkey_boring'

            literal = f.find('./{http://www.opengis.net/fes/2.0}Literal')
            assert literal.text in l_modified

            l_modified.remove(literal.text)

        assert len(l_modified) == 0
