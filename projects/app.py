from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# JSON file for data storage
DATABASE = 'database.json'

# Load existing users from the JSON file
def load_users():
    try:
        with open(DATABASE, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    return users

# Save users to the JSON file
def save_users(users):
    with open(DATABASE, 'w') as file:
        json.dump(users, file)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the login credentials
        users = load_users()
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        if user:
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        pin = request.form['pin']

        # Load existing users and append the new user
        users = load_users()
        users.append({'username': username, 'password': password, 'phone': phone, 'pin': pin})

        # Save the updated user list
        save_users(users)

        return redirect('/')

    return render_template('register.html')

@app.route('/payment', methods=['POST'])
def payment():
    if request.method == 'POST':
        entered_pin = request.form['inputPin']
        contact_pin = request.form['contact_pin']
    with open('database.json') as f:
        data = json.load(f)
        username = session['username']
        print(username)
        for i in range (0,len(data)):
            if data[i]["username"]==username:
                user_pin = data[i]['pin']
        if entered_pin == user_pin:
            return render_template('payment_success.html')
        else:
            return render_template('payment_failed.html')


@app.route('/pay_to_contacts', methods=['GET', 'POST'])
def pay_to_contacts():
    if 'username' not in session:
        return redirect('/')
    contacts = []
    for i in range(1, 21):
        contacts.append({'name': f'Contact {i}','pin':f'{i:04}'})

    if request.method == 'POST':
        entered_pin = request.form['inputPin']
        contact_name = request.form['contact_name']
        contact_pin = request.form['contact_pin']

    return render_template('pay_to_contacts.html', contacts=contacts)



@app.route('/recharge', methods=['GET', 'POST'])
def recharge():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        phone_number = request.form['phone_number']
        amount = request.form['amount']

        # Perform the recharge process (you can customize this based on your requirements)
        # Here, we simply display a confirmation message with the phone number and amount
        recharge_data = {
            'phone_number': phone_number,
            'amount': amount
        }

        return render_template('recharge_success.html', recharge_data=recharge_data)

    return render_template('recharge.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

