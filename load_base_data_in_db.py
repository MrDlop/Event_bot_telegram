from data import db_session, user_types

db_session.global_init("databases/db.db")
db_sess = db_session.create_session()

type_ = user_types.UserTypes()
type_.name = 'user'
db_sess.add(type_)

type_ = user_types.UserTypes()
type_.name = 'admin_0'
db_sess.add(type_)

type_ = user_types.UserTypes()
type_.name = 'admin_1'
db_sess.add(type_)

db_sess.commit()
db_sess.close()
