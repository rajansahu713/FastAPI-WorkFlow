# import pytest
# from httpx import AsyncClient
# from main import app

# @pytest.mark.asyncio
# async def test_create_blog():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/blogs/", json={"title": "My First Blog", "content": "This is a test blog."})
#     assert response.status_code == 200
#     assert response.json()["title"] == "My First Blog"

# @pytest.mark.asyncio
# async def test_get_blog():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/blogs/", json={"title": "Second Blog", "content": "Another blog content."})
#         blog_id = response.json()["id"]

#         response = await client.get(f"/blogs/{blog_id}")
#     assert response.status_code == 200
#     assert response.json()["title"] == "Second Blog"

# @pytest.mark.asyncio
# async def test_update_blog():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/blogs/", json={"title": "Update Blog", "content": "Old content"})
#         blog_id = response.json()["id"]

#         response = await client.put(f"/blogs/{blog_id}", json={"title": "Updated Blog", "content": "New content"})
#     assert response.status_code == 200
#     assert response.json()["title"] == "Updated Blog"

# @pytest.mark.asyncio
# async def test_delete_blog():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/blogs/", json={"title": "To Delete", "content": "Content to be deleted"})
#         blog_id = response.json()["id"]

#         response = await client.delete(f"/blogs/{blog_id}")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Blog deleted successfully"
