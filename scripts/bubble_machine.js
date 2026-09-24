// bubble_machine.js: a pretend bubble blower (display-only, never run)
const COLORS = ["pink", "sky", "mint", "lemon", "grape"];

class Bubble {
  constructor(size, color) {
    this.size = size;
    this.color = color;
    this.popped = false;
  }

  float(seconds) {
    return `${this.color} bubble floats for ${seconds}s`;
  }

  pop() {
    this.popped = true;
    return "POP!";
  }
}

function blow(count = 5) {
  const bubbles = [];
  for (let i = 0; i < count; i++) {
    const color = COLORS[i % COLORS.length];
    bubbles.push(new Bubble(Math.random() * 10, color));
  }
  return bubbles;
}

const party = blow(12);
party
  .filter((b) => b.size > 3)
  .forEach((b) => console.log(b.float(2), b.pop()));

module.exports = { Bubble, blow };
