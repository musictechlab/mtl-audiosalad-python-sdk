from datetime import datetime, timedelta
from unittest.mock import patch
from unittest.mock import MagicMock
import pytest

from audiosalad_sdk.services.api import AudioSaladAPI


@pytest.fixture
def service():
    return AudioSaladAPI(access_id="mock_access_id", refresh_token="mock_refresh_token")


@pytest.fixture
def mock_request():
    with patch("requests.request") as req:
        resp = MagicMock()
        resp.raise_for_status.return_value = None
        resp.json.return_value = {"status": "success", "data": []}
        req.return_value = resp
        yield req


@pytest.fixture
def mock_client():
    with patch("audiosalad_sdk.client.AudioSaladClient") as mock:
        client = mock.return_value
        client.get_releases.return_value = [
            {
                "id": "rel_XYZ123",
                "format": "EP",
                "format_type": "Digital",
                "catalog": "NSW-042",
                "upc": "842001234567",
                "custom_id": "NSW-CID-042",
                "state": "active",
                "title": "Starlit Echoes",
                "version": None,
                "display_artist": "Ava Nightingale",
                "label": "Nebula Soundworks",
                "labelId": "lbl_9f3a",
                "compilation": False,
                "release_date": "2025-03-22",
                "p_info": "2025 Nebula Soundworks",
                "publishing_info": {"year": "2025", "owner": "Nebula Soundworks"},
                "c_info": "2025 Nebula Soundworks",
                "copyright_info": {"year": "2025", "owner": "Nebula Soundworks"},
                "rights_holders": "Nebula Soundworks",
                "advisory": "None",
                "metadata_language": "English",
                "audio_language": "Instrumental",
                "categories": ["Electronic", "Ambient"],
                "participants": [
                    {
                        "id": "art_ava01",
                        "name": "Ava Nightingale",
                        "role": "Main Artist",
                        "sort_order": 0,
                    }
                ],
                "territories": "PL,DE,FR",
                "modified": "2025-03-10T00:00:00Z",
                "tracks": [
                    {
                        "id": "trk_0001",
                        "discnum": "1",
                        "tracknum": "1",
                        "title": "Nebula Drift",
                        "isrc": "GBNS12500001",
                        "custom_id": "NSW-TRK-0001",
                        "length": "312",
                        "display_artist": "Ava Nightingale",
                        "p_info": "2025 Nebula Soundworks",
                        "publishing_info": {
                            "year": "2025",
                            "owner": "Nebula Soundworks",
                        },
                        "c_info": "2025 Nebula Soundworks",
                        "copyright_info": {
                            "year": "2025",
                            "owner": "Nebula Soundworks",
                        },
                        "rights_holders": "Nebula Soundworks",
                        "advisory": "None",
                        "audio_language": "Instrumental",
                        "categories": ["Electronic", "Ambient"],
                        "participants": [
                            {
                                "id": "art_ava01",
                                "name": "Ava Nightingale",
                                "role": "Main Artist",
                                "sort_order": 0,
                            }
                        ],
                        "permission_stream": "1",
                        "permission_download_nondrm": "1",
                    }
                ],
                "tags": ["Downtempo", "Chill"],
            }
        ]
        client.get_label_by_id.return_value = [
            {
                "id": "lbl_9f3a",
                "name": "Nebula Soundworks",
                "display_name": "Nebula Soundworks",
                "distributor": "0",
                "parent_label_id": "0",
                "custom_id": None,
                "created": "2025-03-01T00:00:00Z",
                "modified": "2025-03-01T00:00:00Z",
                "yt_asset_labels": [],
                "dsp_ids": [
                    {"dsp": "spotify", "id": "sp_9f3a"},
                    {"dsp": "apple", "id": "am_9f3a"},
                ],
            }
        ]
        client.get_release_ids.return_value = [
            "rel_XYZ123",
            "rel_ABC456",
            "rel_QWE789",
        ]
        client.list_delivery_targets.return_value = [
            {"id": "target_001", "name": "Spotify"},
            {"id": "target_002", "name": "Apple Music"},
            {"id": "target_003", "name": "Amazon Music"},
            {"id": "target_004", "name": "TIDAL"},
            {"id": "target_005", "name": "YouTube Music"},
        ]
        yield client


@pytest.fixture
def mock_log_system_event():
    with patch("audiosalad_sdk.utils.log_system_event") as mock:
        yield mock


class TestAudiosaladService:
    def test_init(self, service):
        assert service.client is not None

    def test_get_all_releases(self, service, mock_client):
        releases = service.get_all_releases()
        assert len(releases) == 1
        assert releases[0]["id"] == "rel_XYZ123"
        assert releases[0]["title"] == "Starlit Echoes"
        assert releases[0]["upc"] == "842001234567"
        mock_client.get_all_releases.assert_called_once()

    def test_get_release_by_id(self, service, mock_client):
        release = service.get_release_by_id("rel_XYZ123")
        assert release[0]["id"] == "rel_XYZ123"
        assert release[0]["title"] == "Starlit Echoes"
        mock_client.get_release.assert_called_once_with("rel_XYZ123")

    def test_get_label_by_id(self, service, mock_client):
        label = service.get_label_by_id("lbl_9f3a")
        assert label[0]["id"] == "lbl_9f3a"
        assert label[0]["name"] == "Nebula Soundworks"
        mock_client.get_label_by_id.assert_called_once_with("lbl_9f3a")

    def test_get_release_ids(self, service, mock_client):
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        release_ids = service.get_release_ids(start_date, end_date)
        assert len(release_ids) == 3
        assert "rel_XYZ123" in release_ids
        mock_client.get_release_ids.assert_called_once_with(start_date, end_date)

    def test_list_delivery_targets(self, service, mock_client):
        targets = service.list_delivery_targets()
        assert len(targets) == 5
        assert targets[0]["name"] == "Spotify"
        assert targets[1]["name"] == "Apple Music"
        mock_client.list_delivery_targets.assert_called_once()

    def test_error_handling(self, service, mock_client, mock_log_system_event):
        mock_client.get_all_releases.side_effect = Exception("API Error")
        with pytest.raises(Exception) as exc_info:
            service.get_all_releases()
            assert str(exc_info.value) == "API Error"
            mock_log_system_event.assert_called_once()
