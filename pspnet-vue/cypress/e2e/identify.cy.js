const identifyUrl = "http://localhost:8080/identify";
describe("Check default state", () => {
  it("Empty image gallery", () => {
    cy.visit(identifyUrl);
    cy.get("#image-gallery").contains("No images uploaded");
  });
  it("Empty file list", () => {
    cy.visit(identifyUrl);
    cy.get("#file-list").contains("No images uploaded");
  });
  it("File list search box disabled", () => {
    cy.visit(identifyUrl);
    cy.get("#file-list input[placeholder='Search (disabled)']").should(
      "be.disabled"
    );
  });
  it("Empty dataset information", () => {
    cy.visit(identifyUrl);
    cy.get("#dataset-name[placeholder='example-dataset-name']").should(
      "have.value",
      ""
    );
    cy.get("#dataset-notes[placeholder='Optional']").should("have.value", "");
    cy.get("#dataset-geoloc").should("have.value", "");
  });
  it("No visibility setting selected", () => {
    cy.visit(identifyUrl);
    cy.get("#radio-visibility [data-headlessui-state]")
      .should("have.length", 3)
      .and("have.attr", "data-headlessui-state")
      .and("eq", "");
  });
  it("No model selected", () => {
    cy.visit(identifyUrl)
    cy.get("#menu-button-model").contains("Select model")
  })
  it("Identify button disbaled", () => {
    cy.visit(identifyUrl)
    cy.get("#button-identify").should("be.disabled")
  })
});
