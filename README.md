# Vogue Estates Luxury Real-Estate Backend

Welcome to the Vogue Estates Luxury Real-Estate Backend project! This backend serves as the foundation for a luxury real-estate website where agents affiliated with Vogue Estates can create profiles using their real-estate credentials which allows them to add and remove any listings, and users can register to access exclusive luxury listings from Vogue Estates.

## Getting Started

Account Creation: Begin your journey by creating a personalized account on Vogue Estates. This straightforward and secure process ensures that you have a unique space to explore our exclusive luxury listings.

Browse Listings: Once you've successfully logged in, you'll gain access to our extensive collection of luxury properties. Browse through our listings to discover the epitome of elegance and sophistication.

Contact Agents: Should you find a property that captivates your interest, utilize the provided contact forms to reach out to our dedicated agents. They're here to assist you in turning your real estate dreams into reality.

Agent Tools: As a Vogue Estates agent, you have access to powerful tools for managing listings. Add exclusive properties to our collection and remove listings as needed to ensure our users have access to the finest luxury real estate offerings.



## Project Overview

This project enables agents and users to register and log in to their accounts on Vogue Estates. Agents can manage their listings, and users can view exclusive luxury listings available through Vogue Estates. Below are the main functionalities and features of the backend:

- **User and Agent Registration**: Users and agents can register on the platform using their credentials.
- **User and Agent Login**: Registered users and agents can log in to their accounts.
- **Listing Management**: Agents can add and remove listings on their profile.
- **Agent Details**: Users can access details of all agents on the team page


## Routes

Below are the main API routes available in this backend:

- **GET /**: Route that loads the main page.
- **POST /users/register/**: Sign up route for users and agents.
- **POST /agents/register/**: Sign up route for agents.
- **POST /users/login/**: Route for user login.
- **POST /agent/login/**: Route for agent login.
- **GET/PUT/DELETE /agents/**: Route for fetching user profile and performing CRUD operations.
- **GET/PUT/DELETE /agentdetails/<int:id>/**: Route for accessing and managing agent details and listings.
- **GET/PUT/DELETE /agentlistingdetails/<int:id>/**: Route for accessing and managing details of a particular listing.

## MVP (Minimum Viable Product)

The MVP includes the following functionalities:

- Users and agents should be able to create an account on Vogue Estates with salted passwords.
- Users and agents should be able to log in to their accounts on Vogue Estates.
- Agents should be able to add and remove listings on their profile with their credentials.

## Contribution

Lesley R.	https://github.com/GlitterAngle (Back-end)
Aldiana H.	https://github.com/aldianahot14 (Back-end)

## Back-end

django
Python
heroku

## Next-Step
Implement a share feature so Clients can share current listings
As a user I would like to view specific agents current listings 
Implement google maps


