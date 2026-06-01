from app import app
import database as db

with app.test_client() as client:
    # mock session
    with client.session_transaction() as sess:
        sess['cart'] = {'1': 2}
    
    # post to checkout
    response = client.post('/checkout', data={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test2@test.com',
        'phone': '123',
        'street_address': 'St',
        'city': 'City',
        'state': 'State',
        'zip_code': '12345'
    })
    
    print("Status:", response.status_code)
    print("Location:", response.headers.get('Location'))
    if response.status_code != 302:
        print(response.get_data(as_text=True))
