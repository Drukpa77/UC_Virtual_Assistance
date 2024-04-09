// This file is part of the irunawiki client code

import useScrollTrigger from '@/hooks/useScrollTrigger';
import Slide from '@/components/ui/Slide';
import { ScrollProps } from './types';

export default function HideOnScroll({ direction, children }: ScrollProps) {
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction={direction} flow={!trigger}>
      {children}
    </Slide>
  );
}