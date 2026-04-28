from src.service.database import DatabaseManager

if __name__ == "__main__":
    dm = DatabaseManager()
    dm.create_cameras_db()
