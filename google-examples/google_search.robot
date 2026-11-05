*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Search Google Test
    Open Browser    https://www.google.com    chrome
    Input Text      name=q    Playwright
    Press Keys      name=q    RETURN
    Close Browser
