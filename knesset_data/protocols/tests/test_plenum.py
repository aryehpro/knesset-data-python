# -*- coding: utf-8 -*-
import unittest
from knesset_data.protocols.plenum import PlenumProtocolFile
from datetime import datetime
import os

import six

if six.PY2:
    def myopen(a, b, **c):
        return open(a, b)
elif six.PY3:
    def myopen(a, b, **c):
        return open(a, b, **c)
else:
    raise RuntimeError('not supported version of py in six module')


# this function is used by test_base to test the base protocol functionality
def plenum_protocol_assertions(test_case, protocol):
    test_case.assertEqual(protocol.knesset_num_heb, 'עשרים')
    test_case.assertEqual(protocol.meeting_num_heb, 'שמונים')
    test_case.assertEqual(protocol.booklet_num_heb, 'י"א')
    test_case.assertEqual(protocol.booklet_meeting_num_heb, "פ'")
    test_case.assertEqual(protocol.date_string_heb, ('23', 'דצמבר', '2015'))
    test_case.assertEqual(protocol.time_string, ('11', '00'))
    test_case.assertEqual(protocol.datetime, datetime(2015, 12, 23, 11, 0))
    test_case.assertEqual(protocol.knesset_num, 20)
    test_case.assertEqual(protocol.booklet_num, 11)
    test_case.assertEqual(protocol.booklet_meeting_num, 80)


class TestPlenumProtocolFile(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.protocol_generator = {}

        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptm_318579.doc')
        self.protocol_generator['20-318579'] = PlenumProtocolFile.get_from_filename(source_doc_file_name)

        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptm_381742.doc')
        self.protocol_generator['20-381742'] = PlenumProtocolFile.get_from_filename(source_doc_file_name)

    @unittest.skip("@aryehpro: refactoring tests")
    def test_from_file(self):
        with PlenumProtocolFile.get_from_filename(
                os.path.join(os.path.dirname(__file__), '20_ptm_318579.doc')) as protocol:
            plenum_protocol_assertions(self, protocol)

    # region Test protocol header parsing

    def test_knesset_num_heb(self):
        expected_data = 'עשרים'

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.knesset_num_heb, expected_data, 'Hebrew Knesset number not parsed correctly')

    def test_knesset_num(self):
        expected_data = 20

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.knesset_num, expected_data, 'Knesset number not parsed correctly')

    def test_meeting_num_heb(self):
        expected_data = 'מאתיים-ותשע-עשרה'

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.meeting_num_heb, expected_data, 'Hebrew meeting number not parsed correctly')

    def test_booklet_num_heb(self):
        expected_data = 'כ"א'

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.booklet_num_heb, expected_data, 'Hebrew booklet number not parsed correctly')

    def test_booklet_num(self):
        expected_data = 21

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.booklet_num, expected_data, 'Booklet number not parsed correctly')

    def test_booklet_meeting_num_heb(self):
        expected_data = 'רי"ט'

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.booklet_meeting_num_heb, expected_data, 'Hebrew booklet meeting number not '
                                                                              'parsed correctly')

    def test_booklet_meeting_num(self):
        expected_data = 219

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.booklet_meeting_num, expected_data, 'Booklet meeting number not parsed correctly')

    def test_date_string_heb(self):
        expected_data = ('21', 'מרס', '2017')

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.date_string_heb, expected_data, 'Hebrew date string not parsed correctly')

    def test_time_string(self):
        expected_data = ('16', '00')

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.time_string, expected_data, 'Time string not parsed correctly')

    def test_datetime(self):
        expected_data = datetime(2017, 3, 21, 16, 0)

        with self.protocol_generator['20-381742'] as protocol:
            self.assertEqual(protocol.datetime, expected_data, 'Datetime timestamp not parsed correctly')

    # endregion

    def _get_protocol_data(self, protocol, keys):
        res = {}
        for k in keys:
            try:
                res[k] = getattr(protocol, k)
            except Exception as e:
                res[k] = str(e)
        return res

    @unittest.skip("@aryehpro: refactoring tests")
    def test_from_data(self):
        data = myopen(os.path.join(os.path.dirname(__file__), '20_ptm_381742.doc'), 'rb').read()
        with PlenumProtocolFile.get_from_data(data) as protocol:

            if six.PY2:
                expected_exception =  "'NoneType' object has no attribute 'decode'"
            if six.PY3:
                expected_exception =  "'NoneType' object is not iterable"

            expected_data = {'knesset_num_heb': 'עשרים',
                             'meeting_num_heb': 'מאתיים-ותשע-עשרה',
                             "booklet_num_heb": None,
                             'booklet_meeting_num_heb': 'רי"ט',
                             'date_string_heb': ('21', 'מרס', '2017'),
                             'time_string': ('16', '00'),
                             'datetime': datetime(2017, 3, 21, 16, 0),
                             "knesset_num": 20,
                             'booklet_num': expected_exception,
                             "booklet_meeting_num": 219}
            actual_data = self._get_protocol_data(protocol, expected_data)
            self.assertEqual(actual_data, expected_data)
