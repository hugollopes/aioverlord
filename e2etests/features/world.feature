Feature: Topology
    enable setting up agents in the world


    Scenario: select topology and check things are visible
        Given I open application and login with user "test@testmail.com" with password "hackpass" and role "user"
        When user accesses world
        And user buys agents
        And user assigns agents
        Then then user starts to make credits.
