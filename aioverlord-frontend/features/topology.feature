Feature: Topology
    enable buying of neurons and neural network topologies


    Scenario: select topology and check things are visible
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click topology
        Then topology is visible
