# Rental Property Analysis Calculator

Automatically analyze thousands of properties at once to find possible profitable listings.

## Purposes

I created this tool so that I could more easily sift through possible investment properties without manually entering listing data from websites like Zillow, Redfin, or Trulia. I don't have time for that!

## How it works

Users have the option to run an analysis in one of two ways:

1. Manually with the rental calculator form
2. Let the bot do it! (after initial settings setup)

### The analysis

Each analysis will provide the income, expenses, monthly cashflow, cap rate, cash on cash ROI, net operating income, total cash needed to get into the deal, and many other numbers in order to give the user an idea of whether the property is a good investment for them... or not.

Interactive [plotly](https://plotly.com) visualizations:

1. Pie chart breaking down income and expenses
2. Table containing analysis over loan term
3. Line graph tracking income, expenses and cashflow over time
4. Line graph tracking loan balance, property value and equity over time

Each analysis, regardless of how it was created, is editable and also downloadable as a PDF.

### The bot

To use the bot, users only have to enter some basic info into their account settings and the bot is on its way to providing the user as many analyses as their search criteria can find.

Simply give the bot a search area (follow the instructions in the help sections) and enter numbers in the "Investment Quality Settings" (optional)

The bot uses your search criteria to:

1. Create a search url for Redfin.com listings
2. Download the csv file of data for those listings
3. Parse the csv data and retrieve specific listing urls
4. Scrape data from the listing such as property image, listing price, annual property taxes, bedrooms, bathrooms, description, etc.
5. Search Zillow Rental Manager for a rental Zestimate for each property
6. Run analysis for each property based on gathered data

## Other features

### Calculator settings

Users have the option of adding info to "Calculator Settings" which will pre-fill the rental calculator form with those same criteria for faster input. Those settings are also used by the bot for analysis.

### Investment quality settings

I highly recommend using these. They will give you a :thumbsup:, :shrug:, or :thumbsdown: as a quick way to tell you if a certain property will be profitable for you given the parameters set in the "Investment Quality Settings"

### Blacklist settings

These settings provide users the ability to blacklist an address when an analysis is deleted. This will prevent the bot from running analyses on properties listed in the blacklisted addresses so as to prevent the user from having to delete an undesired analysis every time the bot is run for a search area.

## Demo

#### Calculator Overview

![calculator](https://github.com/gmlesher/rental-property-calculator/blob/readme/calculator.gif?raw=true)

#### Property Analysis

![analysis](https://github.com/gmlesher/rental-property-calculator/blob/readme/analysis.gif?raw=true)

#### PDF Download

![pdf](https://github.com/gmlesher/rental-property-calculator/blob/readme/pdf.gif?raw=true)

#### Settings Overview

![settings](https://github.com/gmlesher/rental-property-calculator/blob/readme/settings.gif?raw=true)
