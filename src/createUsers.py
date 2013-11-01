import sqlite3
from userdb.userdb import UserDatabase
from test.users.userdbtest import DummyEmailSender
conn = sqlite3.connect("users/users.db")
userDb = UserDatabase(emailSender = DummyEmailSender())
userDb.createDatabase(conn, True)
userId = userDb.registerUser("admin@sehicl.org.uk", "User Admin", None, "wceag1es", conn)
userDb.activateUser(userId, conn)
conn.cursor().execute("insert into role (id, role) values(?, 'admin')", (userId,))
conn.commit()
conn.close()