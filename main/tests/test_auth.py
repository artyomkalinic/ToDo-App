def test_register_and_login(client):
    response = client.post("/user/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201


    response = client.post("/user/register", json={
        "username": "testuser", 
        "password": "testpass123"
    })
    assert response.status_code == 403


    response = client.post("/user/login", data={
        "username": "testuser", 
        "password": "testpass123"
    })
    assert response.status_code == 200


    response = client.post("/user/login", data={
        "username": "testuser1", 
        "password": "testpass123"
    })
    assert response.status_code == 404


    response = client.post("/user/login", data={
        "username": "testuser", 
        "password": "testpass1234"
    })
    assert response.status_code == 401

