Feature: Debug functions
    user can access special functions for debugging the application


    Scenario: file upload
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click button file upload
        Then I see choose file button
