from flask_sqlalchemy import SQLAlchemy
from app.model import init_model
import logging
import pymysql

logger = logging.getLogger("dao")


class DaoPool:
    sqlDAO = None
    esDAO = None

    def __init__(self):
        pass

    def init_app(self, app):
        with app.app_context():
            # db init
            logger.info("init database at: "
                + app.config["DATABASE"]["host"]
                + ":"
                + str(app.config["DATABASE"]["port"])
                + "/"
                + app.config["DATABASE"]["database"])
            # create database if it doesn't exist
            conn = pymysql.connect(
                host=app.config["DATABASE"]["host"],
                port=app.config["DATABASE"]["port"],
                user=app.config["DATABASE"]["user"],
                password=app.config["DATABASE"]["password"],
                cursorclass=pymysql.cursors.DictCursor,
            )
            try:
                cur = conn.cursor()
                # execute sql
                cur.execute("CREATE DATABASE IF NOT EXISTS " + app.config["DATABASE"]["database"])
                # close
                cur.close()
                conn.close()
            except pymysql.err.MySQLError as _error:
                logger.error("database created failed")
                raise _error
            # connect to database
            app.config["SQLALCHEMY_DATABASE_URI"] = (
                "mysql+pymysql://"
                + app.config["DATABASE"]["user"]
                + ":"
                + app.config["DATABASE"]["password"]
                + "@"
                + app.config["DATABASE"]["host"]
                + ":"
                + str(app.config["DATABASE"]["port"])
                + "/"
                + app.config["DATABASE"]["database"]
            )
            self.sqlDAO = SQLAlchemy(app)
            # create table
            logger.info("create table......")
            init_model(self.sqlDAO)
            logger.info("table created.")
            logger.info("database initialization complete.")


daoPool = DaoPool()
