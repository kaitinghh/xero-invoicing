# -*- coding: utf-8 -*-
import os
from functools import wraps
from io import BytesIO
from logging.config import dictConfig
from flask import Flask, session
from flask_oauthlib.contrib.client import OAuth, OAuth2Application
from flask_session import Session
from xero_python.accounting import AccountingApi
from xero_python.assets import AssetApi
from xero_python.project import ProjectApi
from xero_python.payrollau import PayrollAuApi
from xero_python.payrolluk import PayrollUkApi
from xero_python.payrollnz import PayrollNzApi
from xero_python.file import FilesApi
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from xero_python.exceptions import AccountingBadRequestException, PayrollUkBadRequestException
from xero_python.identity import IdentityApi
from xero_python.utils import getvalue
# import logging_settings
from utils import jsonify, serialize_model

# dictConfig(logging_settings.default_settings)

# configure main flask application
app = Flask(__name__)
app.config.from_object("default_settings")
app.config.from_pyfile("config.py", silent=True)

if app.config["ENV"] != "production":
    # allow oauth2 loop to run over http (used for local testing only)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# configure persistent session cache
Session(app)

# configure flask-oauthlib application
oauth = OAuth(app)
xero = oauth.remote_app(
    name="xero",
    version="2",
    client_id=app.config["CLIENT_ID"],
    client_secret=app.config["CLIENT_SECRET"],
    endpoint_url="https://api.xero.com/",
    authorization_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope="offline_access openid profile email accounting.transactions "
    "accounting.transactions.read accounting.reports.read "
    "accounting.journals.read accounting.settings accounting.settings.read "
    "accounting.contacts accounting.contacts.read accounting.attachments "
    "accounting.attachments.read assets projects "
    "files "
    "payroll.employees payroll.payruns payroll.payslip payroll.timesheets payroll.settings",
)  # type: OAuth2Application


# configure xero-python sdk client
api_client = ApiClient(
    Configuration(
        debug=app.config["DEBUG"],
        oauth2_token=OAuth2Token(
            client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"]
        ),
    ),
    pool_threads=1,
)

# configure token persistence and exchange point between flask-oauthlib and xero-python
@xero.tokengetter
@api_client.oauth2_token_getter
def obtain_xero_oauth2_token():
    return session.get("token")

@xero.tokensaver
@api_client.oauth2_token_saver
def store_xero_oauth2_token(token):
    session["token"] = token
    session.modified = True

# configure api_client for use with xero-python sdk client
api_client = ApiClient(
    Configuration(
        debug=false,
        oauth2_token=OAuth2Token(
            client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET"
        ),
    ),
    pool_threads=1,
)

api_client.set_oauth2_token("YOUR_ACCESS_TOKEN")

def accounting_create_invoices():
    api_instance = AccountingApi(api_client)
    xero_tenant_id = 'YOUR_XERO_TENANT_ID'
    summarize_errors = 'True'
    date_value = dateutil.parser.parse('2020-10-10T00:00:00Z')
    due_date_value = dateutil.parser.parse('2020-10-28T00:00:00Z')

    contact = Contact(
        contact_id = "00000000-0000-0000-0000-000000000000")

    line_item_tracking = LineItemTracking(
        tracking_category_id = "00000000-0000-0000-0000-000000000000",
        tracking_option_id = "00000000-0000-0000-0000-000000000000")
    
    line_item_trackings = []    
    line_item_trackings.append(line_item_tracking)

    line_item = LineItem(
        description = "Foobar",
        quantity = 1.0,
        unit_amount = 20.0,
        account_code = "000",
        tracking = lineItemTrackings)
    
    line_items = []    
    line_items.append(line_item)

    invoice = Invoice(
        type = "ACCREC",
        contact = contact,
        date = date_value,
        due_date = due_date_value,
        line_items = line_items,
        reference = "Website Design",
        status = "DRAFT")

    invoices = Invoices( 
        invoices = [invoice])
    
    try:
        api_response = api_instance.create_invoices(xero_tenant_id, invoices, summarize_errors, unitdp)
        print(api_response)
    except AccountingBadRequestException as e:
        print("Exception when calling AccountingApi->createInvoices: %s\n" % e)