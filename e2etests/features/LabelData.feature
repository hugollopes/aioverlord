Feature: Label Data
    user can label data


    Scenario: click label data
        Given I open application and login with user "test@testmail.com" with password "hackpass" and role "user"
        And Picture "neural.jpg" exists in the database and a classification exists
        And I click button label data
        Then I see is triangle
