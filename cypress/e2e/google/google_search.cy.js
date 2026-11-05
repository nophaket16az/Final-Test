describe('Google Search Test', () => {
  it('Searches for Selenium on Google', () => {
    cy.visit('https://www.google.com')

    // พิมพ์คำสั่งในช่องค้นหาแล้วกด Enter ({enter})
    cy.get('textarea[name="q"]').type('Selenium{enter}')
  })
})
