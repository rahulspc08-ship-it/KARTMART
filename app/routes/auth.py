from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app.extensions import db
from app.models import User
from app.services import CartService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role

            # Merge guest cart into user cart
            guest_session_id = session.get('guest_id')
            if guest_session_id:
                CartService.merge_guest_cart(guest_session_id, user.id)

            flash(f"Welcome back, {user.name}!", "success")
            next_url = request.args.get('next')
            if user.is_admin and not next_url:
                return redirect(url_for('admin.dashboard'))
            return redirect(next_url or url_for('products.index'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        pincode = request.form.get('pincode', '').strip()

        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        user = User(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            role='customer'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Auto-login after registration
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['user_role'] = user.role

        guest_session_id = session.get('guest_id')
        if guest_session_id:
            CartService.merge_guest_cart(guest_session_id, user.id)

        flash(f"Account created successfully! Welcome to KARTMART, {user.name}!", "success")
        return redirect(url_for('products.index'))

    return render_template('auth/register.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('user_id'):
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('products.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            if not user.is_admin:
                flash("This account does not have administrator privileges. Please log in as customer or register as an administrator.", "warning")
                return render_template('auth/admin_login.html')

            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role

            flash(f"Welcome back to KARTMART Admin Console, {user.name}!", "success")
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            flash("Invalid administrator email or password.", "danger")

    return render_template('auth/admin_login.html')


@auth_bp.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if session.get('user_id') and session.get('user_role') == 'admin':
        return redirect(url_for('admin.dashboard'))

    admin_key = current_app.config.get('ADMIN_REGISTRATION_KEY', 'Admin@2026')

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        provided_key = request.form.get('admin_key', '').strip()
        phone = request.form.get('phone', '').strip()

        if not name or not email or not password or not provided_key:
            flash("Name, email, password, and Admin Security Key are required.", "danger")
            return render_template('auth/admin_register.html', default_key=admin_key)

        if provided_key != admin_key:
            flash("Invalid Admin Security Key. Authorized credentials required to register as Administrator.", "danger")
            return render_template('auth/admin_register.html', default_key=admin_key)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/admin_register.html', default_key=admin_key)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/admin_register.html', default_key=admin_key)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if existing_user.is_admin:
                flash("An administrator account with this email already exists. Please log in.", "warning")
                return redirect(url_for('auth.admin_login'))
            else:
                existing_user.role = 'admin'
                existing_user.name = name
                existing_user.set_password(password)
                if phone:
                    existing_user.phone = phone
                db.session.commit()
                session['user_id'] = existing_user.id
                session['user_name'] = existing_user.name
                session['user_email'] = existing_user.email
                session['user_role'] = 'admin'
                flash(f"Account granted Administrator role! Welcome to Admin Console, {existing_user.name}!", "success")
                return redirect(url_for('admin.dashboard'))

        user = User(
            name=name,
            email=email,
            phone=phone,
            role='admin'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['user_role'] = user.role

        flash(f"Administrator account created successfully! Welcome to KARTMART Admin Console, {user.name}!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('auth/admin_register.html', default_key=admin_key)


@auth_bp.route('/logout')
def logout():
    name = session.get('user_name', 'Customer')
    session.clear()
    flash(f"Logged out successfully. See you soon, {name}!", "info")
    return redirect(url_for('products.index'))


@auth_bp.route('/demo-login/<role>')
def demo_login(role):
    """Convenience 1-click login for demonstration testing."""
    target_email = 'admin@kartmart.local' if role == 'admin' else 'customer@kartmart.local'
    user = User.query.filter_by(email=target_email).first()
    
    if not user:
        # Fallback create if not yet seeded
        user = User(
            name="Store Admin" if role == 'admin' else "Demo Customer",
            email=target_email,
            role=role,
            phone="9876543210",
            address="123 Tech Park, MG Road",
            city="Bengaluru",
            pincode="560001"
        )
        user.set_password("Admin@123" if role == 'admin' else "Customer@123")
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    session['user_name'] = user.name
    session['user_email'] = user.email
    session['user_role'] = user.role

    flash(f"Logged in as Demo {role.capitalize()}: {user.name}", "success")
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('products.index'))
