Feature: Label Data
    user can label data


    Scenario: click label data
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        #Given I open application
        #And user "test@testmail.com" exists in server with password "hackpass" and role "user"
        And cookies are empty
        Then login dialog is visible
        And I fullfill with user "test@testmail.com" with password "hackpass"
        And I click Sign In
        Then user is visible with "test@testmail.com"
        And Login is not visible
        And I click button label data
        Then I see is triangle
