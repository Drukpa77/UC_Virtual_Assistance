// This file is part of the irunawiki client code

import React from 'react';

export default function useScrollTrigger() {
  const [isScrollingDown, setIsScrollingDown] = React.useState<boolean>(false);
  const [lastScroll, setLastScroll] = React.useState<number>(0);

  React.useEffect(() => {
    const handleScroll = () => {
      const currentPosition = window.pageYOffset;
      if (currentPosition > 0) {
        setIsScrollingDown(currentPosition > (lastScroll || 0));
        setLastScroll(currentPosition);
      } else {
        // if negative scroll
        setLastScroll(0); // reach the top
        setIsScrollingDown(false); // stop scrolling
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [lastScroll]);

  return isScrollingDown;
}