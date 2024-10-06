import { render, screen } from "@testing-library/react";
import HomePage from "views/HomePage";
import { MemoryRouter } from "react-router-dom"; 

beforeAll(() => {
  window.scrollTo = jest.fn();
});

test("render HomePage", () => {
  render(
    <MemoryRouter>
      <HomePage />
    </MemoryRouter>
  );

  const linkElement = screen.getByTestId("landsat-viz-text");
  expect(linkElement).toBeInTheDocument();
});