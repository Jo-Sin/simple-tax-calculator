# simple-tax-calculator

A simple tax calculator based on the info provided on the ATO website. It assumes you were a full year resident for the purpose of calculation and it doesn't consider other factors like Medicare levy.

## Run project

```
docker-compose build
docker-compose up
```

## Backend

It's a Flask server that scrapes [the ATO resident tax rates page](https://www.ato.gov.au/tax-rates-and-codes/tax-rates-australian-residents).

## Frontend

An Angular app that loads the data from Flask backend and displays a short form to help user calculate their tax.