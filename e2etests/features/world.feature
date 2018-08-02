Feature: Topology
    enable setting up agents in the world


    Scenario: select topology and check things are visible
        Given I open application and login with user "test@testmail.com" with password "hackpass" and role "user"
        And user "test@testmail.com" has "1" neurons and "101" credits
        When user accesses world
        And user buys agent
        And user assigns agent
#        Then then user starts to make credits.
