from app import db, bcrypt
from flask import render_template, flash, url_for, redirect, request, Blueprint
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import send_reset_mail, upload_image


users = Blueprint('users', __name__)


@users.route('/register', methods=['POST', 'GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sign up successful, please log in', category='success')
        return redirect(url_for('users.login_page'))
    return render_template('register.html', title="Sign Up", form=form)


#===============================================================================

@users.route('/login', methods=['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Sign In successful', category='success') 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Incorrect username/password', category='danger')       
    return render_template('login.html', title="Sign In", form=form)


#========================================================================================================

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_name = upload_image(form.image_file.data)
            current_user.image_file = image_name
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Account updated!', category='success')
        return redirect(url_for('users.account_page'))
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('account.html', title="My Profile", form=form, image_file=image_file)
    


# =============================== Password Reset =============================================

@users.route('/request_reset', methods=['POST', 'GET'])
def request_reset():
    if current_user.is_authenticated:
        flash('You must be logged out to access password reset page', category='info')
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash('Password reset email sent!', category='success')
        return redirect(url_for('users.request_reset'))
    return render_template('request_token.html', title='Request Password Reset', form=form)




# ------------------------------------------ Reset Password ------------------------------------

@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        flash('You must be logged out to access password reset page', category='info')
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid/Expired token!', category='warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password updated', category='success')
        return redirect(url_for('users.login_page'))
    return render_template('reset_password.html', title='Request Password Reset', form=form)

# =========================================================================================================
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))