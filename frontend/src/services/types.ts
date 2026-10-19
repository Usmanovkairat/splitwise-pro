export interface Group {
  id: string;
  name: string;
  currency: string;
  description: string;
  created_at: string;
}
export interface Member {
  id: string;
  group_id: string;
  name: string;
}
export type SplitType = "equal" | "exact" | "percentage";
export interface ExpenseInput {
  description: string;
  amount_minor: number;
  payer_id: string;
  category: string;
  date: string;
  split_type: SplitType;
  split_values: Record<string, number>;
}
export interface Expense extends ExpenseInput {
  id: string;
  group_id: string;
  shares: { member_id: string; amount_minor: number }[];
}
export interface SettlementInput {
  from_member_id: string;
  to_member_id: string;
  amount_minor: number;
  date: string;
  note: string;
}
export interface Settlement extends SettlementInput {
  id: string;
  group_id: string;
}
export interface Balances {
  members: {
    member_id: string;
    name: string;
    paid_minor: number;
    owed_minor: number;
    net_minor: number;
  }[];
  suggestions: {
    from_member_id: string;
    to_member_id: string;
    amount_minor: number;
  }[];
  total_minor: number;
}
export interface Analytics {
  total_minor: number;
  by_category: { category: string; amount_minor: number }[];
  over_time: { date: string; amount_minor: number }[];
  contributions: { member_id: string; name: string; amount_minor: number }[];
  outstanding_minor: number;
}
export interface Service {
  listGroups(): Promise<Group[]>;
  createGroup(
    data: Pick<Group, "name" | "currency" | "description">,
  ): Promise<Group>;
  updateGroup(
    id: string,
    data: Pick<Group, "name" | "description">,
  ): Promise<Group>;
  deleteGroup(id: string): Promise<void>;
  listMembers(id: string): Promise<Member[]>;
  addMember(id: string, name: string): Promise<Member>;
  removeMember(id: string, memberId: string): Promise<void>;
  listExpenses(id: string): Promise<Expense[]>;
  createExpense(id: string, data: ExpenseInput): Promise<Expense>;
  updateExpense(
    id: string,
    expenseId: string,
    data: ExpenseInput,
  ): Promise<Expense>;
  deleteExpense(id: string, expenseId: string): Promise<void>;
  balances(id: string): Promise<Balances>;
  listSettlements(id: string): Promise<Settlement[]>;
  createSettlement(id: string, data: SettlementInput): Promise<Settlement>;
  analytics(id: string): Promise<Analytics>;
}
