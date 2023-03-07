import IdentifyView from "./IdentifyView.vue";

describe("<IdentifyView />", () => {
  it("renders", () => {
    // see: https://on.cypress.io/mounting-vue
    cy.mount(IdentifyView);
  });
});

describe("Check default state", () => {
  it("Empty image gallery", () => {
    cy.mount(IdentifyView);
    cy.get("#image-gallery").contains("No images uploaded");
  });
  it("Empty file list", () => {
    cy.mount(IdentifyView);
    cy.get("#file-list").contains("No images uploaded");
  });
  it("File list search box disabled", () => {
    cy.mount(IdentifyView);
    cy.get("#file-list input[placeholder='Search (disabled)']").should(
      "be.disabled"
    );
  });
  it("Empty dataset information", () => {
    cy.mount(IdentifyView);
    cy.get("#dataset-name[placeholder='example-dataset-name']").should(
      "have.value",
      ""
    );
    cy.get("#dataset-notes[placeholder='Optional']").should("have.value", "");
    cy.get("#dataset-geoloc").should("have.value", "");
  });
  it("No visibility setting selected", () => {
    cy.mount(IdentifyView);
    cy.get("#radio-visibility [data-headlessui-state]")
      .should("have.length", 3)
      .and("have.attr", "data-headlessui-state")
      .and("eq", "");
  });
  it("No model selected", () => {
    cy.mount(IdentifyView);
    cy.get("#menu-button-model").contains("Select model");
  });
  it("Identify button disbaled", () => {
    cy.mount(IdentifyView);
    cy.get("#button-identify").should("be.disabled");
  });
});
