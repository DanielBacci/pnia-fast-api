import vcr
from fastapi.testclient import TestClient

from source.routes import app

client = TestClient(app)


class TestLoadFile:

    def test_loan_file(self):
        response = client.post("/load-file")
        assert response.status_code == 200
        assert response.json() == {}


class TestAggregate:

    @vcr.use_cassette('source/tests/vcr_cassettes/four_phones.yaml')
    def test_aggregate_four_phones(self):
        response = client.post(
            "/aggregate",
            data='["+1983248", "001382355", "+1478192", "+4439877"]'
        )
        assert response.status_code == 200
        assert response.json() == {
            '1': {'Clothing': 1, 'Technology': 2},
            '44': {'Banking': 1}
        }

    @vcr.use_cassette('source/tests/vcr_cassettes/none_phones.yaml')
    def test_aggregate_without_valid_phones(self):
        response = client.post(
            "/aggregate",
            data='["19"]'
        )
        assert response.status_code == 200
        assert response.json() == {}
