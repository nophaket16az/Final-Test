*** Settings ***
Documentation     ทดสอบหน้า Login ด้วย Robot Framework + SeleniumLibrary
Library           SeleniumLibrary
Suite Setup       Open Browser    ${URL}    ${BROWSER}    options=${OPTIONS}
Suite Teardown    Close All Browsers
Test Setup        Go To    ${URL}

*** Variables ***
# เปลี่ยนตอนรันได้ เช่น  robot -v URL:https://www.saucedemo.com -v BROWSER:headlesschrome login.robot
${URL}            http://localhost:8000
${BROWSER}        chrome
${OPTIONS}        add_argument("--start-maximized")
${USERNAME}       standard_user
${PASSWORD}       secret_sauce

*** Test Cases ***
TC01 Login Success
    Login    ${USERNAME}    ${PASSWORD}
    Element Text Should Be    css:.title    Products

TC02 Add To Cart
    Login    ${USERNAME}    ${PASSWORD}
    Click Button    id:add-to-cart-sauce-labs-backpack
    Element Text Should Be    css:.shopping_cart_badge    1

TC03 Wrong Password
    [Template]    Login Should Fail With
    standard_user      wrong_pass       Username and password do not match

TC04 Empty Username
    [Template]    Login Should Fail With
    ${EMPTY}           secret_sauce     Username is required

TC05 Empty Password
    [Template]    Login Should Fail With
    standard_user      ${EMPTY}         Password is required

TC06 Locked Out User
    [Template]    Login Should Fail With
    locked_out_user    secret_sauce     locked out

*** Keywords ***
Login
    [Arguments]    ${user}    ${pass}
    Input Text        id:user-name    ${user}
    Input Password    id:password     ${pass}
    Click Button      id:login-button

Login Should Fail With
    [Arguments]    ${user}    ${pass}    ${expected_error}
    Go To    ${URL}
    Login    ${user}    ${pass}
    Element Should Contain    css:[data-test="error"]    ${expected_error}
