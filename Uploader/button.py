#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @Tellybots

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import shutil
import time
from datetime import datetime
from pyrogram import enums 
from Uploader.config import Config
from Uploader.script import Translation
from Uploader.thumbnail import *
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram.types import InputMediaPhoto
from Uploader.functions.display_progress import progress_for_pyrogram, humanbytes
from Uploader.database.database import db
from PIL import Image
from Uploader.functions.ran_text import random_char

