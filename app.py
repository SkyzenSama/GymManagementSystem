from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'ERGETEAMPASS'  # Replace with a secure secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user['user_id'], user['username'], user['password_hash'])
    return None

# Veritabanı bağlantısı için yardımcı fonksiyon
def get_db_connection():
    conn = sqlite3.connect('gym_management_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['user_id'], user['username'], user['password_hash'])
            login_user(user_obj)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Protecting Routes with @login_required
@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Form verilerini al
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        joining_date = request.form['joining_date']
        date_of_birth = request.form['date_of_birth']
        membership_type = request.form['membership_type']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']
        trainer_id = request.form['trainer_id']

        # Veritabanına ekle
        cursor.execute('''
            INSERT INTO Members (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number, trainer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number, trainer_id))
        conn.commit()
        conn.close()
        flash('Member added successfully!', 'success')
        return redirect(url_for('view_members'))

    # Eğitmenleri getir
    cursor.execute('SELECT trainer_id, name FROM Trainers')
    trainers = cursor.fetchall()
    conn.close()
    return render_template('add_member.html', trainers=trainers)

@app.route('/delete_member/<int:member_id>', methods=['POST'])
@login_required
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
    conn.commit()
    conn.close()
    flash('Member deleted successfully!', 'info')
    return redirect(url_for('view_members'))

@app.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Formdan gelen değerleri al
        name = request.form['name']
        gender = request.form['gender']
        joining_date = request.form['joining_date']
        contact_number = request.form['contact_number']
        date_of_birth = request.form['date_of_birth']
        membership_type = request.form['membership_type']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']
        trainer_id = request.form['trainer_id']

        # Veriyi güncelle
        cursor.execute('''
            UPDATE Members 
            SET name = ?, gender = ?, joining_date = ?, contact_number = ?, 
                date_of_birth = ?, membership_type = ?, emergency_contact_name = ?, 
                emergency_contact_number = ?, trainer_id = ?
            WHERE member_id = ?
        ''', (name, gender, joining_date, contact_number, date_of_birth,
              membership_type, emergency_contact_name, emergency_contact_number, trainer_id, member_id))
        conn.commit()
        conn.close()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('view_members'))

    # Üye ve eğitmen bilgilerini çek
    cursor.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,))
    member = cursor.fetchone()
    cursor.execute('SELECT trainer_id, name FROM Trainers')
    trainers = cursor.fetchall()
    conn.close()
    return render_template('edit_member.html', member=member, trainers=trainers)

@app.route('/view_members')
@login_required
def view_members():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Üyeleri ve eğitmen isimlerini birleştirerek getir
    cursor.execute('''
        SELECT Members.*, Trainers.name AS trainer_name
        FROM Members
        LEFT JOIN Trainers ON Members.trainer_id = Trainers.trainer_id
    ''')
    members = cursor.fetchall()
    conn.close()

    return render_template('view_members.html', members=members)

@app.route('/search_members', methods=['GET'])
@login_required
def search_members():
    query = request.args.get('query')  # Arama sorgusunu al
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Members WHERE name LIKE ? OR membership_type LIKE ?", (f"%{query}%", f"%{query}%"))
    members = cursor.fetchall()
    conn.close()
    return render_template('view_members.html', members=members)

@app.route('/view_trainers')
@login_required
def view_trainers():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Eğitmen ve atanan workout bilgilerini getir
    cursor.execute('''
        SELECT 
            Trainers.*, 
            GROUP_CONCAT(Workout_Routines.routine_name, ', ') AS assigned_workouts
        FROM Trainers
        LEFT JOIN Trainer_Workouts ON Trainers.trainer_id = Trainer_Workouts.trainer_id
        LEFT JOIN Workout_Routines ON Trainer_Workouts.routine_id = Workout_Routines.routine_id
        GROUP BY Trainers.trainer_id
    ''')
    trainers = cursor.fetchall()
    conn.close()

    return render_template('view_trainers.html', trainers=trainers)

@app.route('/view_workouts')
@login_required
def view_workouts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Workout_Routines')
    workouts = cursor.fetchall()
    conn.close()
    return render_template('view_workouts.html', workouts=workouts)

@app.route('/view_equipment')
@login_required
def view_equipment():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Gym_Equipment')
    equipment = cursor.fetchall()
    conn.close()
    return render_template('view_equipment.html', equipment=equipment)

@app.route('/search_equipment', methods=['GET'])
@login_required
def search_equipment():
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Gym_Equipment WHERE name LIKE ?", (f"%{query}%",))
    equipment = cursor.fetchall()
    conn.close()
    return render_template('view_equipment.html', equipment=equipment)

@app.route('/add_equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        manufacturer = request.form['manufacturer']
        maintenance_date = request.form['maintenance_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Gym_Equipment (name, quantity, price, manufacturer, maintenance_date) VALUES (?, ?, ?, ?, ?)',
                       (name, quantity, price, manufacturer, maintenance_date))
        conn.commit()
        conn.close()
        flash('Equipment added successfully!', 'success')
        return redirect(url_for('view_equipment'))
    return render_template('add_equipment.html')

@app.route('/edit_equipment/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_equipment(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        manufacturer = request.form['manufacturer']
        maintenance_date = request.form['maintenance_date']

        cursor.execute('''
            UPDATE Gym_Equipment 
            SET name = ?, quantity = ?, price = ?, manufacturer = ?, maintenance_date = ?
            WHERE item_id = ?
        ''', (name, quantity, price, manufacturer, maintenance_date, item_id))
        conn.commit()
        conn.close()
        flash('Equipment updated successfully!', 'success')
        return redirect(url_for('view_equipment'))

    cursor.execute('SELECT * FROM Gym_Equipment WHERE item_id = ?', (item_id,))
    equipment = cursor.fetchone()
    conn.close()
    return render_template('edit_equipment.html', equipment=equipment)

@app.route('/delete_equipment/<int:item_id>', methods=['POST'])
@login_required
def delete_equipment(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Gym_Equipment WHERE item_id = ?', (item_id,))
    conn.commit()
    conn.close()
    flash('Equipment deleted successfully!', 'info')
    return redirect(url_for('view_equipment'))

@app.route('/add_workout', methods=['GET', 'POST'])
@login_required
def add_workout():
    if request.method == 'POST':
        routine_name = request.form['routine_name']
        description = request.form['description']
        duration = request.form['duration']
        difficulty_level = request.form['difficulty_level']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Workout_Routines (routine_name, description, duration, difficulty_level) VALUES (?, ?, ?, ?)',
                       (routine_name, description, duration, difficulty_level))
        conn.commit()
        conn.close()
        flash('Workout routine added successfully!', 'success')
        return redirect(url_for('view_workouts'))
    return render_template('add_workout.html')

@app.route('/edit_workout/<int:routine_id>', methods=['GET', 'POST'])
@login_required
def edit_workout(routine_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        routine_name = request.form['routine_name']
        description = request.form['description']
        duration = request.form['duration']
        difficulty_level = request.form['difficulty_level']

        cursor.execute('''
            UPDATE Workout_Routines 
            SET routine_name = ?, description = ?, duration = ?, difficulty_level = ?
            WHERE routine_id = ?
        ''', (routine_name, description, duration, difficulty_level, routine_id))
        conn.commit()
        conn.close()
        flash('Workout routine updated successfully!', 'success')
        return redirect(url_for('view_workouts'))

    cursor.execute('SELECT * FROM Workout_Routines WHERE routine_id = ?', (routine_id,))
    workout = cursor.fetchone()
    conn.close()
    return render_template('edit_workout.html', workout=workout)

@app.route('/delete_workout/<int:routine_id>', methods=['POST'])
@login_required
def delete_workout(routine_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Workout_Routines WHERE routine_id = ?', (routine_id,))
    conn.commit()
    conn.close()
    flash('Workout routine deleted successfully!', 'info')
    return redirect(url_for('view_workouts'))

@app.route('/search_workouts', methods=['GET'])
@login_required
def search_workouts():
    query = request.args.get('query')  # Kullanıcıdan gelen arama sorgusunu al
    conn = get_db_connection()
    cursor = conn.cursor()

    # Arama sorgusu: workout ismi veya açıklamasında geçen değerleri bul
    cursor.execute("""
        SELECT * FROM Workout_Routines 
        WHERE routine_name LIKE ? OR description LIKE ?
    """, (f"%{query}%", f"%{query}%"))

    workouts = cursor.fetchall()
    conn.close()

    # Sonuçları view_workouts.html şablonuna gönder
    return render_template('view_workouts.html', workouts=workouts)

@app.route('/search_trainers', methods=['GET'])
@login_required
def search_trainers():
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Trainers 
        WHERE name LIKE ? OR role LIKE ?
    """, (f"%{query}%", f"%{query}%"))
    trainers = cursor.fetchall()
    conn.close()
    return render_template('view_trainers.html', trainers=trainers)

@app.route('/add_trainer', methods=['GET', 'POST'])
@login_required
def add_trainer():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        role = request.form['role']
        experience = request.form['experience']
        specialty = request.form['specialty']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Trainers (name, gender, contact_number, role, experience, specialty) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, gender, contact_number, role, experience, specialty))
        conn.commit()
        conn.close()
        flash('Trainer added successfully!', 'success')
        return redirect(url_for('view_trainers'))
    return render_template('add_trainer.html')

@app.route('/edit_trainer/<int:trainer_id>', methods=['GET', 'POST'])
@login_required
def edit_trainer(trainer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        contact_number = request.form['contact_number']
        role = request.form['role']
        experience = request.form['experience']
        specialty = request.form['specialty']

        cursor.execute('''
            UPDATE Trainers 
            SET name = ?, gender = ?, contact_number = ?, role = ?, experience = ?, specialty = ?
            WHERE trainer_id = ?
        ''', (name, gender, contact_number, role, experience, specialty, trainer_id))
        conn.commit()
        conn.close()
        flash('Trainer updated successfully!', 'success')
        return redirect(url_for('view_trainers'))

    cursor.execute('SELECT * FROM Trainers WHERE trainer_id = ?', (trainer_id,))
    trainer = cursor.fetchone()
    conn.close()
    return render_template('edit_trainer.html', trainer=trainer)

@app.route('/delete_trainer/<int:trainer_id>', methods=['POST'])
@login_required
def delete_trainer(trainer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Trainers WHERE trainer_id = ?', (trainer_id,))
    conn.commit()
    conn.close()
    flash('Trainer deleted successfully!', 'info')
    return redirect(url_for('view_trainers'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Toplam üye sayısı
    cursor.execute('SELECT COUNT(*) AS total_members FROM Members')
    total_members = cursor.fetchone()['total_members']

    # Eğitmen başına üye sayısı
    cursor.execute('''
        SELECT Trainers.name AS trainer_name, COUNT(Members.member_id) AS total_members
        FROM Trainers
        LEFT JOIN Members ON Trainers.trainer_id = Members.trainer_id
        GROUP BY Trainers.trainer_id
    ''')
    trainer_stats = cursor.fetchall()

    # Üyelik türüne göre dağılım
    cursor.execute('''
        SELECT membership_type, COUNT(*) AS total_members
        FROM Members
        GROUP BY membership_type
    ''')
    membership_stats = cursor.fetchall()

    # Eğitmen başına atanan workoutlar
    cursor.execute('''
        SELECT Trainers.name AS trainer_name, 
               GROUP_CONCAT(Workout_Routines.routine_name, ', ') AS workouts
        FROM Trainers
        LEFT JOIN Trainer_Workouts ON Trainers.trainer_id = Trainer_Workouts.trainer_id
        LEFT JOIN Workout_Routines ON Trainer_Workouts.routine_id = Workout_Routines.routine_id
        GROUP BY Trainers.trainer_id
    ''')
    trainer_workouts = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html',
                           total_members=total_members,
                           trainer_stats=trainer_stats,
                           membership_stats=membership_stats,
                           trainer_workouts=trainer_workouts)

@app.route('/filter_members', methods=['GET', 'POST'])
@login_required
def filter_members():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Formdan alınan filtreleme kriterleri
    membership_type = request.args.get('membership_type')
    trainer_id = request.args.get('trainer_id')
    joining_date_start = request.args.get('joining_date_start')
    joining_date_end = request.args.get('joining_date_end')

    # SQL sorgusunu oluştur
    query = '''
        SELECT Members.*, Trainers.name AS trainer_name
        FROM Members
        LEFT JOIN Trainers ON Members.trainer_id = Trainers.trainer_id
        WHERE 1=1
    '''
    params = []

    if membership_type:
        query += ' AND Members.membership_type = ?'
        params.append(membership_type)
    if trainer_id:
        query += ' AND Members.trainer_id = ?'
        params.append(trainer_id)
    if joining_date_start and joining_date_end:
        query += ' AND Members.joining_date BETWEEN ? AND ?'
        params.append(joining_date_start)
        params.append(joining_date_end)

    cursor.execute(query, params)
    members = cursor.fetchall()

    # Eğitmenleri listelemek için
    cursor.execute('SELECT trainer_id, name FROM Trainers')
    trainers = cursor.fetchall()

    conn.close()
    return render_template('filter_members.html', members=members, trainers=trainers)

@app.route('/assign_workout/<int:trainer_id>', methods=['GET', 'POST'])
@login_required
def assign_workout(trainer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        routine_id = request.form['routine_id']
        try:
            cursor.execute('''
                INSERT INTO Trainer_Workouts (trainer_id, routine_id)
                VALUES (?, ?)
            ''', (trainer_id, routine_id))
            conn.commit()
            flash('Workout assigned successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('This workout is already assigned to the trainer.', 'warning')
        conn.close()
        return redirect(url_for('view_trainers'))

    # Eğitmeni ve antrenman listesini getir
    cursor.execute('SELECT * FROM Trainers WHERE trainer_id = ?', (trainer_id,))
    trainer = cursor.fetchone()

    cursor.execute('SELECT * FROM Workout_Routines')
    workouts = cursor.fetchall()
    conn.close()

    return render_template('assign_workout.html', trainer=trainer, workouts=workouts)



if __name__ == '__main__':
    app.run(debug=True)
