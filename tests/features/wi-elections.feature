Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for candidate <candidate> running for <office> in the <ward>
    Then I should see <votes> out of <total>

  Examples: 20150929__wi__general_ward.csv
    | candidate  | office    | ward                      | votes | total |
    | CINDI DUCHOW | ASSEMBLY | VILLAGE OF HARTLAND WARDS 1-13 | 117    |  140   |
    |THOMAS D. HIBBARD (WRITE-IN)| ASSEMBLY | VILLAGE OF WALES WARDS 1-4 | 10 | 106 |
