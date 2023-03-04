describe('Check home page for section cards', () => {
  it('Checks about card', () => {
    cy.visit('http://localhost:8080')
    cy.get('#home-about-card').click()
  })
  it('Checks explore card', () => {
    cy.visit('http://localhost:8080')
    cy.get('#home-explore-card').click()
  })
  it('Checks identify card', () => {
    cy.visit('http://localhost:8080')
    cy.get('#home-identify-card').click()
  })
})