from flask import Blueprint, render_template, Flask, request, g
import random
import db
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import json

import sys

from io import StringIO
