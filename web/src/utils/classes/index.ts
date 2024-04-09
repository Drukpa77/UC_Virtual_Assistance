export default function classes(...classNames: any[]) {
  // remove undefined / false value
  const filteredClassNames = classNames.filter(className => className);
  const joined = filteredClassNames.join(' ');
  return joined;
}