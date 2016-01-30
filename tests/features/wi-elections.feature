Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for candidate <candidate> running for <office> in the <ward>
    Then I should see <votes> out of <total>

  Examples: 20150929__wi__general_ward.csv
    | candidate                    | office   | ward                           | votes  | total |
    | Cindi Duchow                 | Assembly | Village Of Hartland Wards 1-13 | 117    | 140   |
    | Thomas D. Hibbard (Write-In) | Assembly | Village Of Wales Wards 1-4     | 10     | 106   |
