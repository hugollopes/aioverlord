Feature: Debug functions
    user can access special functions for debugging the application


    Scenario: file upload
        Given I open application
        And I click button file upload
        Then I see choose file button
        And End
