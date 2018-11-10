Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for <party> party candidate <candidate> running for <office> <district> in the <ward> in <county>
    Then I should see <votes> out of <total>

  Examples: 20001107__wi__general__ward.csv
    | party | candidate                     | county    | office                                    | district  | ward                                          | votes | total |
    | REP   | Kitty Rhoades                 | Pierce    | State Assembly                            | 34        | City of Prescott Wards 1 - 4                  | 1036  | 1759  |
    | LIB   | Tim Peterson                  | Racine    | Senate                                    | 88        | Town of Mount Pleasant Wards 7 & 8            | 8     | 1851  |

  Examples: 20001107__wi__general__ward.csv
    | candidate                             | county    | office                                    | district  | ward                                          | votes | total |
    | Scattering                            | Lincoln   | President                                 |           | Town of Bradley Wards 1 - 6                   | 4     | 1457  |

  Examples: 20020910__wi__primary__ward.csv
    | party | candidate                     | county    | office                                    | district  | ward                                          | votes | total |
    | DEM   | Dale Moore                    | Racine    | House                                     | 22        | CITY OF RACINE Ward 30                        | 38    | 151   |
    | REP   | Peggy A. Rosenzweig           | Milwaukee | State Senate                              | 11        | CITY OF MILWAUKEE Ward 286                    | 19    | 58    |

  Examples: 20171219__wi__special__primary__ward.csv
    | party | candidate                     | county    | office                                    | district  | ward                                          | votes | total |
    | WGR   | Scattering                    | St. Croix | State Senate                              | 1         | City of HUDSON Ward 11-12                     | 1     | 1     |
    | DEM   | John Rocco Calabrese          | Dunn      | State Senate                              | 9         | Village of BOYCEVILLE Ward 1                  | 8     | 19    |

  Examples: 20180220__wi__primary__ward.csv
    | candidate                             | county    | office                                    | district  | ward                                          | votes | total |
    | Rebecca Dallet                        | Taylor    | Supreme Court                             |           | Town of MCKINLEY Ward 1                       | 1     | 27    |
    | Brenda L. Yaskal                      | Columbia  | Columbia County Circuit Court, Branch 3   |           | City of PORTAGE Ward 11                       | 0     | 0     |
    | Ralph Sczygelski                      | Manitowoc | Manitowoc County Circuit Court, Branch 2  |           | City of MANITOWOC Wards 17-18,21,23-26,28     | 68    | 245   |

  Examples: 20180403__wi__general__ward.csv
    | candidate                             | county    | office                                    | district  | ward                                          | votes | total |
    | Rebecca Dallet                        | Kewaunee  | Supreme Court                             |           | City of ALGOMA Ward 1-6                       | 279   | 432   |
    | Timothy G. Dugan                      | Milwaukee | Court of Appeals                          | 7         | Village of HALES CORNERS Wards 7-9            | 338   | 338   |
    | Sandra Cardo Gorsuch                  | Sauk      | Sauk County Circuit Court, Branch 3       |           | Town of FREEDOM Ward 2                        | 41    | 65    |

