import React from 'react';
import { render } from '@testing-library/react';
import Box from '.';

describe('<Box/>', () => {
  it('should render with provided class names and props', () => {
    const { container } = render(
      <Box
        className="custom-class"
        m={2}
        p={3}
      >
        Content
      </Box>
    );

    const boxElement = container.firstChild;
    expect(boxElement.tagName).toBe('DIV'); // Default component is 'div'
    expect(boxElement).toHaveClass('custom-class');
    expect(boxElement).toHaveClass('m-2');
    expect(boxElement).toHaveClass('p-3');
    expect(boxElement.textContent).toBe('Content');
  });

  it('should render custom component', () => {
    const { container } = render(
      <Box
        component="span"
      >
        Content
      </Box>
    );

    const boxElement = container.firstChild;
    expect(boxElement.tagName).toBe('SPAN');
    expect(boxElement.textContent).toBe('Content');
  })

  it('should render with values from 1 to 10 for m and p', () => {
    for (let i = 1; i <= 10; i++) {
      const { container } = render(
        <Box m={i} p={i}>
          Content
        </Box>
      );

      const boxElement = container.firstChild;
      expect(boxElement).toHaveClass(`m-${i}`);
      expect(boxElement).toHaveClass(`p-${i}`);
    }
  });
});