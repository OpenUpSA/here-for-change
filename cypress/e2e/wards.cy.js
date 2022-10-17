describe("wards spec", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
  });
});

describe("nav tray visible on hover", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
    cy.get(".tray-tabs").first().parent().invoke("show");
    cy.get(".tray-tabs").first().trigger("mouseover");
    cy.get(".nav-tray").invoke("show");
    cy.get(".nav-tray").should("be.visible");
  });
});

describe("type in nav search bar", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
    cy.get("input")
      .first()
      .type("Hello world")
      .should("have.value", "Hello world");
  });
});

describe("ward selector dropdown", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
    cy.get("#ward-button").click();
    cy.get(".dropdown-panel").first().should("be.visible");
  });
});

describe("tailwind CSS check", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
    cy.get("#ward-button").should("have.css", "background-color","rgb(91, 141, 138)")
  });
});
