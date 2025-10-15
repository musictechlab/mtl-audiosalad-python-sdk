from datetime import datetime, timedelta
import time
from unittest.mock import MagicMock, patch

import pytest

from audiosalad_sdk.client import AudioSaladClient


@pytest.fixture
def client():
    return AudioSaladClient(
        access_id="mock_access_id", refresh_token="mock_refresh_token"
    )


@pytest.fixture(autouse=True)
def mock_token_refresh(monkeypatch):
    def fake_refresh(self):
        self.access_token = "test_access_token"
        self.refresh_token = "test_refresh_token"
        self.access_token_expires_at = time.time() + 3600
        self.refresh_token_expires_at = time.time() + 86400

    monkeypatch.setattr(AudioSaladClient, "_refresh_access_token", fake_refresh)


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = [
        {
            "id": "rel_001",
            "format": "Single",
            "format_type": "Digital",
            "catalog": "NS001",
            "upc": "987654321098",
            "custom_id": "NSW-MOCKID",
            "state": "active",
            "title": "Celestial Flow",
            "version": None,
            "display_artist": "Luna Rae",
            "label": "Nebula Sounds",
            "labelId": "lbl_001",
            "compilation": False,
            "release_date": "2025-02-01",
            "p_info": "2025 Nebula Sounds",
            "publishing_info": {"year": "2025", "owner": "Nebula Sounds"},
            "c_info": "2025 Nebula Sounds",
            "copyright_info": {"year": "2025", "owner": "Nebula Sounds"},
            "rights_holders": "Nebula Sounds",
            "advisory": "None",
            "metadata_language": "English",
            "audio_language": "Instrumental",
            "categories": ["Electronic", "Downtempo"],
            "participants": [
                {
                    "id": "art_001",
                    "name": "Luna Rae",
                    "role": "Main Artist",
                    "sort_order": 0,
                }
            ],
            "territories": "PL,DE,FR",
            "modified": "2025-01-20T00:00:00Z",
            "tracks": [
                {
                    "id": "trk_001",
                    "discnum": "1",
                    "tracknum": "1",
                    "title": "Orbit Lights",
                    "isrc": "GBNS12500009",
                    "custom_id": "NSW-TRK-001",
                    "length": "260",
                    "display_artist": "Luna Rae",
                    "p_info": "2025 Nebula Sounds",
                    "publishing_info": {"year": "2025", "owner": "Nebula Sounds"},
                    "c_info": "2025 Nebula Sounds",
                    "copyright_info": {"year": "2025", "owner": "Nebula Sounds"},
                    "rights_holders": "Nebula Sounds",
                    "advisory": "None",
                    "audio_language": "Instrumental",
                    "categories": ["Electronic", "Ambient"],
                    "participants": [
                        {
                            "id": "art_001",
                            "name": "Luna Rae",
                            "role": "Main Artist",
                            "sort_order": 0,
                        }
                    ],
                    "permission_stream": "1",
                    "permission_download_nondrm": "1",
                }
            ],
            "tags": ["Calm", "Dreamy"],
        }
    ]
    return mock


@pytest.fixture
def mock_label_response():
    mock = MagicMock()
    mock.json.return_value = [
        {
            "id": "lbl_001",
            "name": "Nebula Sounds",
            "display_name": "Nebula Sounds",
            "distributor": "0",
            "parent_label_id": "0",
            "custom_id": None,
            "created": "2025-01-15T00:00:00Z",
            "modified": "2025-01-15T00:00:00Z",
            "yt_asset_labels": [],
            "dsp_ids": [{"dsp": "apple", "id": "apple_lbl001"}],
        }
    ]
    return mock


@pytest.fixture
def mock_release_ids_response():
    mock = MagicMock()
    mock.json.return_value = ["rel_001", "rel_002", "rel_003"]
    return mock


