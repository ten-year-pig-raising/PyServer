# -*- coding: utf-8 -*-
from application.celery import app
import logging

logger = logging.getLogger(__name__)


@app.task
def task__1(*args, **kwargs):
    logger.info("===========task__1==================")
    logger.info("=================args===============")
    logger.info(args)
    logger.info("=================kwargs===============")
    logger.info(kwargs)
    # shop_tasks.evaluation_of_early_warnings(1, 100)


@app.task
def task__2(*args, **kwargs):
    logger.info("===========task__2==================")


@app.task
def task__3(*args, **kwargs):
    logger.info("===========task__3==================")


@app.task
def task__4(*args, **kwargs):
    logger.info("===========task__4==================")


@app.task
def task__5(*args, **kwargs):
    logger.info("===========task__5==================")
