# Problem: How to compare yaml files regardless of ordering differences?

**Date:** 2026-09-25

**Source:** Stack Overflow

**Category:** mobile

**Why Selected:** Trending problem in mobile category

## Description

I need to compare yaml files that are generated from two different processes and are ordered differently and detect if they are logically the same ideally in python. yaml file 1: apiVersion: apps/v1 kind: Deployment metadata: name: nginx-deployment labels: app: nginx spec: replicas: 3 selector: matchLabels: app: nginx template: metadata: labels: app: nginx spec: containers: - name: nginx image: nginx:1.14.2 ports: - containerPort: 80 yaml file 2: apiVersion: apps/v1 kind: Deployment metadata: la

## Original URL

https://stackoverflow.com/questions/68488797/how-to-compare-yaml-files-regardless-of-ordering-differences
