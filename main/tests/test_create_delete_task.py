def test_create_and_delete_task(client):
    client.post("/user/register", json={"username": "taskuser", "password": "taskpass"})
    response = client.post("/user/login", data={"username": "taskuser", "password": "taskpass"})
    assert response.status_code == 200


    cookies = response.cookies
    response = client.post("/task/create", json={"name": "Test Task", "description": "desc"}, cookies=cookies)
    assert response.status_code == 200


    task_id = response.json()["id"]
    response = client.request(method="DELETE", url="/task/delete", json={"id": task_id}, cookies=cookies)
    assert response.status_code == 200


    response = client.request(method="DELETE", url="/task/delete", json={"id": 10}, cookies=cookies)
    assert response.status_code == 404

   


    