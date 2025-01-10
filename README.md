# MJ Rookie Card Tracker Project
My Project utilizes the Ebay Developer API to track and monitor the prices of the Michael Jordan 1986-87 Fleer Rookie Card, utilizing Tableau to create a real-time dashboard of listings data.

# The Inspiration
This project was inspired by my dad, who's prized possessions include multiple ungraded versions of the famous Michael Jordan card that he obtained while he was a kid. Although he vows to hold on to the cards and not sell them, my project can serve useful for my dad in montioring the current state of the market if he would choose to sell it.

# The Card
The 1986-87 Michael Jordan Rookie Card is one of the most notable and coveted basketball trading cards. Although the year 1986-87 is not MJ's rookie year, it is part of the first set of released Fleer cards, and the image is from his rookie season. The image, with MJ going up for a dunk with his signature tongue sticking out, is one of the most iconic player images in NBA trading card history.

# The Data
Starting on **12/28/24**, I have scraped the Ebay Marketplace daily (using Cron scheduler) to track the listings of the MJ Rookie card. 

Data collected on listings includes:
- Listing Title/ID
- Listing Condition (PSA Rating 1-10)
- Listing Price
- Listing Start Date
- Current Date
- Listing Location

# The Dashboard
https://public.tableau.com/app/profile/noah.eisenberg/viz/EbayWorkbook/Dashboard1

Used Tableau to create an interactive dashboard that includes various visualizations depciting the current and evolving state of the card's Ebay market. 






