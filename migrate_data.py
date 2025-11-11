import sqlite3
from app import db, Admin, Candidate, Job, Application
from werkzeug.security import generate_password_hash

def migrate_data():
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('hiring_platform.db')
    sqlite_conn.row_factory = sqlite3.Row
    sqlite_cursor = sqlite_conn.cursor()

    try:
        # Create all tables in PostgreSQL
        db.create_all()

        # Migrate Admins
        print("Migrating Admins...")
        sqlite_cursor.execute("SELECT * FROM admins")
        admins = sqlite_cursor.fetchall()
        for admin in admins:
            new_admin = Admin(
                id=admin['id'],
                company_name=admin['company_name'],
                email=admin['email'],
                phone=admin['phone'],
                password=admin['password']
            )
            db.session.add(new_admin)
        db.session.commit()
        print(f"Migrated {len(admins)} admins")

        # Migrate Candidates
        print("Migrating Candidates...")
        sqlite_cursor.execute("SELECT * FROM candidates")
        candidates = sqlite_cursor.fetchall()
        for candidate in candidates:
            new_candidate = Candidate(
                id=candidate['id'],
                name=candidate['name'],
                email=candidate['email'],
                password=candidate['password']
            )
            db.session.add(new_candidate)
        db.session.commit()
        print(f"Migrated {len(candidates)} candidates")

        # Migrate Jobs
        print("Migrating Jobs...")
        sqlite_cursor.execute("SELECT * FROM jobs")
        jobs = sqlite_cursor.fetchall()
        for job in jobs:
            new_job = Job(
                id=job['id'],
                admin_id=job['admin_id'],
                title=job['title'],
                description=job['description']
            )
            db.session.add(new_job)
        db.session.commit()
        print(f"Migrated {len(jobs)} jobs")

        # Migrate Applications
        print("Migrating Applications...")
        sqlite_cursor.execute("SELECT * FROM applications")
        applications = sqlite_cursor.fetchall()
        for app in applications:
            new_application = Application(
                id=app['id'],
                candidate_id=app['candidate_id'],
                job_id=app['job_id'],
                resume_text=app['resume_text'],
                status=app['status'],
                shortlist_reason=app['shortlist_reason'],
                report_path=app['report_path'],
                interview_results=app['interview_results']
            )
            db.session.add(new_application)
        db.session.commit()
        print(f"Migrated {len(applications)} applications")

        print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        db.session.rollback()
    finally:
        sqlite_conn.close()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        migrate_data()