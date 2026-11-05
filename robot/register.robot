*** Settings ***
Documentation     ทดสอบช่องอายุ 18-60 ด้วยเทคนิค EP + BVA (data-driven ด้วย Test Template)
Library           SeleniumLibrary
Suite Setup       Open Browser    ${URL}/register.html    ${BROWSER}    options=${OPTIONS}
Suite Teardown    Close All Browsers
Test Template     Age Should Show

*** Variables ***
${URL}            http://localhost:8000
${BROWSER}        chrome
${OPTIONS}        add_argument("--start-maximized")
${INVALID}        Age must be between 18 and 60

*** Test Cases ***    AGE        EXPECTED
EP Invalid Low        10         ${INVALID}
EP Valid              35         Valid age
EP Invalid High       70         ${INVALID}
BVA Min Minus 1       17         ${INVALID}
BVA Min               18         Valid age
BVA Min Plus 1        19         Valid age
BVA Max Minus 1       59         Valid age
BVA Max               60         Valid age
BVA Max Plus 1        61         ${INVALID}
Empty Age             ${EMPTY}   Age is required
Not A Number          abc        Age must be a number

*** Keywords ***
Age Should Show
    [Arguments]    ${age}    ${expected}
    Go To    ${URL}/register.html
    Input Text      id:age    ${age}
    Click Button    id:submit
    Element Text Should Be    id:result    ${expected}
