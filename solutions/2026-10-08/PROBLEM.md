# Problem: Laravel, How to ignore (except) some fields when update model using json and laravel

**Date:** 2026-10-08

**Source:** Stack Overflow

**Category:** ai_ml

**Why Selected:** Trending problem in ai_ml category

## Description

The function below is to update user information, I need to validate if email is not duplicated, also to ignore password if its field left empty, I don't why this function not working! public function update(Request $request, $id) { $this->validate($request->all(), [ 'fname' => 'required', 'email' => 'required|email|unique:users,email,'.$id, 'password' => 'same:confirm-password', 'roles' => 'required' ]); $input = $request->all()->except(['country_id', 'region_id']); if(!empty($input['password']

## Original URL

https://stackoverflow.com/questions/59696881/laravel-how-to-ignore-except-some-fields-when-update-model-using-json-and-lar
