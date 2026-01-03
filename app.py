import os
from flask import Flask, render_template, url_for, flash, redirect, request
from models import db, User, Expense
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)



app.config['SECRET_KEY'] =os.getenv('SECRET_KEY') 


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Routes

@app.route("/")
@app.route("/dashboard")
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_spent = sum(exp.amount for exp in expenses)


    #dictionary: {'Food': 500, 'Bills': 200}
    chart_data = {}
    for exp in expenses:
        chart_data[exp.category] = chart_data.get(exp.category, 0) + exp.amount

    return render_template('dashboard.html', 
                           expenses=expenses, 
                           total=total_spent, 
                           labels=list(chart_data.keys()), 
                           values=list(chart_data.values()))

@app.route("/delete_expense/<int:id>")
@login_required
def delete_expense(id):
    
    expense_to_delete = Expense.query.get_or_404(id)
    
    
    if expense_to_delete.author != current_user:
        flash("You do not have permission to delete this.", "danger")
        return redirect(url_for('dashboard'))
    
   
    db.session.delete(expense_to_delete)
    db.session.commit()
    
    flash("Expense deleted successfully!", "info")
    return redirect(url_for('dashboard'))

@app.route("/add_expense", methods=['POST'])
@login_required
def add_expense():
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')
    
    if title and amount:
        new_expense = Expense(title=title, amount=float(amount), category=category, author=current_user)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added!', 'success')
    return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)