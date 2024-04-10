import React, { ReactNode } from 'react';
export interface PureBoxProps<T> extends React.HTMLAttributes<T> {
  component?: keyof JSX.IntrinsicElements | React.ComponentType<any>;
  children?: ReactNode;
}