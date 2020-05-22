from application import app

def test_index_returns_200():
        request, response = app.test_client.get('/')
        assert response.status == 200

def test_non_existing_page_returns_404():
        request, response = app.test_client.get('/blablabla')
        assert response.status == 404
