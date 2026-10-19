import type {
  Analytics,
  Balances,
  Expense,
  ExpenseInput,
  Group,
  Member,
  Service,
  Settlement,
  SettlementInput,
} from "./types";
const clone = <T>(value: T): T => structuredClone(value);
const fail = (message: string): never => {
  throw new Error(message);
};
export function calculateShares(
  amount: number,
  values: Record<string, number>,
  type: string,
) {
  const ids = Object.keys(values).sort();
  if (!Number.isSafeInteger(amount) || amount <= 0)
    fail("Enter a positive amount with at most two decimal places.");
  if (!ids.length) fail("Select at least one participant.");
  if (Object.values(values).some((x) => !Number.isSafeInteger(x) || x < 0))
    fail("Split values must be non-negative integers.");
  if (type === "exact") {
    if (Object.values(values).reduce((a, b) => a + b, 0) !== amount)
      fail("Exact shares must equal the expense total.");
    return ids.map((member_id) => ({
      member_id,
      amount_minor: values[member_id],
    }));
  }
  if (
    type === "percentage" &&
    Object.values(values).reduce((a, b) => a + b, 0) !== 10000
  )
    fail("Percentages must add up to 100%.");
  const denominator = type === "equal" ? ids.length : 10000;
  const shares = ids.map((member_id) => ({
    member_id,
    amount_minor: Math.floor(
      (amount * (type === "equal" ? 1 : values[member_id])) / denominator,
    ),
  }));
  let remaining = amount - shares.reduce((s, x) => s + x.amount_minor, 0);
  const order = [...shares].sort(
    (a, b) =>
      ((amount * (type === "equal" ? 1 : values[b.member_id])) % denominator) -
        ((amount * (type === "equal" ? 1 : values[a.member_id])) %
          denominator) || a.member_id.localeCompare(b.member_id),
  );
  for (let i = 0; remaining > 0; i++, remaining--)
    order[i % order.length].amount_minor++;
  return shares;
}
const seedGroups: Group[] = [
  {
    id: "g1",
    name: "Lisbon getaway",
    currency: "USD",
    description: "Good friends. Great pastel de nata.",
    created_at: "2026-10-01T12:00:00Z",
  },
  {
    id: "g2",
    name: "The apartment",
    currency: "USD",
    description: "A little place we call home.",
    created_at: "2026-09-01T12:00:00Z",
  },
  {
    id: "g3",
    name: "Friday dinner club",
    currency: "USD",
    description: "A new table, every Friday.",
    created_at: "2026-10-02T12:00:00Z",
  },
];
const seedMembers: Member[] = [
  { id: "m1", group_id: "g1", name: "Kairat" },
  { id: "m2", group_id: "g1", name: "Aigerim" },
  { id: "m3", group_id: "g1", name: "Timur" },
  { id: "m4", group_id: "g1", name: "Dana" },
  { id: "m5", group_id: "g2", name: "Kairat" },
  { id: "m6", group_id: "g2", name: "Timur" },
  { id: "m7", group_id: "g3", name: "Kairat" },
  { id: "m8", group_id: "g3", name: "Dana" },
];
const rows: [string, number, string, string, string][] = [
  ["Apartment in Alfama", 48000, "m1", "Accommodation", "2026-10-12"],
  ["Dinner at Time Out Market", 12680, "m2", "Food & drinks", "2026-10-13"],
  ["Tram tickets", 1440, "m3", "Travel", "2026-10-14"],
  ["Day trip to Sintra", 9600, "m1", "Entertainment", "2026-10-15"],
  ["Coffee & pastel de nata", 3240, "m4", "Food & drinks", "2026-10-16"],
  ["Airport transfers", 6800, "m2", "Travel", "2026-10-17"],
];
export function createMockService(): Service {
  let groups = clone(seedGroups),
    members = clone(seedMembers),
    expenses: Expense[] = rows.map((r, i) => ({
      id: `e${i + 1}`,
      group_id: "g1",
      description: r[0],
      amount_minor: r[1],
      payer_id: r[2],
      category: r[3],
      date: r[4],
      split_type: "equal",
      split_values: { m1: 1, m2: 1, m3: 1, m4: 1 },
      shares: calculateShares(r[1], { m1: 1, m2: 1, m3: 1, m4: 1 }, "equal"),
    })),
    settlements: Settlement[] = [];
  let sequence = 100;
  const group = (id: string) =>
    groups.find((g) => g.id === id) || fail("Group not found.");
  const getMembers = (id: string) => {
    group(id);
    return members.filter((m) => m.group_id === id);
  };
  const validateExpense = (id: string, data: ExpenseInput) => {
    const valid = getMembers(id).map((m) => m.id);
    if (!data.description.trim()) fail("A description is required.");
    if (
      !valid.includes(data.payer_id) ||
      Object.keys(data.split_values).some((x) => !valid.includes(x))
    )
      fail("Select valid group members.");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(data.date))
      fail("A valid date is required.");
    return calculateShares(
      data.amount_minor,
      data.split_values,
      data.split_type,
    );
  };
  const getBalances = (id: string): Balances => {
    const result = getMembers(id).map((m) => ({
      member_id: m.id,
      name: m.name,
      paid_minor: 0,
      owed_minor: 0,
      net_minor: 0,
    }));
    const index = Object.fromEntries(result.map((m) => [m.member_id, m]));
    for (const e of expenses.filter((e) => e.group_id === id)) {
      index[e.payer_id].paid_minor += e.amount_minor;
      for (const share of e.shares)
        index[share.member_id].owed_minor += share.amount_minor;
    }
    for (const m of result) m.net_minor = m.paid_minor - m.owed_minor;
    for (const s of settlements.filter((s) => s.group_id === id)) {
      index[s.from_member_id].net_minor += s.amount_minor;
      index[s.to_member_id].net_minor -= s.amount_minor;
    }
    const debtors = result
      .filter((m) => m.net_minor < 0)
      .map((m) => ({ id: m.member_id, left: -m.net_minor }))
      .sort((a, b) => a.id.localeCompare(b.id));
    const creditors = result
      .filter((m) => m.net_minor > 0)
      .map((m) => ({ id: m.member_id, left: m.net_minor }))
      .sort((a, b) => a.id.localeCompare(b.id));
    const suggestions: Balances["suggestions"] = [];
    for (const d of debtors)
      for (const c of creditors) {
        const amount = Math.min(d.left, c.left);
        if (amount) {
          suggestions.push({
            from_member_id: d.id,
            to_member_id: c.id,
            amount_minor: amount,
          });
          d.left -= amount;
          c.left -= amount;
        }
      }
    return {
      members: result,
      suggestions,
      total_minor: expenses
        .filter((e) => e.group_id === id)
        .reduce((sum, e) => sum + e.amount_minor, 0),
    };
  };
  return {
    async listGroups() {
      return clone(groups);
    },
    async createGroup(data) {
      if (!data.name.trim()) fail("Group name is required.");
      const g = {
        ...data,
        name: data.name.trim(),
        id: `g${sequence++}`,
        created_at: new Date().toISOString(),
      };
      groups.push(g);
      return clone(g);
    },
    async updateGroup(id, data) {
      const g = group(id);
      if (!data.name.trim()) fail("Group name is required.");
      Object.assign(g, data);
      return clone(g);
    },
    async deleteGroup(id) {
      group(id);
      groups = groups.filter((g) => g.id !== id);
      members = members.filter((m) => m.group_id !== id);
      expenses = expenses.filter((e) => e.group_id !== id);
      settlements = settlements.filter((s) => s.group_id !== id);
    },
    async listMembers(id) {
      return clone(getMembers(id));
    },
    async addMember(id, name) {
      getMembers(id);
      if (!name.trim()) fail("Member name is required.");
      if (
        getMembers(id).some(
          (m) => m.name.toLowerCase() === name.trim().toLowerCase(),
        )
      )
        fail("A member with this name already exists.");
      const m = { id: `m${sequence++}`, group_id: id, name: name.trim() };
      members.push(m);
      return clone(m);
    },
    async removeMember(id, memberId) {
      getMembers(id);
      if (
        expenses.some(
          (e) =>
            e.group_id === id &&
            (e.payer_id === memberId ||
              e.shares.some((s) => s.member_id === memberId)),
        ) ||
        settlements.some(
          (s) =>
            s.group_id === id &&
            (s.from_member_id === memberId || s.to_member_id === memberId),
        )
      )
        fail("Members with recorded activity cannot be removed.");
      members = members.filter(
        (m) => !(m.group_id === id && m.id === memberId),
      );
    },
    async listExpenses(id) {
      group(id);
      return clone(
        expenses
          .filter((e) => e.group_id === id)
          .sort((a, b) => b.date.localeCompare(a.date)),
      );
    },
    async createExpense(id, data) {
      const shares = validateExpense(id, data);
      const e = { ...data, id: `e${sequence++}`, group_id: id, shares };
      expenses.push(e);
      return clone(e);
    },
    async updateExpense(id, expenseId, data) {
      const shares = validateExpense(id, data);
      const e =
        expenses.find((e) => e.id === expenseId && e.group_id === id) ||
        fail("Expense not found.");
      Object.assign(e, data, { shares });
      return clone(e);
    },
    async deleteExpense(id, expenseId) {
      group(id);
      if (!expenses.some((e) => e.id === expenseId && e.group_id === id))
        fail("Expense not found.");
      expenses = expenses.filter(
        (e) => !(e.id === expenseId && e.group_id === id),
      );
    },
    async balances(id) {
      return clone(getBalances(id));
    },
    async listSettlements(id) {
      group(id);
      return clone(settlements.filter((s) => s.group_id === id));
    },
    async createSettlement(id, data: SettlementInput) {
      const valid = getMembers(id).map((m) => m.id);
      if (
        !valid.includes(data.from_member_id) ||
        !valid.includes(data.to_member_id) ||
        data.from_member_id === data.to_member_id
      )
        fail("Choose two different group members.");
      if (!Number.isSafeInteger(data.amount_minor) || data.amount_minor <= 0)
        fail("Enter a positive settlement amount.");
      const b = getBalances(id);
      const from = b.members.find((m) => m.member_id === data.from_member_id)!;
      const to = b.members.find((m) => m.member_id === data.to_member_id)!;
      if (data.amount_minor > Math.min(-from.net_minor, to.net_minor))
        fail("Settlement exceeds the outstanding balance.");
      const s = { ...data, id: `s${sequence++}`, group_id: id };
      settlements.push(s);
      return clone(s);
    },
    async analytics(id): Promise<Analytics> {
      const b = getBalances(id),
        es = expenses.filter((e) => e.group_id === id);
      const cats: Record<string, number> = {},
        dates: Record<string, number> = {};
      for (const e of es) {
        cats[e.category] = (cats[e.category] || 0) + e.amount_minor;
        dates[e.date] = (dates[e.date] || 0) + e.amount_minor;
      }
      return {
        total_minor: b.total_minor,
        by_category: Object.entries(cats).map(([category, amount_minor]) => ({
          category,
          amount_minor,
        })),
        over_time: Object.entries(dates)
          .sort()
          .map(([date, amount_minor]) => ({ date, amount_minor })),
        contributions: b.members.map((m) => ({
          member_id: m.member_id,
          name: m.name,
          amount_minor: m.paid_minor,
        })),
        outstanding_minor: b.members.reduce(
          (sum, m) => sum + Math.max(0, m.net_minor),
          0,
        ),
      };
    },
  };
}
export const mockService = createMockService();
