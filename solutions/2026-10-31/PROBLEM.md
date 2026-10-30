# Problem: smtplib: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid

**Date:** 2026-10-31

**Source:** Stack Overflow

**Category:** devops

**Why Selected:** Trending problem in devops category

## Description

I'm try to send an email in python usign the library smtplib. But I have this error: ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Hostname mismatch, certificate is not valid for 'smtp.mydomain.es'. (_ssl.c:1129) import smtplib, ssl context = ssl.create_default_context() server = smtplib.SMTP('smtp.mydomain.es', 587) server.ehlo() server.starttls(context=context) server.ehlo() server.login('email@mydomain.es', 'mypassword') How can I solve this error?

## Original URL

https://stackoverflow.com/questions/71406592/smtplib-ssl-sslcertverificationerror-ssl-certificate-verify-failed-certific
