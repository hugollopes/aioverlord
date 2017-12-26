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
        And user "test@testmail.com" has "1" neurons and "100" credits
        Then click buy neurons
        Then number of user neurons is "2"
        And credits are less than "100"
        And after "10" seconds credits are more than "20"

    Scenario: no credits for neurons
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And user "test@testmail.com" has "1" neurons and "0" credits
        And I click topology
        Then topology is visible
        And buy neurons is visible
        Then click buy neurons
        And number of user neurons is "1"
        #meaning could not buy them
