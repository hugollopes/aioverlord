Feature: Topology
    enable buying of neurons and neural network topologies


    Scenario: select topology and check things are visible
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click topology
        Then topology is visible
        And buy neurons is visible

    Scenario: buy neuron
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click topology
        Then topology is visible
        And buy neurons is visible
        And number of user neurons is "1"
        And number of user credits is "10"
        Then click buy neurons
        Then number of user neurons is "2"
        And credits are less than "10"
        And after "10" seconds credits are more than "20"

    Scenario: no credits for neurons
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And User has "0" credits and "1" neurons
        And I click topology
        Then topology is visible
        And buy neurons is visible
        And number of user neurons is "1"
        Then click buy neurons is disabled
