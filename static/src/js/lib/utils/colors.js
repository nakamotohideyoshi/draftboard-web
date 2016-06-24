/**
 * Helper method to find a middle hex
 * - used with two semi circles to make an angular gradient on the circle stroke of LivePMRProgressBar
 *
 * @param  {string} Starting hex string (without the leading #)
 * @param  {string} Ending hex string (without the leading #)
 * @param  {number} What percentage between the two hex strings do we need to return, range of 0-1
 * @return {string} The generated hex string
 */
export const percentageHexColor = (start, end, percentage) => {
  const hex = (x) => {
    const strX = x.toString(16);
    return (strX.length === 1) ? `0${strX}` : strX;
  };

  // no need to calculate if it's already there
  if (percentage === 0) return start;
  if (percentage === 1) return end;

  const r = Math.ceil(
    parseInt(start.substring(0, 2), 16) * percentage + parseInt(end.substring(0, 2), 16) * (1 - percentage)
  );
  const g = Math.ceil(
    parseInt(start.substring(2, 4), 16) * percentage + parseInt(end.substring(2, 4), 16) * (1 - percentage)
  );
  const b = Math.ceil(
    parseInt(start.substring(4, 6), 16) * percentage + parseInt(end.substring(4, 6), 16) * (1 - percentage)
  );

  return hex(r) + hex(g) + hex(b);
};
