from unittest.mock import Mock, patch

from source.models import PhoneBusiness, PhoneBusinessModel, PrefixTrie


class TestPrefixTrie:

    def test_build_should_return_a_valid_trie(self):
        prefix = PrefixTrie()
        trie = prefix.build()
        assert trie['1']['end']
        assert trie['2']['end']
        assert trie['3']['0']['0']['0']['0']['0']['0']['end']
        assert not trie['3']['0']['0']['0']['0'].get('ent')

    def test_search_prefix_match_prefix(self):
        prefix = PrefixTrie()
        trie = prefix.build()
        assert prefix.search_prefix(trie, '1')

    def test_search_prefix_unmatch_prefix(self):
        prefix = PrefixTrie()
        trie = prefix.build()
        assert not prefix.search_prefix(trie, '9')


class TestPhoneBusiness:

    def test_phones_from_body_should_retrieve_a_list_without_parameter_name(
        self
    ):
        phone = PhoneBusiness()
        phones = phone.phones_from_body(
            b'["+1983248", "001382355", "+1478192", "+4439877"]'
        )
        assert isinstance(phones, list)

    def test_retrieve_business_should_return_empty_when_there_are_no_phones(
        self
    ):
        phone = PhoneBusiness()
        assert not phone.retrieve_business([])

    @patch('source.models.requests.get')
    def test_retrieve_business_should_return_a_business_phone(
        self,
        mock_get
    ):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = {
            "number": "+4439877",
            "sector": "Banking"
        }
        phone = PhoneBusiness()
        assert len(phone.retrieve_business(['123456'])) == 1

    def test_neat_number_should_return_number_without_00(self):
        phone = PhoneBusiness()
        assert phone.neat_number('00123') == '123'

    def test_neat_number_should_return_only_number(self):
        phone = PhoneBusiness()
        assert phone.neat_number('+1 1123') == '11123'

    @patch('source.models.PhoneBusiness.retrieve_business')
    def test_build_return_match_values(self, retrieve_business_mock):
        retrieve_business_mock.return_value = [
            PhoneBusinessModel(
                number='+1983248',
                number_neat='1983248',
                type='Technology',
                reason=''
            ),
            PhoneBusinessModel(
                number='001382355',
                number_neat='1382355',
                type='Technology',
                reason=''
            ),
            PhoneBusinessModel(
                number='+1478192',
                number_neat='1478192',
                type='Clothing',
                reason=''
            ),
            PhoneBusinessModel(
                number='+4439877',
                number_neat='4439877',
                type='Banking',
                reason=''
            )
        ]
        phone = PhoneBusiness()
        values = phone.build(["+1983248", "001382355", "+1478192", "+4439877"])
        assert values['1']['Technology'] == 2
        assert values['1']['Clothing'] == 1
        assert values['44']['Banking'] == 1
