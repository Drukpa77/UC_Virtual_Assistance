import React, { createElement } from 'react';
import { PureBoxProps } from './types';

export default function PureBox({ component = 'div', ...props }: PureBoxProps<HTMLElement>) {
  return createElement(component, props);
}