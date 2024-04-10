// this file belongs to irunawiki organisation

import React from 'react';
import PureBox from '../PureBox';
import { BoxProps } from './types';
import classes from '@/utils/classes';
import styles from './style.module.css';



export default function Box({ component = 'div', className, ...props }: BoxProps<HTMLElement>) {
  const {
    m, mt, mr, mb, ml,
    p, pt, pr, pb, pl,
    textAlign,
    fontWeight,
    ...restProps
  } = props;

  const classNames = classes(
    m !== undefined && styles[`m-${m}`],
    mt !== undefined && styles[`mt-${mt}`],
    mr !== undefined && styles[`mr-${mr}`],
    mb !== undefined && styles[`mb-${mb}`],
    ml !== undefined && styles[`ml-${ml}`],
    p !== undefined && styles[`p-${p}`],
    pt !== undefined && styles[`pt-${pt}`],
    pr !== undefined && styles[`pr-${pr}`],
    pb !== undefined && styles[`pb-${pb}`],
    pl !== undefined && styles[`pl-${pl}`],
    textAlign ? styles[`text-align-${textAlign}`]: '',
    fontWeight ? styles[`font-weight-${fontWeight}`] : '',
    className || ''
  );
  return <PureBox component={component} className={classNames} {...restProps}/>
}