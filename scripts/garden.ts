// garden.ts: a typed vegetable patch (pretend, never compiled)
type Veggie = "carrot" | "pea" | "pumpkin" | "tomato";

interface Plot {
  id: number;
  veggie: Veggie;
  water: number;
  sunny: boolean;
}

const garden: Plot[] = [
  { id: 1, veggie: "carrot", water: 3, sunny: true },
  { id: 2, veggie: "pea", water: 1, sunny: false },
  { id: 3, veggie: "pumpkin", water: 5, sunny: true },
];

function waterAll(plots: Plot[], cups: number): Plot[] {
  return plots.map((p) => ({ ...p, water: p.water + cups }));
}

async function harvest(plot: Plot): Promise<string> {
  await new Promise((r) => setTimeout(r, 300));
  return plot.water > 4 ? `big ${plot.veggie}!` : `tiny ${plot.veggie}`;
}

export async function main(): Promise<void> {
  const watered = waterAll(garden, 2);
  for (const plot of watered.filter((p) => p.sunny)) {
    console.log(await harvest(plot));
  }
}
