// ทดสอบหน้า Login (cy.visit('/') = เปิด baseUrl ใน cypress.config.js)
const login = (username, password) => {
  cy.visit('/')
  if (username) cy.get('#user-name').type(username)
  if (password) cy.get('#password').type(password)
  cy.get('#login-button').click()
}

describe('Login', () => {
  it('TC01 login success', () => {
    login('standard_user', 'secret_sauce')
    cy.get('.title').should('have.text', 'Products')
  })

  it('TC02 add to cart', () => {
    login('standard_user', 'secret_sauce')
    cy.get('#add-to-cart-sauce-labs-backpack').click()
    cy.get('.shopping_cart_badge').should('have.text', '1')
  })

  const failCases = [
    ['standard_user', 'wrong_pass', 'Username and password do not match'],
    ['', 'secret_sauce', 'Username is required'],
    ['standard_user', '', 'Password is required'],
    ['locked_out_user', 'secret_sauce', 'locked out'],
  ]
  failCases.forEach(([username, password, expected]) => {
    it(`login fail: "${username}" / "${password}"`, () => {
      login(username, password)
      cy.get('[data-test="error"]').should('contain', expected)
    })
  })
})
