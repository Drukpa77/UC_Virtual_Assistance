import React from "react";
import { render, screen } from "@testing-library/react";
import Row from ".";

describe("<Row/>", () => {
  it("should render children correctly", () => {
    render(
      <Row>
        <div>Child 1</div>
        <div>Child 2</div>
      </Row>
    );

    expect(screen.getByText("Child 1")).toBeInTheDocument();
    expect(screen.getByText("Child 2")).toBeInTheDocument();
  });

  it("should apply default justify and align items styles correctly", () => {
    const { container } = render(<Row />);

    expect(container.firstChild).toHaveClass("row");
    expect(container.firstChild).toHaveClass("row-justify-flex-start");
    expect(container.firstChild).toHaveClass("row-align-item-stretch");
  });

  it("should apply custom justify and align items styles correctly", () => {
    const { container } = render(
      <Row justify="center" alignItem="flex-end" />
    );

    expect(container.firstChild).toHaveClass("row");
    expect(container.firstChild).toHaveClass("row-justify-center");
    expect(container.firstChild).toHaveClass("row-align-item-flex-end");
  });

  it("should additional className correctly", () => {
    const { container } = render(<Row className="custom-class" />);

    expect(container.firstChild).toHaveClass("row");
    expect(container.firstChild).toHaveClass("custom-class");
  });
});