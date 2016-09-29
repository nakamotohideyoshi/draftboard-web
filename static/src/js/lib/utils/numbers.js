/**
 * Humanize fantasy points to be readable by user
 *
 * @param  {mixed}  fp           Fantasy points in either string or number
 * @param  {bool} showPlusMinus  Whether to show +,- before the number
 * @return {string}              Humanized fantasy points, rounded to whole if int, else hundredths
 */
export const humanizeFP = (fp, showPlusMinus = false) => {
  switch (typeof fp) {
    case 'number': {
      // check if int
      let cleanedFp;
      if (fp === parseInt(fp, 10)) {
        cleanedFp = fp;
      } else if ((fp * 10) === parseInt(fp * 10, 10)) {
        cleanedFp = fp.toFixed(1);
      // otherwise round to hundredths
      } else {
        cleanedFp = fp.toFixed(2);
      }

      if (!showPlusMinus || cleanedFp === 0) return cleanedFp.toString();

      // add in + bc of showPlusMinus
      if (cleanedFp > 0) return `+${cleanedFp}`;

      // adds in - by default
      return `- ${Math.abs(cleanedFp.toString())}`;
    }
    case 'string':
    default:
      return fp;
  }
};
