import SVGIcon from "@/components/ui/SVGIcon";

export default function ArrowUp({ ...props }) {
  return (
    <SVGIcon {...props} viewBox="0 0 24 24">
      <path d="m4 12 1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8z"></path>
    </SVGIcon>
  );
}