@pytest.fixture
def mock_delivery_targets_response():
    mock = MagicMock()
    mock.json.return_value = [
        {"id": "target_001", "name": "Spotify"},
        {"id": "target_002", "name": "Apple Music"},
        {"id": "target_003", "name": "Amazon Music"},
        {"id": "target_004", "name": "TIDAL"},
        {"id": "target_005", "name": "YouTube Music"},
    ]
    return mock


class TestAudioSaladClient:
    def test_init(self, client):
        assert client.access_id == "mock_access_id"
        assert client.refresh_token == "mock_refresh_token"
        assert (
            client.base_url
            == "https://<client-namespace>.dashboard.audiosalad.com/client-api"
        )

    @patch("requests.get")
    def test_get_release_by_id(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_release("rel_001")
        assert response[0]["id"] == "rel_001"
        assert response[0]["title"] == "Celestial Flow"
        mock_get.assert_called_once_with(
            f"{client.base_url}/releases/rel_001",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_tracks(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_tracks()
        assert response["status"] == "success"
        mock_get.assert_called_once_with(
            f"{client.base_url}/tracks",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_track_by_id(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_track_by_id("mock_track")
        assert response["status"] == "success"
        assert response["data"]["id"] == "mock_track"
        mock_get.assert_called_once_with(
            f"{client.base_url}/tracks/mock_track",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_all_artists(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_all_artists()
        assert response["status"] == "success"
        mock_get.assert_called_once_with(
            f"{client.base_url}/artists",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_artist_by_id(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_artist_by_id("mock_artist")
        assert response["status"] == "success"
        assert response["data"]["id"] == "mock_artist"
        mock_get.assert_called_once_with(
            f"{client.base_url}/artists/mock_artist",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_all_labels(self, mock_get, client, mock_response):
        mock_get.return_value = mock_response
        response = client.get_all_labels()
        assert response["status"] == "success"
        mock_get.assert_called_once_with(
            f"{client.base_url}/labels",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_label_by_id(self, mock_get, client, mock_label_response):
        mock_get.return_value = mock_label_response
        response = client.get_label_by_id("lbl_001")
        assert response[0]["id"] == "lbl_001"
        assert response[0]["name"] == "Nebula Sounds"
        mock_get.assert_called_once_with(
            f"{client.base_url}/labels/lbl_001",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_sales_report_for_period(self, mock_get, client, mock_response):
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        mock_get.return_value = mock_response
        response = client.get_sales_report_for_period(start_date, end_date)
        assert response["status"] == "success"
        mock_get.assert_called_once_with(
            f"{client.base_url}/reports/sales",
            params={
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            },
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_earnings_report_for_period(self, mock_get, client, mock_response):
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        mock_get.return_value = mock_response
        response = client.get_earnings_report_for_period(start_date, end_date)
        assert response["status"] == "success"
        mock_get.assert_called_once_with(
            f"{client.base_url}/reports/earnings",
            params={
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            },
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_get_release_ids(self, mock_get, client, mock_release_ids_response):
        mock_get.return_value = mock_release_ids_response
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        response = client.get_release_ids(start_date, end_date)
        assert len(response) == 3
        assert "rel_001" in response
        mock_get.assert_called_once_with(
            f"{client.base_url}/release-ids",
            params={
                "modified_start": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "modified_end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.post")
    def test_list_delivery_targets(
        self, mock_post, client, mock_delivery_targets_response
    ):
        mock_post.return_value = mock_delivery_targets_response
        response = client.list_delivery_targets()
        print("--------", response)

        assert len(response) == 5
        assert response[0]["name"] == "Spotify"
        assert response[1]["name"] == "Apple Music"
        mock_post.assert_called_once_with(
            f"{client.base_url}/delivery-targets",
            headers={"Authorization": f"Bearer {client.api_key}"},
        )

    @patch("requests.get")
    def test_error_handling(self, mock_get, client):
        mock_get.side_effect = Exception("Mock API Error")
        with pytest.raises(Exception) as exc_info:
            client.get_releases()
            assert str(exc_info.value) == "Mock API Error"
