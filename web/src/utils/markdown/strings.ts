export function formatMDLinks(inputString: string) {
  const regex: RegExp = /\[(.*?)\]\s*\(\s*([^)]*?)\s*\)/g;

  const result = inputString.replace(regex, (match, p1, p2) => {
    const text = p1.trim();
    const link = p2.trim().replaceAll(' ', '');
    return `[${text}](${link})`;
  });
  return result
}