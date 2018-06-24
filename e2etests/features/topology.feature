Feature: Topology
    enable buying of neurons and neural network topologies


    Scenario: select topology and check things are visible
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click topology
        Then topology is visible
        And buy neurons is visible
        And network button is visible
        Then I click network button
        Then network visible

    Scenario: buy neuron
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And I click topology
        Then topology is visible
        And buy neurons is visible
        And user "test@testmail.com" has "1" neurons and "101" credits
        And buy neurons is enabled
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
        And buy neurons is disabled
        Then click buy neurons
        And number of user neurons is "1"

    Scenario: buy topology
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And user "test@testmail.com" has "1" neurons and "100" credits
        And I click topology
        Then topology is visible
        And buy "2 hidden layers" topology is visible
        And click buy topology "2 hidden layers"
        Then then topology "2 hidden layers" belongs to user

    Scenario: no cash for topology
        Given I open aplication and login with user "test@testmail.com" with password "hackpass" and role "user"
        And user "test@testmail.com" has "1" neurons and "90" credits
        And I click topology
        Then topology is visible
        And buy "3 hidden layers" topology is disabled
        Then user "test@testmail.com" has "1" neurons and "100" credits
        Then buy "3 hidden layers" topology is enabled
