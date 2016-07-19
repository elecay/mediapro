# -*- coding: utf-8 -*-
import logging
import logging.config
import yaml
import tornado.ioloop
import tornado.web

from config import Config
from core.connection_provider import MongoConnectionProvider
from services.task_services import TaskServices

from routes.handlers import TasksHandler, TaskHandler, TaskPayloadHandler

conf_env_path = 'configuration/dev.cfg'
conf_logging_path = 'configuration/logging.yml'


def make_app():
    """
    Initialize the server with the endpoints.
    :return: None
    """
    return tornado.web.Application([
        # TasksHandler
        (r"/api/tasks", TasksHandler,
         dict(service=TaskServices())),
        # TaskHandler
        (r"/api/tasks/([a-zA-Z0-9]+)", TaskHandler,
         dict(service=TaskServices())),
        # TaskPayloadHandler
        (r"/api/tasks/([a-zA-Z0-9]+)/payload", TaskPayloadHandler,
         dict(service=TaskServices())),
        (r"/api/tasks/([a-zA-Z0-9]+)/payload/([a-zA-Z0-9]+)",
         TaskPayloadHandler, dict(service=TaskServices()))
    ])


def init_db_connection(conf):
    """
    Initialize the database connection.
    :param conf: configuration attributes.
    :return: None
    """
    MongoConnectionProvider.connect(conf['mongodb']['uri'])


def init_logging(log_config_path):
    """
    Initialize logging system.
    :param log_config_path: relative path to the logging configuration file.
    :return:
    """
    log_cfg = yaml.load(open(log_config_path, 'r'))
    logging.config.dictConfig(log_cfg)


if __name__ == "__main__":
    cfg = Config(conf_env_path)

    init_db_connection(cfg)
    init_logging(conf_logging_path)

    app = make_app()
    app.listen(cfg['server']['port'])
    tornado.ioloop.IOLoop.current().start()
