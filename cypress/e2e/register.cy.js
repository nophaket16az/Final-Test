// EP + BVA ของกฎ "อายุ 18-60"
const INVALID = 'Age must be between 18 and 60'
const cases = [
  ['10', INVALID], ['35', 'Valid age'], ['70', INVALID],   // EP
  ['17', INVALID], ['18', 'Valid age'], ['19', 'Valid age'], // BVA min
  ['59', 'Valid age'], ['60', 'Valid age'], ['61', INVALID], // BVA max
  ['', 'Age is required'], ['abc', 'Age must be a number'],
]

describe('Register age 18-60', () => {
  cases.forEach(([age, expected]) => {
    it(`age "${age}" -> ${expected}`, () => {
      cy.visit('/register.html')
      if (age) cy.get('#age').type(age)
      cy.get('#submit').click()
      cy.get('#result').should('have.text', expected)
    })
  })
})
