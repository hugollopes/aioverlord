Feature: User related functionality
    user can login
    user gets informed of his information and see his credits grow

    Scenario: login with no cookies and credits grow
        Given I open application
        And user "test@testmail.com" exists in server with password "hackpass"
        And cookies are empty
        Then login dialog is visible
        And I fullfill with user "test@testmail.com" with password "hackpass"
        And I click Sign In
        Then user is visible with "test@testmail.com"
        Then I see credits grow

    Scenario: login with cookies
        Given I open application
        Given user cookies are "test@testmail.com" and with password "hackpass"
        # need to reopend the application to make cookies visible.
        Given I open application
        And user "test@testmail.com" exists in server with password "hackpass"
        Then login dialog is visible
        And I click Sign In
        Then user is visible with "test@testmail.com"
