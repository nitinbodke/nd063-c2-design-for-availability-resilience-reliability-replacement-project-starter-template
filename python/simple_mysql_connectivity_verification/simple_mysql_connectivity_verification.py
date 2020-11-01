import mysql.connector
from mysql.connector import Error
import logging
import argparse
from configparser import ConfigParser


logging.basicConfig(level=logging.DEBUG, filename='simple_mysql_connectivity_verification.log',
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)


def create_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
        logger.info("Connection to MySQL DB successful")
    except Error as e:
        logger.error(f"The error '{e}' occurred")
    return connection


def create_table(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        logger.info("Table created successfully")
    except Error as e:
        logger.error(f"The error '{e}' occurred")
    finally:
        cursor.close()


def insert_authors(connection, authors):
    query = "INSERT INTO authors(first_name, last_name) VALUES(%s,%s)"
    cursor = connection.cursor()
    try:
        cursor.executemany(query, authors)
        connection.commit()
        logger.info("Data inserted successfully")
    except Error as e:
        logger.error('Error:', e)
    finally:
        cursor.close()


def query_with_fetchall(connection, table):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM " + table)
        rows = cursor.fetchall()
        logger.info('Total Row(s):' + str(cursor.rowcount))
        return rows
    except Error as e:
        logger.error(e)
    finally:
        cursor.close()


def perform_db_operations(host, user, password, database):
    # Open connection to database
    connection = create_connection(host, user, password, database)

    # Create table
    create_author_table = """
    CREATE TABLE IF NOT EXISTS `authors` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `first_name` varchar(40) NOT NULL,
    `last_name` varchar(40) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=latin1"""
    create_table(connection, create_author_table)

    # read data
    authors_from_db_before_insert = query_with_fetchall(connection, 'authors')

    # insert data
    authors = [('Herbert', 'Methley'), ('Olive', 'Wellwood')]
    insert_authors(connection, authors)

    # read data
    authors_from_db_after_insert = query_with_fetchall(connection, 'authors')


def create_parser():
    parser = argparse.ArgumentParser(prog='simple_mysql_connectivity_verification',
                                     description='Verify connectivity by executing create table, insert, read ops',
                                     allow_abbrev=False, epilog='Happy verification!')
    parser.add_argument('config', metavar='config', type=str, action='store', help='Path to config file')
    parser.add_argument('environment', metavar='env', type=str, action='store', help='Environment e.g. local, dev')
    return parser


def main():
    # parse arguments
    args = create_parser().parse_args()
    env = args.environment
    config = args.config

    # parse config
    parser = ConfigParser()
    parser.read(config)

    # validate config
    keys = {'host', 'database', 'user', 'password'}
    if parser[env]:
        section = parser[env]
        missing = keys - set(section.keys())
        if not missing:
            host = section['host']
            user = section['user']
            password = section['password']
            database = section['database']
            perform_db_operations(host, user, password, database)
        else:
            logger.error("Missing keys :" + missing.__str__())
    else:
        logger.error("Section " + env + " not found in config file.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Exception occurred", exc_info=True)
