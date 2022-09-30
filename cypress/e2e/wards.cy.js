describe("wards spec", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-ward-1/");
  });
});

describe("nav tray visible on hover", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-ward-1/");
    cy.get(".tray-tabs").first().parent().invoke("show");
    cy.get(".tray-tabs").first().trigger("mouseover");
    cy.get(".nav-tray").invoke("show");
    cy.get(".nav-tray").should("be.visible");
  });
});

describe("type in nav search bar", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-ward-1/");
    cy.get("input")
      .first()
      .type("Hello world")
      .should("have.value", "Hello world");
  });
});

describe("ward selector dropdown", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-ward-1/");
    cy.get("#ward-button").click();
    cy.get(".dropdown-panel").first().should("be.visible");
  });
});

describe("test toc sections visibility", () => {
  it("passes", () => {
    cy.visit("/municipalities/CPT/wards/cpt-ward-1/");
    cy.get(".toc-btn").eq(1).click();
    cy.get("#contact").contains("Municipality contacts");
  });
});
