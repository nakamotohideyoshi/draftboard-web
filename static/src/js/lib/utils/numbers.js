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
      const cleanedFp = Math.ceil(fp * 100) / 100;

      if (!showPlusMinus || cleanedFp === 0) return cleanedFp.toString();

      // add in + bc of showPlusMinus
      if (cleanedFp > 0) return `+${cleanedFp}`;

      // adds in - by default
      return cleanedFp.toString();
    }
    case 'string':
    default:
      return fp;
  }
};
