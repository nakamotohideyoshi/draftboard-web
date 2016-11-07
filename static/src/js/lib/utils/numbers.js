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

// iterative relaxation, idea from https://goo.gl/V1V8uv
// close values get spread apart
// range of 0 to 1 permitted
export const iterativeRelaxation = (initial) => {
  const t = initial;

  for (let j = 0; j < 20; j++) {
    for (let i = 0; i < t.length - 1; i++) {
      // if at end of bounds
      if (t[i] === 0 || t[i] === 1) continue;

      if (t[i] > t[i + 1] - 0.5) {
        t[i] -= (t[i] - (t[i + 1] - 2));
      }
    }
    for (let i = t.length - 1; i >= 1; i--) {
      // if at end of bounds
      if (t[i] === 0 || t[i] === 1) continue;

      if (t[i] < t[i - 1] + 0.5) {
        t[i] -= (t[i] - (t[i - 1] + 2));
      }
    }
  }

  return t;
};

export const addOrdinal = (amount) => {
  const amountInt = parseInt(amount, 10) || 0;

  if (isNaN(amountInt)) return false;
  if (amountInt <= 0) return false;

  let ordinal = '';
  switch (amountInt) {
    case 1:
      ordinal = 'st';
      break;
    case 2:
      ordinal = 'nd';
      break;
    case 3:
      ordinal = 'rd';
      break;
    default:
      ordinal = 'th';
  }

  return `${amountInt}${ordinal}`;
};
