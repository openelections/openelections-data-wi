Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for candidate <candidate> running for <office> in the <ward> in <county>
    Then I should see <votes> out of <total>

  Examples: 20100216__wi__primary_ward.csv
    | candidate                       | county     | office                         | ward                              | votes      | total |
    | John M. O'Boyle                 | Pierce     | Pierce County Circuit Court    | VILLAGE OF PLUM CITY                              | 6          | 75    |

  Examples: 20100406__wi__general_ward.csv
    | candidate                       | county     | office                         | ward                              | votes      | total |
    | Linda M. Van De Water           | Calumet    | Court of Appeals               | VILLAGE OF POTTER                            | 8          | 17    |
    | Edward E. Leineweber            | Dane       | Court of Appeals               | TOWN OF MADISON Wards 2 - 11                      | 50         | 238       |

  # Examples: 20100914__wi__primary_ward.csv

  Examples: 20101102__wi__general_ward.csv
    | candidate                       | county     | office                         | ward                           | votes | total |
    | James James & No Candidate      | Kewaunee   | Governor/Lieutenant Governor   | VILLAGE OF LUXEMBURG Wards 1 & 2       | 2     | 934   |
    | Scattering                      | Iron       | Attorney General               | CITY OF MONTREAL Ward 1   | 0     | 157   |
    | Ernest J. Pagels Jr. (Write-In) | Pierce     | United States Senator          | VILLAGE OF ELMWOOD Ward 1   | 9     | 245   |
    | L. D. Rockwell                  | Walworth   | State Senate                   | CITY OF LAKE GENEVA Wards 3-6, 9-11, 13, 14, 16, 17, 19 - 25 | 376   | 1106  |
    | Rich Zipperer                   | Washington | State Senate                   | CITY OF HARTFORD Wards 12 - 15, 17, 19 - 22, 26 - 28, 30, 33 - 35, 40 & 41, 49 | 1251  | 1255  |
    | Ted Zigmunt                     | Brown      | Assembly                       | CITY OF DE PERE Wards 15 - 17            | 53     | 143    |
    | Gary Tauchen                    | Waupaca    | Assembly                       | VILLAGE OF EMBARRASS Ward 1         | 102    | 102    |
    | Richard J. Spanbauer            | Fond Du Lac | Assembly                      | CITY OF FOND DU LAC Ward 39                  | 0      | 0      |
    | Samantha Kerkman                | Kenosha    | Assembly                       | CITY OF KENOSHA Ward 58                  | 1      | 2      |
    | Scott Suder                     | Taylor     | Assembly                       | TOWN OF TAFT Ward 1                        | 46     | 47     |
    | Don Pridemore                   | Dodge      | Assembly                       | CITY OF HARTFORD Ward 16                  | 0      | 0      |

  Examples: 20110405__wi__general_ward.csv
    | candidate             | county    | office                       | ward                           | votes | total |
    | David T. Prosser, Jr. | MANITOWOC | JUSTICE OF THE SUPREME COURT | CITY OF MANITOWOC Wards 17, 18, 22, 24 - 26, 28 - 30, 32, 34 & 36 | 306  | 555  |

  Examples: 20110503__wi__special_general_ward.csv
    | candidate       | county     | office   | ward                           | votes | total |
    | RICK AARON      | OZAUKEE    | ASSEMBLY | TOWN OF GRAFTON WARDS 1 2, & 6 | 69	   | 422   |
    | DUEY STROEBEL   | WASHINGTON | ASSEMBLY | TOWN OF TRENTON WDS-1.2.5.6.7  | 316  | 375   |
    | ANDREW ALLEN BERG (WRITE IN) | RACINE   | ASSEMBLY | VILLAGE OF WATERFORD Wards 1 - 7 | 9   | 900   |

  Examples: 20111011__wi__special_primary_ward.csv
    | candidate       | county     | office   | ward                           | votes | total |
    | David A. Drewes | La Crosse  | ASSEMBLY | TOWN OF CAMPBELL Town of Campbell - Ward 7 | 0 | 0 |

  Examples: 20111108__wi__special_general_ward.csv
    | candidate       | county     | office   | ward                           | votes | total |
    | David A. Drewes | La Crosse  | ASSEMBLY | CITY OF LA CROSSE Ward 15      | 161   | 573   |

  Examples: 20120403__wi__primary_ward.csv
    | candidate               | county    | office                                            | ward                     | votes  | total  |
    | MICHELE BACHMANN        | ADAMS     | President of the United States                    | TOWN OF QUINCY Ward 1    | 4	    | 151    |
    | UNINSTRUCTED DELEGATION | WASHBURN  | President of the United States                    | Town of Gull Lake Ward 1          | 6      | 20     |
    | JOHN C. ALBERT          | DANE      | DANE COUNTY CIRCUIT COURT JUDGE, BRANCH 3         | TOWN OF OREGON WARDS 1-4 | 583    | 584    |
    | THOMAS J. GRITTON       | WINNEBAGO | WINNEBAGO COUNTY CIRCUIT COURT JUDGE, BRANCH 1    | CITY OF OSHKOSH D8 W15   | 359    | 361    |
    | SCATTERING              | WINNEBAGO | COURT OF APPEALS                                  | TOWN OF ALGOMA Wards 1-2, 7-10    | 4      | 791     |
    | ROBERT E. EATON         | ASHLAND   | ASHLAND COUNTY CIRCUIT COURT JUDGE                | VILLAGE OF BUTTERNUT Wards 1 & 2     | 69     | 69      |
    | JAMES JUDGE DUVALL      | PEPIN     | BUFFALO-PEPIN COUNTY CIRCUIT COURT JUDGE          | CITY OF DURAND Wards 1 - 3        | 434    | 434    |   
    | NELSON WESLEY PHILLIPS, III | MILWAUKEE | MILWAUKEE COUNTY CIRCUIT COURT JUDGE, BRANCH 17 | VILLAGE OF BAYSIDE Ward 1s & 3s Congress 6 | 6   | 16   | 
    | NICHOLAS J. BRAZEAU, JR. | WOOD     | WOOD COUNTY CIRCUIT COURT JUDGE, BRANCH 2         | CITY OF WISCONSIN RAPIDS Ward 23  | 67     | 69     |

  Examples: 20120605__wi__general-recall_ward.csv
    | candidate               | county    | office              | ward                                    | votes  | total  |
    | Hari Trivedi            | Adams     | Governor            | Town of Adams Wards 1-3                  | 6      | 525  |
    | Scattering              | Wood      | Governor            | City Of Wisconsin Rapids Wards 16 -23 & 25 | 3    | 2221  |
    | Rebecca Kleefisch       | St. Croix | Lieutenant Governor | CITY OF HUDSON Wards 1 & 2             | 324   | 579       | 
    | Van H. Wanggaard         | Racine    | State Senate        | Village of Mount Pleasant Wards 19,21,22,23 | 1321    | 2523     |
    | Donna Seidel            | Taylor    | State Senate        | CITY OF MEDFORD Wards 1-8     | 588     | 1638    | 


  Examples: 20120814__wi__primary_ward.csv
    | candidate        | county    | office                 | ward                                | votes  | total  |
    | Al Ott           | Outagamie | Assembly               | Village of Combined Locks Wards 1-4 | 263    | 368    |

  Examples: 20121106__wi__general_ward.csv
    | candidate               | county    | office                         | ward                     | votes  | total  |
    | BARACK OBAMA & JOE BIDEN  | CHIPPEWA  | President of the United States | TOWN OF HALLIE Ward 1    | 54	   | 100    |
    | JOSEPH KEXEL            | WALWORTH  | US SENATOR                     | TOWN OF GENEVA Wards 1-8 | 77     | 2525   |
    | SHEILA HARSDORF         | POLK      | STATE SENATE                   | TOWN OF LAKETOWN Ward 1  | 316    | 542    |

  Examples: 20121204__wi__special_general_ward.csv
    | candidate    | county   | office       | ward                         | votes  | total |
    | PAUL FARROW  | Waukesha | STATE SENATE | CITY OF PEWAUKEE WARDS 8-10  | 274	   | 281    |

  Examples: 20130219__wi__special_primary_ward.csv
    | candidate    | county   | office   | ward                         | votes  | total |
    | MATT MORZY   | Waukesha | ASSEMBLY | CITY OF WAUKESHA Ward 4      | 6	     | 70    |
    | ADAM NEYLON	 | Waukesha | ASSEMBLY | CITY OF PEWAUKEE WARDS 5-7   | 219    | 559   |

  Examples: 20130402__wi__general_ward.csv
    | candidate     | county   | office                                     | ward                           | votes  | total |
    | Tony Evers    | Adams    | State Superintendent Of Public Instruction | Town Of Monroe Ward 1          | 53     | 94    |
    | Tony Evers    | Columbia | State Superintendent Of Public Instruction | City Of Wisconsin Dells Ward 1 | 54     | 74    |
    | Don Pridemore | Dane     | State Superintendent Of Public Instruction | City Of Madison Ward 49        | 12     | 82	   |
    | Don Pridemore | Wood     | State Superintendent Of Public Instruction | Town Of Seneca Wards 1 -3      | 55     | 136	   |

  Examples: 20131119__wi__special_primary_ward.csv
    | candidate       | county    | office   | ward                            | votes  | total |
    | Stephanie Mares | Milwaukee | Assembly | Village of Greendale Wards 9-10 | 132    | 231   |

  Examples: 20131217__wi__special_general_ward.csv
    | candidate         | county    | office                            | ward                        | votes | total |
    | John R. Hermes    | Milwaukee | Assembly                          | City of Greenfield Ward 20  | 86    | 223   |


  Examples: 20140812__wi__primary_ward.csv
    | candidate         | county  | office                            | ward                        | votes | total |
    | MARY BURKE        | BROWN   | GOVERNOR                          | TOWN OF HOLLAND Wards 1 - 2 | 41    | 49    |
    | JERRY BROITZMAN   | DANE    | SECRETARY OF STATE                | CITY OF MADISON Ward 38     | 3     | 3     |
    | REBECCA KLEEFISCH | DOUGLAS | LIEUTENANT GOVERNOR               | TOWN OF BRULE Wards 1 & 2   | 9     | 9     |

  Examples: 20141104__wi__general_ward.csv
    | candidate                 | county    | office                       | ward                            | votes  | total |
    | Mary Burke & John Lehman    | Adams     | Governor/Lieutenant Governor | Town Of Adams Wards 1-3         | 233    | 500   |
    | Steve R. Evans (Write-In) | Dane      | Governor/Lieutenant Governor | City Of Verona Wards 1, 5       | 0      | 1037  |
    | Chris Kapenga             | Waukesha  | Assembly                     | Village of Summit Wards 2,3,4,5 | 1227   | 1643  |
    | Peter Flesch              | Vernon    | Assembly                     | City of Westby Wards 1 - 5      | 375    | 837   |
    | Dean P. Debroux           | Outagamie | State Senate                 | City of Appleton Ward 59        | 1      | 1     |
    | Lawrence Dale             | Wood      | Congressional                | City of Pittsville Ward 1       | 7      | 356   |
    | Jerry Shidell             | Ashland   | State Treasurer              | City of Mellen Ward 1           | 3      | 221   |

  Examples: 20150623__wi__special_primary_ward.csv
    | candidate                    | county   | office       | ward                              | votes  | total |
    | Sherryll Shaddock            | Waukesha | State Senate | City of Waukesha Ward 38          | 19     | 19    |

  Examples: 20150901__wi__special_primary_ward.csv
    | candidate          | county   | office   | ward                              | votes  | total |
    | Scattering         | Waukesha | Representative To The Assembly | Village of Oconomowoc Lake Ward 1 | 0      | 28    |
    | Spencer Zimmerman  | Waukesha | Representative To The Assembly | Town of Genesee Wards 1-5, 9 10   | 9      | 278   |

  Examples: 20150929__wi__special_general_ward.csv
    | candidate                    | county   | office   | ward                           | votes  | total |
    | Cindi Duchow                 | Waukesha | Assembly | Village Of Hartland Wards 1-13 | 117    | 140   |
    | Thomas D. Hibbard (Write-In) | Waukesha | Assembly | Village Of Wales Wards 1-4     | 10     | 106   |
    | Scattering                   | Waukesha | Assembly | City of Delafield Wards 1 - 14 | 18     | 217   |
