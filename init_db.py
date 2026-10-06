import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash

def create_connection(db_file):
    """Veritabanı bağlantısı oluşturur ve yabancı anahtar desteğini etkinleştirir."""
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(f"Veritabanına bağlanırken hata oluştu: {e}")
        return None

def create_table(conn, create_table_sql):
    """Veritabanında tablo oluşturur."""
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(f"Tablo oluşturulurken hata oluştu: {e}")

def init_db():
    database = 'gym_management_system.db'

    # Tablo oluşturma SQL komutları
    sql_create_members_table = '''
    CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT,
        joining_date DATE,
        contact_number TEXT,
        date_of_birth DATE,
        membership_type TEXT,
        emergency_contact_name TEXT,
        emergency_contact_number TEXT,
        trainer_id INTEGER,
        FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id) ON DELETE SET NULL
    );
    '''

    sql_create_trainers_table = '''
    CREATE TABLE IF NOT EXISTS Trainers (
        trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT,
        contact_number TEXT,
        role TEXT,
        experience INTEGER,
        specialty TEXT
    );
    '''

    sql_create_gym_equipment_table = '''
    CREATE TABLE IF NOT EXISTS Gym_Equipment (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        quantity INTEGER DEFAULT 0,
        price REAL CHECK(price >= 0),
        manufacturer TEXT,
        maintenance_date DATE
    );
    '''

    sql_create_workout_routines_table = '''
    CREATE TABLE IF NOT EXISTS Workout_Routines (
        routine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        routine_name TEXT NOT NULL UNIQUE,
        description TEXT,
        duration INTEGER CHECK(duration > 0),
        difficulty_level TEXT
    );
    '''

    sql_create_trainer_workouts_table = '''
    CREATE TABLE IF NOT EXISTS Trainer_Workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_id INTEGER NOT NULL,
        routine_id INTEGER NOT NULL,
        FOREIGN KEY (trainer_id) REFERENCES Trainers(trainer_id) ON DELETE CASCADE,
        FOREIGN KEY (routine_id) REFERENCES Workout_Routines(routine_id) ON DELETE CASCADE,
        UNIQUE(trainer_id, routine_id)
    );
    '''

    sql_create_users_table = '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    );
    '''

    # Veritabanı bağlantısı oluştur
    conn = create_connection(database)

    if conn is not None:
        # Tablo oluşturma işlemleri
        create_table(conn, sql_create_trainers_table)
        create_table(conn, sql_create_members_table)
        create_table(conn, sql_create_gym_equipment_table)
        create_table(conn, sql_create_workout_routines_table)
        create_table(conn, sql_create_trainer_workouts_table)
        create_table(conn, sql_create_users_table)

        # Örnek veriler ekleme
        with conn:
            cursor = conn.cursor()

            # Eğitmenler için örnek veri
            trainers_data = [
                ('Mike Ross', 'Male', '555-1010', 'Personal Trainer', 5, 'Weightlifting'),
                ('Rachel Zane', 'Female', '555-2020', 'Group Trainer', 3, 'Yoga')
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO Trainers (name, gender, contact_number, role, experience, specialty)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', trainers_data)

            # Üyeler için örnek veri
            # Eğitmen ID'lerini doğru eşleştirmek için önce eğitmenleri çekiyoruz
            cursor.execute("SELECT trainer_id FROM Trainers WHERE name = ?", ('Mike Ross',))
            mike_id = cursor.fetchone()
            mike_id = mike_id['trainer_id'] if mike_id else None

            cursor.execute("SELECT trainer_id FROM Trainers WHERE name = ?", ('Rachel Zane',))
            rachel_id = cursor.fetchone()
            rachel_id = rachel_id['trainer_id'] if rachel_id else None

            members_data = [
                ('John Doe', 'Male', '2023-01-15', '555-1234', '1990-05-20', 'Gold', 'Jane Doe', '555-5678', mike_id),
                ('Alice Smith', 'Female', '2023-02-10', '555-2345', '1985-08-12', 'Silver', 'Bob Smith', '555-6789', rachel_id)
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO Members (name, gender, joining_date, contact_number, date_of_birth, membership_type, emergency_contact_name, emergency_contact_number, trainer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', members_data)

            # Workout Routines için örnek veri
            workouts_data = [
                ('Full Body Workout', 'A comprehensive workout for the whole body', 60, 'Intermediate'),
                ('Cardio Blast', 'High-intensity cardio routine', 45, 'Advanced'),
                ('Strength Training', 'Focus on building muscle strength', 50, 'Beginner'),
                ('Yoga Flow', 'Relaxing yoga sequence', 30, 'Beginner'),
                ('HIIT Session', 'High-Intensity Interval Training', 40, 'Advanced')
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO Workout_Routines (routine_name, description, duration, difficulty_level)
                VALUES (?, ?, ?, ?);
            ''', workouts_data)

            # Gym Equipment için örnek veri
            equipment_data = [
                ('Treadmill', 5, 1200.00, 'FitCo', '2023-01-01'),
                ('Dumbbell Set', 10, 500.00, 'IronWorks', '2023-02-15')
            ]
            cursor.executemany('''
                INSERT OR IGNORE INTO Gym_Equipment (name, quantity, price, manufacturer, maintenance_date)
                VALUES (?, ?, ?, ?, ?);
            ''', equipment_data)

            # Workout Assignments örnek veri
            # Önce Workout Routines ve Trainers'ı alıyoruz
            cursor.execute("SELECT routine_id FROM Workout_Routines WHERE routine_name = ?", ('Full Body Workout',))
            fbw_id = cursor.fetchone()
            fbw_id = fbw_id['routine_id'] if fbw_id else None

            cursor.execute("SELECT routine_id FROM Workout_Routines WHERE routine_name = ?", ('Yoga Flow',))
            yf_id = cursor.fetchone()
            yf_id = yf_id['routine_id'] if yf_id else None

            if mike_id and fbw_id:
                cursor.execute('''
                    INSERT OR IGNORE INTO Trainer_Workouts (trainer_id, routine_id)
                    VALUES (?, ?);
                ''', (mike_id, fbw_id))

            if rachel_id and yf_id:
                cursor.execute('''
                    INSERT OR IGNORE INTO Trainer_Workouts (trainer_id, routine_id)
                    VALUES (?, ?);
                ''', (rachel_id, yf_id))

            # Users için örnek veri (Admin kullanıcısı)
            admin_username = 'admin'
            admin_password = '123'  # Güvenli bir parola ile değiştirin
            password_hash = generate_password_hash(admin_password, method='pbkdf2:sha256', salt_length=8)

            cursor.execute('''
                INSERT OR IGNORE INTO Users (username, password_hash)
                VALUES (?, ?);
            ''', (admin_username, password_hash))

        conn.close()
        print("Veritabanı başarıyla başlatıldı ve örnek veriler eklendi!")

if __name__ == '__main__':
    init_db()
