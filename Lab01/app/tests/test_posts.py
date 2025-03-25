# Test 1: Verify posts index page loads successfully
def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

# Test 2: Verify posts index uses correct template and context
def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

# Test 3: Verify individual post page displays correct content
def test_post_page(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert posts_list[0]['title'] in response.text
    assert posts_list[0]['text'] in response.text
    assert posts_list[0]['author'] in response.text
    assert posts_list[0]['date'].strftime('%d.%m.%Y') in response.text

# Test 4: Verify post page uses correct template and context
def test_post_page_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts/0')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == posts_list[0]['title']
        assert context['post'] == posts_list[0]

# Test 5: Verify post page contains required comment elements
def test_post_page_elements(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert 'Оставьте комментарий' in response.text
    assert 'Отправить' in response.text

# Test 6: Verify post date displays in correct format
def test_post_page_date_format(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    expected_date = posts_list[0]['date'].strftime('%d.%m.%Y')
    assert expected_date in response.text

# Test 7: Verify post image is properly displayed
def test_post_page_image(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert f"images/{posts_list[0]['image_id']}" in response.text

# Test 8: Verify comments display correctly on post page
def test_post_page_comments(client, mocker, posts_list):
    posts_list[0]['comments'] = [
        {'author': 'Test Author', 'text': 'Test comment', 'replies': []}
    ]
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert 'Test Author' in response.text
    assert 'Test comment' in response.text

# Test 9: Verify comment replies display correctly
def test_post_page_replies(client, mocker, posts_list):
    posts_list[0]['comments'] = [
        {
            'author': 'Parent Author', 
            'text': 'Parent comment',
            'replies': [
                {'author': 'Child Author', 'text': 'Reply comment'}
            ]
        }
    ]
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert 'Parent Author' in response.text
    assert 'Parent comment' in response.text
    assert 'Child Author' in response.text
    assert 'Reply comment' in response.text

# Test 10: Verify 404 error for non-existent posts
def test_non_existent_post(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/999')
    assert response.status_code == 404

# Test 11: Verify footer contains required information
def test_footer_exists(client):
    response = client.get('/')
    assert 'Махмуд Али Айманович' in response.text
    assert '231-352' in response.text

# Test 12: Verify about page loads correctly
def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert 'Об авторе' in response.text

# Test 13: Verify index page loads correctly
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Задание к лабораторной работе' in response.text

# Test 14: Verify navigation links are present
def test_navigation_links(client):
    response = client.get('/')
    assert 'Посты' in response.text
    assert 'Об авторе' in response.text
    assert 'Задание' in response.text

# Test 15: Verify post links exist on index page
def test_post_links_from_index(client):
    response = client.get('/posts')
    assert 'Читать дальше' in response.text