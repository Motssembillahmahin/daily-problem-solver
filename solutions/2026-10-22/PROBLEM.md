# Problem: TypeError: _MailMixin.connect() missing 1 required positional argument: 'self'

**Date:** 2026-10-22

**Source:** Stack Overflow

**Category:** webdev

**Why Selected:** Trending problem in webdev category

## Description

I'm trying to setup email notifications within my Flask app and I am running to the following error when trying trigger the function. TypeError: _MailMixin.connect() missing 1 required positional argument: 'self' main.py: from website import create_app from flask_mail import Mail app = create_app() app.config['MAIL_SERVER'] = 'smtp.gmail.com' app.config['MAIL_PORT'] = 465 app.config['MAIL_USERNAME'] = 'email removed for privacy' app.config['MAIL_PASSWORD'] = '******' app.config['MAIL_USE_TLSmai'

## Original URL

https://stackoverflow.com/questions/80011058/typeerror-mailmixin-connect-missing-1-required-positional-argument-self
