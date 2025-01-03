from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Contact, Listing, User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash  # Güvenli şifreleme

main = Blueprint('main', __name__)

@main.route("/")
def index():
    # Kullanıcı giriş yapmamışsa, giriş yap sayfasına yönlendir
    if 'id' not in session:
        return redirect(url_for('main.login'))  # Giriş yap sayfasına yönlendir

    listings = Listing.query.all()
    username = session.get('username')
    return render_template("index.html", listings=listings, username=username)


    
@main.route("/listings/<int:id>")
def listing_detail(id):
    listing = Listing.query.get_or_404(id)
    return render_template("listings.html", listing=listing)

@main.route("/add-listing", methods=["GET", "POST"])
def add_listing():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        price = request.form["price"]
        location = request.form["location"]
        image_url = request.form.get("image_url", "")

        new_listing = Listing(
            title=title,
            description=description,
            price=price,
            location=location,
            image_url=image_url
        )
        db.session.add(new_listing)
        db.session.commit()
        flash('İlan başarıyla eklendi.', 'success')
        return redirect(url_for("main.index"))
    return render_template("add_listing.html")

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()
        flash('Mesajınız başarıyla gönderildi.', 'success')
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash('Tüm alanları doldurmalısınız.', 'danger')
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash('Şifreler uyuşmuyor.', 'danger')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Kayıt başarılı!', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            flash('Bir hata oluştu, lütfen tekrar deneyin.', 'danger')
            print(e)
            return redirect(url_for('main.register'))

    return render_template('register.html')




@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:  # Eksik alan kontrolü
            flash('E-posta ve şifre zorunludur.', 'danger')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['id'] = user.id
            session['username'] = user.username
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Hatalı e-posta veya şifre!', 'danger')

    return render_template('login.html')


@main.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('username', None)
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('main.login'))


