# Problem: Why isn't the Flask-Login current_user.is_authenticated consistent?

**Date:** 2026-11-25

**Source:** Stack Overflow

**Category:** webdev

**Why Selected:** Trending problem in webdev category

## Description

I have an Angular app that is making API calls to the backend Flask app. The Flask app is using Flask-Login to authenticate users when they login. When the user logs in with the login() function I defined, current_user.is_authenticated returns True . When I call another function called get_is_logged_in() , current_user.is_authenticated returns False . My User class inherits from UserMixin , so it has all of the required properties and methods as explained in the documentation ( https://flask-log

## Original URL

https://stackoverflow.com/questions/54431408/why-isnt-the-flask-login-current-user-is-authenticated-consistent
