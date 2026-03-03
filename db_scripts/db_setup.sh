#!/bin/bash

# --- CONFIGURATION ---
ROOT_USER="root"
ROOT_PASS="mysqlpassword"  # Credentials to use or set
DB_NAME="workflow_db"
DB_USER="workflow_user"
DB_PASS="WorkflowPass456!"

echo "--- MySQL Workflow Environment Setup ---"

# 1. Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "MySQL is NOT installed on this system."

    read -p "Would you like to install MySQL now? (y/n): " install_confirm
    if [[ $install_confirm == [yY] || $install_confirm == [yY][eE][sS] ]]; then
        echo "Installing MySQL..."

        # OS Detection & Installation
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y mysql-server
            sudo systemctl start mysql
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install mysql && brew services start mysql
        fi

        # --- NEW CONFIRMATION STEP ---
        echo "Installation complete."
        read -p "Setup '$ROOT_USER' with the password provided in the script? (y/n): " root_confirm
        if [[ $root_confirm == [yY] || $root_confirm == [yY][eE][sS] ]]; then
            echo "Setting up initial root credentials..."
            sudo mysql -e "ALTER USER '$ROOT_USER'@'localhost' IDENTIFIED WITH mysql_native_password BY '$ROOT_PASS'; FLUSH PRIVILEGES;"
        else
            echo "Root setup skipped. You will need to configure root manually."
            exit 1
        fi
    else
        echo "Installation cancelled."
        exit 1
    fi
fi

# 2. Verify Access (Works for both existing and newly installed versions)
echo "Attempting to login as '$ROOT_USER'..."

if mysql -u "$ROOT_USER" -p"$ROOT_PASS" -e "quit" &> /dev/null; then
    echo "✅ Success: Root access confirmed."
    MYSQL_CMD="mysql -u $ROOT_USER -p$ROOT_PASS"
else
    echo "❌ Error: Could not log in. Either the password in the script is wrong or MySQL is not running."
    exit 1
fi

# 3. Setup Database and Worker User
echo "Configuring Database: $DB_NAME and User: $DB_USER..."

$MYSQL_CMD <<EOF
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`;
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "----------------------------------------"
echo "Setup Complete!"
echo "----------------------------------------"
