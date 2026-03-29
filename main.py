from dotenv import load_dotenv
import os
from view.main_view import Main_View
from control.main_controller import Main_Controller

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "IDK_WMS")
}

def main():
    view_principal = Main_View()
    controller_principal = Main_Controller(view_principal, db_config)
    view_principal.controller = controller_principal
    view_principal.run()

if __name__ == "__main__":
    main()