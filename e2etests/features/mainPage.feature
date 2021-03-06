Feature: Main page
    To establish that our application has a main page
    As a user, I want to have a main page


    Scenario: Verify main Page
        Given I open application and login with user "test@testmail.com" with password "hackpass" and role "user"
        Then the title exists
        And neurons visible
        And credits visible
        And network visible
        And network neurons visible
        And network synapses visible
