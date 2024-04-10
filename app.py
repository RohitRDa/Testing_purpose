from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import time
import os  # Import the 'os' module to check file existence

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key

# Define the path to your CSV file
csv_file_path = 'data.csv'
from datetime import datetime



# Initialize an empty list to hold data read from the CSV file
data = []

# Check if the CSV file exists, and create it if it doesn't
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['user_id', 'username', 'email', 'phone']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

# Load initial data from the CSV file into the 'data' list
with open(csv_file_path, 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

@app.route('/')
def index():
  return render_template('index.html')

# @app.route('/page1')
# def page1():
  
  
#   return render_template('page1.html')


from datetime import datetime  # Import the datetime module

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    success_message = None
    # Define a dictionary to map option values to country names
    country_names = {
        "option1": "USA",
        "option2": "India",
        "option3": "Canada",
    }


    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        country = request.form['country']  # Get the country value from the form

        # Check if the 'subscribe_to_newsletter' checkbox is checked
        subscribe_to_newsletter = "Yes" if 'subscribe_to_newsletter' in request.form else "No"

        # Check if the 'interest' checkbox is checked
        agree_to_terms = "Yes" if 'interest' in request.form else "No"

        # Get the date and time and format it
        # datetime_str = request.form['datetime']
        # formatted_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M").strftime("%d-%b-%Y %I:%M %p")
        input_date = request.form['datetime']
            # Format the date as "YYYY-MM-DD"
        formatted_date = datetime.strptime(input_date, "%d-%b-%Y").strftime("%Y-%m-%d")


        # Create a new data entry as a dictionary
        new_entry = {
            'user_id': str(time.time()),
            'username': username,
            'email': email,
            'phone': phone,
            'country': country,  # Add the 'country' field
            'subscribe_to_newsletter': subscribe_to_newsletter,
            'agree_to_terms': agree_to_terms,
            'datetime': formatted_date
        }

        # Append the new entry to the 'data' list
        data.append(new_entry)

        # Save the updated data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['user_id', 'username', 'email', 'phone', 'country', 'subscribe_to_newsletter', 'agree_to_terms', 'datetime', 'formatted_datetime']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

        success_message = "Data inserted successfully!"  # Set the success message

    return render_template('page1.html', success_message=success_message)



@app.route('/page2')
def page2():
        # Define a dictionary to map option values to country names
    country_names = {
        "option1": "USA",
        "option2": "India",
        "option3": "Canada",
    }

    return render_template('page2.html', data=data, country_names=country_names)


@app.route('/page3', methods=['GET', 'POST'])
def page3():
    user_options = [{'user_id': entry['user_id'], 'username': entry['username']} for entry in data]
    selected_username = request.form.get('selected_user_id') or ''  # Set it to an empty string if it's None
    return render_template('page3.html', selected_user_id=selected_username, selected_entry=user_options, user_options=user_options)



@app.route('/autocomplete_usernames', methods=['GET'])
def autocomplete_usernames():
    term = request.args.get('term', '').lower()
    suggestions = [entry['username'] for entry in data if term in entry['username'].lower()]
    return jsonify(suggestions)




from datetime import datetime

@app.route('/select_entry', methods=['GET', 'POST'])
def select_entry():
    selected_username = request.form['selected_user_id']
    selected_entry = None

    # Find the selected entry using the user_id
    for entry in data:
        if entry['username'] == selected_username:
            selected_entry = entry
            # Format the datetime value here for the UI
            selected_entry['formatted_datetime'] = datetime.strptime(selected_entry['datetime'], "%Y-%m-%d").strftime("%d-%b-%Y")

            # Set the values for the checkboxes
            selected_entry['subscribe_to_newsletter'] = 'Yes' if selected_entry.get('subscribe_to_newsletter', '') == 'Yes' else 'No'
            selected_entry['agree_to_terms'] = 'Yes' if selected_entry.get('agree_to_terms', '') == 'Yes' else 'No'

            break

    # Create a list of usernames and user_ids for the select options
    select_options = [{'user_id': entry['user_id'], 'username': entry['username']} for entry in data]

    # Render the 'page3.html' template with selected data and select options
    return render_template('page3.html', user_options=select_options, selected_user_id=selected_username, selected_entry=selected_entry)

from datetime import datetime


@app.route('/save_entry', methods=['POST'])
def save_entry():
    # Get data from the form
    USER_ID = request.form['selected_user_id']
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    subscribe_to_newsletter = 'Yes' if 'subscribe_to_newsletter' in request.form else 'No'
    country = request.form['country']
    selected_username = request.form.get('selected_user_id', '')  # Set it to an empty string if it's None

    # Correct the format string for datetime parsing
    datetime_str_ui = request.form['datetime']  # Date in "01-Oct-2023" format from the UI
    datetime_obj = datetime.strptime(datetime_str_ui, "%d-%b-%Y")
    formatted_datetime_db = datetime_obj.strftime("%Y-%m-%d")  # Format for database storage

    agree_to_terms = 'Yes' if 'agree_to_terms' in request.form else 'No'  # Check if the checkbox is checked
    selected_user_id = request.form['selected_user_id']

    # Initialize selected_entry
    selected_entry = None

    # Find the selected entry using the user_id
    for entry in data:
        if str(entry['user_id']) == selected_user_id:
            selected_entry = entry
            entry['username'] = username
            entry['email'] = email
            entry['phone'] = phone
            entry['subscribe_to_newsletter'] = subscribe_to_newsletter
            entry['country'] = country
            entry['datetime'] = formatted_datetime_db  # Store the formatted datetime in the database format
            entry['formatted_datetime'] = datetime_str_ui  # Update the formatted_datetime field for UI
            entry['agree_to_terms'] = agree_to_terms
            break

        # Save the updated data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['user_id', 'username', 'email', 'phone', 'subscribe_to_newsletter', 'country', 'datetime', 'formatted_datetime', 'agree_to_terms']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

    print(selected_user_id)
    flash('Data updated successfully')

    # Redirect back to the initial page (page3) with the update message
    return redirect(url_for('page3'))





@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    USER_ID = request.form['selected_user_id']

    # Find and remove the selected entry using the user_id
    entry_to_delete = None
    for entry in data:
        if entry['user_id'] == USER_ID:
            entry_to_delete = entry
            break

    if entry_to_delete:
        data.remove(entry_to_delete)

        # Save the updated data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['user_id', 'username', 'email', 'phone', 'subscribe_to_newsletter', 'country', 'datetime', 'formatted_datetime', 'agree_to_terms']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

        flash('Entry deleted successfully')
    else:
        flash('Entry not found')

    # Redirect back to the initial page (page3) with the appropriate message
    return redirect(url_for('page3'))


@app.route('/page4')
def page4():
        
    country_names = {
        "option1": "USA",
        "option2": "India",
        "option3": "Canada",
    }
    return render_template('page4.html', data=data,country_names=country_names)

from datetime import datetime

@app.route('/edit_entry/<string:user_id>', methods=['GET', 'POST'])
def edit_entry(user_id):
    entry_to_edit = None

    for entry in data:
        if entry['user_id'] == user_id:
            entry_to_edit = entry
            break

    if entry_to_edit is None:
        return "Entry not found"  # Handle this case as needed

    if request.method == 'POST':
        # Update the entry with the new data
        entry_to_edit['username'] = request.form['username']
        entry_to_edit['email'] = request.form['email']
        entry_to_edit['phone'] = request.form['phone']
        entry_to_edit['country'] = request.form['country']

        # Format the date for database storage (YYYY-MM-DD format)
        datetime_str_ui = request.form['datetime']  # Date in "01-Oct-2023" format from the UI
        datetime_obj = datetime.strptime(datetime_str_ui, "%d-%b-%Y")
        formatted_datetime_db = datetime_obj.strftime("%Y-%m-%d")

        entry_to_edit['datetime'] = formatted_datetime_db  # Store the formatted datetime in the database format

        entry_to_edit['subscribe_to_newsletter'] = 'Yes' if 'subscribe_to_newsletter' in request.form else 'No'
        entry_to_edit['agree_to_terms'] = 'Yes' if 'agree_to_terms' in request.form else 'No'

        # Save the updated data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['user_id', 'username', 'email', 'phone', 'subscribe_to_newsletter', 'country', 'datetime', 'formatted_datetime', 'agree_to_terms']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)

        flash('Data updated successfully')
        return redirect(url_for('page2'))

    return render_template('edit_entry.html', entry=entry_to_edit)


from flask import jsonify


# In your Flask app:
from flask import jsonify

# @app.route('/autocomplete_usernames')
# def autocomplete_usernames():
#     term = request.args.get('term', '')

#     # Filter usernames based on the user's input
#     suggestions = [entry['username'] for entry in data if term.lower() in entry['username'].lower()]

#     return jsonify(suggestions)


from datetime import datetime

if __name__ == '__main__':
   app.run(debug=True,port='5009')
