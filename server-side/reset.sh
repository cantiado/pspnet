#!/bin/sh

echo "Deleting images..."
rm -rf images/*
echo "Deleting user DB..."
rm instance/user.db
echo "Creating new database..."
python <<HEREDOC
from app import app, db
app.app_context().push()
db.create_all()
HEREDOC
echo "All done!"
