from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    request,
    jsonify,
    json,
    session,
)
import secrets

secret_key = secrets.token_hex(16)
print(secret_key)

app = Flask(__name__)

app.secret_key = "your_secret_key_here"

d = 0  # represents amount of money deposited
w = 0  # represnts money withdrawn
cb = 0  # represents current balance

transactions = []


@app.route("/")
def index():
    cb = session.get("current_balance")
    return render_template("index.html", currentBalance=cb)


@app.route("/templates/signup.html", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/", methods=["POST"])
def process_signup():
    global name
    global pin
    global cb

    name = request.form["username"]
    pin = request.form["pin"]

    if len(pin) == 6:
        pin = pin
        cb = 0  # Set initial current balance
        session["current_balance"] = cb  # Store current balance in the session
        session[
            "transactions"
        ] = []  # Initialize an empty transaction list for the user
        print(f"Thank you {name}, your account has been successfully created.")
        return render_template("login.html")
    else:
        return "The pin has to be 6-digits, please go back and try again."


@app.route("/templates/login.html", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    name1 = request.form["username"]
    pin1 = request.form["pin"]

    if "name" not in globals():
        # Redirect the user to the signup page if the name is not defined
        return redirect(url_for("signup"))

    if name1 != name or pin1 != pin:
        return "Your username or pin does not match, please try again."
    elif len(pin1) != 6:
        return "Please enter a 6-character pin."
    else:
        username = name1
        session["username"] = username
        cb = session.get("current_balance")  # Retrieve current balance from the session
        return render_template("index.html", currentBalance=cb)


@app.route("/logout")
def logout():
    # Remove the username from the session
    session.pop("username", None)

    # Redirect the user to the home page or any other desired page
    return redirect("/")


@app.route("/templates/deposit.html", methods=["GET"])
def deposit():
    cb = session.get("current_balance")
    return render_template("deposit.html", curreentBalance=cb)


@app.route("/deposit", methods=["POST", "GET"])
def process_deposit():
    amount = float(request.form.get("amount"))  # Retrieve the amount from the form data

    try:
        # Perform the deposit logic here
        # ...
        cb = get_cb()
        d = amount
        cb += d
        save_cb(cb)

        # Update the current balance in the session
        session["current_balance"] = cb

        # Return a JSON response with the updated balance
        response = {"currentBalance": cb}
        return jsonify(response)
    except Exception as e:
        error_response = {"error": str(e)}
        return jsonify(error_response), 500


def get_cb():
    # Retrieve the current balance from the global variable
    return cb


def save_cb(balance):
    # Save the updated balance to the global variable
    global cb
    cb = balance
    session["current_balance"] = cb


@app.route("/templates/withdraw.html", methods=["GET"])
def withdraw():
    cb = get_cb()
    return render_template("withdraw.html", currentBalance=cb)


@app.route("/withdraw", methods=["POST"])
def process_withdraw():
    amount = float(request.form.get("amount"))  # Retrieve the amount from the form data
    try:
        cb = get_cb()
        if amount > cb:
            return (
                jsonify(
                    {"error": "Insufficient funds"}
                ),  # Insufficient funds for withdrawal
                400,
            )
        cb -= amount
        save_cb(cb)  # Update the balance after withdrawal

        session["current_balance"] = cb  # Update the current balance in the session

        response = {
            "currentBalance": cb
        }  # Return a JSON response with the updated balance
        return jsonify(response)
    except Exception as e:
        # Return an error response if any exception occurs
        error_response = {"error": str(e)}
        return jsonify(error_response), 500  # Use an appropriate HTTP status code


@app.route("/templates/forgotpin.html", methods=["GET"])
def forgot_pin():
    return render_template("forgotpin.html")


@app.route("/forgotpin", methods=["GET", "POST"])
def reset_pin():
    if request.method == "POST":
        new_pin = request.form.get("new_pin")

        if len(new_pin) != 6:
            return "The pin has to be 6-digits"
        # Update the pin with the new value
        else:
            pin = new_pin
            return redirect(url_for("login"))
    else:
        return render_template("forgotpin.html")


@app.route("/templates/transfer.html", methods=["GET"])
def transfer():
    if "username" not in session:
        return redirect(
            "/login"
        )  # Redirect to the login page if the user is not logged in

    # Retrieve the current balance from the session or set it to 0 if not present
    cb = session.get("current_balance")

    # Retrieve the user's transaction history from the session or set it to an empty list if not present
    transactions = session.get("transactions", [])

    return render_template(
        "transfer.html", currentBalance=cb, transactions=transactions
    )


@app.route("/transfer", methods=["POST"])
def transfer_amount():
    if "username" not in session:
        return redirect(
            "/login"
        )  # Redirect to the login page if the user is not logged in

    # Retrieve the current balance from the session or set it to 0 if not present
    cb = session.get("current_balance")

    # Retrieve the user's transaction history from the session or set it to an empty list if not present
    transactions = session.get("transactions", [])

    receiver_account = request.form.get("account-number")
    amount = int(request.form.get("amount"))

    if amount > cb:
        return "Insufficient funds"  # Display an error message if the amount is greater than the current balance
    else:
        cb -= amount
        transaction = f"{amount} has been transferred to account: {receiver_account}, your remaining balance is {cb}"
        transactions.append(
            transaction
        )  # Store the transaction in the user's transaction history

    # Update the current balance and transaction history in the session
    session["current_balance"] = cb
    session["transactions"] = transactions

    return render_template(
        "transfer.html", currentBalance=cb, transactions=transactions
    )


if __name__ == "__main__":
    app.run(debug=True)
