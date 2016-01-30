Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for candidate <candidate> running for <office> in the <ward>
    Then I should see <votes> out of <total>

  Examples: 20150929__wi__general_ward.csv
    | candidate                    | office   | ward                           | votes  | total |
    | Cindi Duchow                 | Assembly | Village Of Hartland Wards 1-13 | 117    | 140   |
    | Thomas D. Hibbard (Write-In) | Assembly | Village Of Wales Wards 1-4     | 10     | 106   |

  Examples: 20130402__wi__general_ward.csv
    | candidate     | office                                     | ward                           | votes  | total |
    | Tony Evers    | State Superintendent Of Public Instruction | Town Of Monroe Ward 1          | 53     | 94    |
    | Tony Evers    | State Superintendent Of Public Instruction | City Of Wisconsin Dells Ward 1 | 54     | 74    |
    | Don Pridemore | State Superintendent Of Public Instruction | City Of Madison Ward 49        | 12     | 82	   |
    | Don Pridemore | State Superintendent Of Public Instruction | Town Of Seneca Wards 1 -3      | 55     | 136	   |

#  Examples: 20141104__wi__general_ward.csv
#    | candidate                 | county | office                       | ward                      | votes  | total |
#    | Mary Burke John Lehman    | Adams  | Governor/Lieutenant Governor | Town Of Adams Wards 1-3   | 253    | 500   |
#    | Steve R. Evans (Write-In) |        | Governor/Lieutenant Governor | City Of Verona Wards 1, 5 | 0      | 1037  |
