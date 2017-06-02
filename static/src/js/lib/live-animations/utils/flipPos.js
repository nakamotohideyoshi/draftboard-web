export const flipOperator = (x, op, y, flip = true) => {
  const operator = !flip ? op : {
    '-': '+',
    '+': '-',
    '*': '/',
    '/': '*',
  }[op];

  return eval(`${x} ${operator} ${y}`);  // eslint-disable-line no-eval
};
