Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for <party> party candidate <candidate> running for <office> in the <ward> in <county>
    Then I should see <votes> out of <total>

  Examples: 20020910__wi__primary_ward.csv
    | party | candidate                         | county    | office                            | ward                                              | votes | total |
    | DEM   | Dale Moore                        | Racine    | House                             | CITY OF RACINE Ward 30                            | 38    | 151   |
    | REP   | Peggy A. Rosenzweig               | Milwaukee | State Senate                      | CITY OF MILWAUKEE Ward 286                        | 19    | 58    |

  Examples: 20041102__wi__general_ward.csv
    | party | candidate                         | county    | office                            | ward                                              | votes | total |
    | IND   | Peter Miguel Camejo & Ralph Nader | Brown     | President                         | VILLAGE OF HOWARD Wards 1 - 8                     | 27    | 3767  |
    | DEM   | Russ Feingold                     | Outagamie | Senate                            | CITY OF APPLETON Ward 22                          | 725   | 1319  |
    | REP   | Tim Michels                       | Oconto    | Senate                            | TOWN OF BRAZEAU Wards 1 - 3                       | 411   | 793   |

  Examples: 20050405__wi__general_ward.csv
    | party | candidate                         | county    | office                            | ward                                              | votes | total |
    | NP    | Paul B. Higginbotham              | Wood      | Court of Appeals                  | TOWN OF SENECA Wards 1 - 3                        | 90    | 90    |

  Examples: 20060110__wi__special_general_ward.csv
    | party | candidate                         | county    | office                            | ward                                              | votes | total |
    | REP   | Scott Newcomer                    | Waukesha  | State Assembly                    | VILLAGE OF NASHOTAH Wards 1 & 2                   | 75    | 106   |


  Examples: 20080219__wi__primary_ward.csv
    | candidate                                 | county     | office                           | ward                                              | votes | total |
    | Ken Sortedahl                             | St. Croix  | St Croix County Circuit Court    | VILLAGE OF DEER PARK                              | 3     | 50    |

  Examples: 20080401__wi__general_ward.csv
    | candidate                                 | county     | office                           | ward                                              | votes | total |
    | James D. Babbitt                          | Barron     | Barron County Circuit Court      | TOWN OF DALLAS Wards 1 & 2                        | 57    | 68    |
    | Burneatta L. Bridge                       | Grant      | Court Of Appeals                 | TOWN OF CASTLE ROCK                               | 48    | 48    |
    | Louis Butler                              | Forest     | Supreme Court                    | TOWN OF POPPLE RIVER                              | 3     | 18    |

  Examples: 20080909__wi__primary_ward.csv
    | party | candidate                         | county     | office                           | ward                                              | votes | total |
    | LIB   | Scattering                        | Ozaukee    | State Senate                     | CITY OF MEQUON Wards 16, 17 & 19                  | 1     | 1     |
    | LIB   | Scattering                        | Marquette  | State Senate                     | TOWN OF BUFFALO Wards 1 & 2                       | 1     | 1     |
    | WGR   | Scattering                        | Dane       | State Senate                     | CITY OF MADISON Ward 7                            | 2     | 2     |
    | WGR   | Scattering                        | Winnebago  | House                            | CITY OF OSHKOSH Ward 33                           | 6     | 6     |

  Examples: 20080909__wi__primary_ward.csv
    | candidate                                 | county     | office                           | ward                                              | votes | total |
    | Tara Johnson                              | LaCrosse   | State Senate                     | TOWN OF SHELBY Wards 1, 4 - 6                     | 38    | 38    |
    | Clyde Winter                              | Ozaukee    | State Senate                     | CITY OF MEQUON Ward 2                             | 1     | 1     |
    | Mark Wollum                               | Dodge      | House                            | CITY OF WAUPUN Wards 1 - 3 & 8                    | 9     | 28    |
    | Joseph Kexel                              | Kenosha    | House                            | TOWN OF SALEM Wards 1, 7, 11 - 15                 | 8     | 8     |
    | Kevin Barrett                             | Crawford   | House                            | TOWN OF UTICA                                     | 3     | 3     |
    | Chad Fradette                             | Brown      | State Senate                     | CITY OF GREEN BAY Ward 7                          | 44    | 45    |
    | Paul Stark                                | Buffalo    | House                            | TOWN OF MAXVILLE                                  | 19    | 19    |
    | Christopher Baeb                          | Door       | State Assembly                   | TOWN OF SEVASTOPOL Wards 1 - 3                    | 39    | 197   |
    | Garey Bies                                | Brown      | State Assembly                   | TOWN OF SCOTT Wards 1 - 4                         | 47    | 47    |
    | Al Ott                                    | Calumet    | State Assembly                   | CITY OF APPLETON Ward 44                          | 20    | 20    |
    | Don Pridemore                             | Washington | State Assembly                   | VILLAGE OF SLINGER Ward 9                         | 11    | 11    |

  Examples: 20081104__wi__general_ward.csv
    | candidate                                 | county     | office                           | ward                                              | votes | total |
    | Mark D. Thibodeau                         | Adams      | Adams County District Attorney   | TOWN OF DELL PRAIRIE Wards 1 & 2                  | 514   | 517   |
    | Robert D. Zapf                            | Kenosha    | Kenosha County District Attorney | VILLAGE OF PLEASANT PRAIRIE Wards 8 - 11          | 2088  | 2122  |
    | Darrell L. Castle Chuck Baldwin           | Marathon   | President                        | VILLAGE OF Kronenwetter Wards 5 - 8               | 7     | 1758  |
    | Dick Skare                                | Door       | State Assembly                   | TOWN OF BAILEYS HARBOR Wards 1 & 2                | 473   | 776   |
    | Chad Fradette                             | Shawano    | State Senate                     | VILLAGE OF PULASKI Wards 4 & 7                    | 35    | 68    |
    | Peter Theron                              | Columbia   | House                            | VILLAGE OF POYNETTE Wards 1 - 3                   | 415   | 1222  |


  Examples: 20090217__wi__primary_ward.csv
    | candidate                       | county     | office                                     | ward                                              | votes | total |
    | Julie Genovese                  | Dane       | Dane County Circuit Court                  | VILLAGE OF ROCKDALE                               | 4     | 14    |
    | Peter C. Rotter                 | Marathon   | Marathon County Circuit Court              | VILLAGE OF BROKAW                                 | 1     | 18    |
    | Lowell E. Holtz                 | Adams      | State Superintendent Of Public Instruction | TOWN OF STRONGS PRAIRIE Wards 1 & 2               | 3     | 35    |

  Examples: 20090407__wi__general_ward.csv
    | candidate                       | county     | office                                     | ward                                              | votes | total |
    | Kitty K. Brennan                | Milwaukee  | Court of Appeals                           | VILLAGE OF HALES CORNERS Wards 7 - 9              | 235   | 236   |
    | Michael W. Hoover               | St. Croix  | Court of Appeals                           | VILLAGE OF SPRING VALLEY Ward 3                   | 1     | 1     |
    | Tony Evers                      | Kenosha    | State Superintendent Of Public Instruction | VILLAGE OF PADDOCK LAKE Wards 1 - 5               | 239   | 419   |
    | Randy R. Koschnick              | Adams      | Supreme Court                              | CITY OF WISCONSIN DELLS Ward 5                    | 1     | 1     |
    | Gene D. Linehan                 | Bayfield   | Bayfield County Circuit Court              | TOWN OF OULU                                      | 23    | 80    |
    | David A. Hansher                | Milwaukee  | Milwaukee County Circuit Court             | CITY OF MILWAUKEE Ward 208                        | 7     | 7     |
    | Scattering                      | Taylor     | Taylor County Circuit Court                | CITY OF MEDFORD Wards 1 & 2                       | 1     | 321   |


  Examples: 20100216__wi__primary_ward.csv
    | candidate                       | county     | office                         | ward                                                          | votes | total |
    | John M. O'Boyle                 | Pierce     | Pierce County Circuit Court    | VILLAGE OF PLUM CITY                                          | 6     | 75    |

  Examples: 20100406__wi__general_ward.csv
    | candidate                       | county     | office                         | ward                                                          | votes | total |
    | Linda M. Van De Water           | Calumet    | Court of Appeals               | VILLAGE OF POTTER                                             | 8     | 17    |
    | Edward E. Leineweber            | Dane       | Court of Appeals               | TOWN OF MADISON Wards 2 - 11                                  | 50    | 238   |

  # Examples: 20100914__wi__primary_ward.csv

  Examples: 20101102__wi__general_ward.csv
    | candidate                       | county      | office                        | ward                                                          | votes | total |
    | James James & No Candidate      | Kewaunee    | Governor                      | VILLAGE OF LUXEMBURG Wards 1 & 2                              | 2     | 934   |
    | Scattering                      | Iron        | Attorney General              | CITY OF MONTREAL Ward 1                                       | 0     | 157   |
    | Ernest J. Pagels Jr. (Write-In) | Pierce      | Senate                        | VILLAGE OF ELMWOOD Ward 1                                     | 9     | 245   |
    | L. D. Rockwell                  | Walworth    | State Senate                  | CITY OF LAKE GENEVA Wards 3-6, 9-11, 13, 14, 16, 17, 19 - 25  | 376   | 1106  |
    | Rich Zipperer                   | Washington  | State Senate | CITY OF HARTFORD Wards 12 - 15, 17, 19 - 22, 26 - 28, 30, 33 - 35, 40 & 41, 49 | 1251  | 1255  |
    | Ted Zigmunt                     | Brown       | State Assembly                | CITY OF DE PERE Wards 15 - 17                                 | 53    | 143   |
    | Gary Tauchen                    | Waupaca     | State Assembly                | VILLAGE OF EMBARRASS Ward 1                                   | 102   | 102   |
    | Richard J. Spanbauer            | Fond Du Lac | State Assembly                | CITY OF FOND DU LAC Ward 39                                   | 0     | 0     |
    | Samantha Kerkman                | Kenosha     | State Assembly                | CITY OF KENOSHA Ward 58                                       | 1     | 2     |
    | Scott Suder                     | Taylor      | State Assembly                | TOWN OF TAFT Ward 1                                           | 46    | 47    |
    | Don Pridemore                   | Dodge       | State Assembly                | CITY OF HARTFORD Ward 16                                      | 0     | 0     |


  Examples: 20110405__wi__general_ward.csv
    | candidate                     | county    | office                       | ward                                                               | votes | total |
    | David T. Prosser, Jr.         | MANITOWOC | SUPREME COURT | CITY OF MANITOWOC Wards 17, 18, 22, 24 - 26, 28 - 30, 32, 34 & 36  | 306   | 555   |

  Examples: 20110503__wi__special_general_ward.csv
    | candidate                     | county        | office                        | ward                                                          | votes | total |
    | RICK AARON                    | OZAUKEE       | State Assembly                | TOWN OF GRAFTON WARDS 1 2, & 6                                | 69    | 422   |
    | DUEY STROEBEL                 | WASHINGTON    | State Assembly                | TOWN OF TRENTON WDS-1.2.5.6.7                                 | 316   | 375   |
    | ANDREW ALLEN BERG (WRITE IN)  | RACINE        | State Assembly                | VILLAGE OF WATERFORD Wards 1 - 7                              | 9     | 900   |

  Examples: 20111011__wi__special_primary_ward.csv
    | candidate                     | county        | office                        | ward                                                          | votes | total |
    | David A. Drewes               | La Crosse     | State Assembly                | TOWN OF CAMPBELL Town of Campbell - Ward 7                    | 0     | 0     |

  Examples: 20111108__wi__special_general_ward.csv
    | candidate                     | county        | office                        | ward                                                          | votes | total |
    | David A. Drewes               | La Crosse     | State Assembly                | CITY OF LA CROSSE Ward 15                                     | 161   | 573   |


  Examples: 20120403__wi__primary_ward.csv
    | party | candidate                 | county    | office                                            | ward                                      | votes | total |
    | REP   | MICHELE BACHMANN          | ADAMS     | President                                         | TOWN OF QUINCY Ward 1                     | 4     | 151   |
    | DEM   | UNINSTRUCTED DELEGATION   | WASHBURN  | President                                         | Town of Gull Lake Ward 1                  | 6     | 20    |

  Examples: 20120403__wi__primary_ward.csv
    | candidate                         | county    | office                                            | ward                                      | votes | total |
    | JOHN C. ALBERT                    | DANE      | DANE COUNTY CIRCUIT COURT JUDGE, BRANCH 3         | TOWN OF OREGON WARDS 1-4                  | 583   | 584   |
    | THOMAS J. GRITTON                 | WINNEBAGO | WINNEBAGO COUNTY CIRCUIT COURT JUDGE, BRANCH 1    | CITY OF OSHKOSH D8 W15                    | 359   | 361   |
    | SCATTERING                        | WINNEBAGO | COURT OF APPEALS                                  | TOWN OF ALGOMA Wards 1-2, 7-10            | 4     | 791   |
    | ROBERT E. EATON                   | ASHLAND   | ASHLAND COUNTY CIRCUIT COURT JUDGE                | VILLAGE OF BUTTERNUT Wards 1 & 2          | 69    | 69    |
    | JAMES JUDGE DUVALL                | PEPIN     | BUFFALO-PEPIN COUNTY CIRCUIT COURT JUDGE          | CITY OF DURAND Wards 1 - 3                | 434   | 434   |
    | NELSON WESLEY PHILLIPS, III       | MILWAUKEE | MILWAUKEE COUNTY CIRCUIT COURT JUDGE, BRANCH 17 | VILLAGE OF BAYSIDE Ward 1s & 3s Congress 6  | 6     | 16    |
    | NICHOLAS J. BRAZEAU, JR.          | WOOD      | WOOD COUNTY CIRCUIT COURT JUDGE, BRANCH 2         | CITY OF WISCONSIN RAPIDS Ward 23          | 67    | 69    |

  Examples: 20120605__wi__general-recall_ward.csv
    | candidate                     | county        | office                        | ward                                                          | votes | total |
    | Hari Trivedi                  | Adams         | Governor                      | Town of Adams Wards 1-3                                       | 6     | 525   |
    | Scattering                    | Wood          | Governor                      | City of Wisconsin Rapids Wards 16 -23 & 25                    | 3     | 2221  |
    | Rebecca Kleefisch             | St. Croix     | Lieutenant Governor           | City of Hudson Wards 1 & 2                                    | 324   | 579   |
    | Van H. Wanggaard              | Racine        | State Senate                  | Village of Mount Pleasant Wards 19,21,22,23                   | 1321  | 2523  |
    | Donna Seidel                  | Taylor        | State Senate                  | City of Medford Wards 1-8                                     | 588   | 1638  |

  Examples: 20120814__wi__primary_ward.csv
    | candidate                     | county        | office                        | ward                                                          | votes | total |
    | Al Ott                        | Outagamie     | State Assembly                | Village of Combined Locks Wards 1-4                           | 263   | 368   |

  Examples: 20121106__wi__general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Barack Obama & Joe Biden      | Chippewa      | President                         | Town of Hallie Ward 1                                     | 54    | 100   |
    | Joseph Kexel                  | Walworth      | Senate                            | Town of Geneva Wards 1-8                                  | 77    | 2525  |
    | Sheila Harsdorf               | Polk          | State Senate                      | Town of Laketown Ward 1                                   | 316   | 542   |

  Examples: 20121204__wi__special_general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Paul Farrow                   | Waukesha      | State Senate                      | City of Pewaukee Wards 8-10                               | 274   | 281   |


  Examples: 20130219__wi__special_primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Matt Morzy                    | Waukesha      | State Assembly                    | City of Waukesha Ward 4                                   | 6     | 70    |
    | Adam Neylon                   | Waukesha      | State Assembly                    | City of Pewaukee Wards 5-7                                | 219   | 559   |

  Examples: 20130402__wi__general_ward.csv
    | candidate                     | county        | office                                        | ward                                          | votes | total |
    | Tony Evers                    | Adams         | State Superintendent Of Public Instruction    | Town Of Monroe Ward 1                         | 53    | 94    |
    | Tony Evers                    | Columbia      | State Superintendent Of Public Instruction    | City Of Wisconsin Dells Ward 1                | 54    | 74    |
    | Don Pridemore                 | Dane          | State Superintendent Of Public Instruction    | City Of Madison Ward 49                       | 12    | 82    |
    | Don Pridemore                 | Wood          | State Superintendent Of Public Instruction    | Town Of Seneca Wards 1 -3                     | 55    | 136   |

  Examples: 20131119__wi__special_primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Stephanie Mares               | Milwaukee     | State Assembly                    | Village of Greendale Wards 9-10                           | 132   | 231   |

  Examples: 20131217__wi__special_general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | John R. Hermes                | Milwaukee     | State Assembly                    | City of Greenfield Ward 20                                | 86    | 223   |


  Examples: 20140812__wi__primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Mary Burke                    | Brown         | Governor                          | Town of Holland Wards 1 - 2                               | 41    | 49    |
    | Jerry Broitzman               | Dane          | Secretary Of State                | City of Madison Ward 38                                   | 3     | 3     |
    | Rebecca Kleefisch             | Douglas       | Lieutenant Governor               | Town of Brule Wards 1 & 2                                 | 9     | 9     |

  Examples: 20141104__wi__general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Mary Burke & John Lehman      | Adams         | Governor                          | Town of Adams Wards 1-3                                   | 233   | 500   |
    | Steve R. Evans (Write-In)     | Dane          | Governor                          | City of Verona Wards 1, 5                                 | 0     | 1037  |
    | Chris Kapenga                 | Waukesha      | State Assembly                    | Village of Summit Wards 2,3,4,5                           | 1227  | 1643  |
    | Peter Flesch                  | Vernon        | State Assembly                    | City of Westby Wards 1 - 5                                | 375   | 837   |
    | Dean P. Debroux               | Outagamie     | State Senate                      | City of Appleton Ward 59                                  | 1     | 1     |
    | Lawrence Dale                 | Wood          | House                             | City of Pittsville Ward 1                                 | 7     | 356   |
    | Jerry Shidell                 | Ashland       | State Treasurer                   | City of Mellen Ward 1                                     | 3     | 221   |


  Examples: 20150623__wi__special_primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Sherryll Shaddock             | Waukesha      | State Senate                      | City of Waukesha Ward 38                                  | 19    | 19    |

  Examples: 20150901__wi__special_primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Scattering                    | Waukesha      | State Assembly                    | Village of Oconomowoc Lake Ward 1                         | 0     | 28    |
    | Spencer Zimmerman             | Waukesha      | State Assembly                    | Town of Genesee Wards 1-5, 9 10                           | 9     | 278   |

  Examples: 20150929__wi__special_general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Cindi Duchow                  | Waukesha      | State Assembly                    | Village of Hartland Wards 1-13                            | 117   | 140   |
    | Thomas D. Hibbard (Write-In)  | Waukesha      | State Assembly                    | Village of Wales Wards 1-4                                | 10    | 106   |
    | Scattering                    | Waukesha      | State Assembly                    | City of Delafield Wards 1 - 14                            | 18    | 217   |

  Examples: 20160405__wi__primary_ward.csv
    | party | candidate                     | county        | office                            | ward                                                      | votes | total |
    | DEM   | Uninstructed Delegation       | Milwaukee     | President                         | CITY OF SOUTH MILWAUKEE Ward 13-16                   | 1     | 867    |

  Examples: 20160405__wi__primary_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Paul F. Reilly                | Sheboygan     | Court of Appeals                  | VILLAGE OF RANDOM LAKE Wards 1-2                          | 494   | 496    |
    | Barbara Hart Key              | Winnebago     | Winnebago County Circuit Court Judge Branch 3 | CITY OF MENASHA Wards 5-6,8-9,23-29,31-35,38  | 449   | 452    |
    | Rebecca G. Bradley            | Chippewa      | Supreme Court      | TOWN OF GOETZ Ward 3                                      | 4     | 4      |

  Examples: 20161108__wi__general_ward.csv
    | candidate                     | county        | office                            | ward                                                      | votes | total |
    | Darrell L. Castle & Scott N. Bradley | Burnett | President                        | TOWN OF WOOD RIVER Ward 1-3                               | 10     | 517   |
    | Ron Johnson                   | Wood          | Senate                            | TOWN OF GRAND RAPIDS Ward 1-11                            | 2573   | 4505  |
    | Sarah Lloyd                   | Dodge         | House                             | CITY OF MAYVILLE Wards 1-8                                | 781    | 2524  |
    | Fred A. Risser                | Dane          | State Senate                      | CITY OF MIDDLETON Wards 19-20                             | 0      | 0     |
    | Cindi Duchow                  | Waukesha      | State Assembly                    | TOWN OF OTTAWA Wards 1-5                                  | 1912   | 1938  |
