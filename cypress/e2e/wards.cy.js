describe("wards spec", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-city-of-cape-town-ward-1/");
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
