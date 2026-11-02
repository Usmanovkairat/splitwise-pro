from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.static_frontend import DIST, mount_frontend


def test_image_asset_location():
    assert DIST == Path(__file__).resolve().parents[2] / 'frontend' / 'dist'


def test_static_spa_api_and_missing_assets(tmp_path):
    (tmp_path / 'assets').mkdir()
    (tmp_path / 'assets' / 'app.js').write_text('console.log("app")')
    (tmp_path / 'index.html').write_text('<main>SplitWise</main>')
    app = create_app(storage='memory')
    mount_frontend(app, tmp_path)
    with TestClient(app) as client:
        assert client.get('/').text == '<main>SplitWise</main>'
        assert client.get('/groups/deep-link').text == '<main>SplitWise</main>'
        assert client.get('/assets/app.js').status_code == 200
        assert client.get('/assets/missing.js').status_code == 404
        assert client.get('/api/health').json()['status'] == 'ok'
        assert client.get('/api/missing').status_code == 404
        assert client.get('/api').status_code == 404
        assert client.get('/assets/..%2F..%2Fsecret').status_code == 404


def test_missing_build_fails_before_serving(tmp_path):
    with pytest.raises(RuntimeError, match='Frontend build missing'):
        mount_frontend(create_app(storage='memory'), tmp_path)


def test_readiness_refuses_unmigrated_database(tmp_path):
    from backend.app.database import make_engine
    from backend.app.sql_repository import SQLAlchemyRepository
    engine = make_engine(f'sqlite:///{tmp_path / "unmigrated.db"}')
    try:
        with TestClient(create_app(SQLAlchemyRepository(engine))) as client:
            response = client.get('/api/health')
            assert response.status_code == 503
            assert response.json() == {'status': 'unavailable'}
    finally:
        engine.dispose()
