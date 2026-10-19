import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import {
  NavLink,
  useLocation,
  useNavigate,
  Routes,
  Route,
} from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  LayoutDashboard,
  Users,
  Receipt,
  ArrowLeftRight,
  ChartNoAxesCombined,
  Settings,
  Plus,
  ArrowUpRight,
  ArrowDownLeft,
  ArrowRight,
  ChevronDown,
  Search,
  Check,
  MoreHorizontal,
  X,
  Trash2,
  Pencil,
  Wallet,
  Leaf,
  Menu,
  CheckCircle2,
  AlertCircle,
  LoaderCircle,
  Plane,
  Home,
  UtensilsCrossed,
  CalendarDays,
  SlidersHorizontal,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from "recharts";
import { Button } from "./components/ui/button";
import { Dialog } from "./components/ui/dialog";
import {
  money,
  initials,
  categories,
  categoryColors,
  today,
} from "./lib/utils";
import { service } from "./services";
import type {
  Expense,
  ExpenseInput,
  Group,
  Member,
  SettlementInput,
  SplitType,
} from "./services/types";
const nav = [
  { to: "/", label: "Overview", icon: LayoutDashboard },
  { to: "/groups", label: "My groups", icon: Users },
  { to: "/expenses", label: "Expenses", icon: Receipt },
  { to: "/balances", label: "Balances", icon: Wallet },
  { to: "/settlements", label: "Settlements", icon: ArrowLeftRight },
  { to: "/analytics", label: "Analytics", icon: ChartNoAxesCombined },
];
function Avatar({
  name,
  index = 0,
  size = "",
}: {
  name: string;
  index?: number;
  size?: string;
}) {
  return (
    <span className={`avatar avatar-${index % 5} ${size}`} title={name}>
      {initials(name)}
    </span>
  );
}
function Empty({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: ReactNode;
}) {
  return (
    <div className="empty">
      <div className="empty-icon">
        <Leaf size={28} />
      </div>
      <h3>{title}</h3>
      <p>{description}</p>
      {action}
    </div>
  );
}
function Field({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: string;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
      {hint && <small>{hint}</small>}
    </label>
  );
}
function App() {
  const queryClient = useQueryClient(),
    location = useLocation(),
    navigate = useNavigate();
  const [selected, setSelected] = useState(""),
    [mobile, setMobile] = useState(false),
    [notice, setNotice] = useState(""),
    [mutationError, setMutationError] = useState(""),
    [displayName, setDisplayName] = useState(
      () =>
        localStorage.getItem("splitwise-display-name")?.trim() ||
        "Kairat Usmanov",
    ),
    [modal, setModal] = useState<
      "group" | "expense" | "settlement" | "member" | "rename" | null
    >(null),
    [editing, setEditing] = useState<Expense | undefined>(),
    [settlementDefaults, setSettlementDefaults] = useState<
      Partial<SettlementInput>
    >({});
  useEffect(() => {
    setMutationError("");
  }, [modal]);
  const groupsQuery = useQuery({
    queryKey: ["groups"],
    queryFn: () => service.listGroups(),
  });
  const groups = groupsQuery.data || [];
  useEffect(() => {
    const requested = location.pathname.match(/^\/groups\/([^/]+)$/)?.[1];
    if (requested && groupsQuery.data?.some((g) => g.id === requested))
      setSelected(requested);
  }, [location.pathname, groupsQuery.data]);
  const group = groups.find((g) => g.id === selected) || groups[0];
  const id = group?.id || "";
  const currency = group?.currency || "USD";
  useEffect(() => {
    if (group && selected !== group.id) setSelected(group.id);
  }, [group, selected]);
  useEffect(() => {
    setMobile(false);
  }, [location.pathname]);
  useEffect(() => {
    if (notice) {
      const timer = setTimeout(() => setNotice(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [notice]);
  const memberQuery = useQuery({
    queryKey: ["members", id],
    queryFn: () => service.listMembers(id),
    enabled: !!id,
  });
  const expenseQuery = useQuery({
    queryKey: ["expenses", id],
    queryFn: () => service.listExpenses(id),
    enabled: !!id,
  });
  const balanceQuery = useQuery({
    queryKey: ["balances", id],
    queryFn: () => service.balances(id),
    enabled: !!id,
  });
  const settlementQuery = useQuery({
    queryKey: ["settlements", id],
    queryFn: () => service.listSettlements(id),
    enabled: !!id,
  });
  const analyticsQuery = useQuery({
    queryKey: ["analytics", id],
    queryFn: () => service.analytics(id),
    enabled: !!id,
  });
  const members = memberQuery.data || [],
    expenses = expenseQuery.data || [],
    balances = balanceQuery.data,
    settlements = settlementQuery.data || [],
    analytics = analyticsQuery.data;
  const groupDataPending =
    !!id &&
    !["/groups", "/settings"].includes(location.pathname) &&
    (memberQuery.isPending ||
      expenseQuery.isPending ||
      balanceQuery.isPending ||
      settlementQuery.isPending ||
      analyticsQuery.isPending);
  const name = (memberId: string) =>
    members.find((m) => m.id === memberId)?.name || "Member";
  const invalidate = async () => {
    await queryClient.invalidateQueries();
  };
  const mutate = useMutation({
    mutationFn: async (fn: () => Promise<unknown>) => fn(),
    onSuccess: async () => {
      await invalidate();
      setMutationError("");
      setNotice("All done. Your workspace is up to date.");
      setModal(null);
      setEditing(undefined);
    },
    onError: (e) => setMutationError(e.message),
  });
  const act = (fn: () => Promise<unknown>) => {
    setMutationError("");
    setNotice("");
    mutate.mutate(fn);
  };
  const addExpense = () => {
    setEditing(undefined);
    setModal("expense");
  };
  const newSettlement = (data: Partial<SettlementInput> = {}) => {
    setSettlementDefaults(data);
    setModal("settlement");
  };
  const deleteExpense = (expense: Expense) => {
    if (
      confirm(
        `Delete “${expense.description}”? This will update group balances.`,
      )
    )
      act(() => service.deleteExpense(id, expense.id));
  };
  const error =
    groupsQuery.error ||
    memberQuery.error ||
    expenseQuery.error ||
    balanceQuery.error ||
    settlementQuery.error ||
    analyticsQuery.error;
  const groupIcons = [Plane, Home, UtensilsCrossed];
  const expenseTable = (limit?: number) => (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Expense</th>
            <th>Paid by</th>
            <th>Date</th>
            <th className="right">Amount</th>
            <th>
              <span className="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {expenses.slice(0, limit).map((e) => (
            <tr key={e.id}>
              <td>
                <div className="expense-description">
                  <span
                    className={`category-icon cat-${categories.indexOf(e.category) % 4}`}
                  >
                    <Receipt size={18} />
                  </span>
                  <div>
                    <strong>{e.description}</strong>
                    <small>
                      {e.category} <span>·</span>{" "}
                      {e.split_type === "equal"
                        ? "Split equally"
                        : e.split_type === "exact"
                          ? "Exact amounts"
                          : "By percentage"}
                    </small>
                  </div>
                </div>
              </td>
              <td>
                <div className="person">
                  <Avatar
                    name={name(e.payer_id)}
                    index={members.findIndex((m) => m.id === e.payer_id)}
                    size="small"
                  />
                  {name(e.payer_id)}
                </div>
              </td>
              <td className="muted">
                {new Date(e.date + "T12:00:00").toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })}
              </td>
              <td className="right amount">
                {money(e.amount_minor, currency)}
              </td>
              <td>
                <div className="row-actions">
                  <button
                    className="icon-button"
                    aria-label={`Edit ${e.description}`}
                    onClick={() => {
                      setEditing(e);
                      setModal("expense");
                    }}
                  >
                    <Pencil size={15} />
                  </button>
                  <button
                    className="icon-button danger"
                    aria-label={`Delete ${e.description}`}
                    onClick={() => deleteExpense(e)}
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {!expenses.length && (
        <Empty
          title="Every shared story starts somewhere"
          description="Add your first expense and we’ll take care of the split."
          action={
            <Button onClick={addExpense}>
              <Plus size={16} />
              Add an expense
            </Button>
          }
        />
      )}
    </div>
  );
  const stats = (
    <div className="stats">
      <div className="stat">
        <div className="stat-label">
          Total group spending <Receipt size={17} />
        </div>
        <strong>{money(analytics?.total_minor || 0, currency)}</strong>
        <span className="stat-detail">
          <span className="tiny-dot" />
          Across {expenses.length} shared expenses
        </span>
      </div>
      <div className="stat">
        <div className="stat-label">
          Outstanding balance <ArrowUpRight size={18} />
        </div>
        <strong>{money(analytics?.outstanding_minor || 0, currency)}</strong>
        <span className="stat-detail">Ready to settle, whenever you are</span>
      </div>
      <div className="stat">
        <div className="stat-label">
          People in this together <Users size={18} />
        </div>
        <strong>
          {members.length}
          <span className="stat-unit"> members</span>
        </strong>
        <div className="avatar-stack">
          {members.slice(0, 5).map((m, i) => (
            <Avatar key={m.id} name={m.name} index={i} size="small" />
          ))}
        </div>
      </div>
    </div>
  );
  const chart = (
    <div className="chart-area">
      {analytics?.over_time.length ? (
        <ResponsiveContainer width="100%" height={205}>
          <AreaChart
            data={analytics.over_time}
            margin={{ top: 15, right: 10, left: -20, bottom: 0 }}
          >
            <defs>
              <linearGradient id="spendGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2b9478" stopOpacity={0.23} />
                <stop offset="100%" stopColor="#2b9478" stopOpacity={0.01} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="date"
              tickFormatter={(d) => d.slice(5)}
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#8a928b", fontSize: 11 }}
            />
            <YAxis
              tickFormatter={(v) => `${v / 100}`}
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#8a928b", fontSize: 11 }}
            />
            <Tooltip
              formatter={(v) => money(Number(v), currency)}
              contentStyle={{ borderRadius: 10, border: "1px solid #e8ebe5" }}
            />
            <Area
              type="monotone"
              dataKey="amount_minor"
              name="Spending"
              stroke="#218c70"
              strokeWidth={2.5}
              fill="url(#spendGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      ) : (
        <Empty
          title="A fresh start"
          description="Your spending story will appear here."
        />
      )}
    </div>
  );
  const suggestions = (
    <>
      {balances?.suggestions.length ? (
        balances.suggestions.map((s, i) => (
          <div
            className="settle-row"
            key={`${s.from_member_id}-${s.to_member_id}`}
          >
            <div className="transfer-avatars">
              <Avatar name={name(s.from_member_id)} index={i + 1} />
              <ArrowRight size={14} />
              <Avatar name={name(s.to_member_id)} index={i} />
            </div>
            <div className="settle-copy">
              <strong>
                {name(s.from_member_id)}{" "}
                <span>owes {name(s.to_member_id)}</span>
              </strong>
              <small>A little less to keep track of</small>
            </div>
            <strong>{money(s.amount_minor, currency)}</strong>
            <Button
              variant="outline"
              size="sm"
              onClick={() => newSettlement(s)}
            >
              Settle up
            </Button>
          </div>
        ))
      ) : (
        <Empty
          title="All square. Nice feeling, right?"
          description="No outstanding balances in this group."
        />
      )}
    </>
  );
  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobile ? "is-open" : ""}`}>
        <NavLink to="/" className="brand">
          <span className="brand-symbol">
            <ArrowUpRight size={23} />
            <ArrowDownLeft size={23} />
          </span>
          <span>
            splitwise<span className="brand-pro">PRO</span>
          </span>
        </NavLink>
        <div className="workspace">
          <span className="workspace-icon">K</span>
          <div>
            <strong>Kairat’s workspace</strong>
            <small>Personal workspace</small>
          </div>
          <ChevronDown size={14} />
        </div>
        <p className="nav-label">WORKSPACE</p>
        <nav>
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                isActive ? "nav-item active" : "nav-item"
              }
            >
              <item.icon size={19} />
              {item.label}
              {item.to === "/groups" && (
                <span className="nav-count">{groups.length}</span>
              )}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <div>
              <Leaf size={20} />
              <span>A little less awkward.</span>
            </div>
            <p>
              Good friends. Clear balances.
              <br />
              More moments that matter.
            </p>
          </div>
          <NavLink
            to="/settings"
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
          >
            <Settings size={19} />
            Settings
          </NavLink>
          <div className="profile">
            <Avatar name={displayName} />
            <div>
              <strong>{displayName}</strong>
              <small>Personal account</small>
            </div>
            <MoreHorizontal size={18} />
          </div>
        </div>
      </aside>
      {mobile && (
        <button
          className="mobile-backdrop"
          aria-label="Close navigation"
          onClick={() => setMobile(false)}
        />
      )}
      <div className="main-shell">
        <header className="topbar">
          <button
            className="icon-button mobile-menu"
            aria-label="Open navigation"
            onClick={() => setMobile(true)}
          >
            <Menu size={22} />
          </button>
          <div className="breadcrumb">
            Workspace <span>/</span>{" "}
            <strong>
              {location.pathname.startsWith("/groups/")
                ? "Group details"
                : nav.find((n) => n.to === location.pathname)?.label ||
                  "Settings"}
            </strong>
          </div>
          <div className="topbar-right">
            <span className="local-badge">
              <span />
              Local workspace
            </span>
            <Avatar name={displayName} size="small" />
          </div>
        </header>
        <main>
          <div className="page-heading">
            <div>
              <p className="eyebrow">SHARED EXPENSES, SIMPLY</p>
              <h1>
                {location.pathname === "/"
                  ? "Good things are better shared."
                  : location.pathname.startsWith("/groups/")
                    ? group?.name || "Group details"
                    : nav.find((n) => n.to === location.pathname)?.label ||
                      "Your preferences"}
              </h1>
              <p className="page-subtitle">
                {location.pathname === "/"
                  ? "A clear picture of your shared spending. More room for the good stuff."
                  : location.pathname === "/groups"
                    ? "Your people, your plans, all in one place."
                    : group
                      ? group.description ||
                        `Keeping things fair in ${group.name}.`
                      : "Make yourself at home. Create a group to get started."}
              </p>
            </div>
            <div className="heading-actions">
              {location.pathname === "/groups" ? (
                <Button onClick={() => setModal("group")}>
                  <Plus size={17} />
                  New group
                </Button>
              ) : (
                location.pathname !== "/settings" && (
                  <Button
                    onClick={addExpense}
                    disabled={!group || members.length === 0}
                  >
                    <Plus size={17} />
                    Add expense
                  </Button>
                )
              )}
            </div>
          </div>
          {notice && (
            <div role="status" className="toast">
              <CheckCircle2 size={19} />
              {notice}
              <button
                className="icon-button"
                aria-label="Dismiss notification"
                onClick={() => setNotice("")}
              >
                <X size={16} />
              </button>
            </div>
          )}
          {mutationError && !modal && (
            <div role="alert" className="error-banner">
              <AlertCircle size={20} />
              <span>{mutationError}</span>
              <button
                className="icon-button"
                aria-label="Dismiss error"
                onClick={() => setMutationError("")}
              >
                <X size={16} />
              </button>
            </div>
          )}
          {error && (
            <div role="alert" className="error-banner">
              <AlertCircle size={20} />
              <span>{error.message}</span>
              <Button variant="outline" size="sm" onClick={() => invalidate()}>
                Try again
              </Button>
            </div>
          )}
          {groupsQuery.isPending ? (
            <div className="loading" role="status">
              <LoaderCircle className="spin" />
              Getting your workspace ready…
            </div>
          ) : (
            <>
              {group &&
                location.pathname !== "/groups" &&
                location.pathname !== "/settings" && (
                  <div className="context-bar">
                    <div className="group-select">
                      <Users size={16} />
                      <select
                        aria-label="Active group"
                        value={id}
                        onChange={(e) => {
                          setSelected(e.target.value);
                          if (location.pathname.startsWith("/groups/"))
                            navigate(`/groups/${e.target.value}`);
                        }}
                      >
                        {groups.map((g) => (
                          <option key={g.id} value={g.id}>
                            {g.name}
                          </option>
                        ))}
                      </select>
                      <ChevronDown size={14} />
                    </div>
                    <span className="currency-badge">{currency}</span>
                    <span className="context-separator" />
                    <span className="context-meta">
                      {members.length} people <span>·</span> {expenses.length}{" "}
                      expenses
                    </span>
                    <button
                      className="text-button context-link"
                      onClick={() => navigate(`/groups/${id}`)}
                    >
                      View group <ArrowUpRight size={14} />
                    </button>
                  </div>
                )}
              {groupDataPending ? (
                <div className="loading" role="status">
                  <LoaderCircle className="spin" size={20} />
                  Loading your group…
                </div>
              ) : !group &&
                location.pathname !== "/groups" &&
                location.pathname !== "/settings" ? (
                <div className="card">
                  <Empty
                    title="Bring your people together"
                    description="Create a group for your next trip, your home, or your weekly dinner."
                    action={
                      <Button onClick={() => setModal("group")}>
                        <Plus size={16} />
                        Create your first group
                      </Button>
                    }
                  />
                </div>
              ) : (
                <Routes>
                  <Route
                    path="/"
                    element={
                      <>
                        {stats}
                        <div className="dashboard-grid">
                          <section className="card spending-card">
                            <div className="card-heading">
                              <div>
                                <h2>Spending at a glance</h2>
                                <p>
                                  A little perspective on the bigger picture
                                </p>
                              </div>
                              <span className="soft-pill">
                                <CalendarDays size={13} />
                                All time
                              </span>
                            </div>
                            {chart}
                          </section>
                          <section className="card category-card">
                            <div className="card-heading">
                              <div>
                                <h2>Where it went</h2>
                                <p>Every little moment adds up</p>
                              </div>
                            </div>
                            <CategoryChart
                              analytics={analytics}
                              currency={currency}
                            />
                          </section>
                        </div>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Recent expenses</h2>
                              <p>The latest from {group?.name}</p>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => navigate("/expenses")}
                            >
                              View all <ArrowRight size={15} />
                            </Button>
                          </div>
                          {expenseTable(5)}
                        </section>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Let’s make it even</h2>
                              <p>Fewer payments. Same fair split.</p>
                            </div>
                            <span className="soft-pill green">
                              <Check size={13} />
                              Simplified
                            </span>
                          </div>
                          {suggestions}
                        </section>
                      </>
                    }
                  />
                  <Route
                    path="/groups"
                    element={
                      <>
                        <div className="section-intro">
                          <span>
                            {groups.length} groups, countless good memories
                          </span>
                          <span className="soft-pill">
                            One currency per group
                          </span>
                        </div>
                        <div className="groups-grid">
                          {groups.map((g, i) => {
                            const Icon = groupIcons[i % 3];
                            return (
                              <button
                                key={g.id}
                                className={`group-card group-theme-${i % 3}`}
                                onClick={() => {
                                  setSelected(g.id);
                                  navigate(`/groups/${g.id}`);
                                }}
                              >
                                <div className="group-art">
                                  <span className="art-orbit" />
                                  <Icon size={44} strokeWidth={1.4} />
                                  <span className="group-currency">
                                    {g.currency}
                                  </span>
                                </div>
                                <div className="group-card-content">
                                  <div>
                                    <h2>{g.name}</h2>
                                    <ArrowUpRight size={19} />
                                  </div>
                                  <p>
                                    {g.description ||
                                      "A fresh shared adventure."}
                                  </p>
                                  <small>
                                    Created{" "}
                                    {new Date(g.created_at).toLocaleDateString(
                                      "en-US",
                                      {
                                        month: "short",
                                        day: "numeric",
                                        year: "numeric",
                                      },
                                    )}
                                  </small>
                                </div>
                              </button>
                            );
                          })}
                          <button
                            className="new-group-card"
                            onClick={() => setModal("group")}
                          >
                            <span>
                              <Plus size={26} />
                            </span>
                            <strong>Make room for a new group</strong>
                            <p>A trip, a home, a new adventure.</p>
                          </button>
                        </div>
                      </>
                    }
                  />
                  <Route
                    path="/groups/:groupId"
                    element={
                      <>
                        {stats}
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>The people behind the plans</h2>
                              <p>Members of {group?.name}</p>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setModal("member")}
                            >
                              <Plus size={15} />
                              Add member
                            </Button>
                          </div>
                          <div className="member-grid">
                            {members.map((m, i) => (
                              <div className="member-card" key={m.id}>
                                <Avatar name={m.name} index={i} />
                                <div>
                                  <strong>{m.name}</strong>
                                  <small>Group member</small>
                                </div>
                                <button
                                  className="icon-button danger"
                                  aria-label={`Remove ${m.name}`}
                                  onClick={() => {
                                    if (
                                      confirm(
                                        `Remove ${m.name} from this group? Members with activity cannot be removed.`,
                                      )
                                    )
                                      act(() => service.removeMember(id, m.id));
                                  }}
                                >
                                  <X size={16} />
                                </button>
                              </div>
                            ))}
                            {!members.length && (
                              <Empty
                                title="Good company starts here"
                                description="Add your first member before recording an expense."
                              />
                            )}
                          </div>
                        </section>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Group expenses</h2>
                              <p>A shared history, in one place.</p>
                            </div>
                          </div>
                          {expenseTable()}
                        </section>
                        <section className="card group-settings">
                          <div>
                            <h2>Group settings</h2>
                            <p>
                              Update your group’s name or close this chapter.
                            </p>
                          </div>
                          <div className="heading-actions">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setModal("rename")}
                            >
                              <Pencil size={14} />
                              Edit group
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => {
                                if (
                                  confirm(
                                    `Delete “${group?.name}” and all its expenses, members and settlements? This cannot be undone.`,
                                  )
                                )
                                  act(async () => {
                                    await service.deleteGroup(id);
                                    setSelected("");
                                    navigate("/groups");
                                  });
                              }}
                            >
                              <Trash2 size={14} />
                              Delete group
                            </Button>
                          </div>
                        </section>
                      </>
                    }
                  />
                  <Route
                    path="/expenses"
                    element={
                      <ExpensePage
                        expenses={expenses}
                        render={expenseTable}
                        currency={currency}
                      />
                    }
                  />
                  <Route
                    path="/balances"
                    element={
                      <>
                        {stats}
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>A fair share for everyone</h2>
                              <p>
                                Paid minus share, adjusted for recorded
                                settlements.
                              </p>
                            </div>
                          </div>
                          <div className="table-scroll">
                            <table>
                              <thead>
                                <tr>
                                  <th>Member</th>
                                  <th className="right">Paid</th>
                                  <th className="right">Their share</th>
                                  <th className="right">Net balance</th>
                                </tr>
                              </thead>
                              <tbody>
                                {balances?.members.map((m, i) => (
                                  <tr key={m.member_id}>
                                    <td>
                                      <div className="person">
                                        <Avatar name={m.name} index={i} />
                                        <strong>{m.name}</strong>
                                      </div>
                                    </td>
                                    <td className="right amount">
                                      {money(m.paid_minor, currency)}
                                    </td>
                                    <td className="right amount">
                                      {money(m.owed_minor, currency)}
                                    </td>
                                    <td
                                      className={`right amount ${m.net_minor > 0 ? "positive" : m.net_minor < 0 ? "negative" : ""}`}
                                    >
                                      {m.net_minor > 0 ? "+" : ""}
                                      {money(m.net_minor, currency)}
                                      <small>
                                        {m.net_minor > 0
                                          ? "gets back"
                                          : m.net_minor < 0
                                            ? "owes"
                                            : "settled"}
                                      </small>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </section>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>The simplest way to settle</h2>
                              <p>
                                Record a payment after you have paid your
                                friend.
                              </p>
                            </div>
                          </div>
                          {suggestions}
                        </section>
                      </>
                    }
                  />
                  <Route
                    path="/settlements"
                    element={
                      <>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Make it even</h2>
                              <p>
                                Record a full or partial payment between
                                members.
                              </p>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => newSettlement()}
                              disabled={members.length < 2}
                            >
                              <Plus size={15} />
                              Record payment
                            </Button>
                          </div>
                          {suggestions}
                        </section>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Settlement history</h2>
                              <p>Little payments, lighter minds.</p>
                            </div>
                            <span className="soft-pill">
                              {settlements.length} recorded
                            </span>
                          </div>
                          {settlements.length ? (
                            <div className="table-scroll">
                              <table>
                                <thead>
                                  <tr>
                                    <th>From</th>
                                    <th>To</th>
                                    <th>Date</th>
                                    <th>Note</th>
                                    <th className="right">Amount</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {settlements.map((s) => (
                                    <tr key={s.id}>
                                      <td>{name(s.from_member_id)}</td>
                                      <td>{name(s.to_member_id)}</td>
                                      <td>{s.date}</td>
                                      <td>{s.note || "—"}</td>
                                      <td className="right amount positive">
                                        {money(s.amount_minor, currency)}
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          ) : (
                            <Empty
                              title="A clean slate"
                              description="Recorded settlements will appear here. This app records payments; it does not transfer money."
                            />
                          )}
                        </section>
                      </>
                    }
                  />
                  <Route
                    path="/analytics"
                    element={
                      <>
                        {stats}
                        <div className="dashboard-grid">
                          <section className="card">
                            <div className="card-heading">
                              <div>
                                <h2>Spending over time</h2>
                                <p>Expense totals for each day</p>
                              </div>
                            </div>
                            {chart}
                          </section>
                          <section className="card">
                            <div className="card-heading">
                              <div>
                                <h2>Spending by category</h2>
                                <p>The things you did together</p>
                              </div>
                            </div>
                            <CategoryChart
                              analytics={analytics}
                              currency={currency}
                            />
                          </section>
                        </div>
                        <section className="card">
                          <div className="card-heading">
                            <div>
                              <h2>Everyone’s contribution</h2>
                              <p>How much each member has paid</p>
                            </div>
                          </div>
                          {analytics?.contributions.length ? (
                            <div className="contribution-chart">
                              <ResponsiveContainer width="100%" height={240}>
                                <BarChart data={analytics.contributions}>
                                  <XAxis
                                    dataKey="name"
                                    axisLine={false}
                                    tickLine={false}
                                  />
                                  <YAxis
                                    tickFormatter={(v) => `${v / 100}`}
                                    axisLine={false}
                                    tickLine={false}
                                  />
                                  <Tooltip
                                    formatter={(v) =>
                                      money(Number(v), currency)
                                    }
                                  />
                                  <Bar
                                    dataKey="amount_minor"
                                    name="Paid"
                                    fill="#268b70"
                                    radius={[6, 6, 0, 0]}
                                    maxBarSize={65}
                                  />
                                </BarChart>
                              </ResponsiveContainer>
                            </div>
                          ) : (
                            <Empty
                              title="Contributions will appear here"
                              description="Add members and expenses to see the picture."
                            />
                          )}
                        </section>
                      </>
                    }
                  />
                  <Route
                    path="/settings"
                    element={
                      <SettingsPage
                        onNotice={setNotice}
                        onSaved={setDisplayName}
                      />
                    }
                  />
                  <Route
                    path="*"
                    element={
                      <Empty
                        title="This page took a wrong turn"
                        description="Your workspace is one click away."
                        action={
                          <Button onClick={() => navigate("/")}>
                            Back to overview
                          </Button>
                        }
                      />
                    }
                  />
                </Routes>
              )}
            </>
          )}
          <footer className="footer">
            <span>
              <Leaf size={13} />A little clarity goes a long way.
            </span>
            <span>
              SplitWise Pro <span>·</span> Made for sharing
            </span>
          </footer>
        </main>
      </div>
      <Dialog
        open={modal === "group" || modal === "rename"}
        onOpenChange={(open) => !open && setModal(null)}
        title={
          modal === "rename"
            ? "A new name, same good company"
            : "Make room for your people"
        }
        description={
          modal === "rename"
            ? "Keep your group details up to date."
            : "Create a group for a trip, a home, or something worth sharing."
        }
      >
        {mutationError && (
          <div role="alert" className="form-error">
            {mutationError}
          </div>
        )}
        <GroupForm
          group={modal === "rename" ? group : undefined}
          pending={mutate.isPending}
          onSubmit={(data) =>
            act(() =>
              modal === "rename"
                ? service.updateGroup(id, data)
                : service.createGroup(data),
            )
          }
        />
      </Dialog>
      <Dialog
        open={modal === "member"}
        onOpenChange={(open) => !open && setModal(null)}
        title="Pull up a chair"
        description="Add someone to your shared group."
      >
        {mutationError && (
          <div role="alert" className="form-error">
            {mutationError}
          </div>
        )}
        <MemberForm
          pending={mutate.isPending}
          onSubmit={(name) => act(() => service.addMember(id, name))}
        />
      </Dialog>
      <Dialog
        open={modal === "expense"}
        onOpenChange={(open) => !open && setModal(null)}
        title={editing ? "Edit the details" : "A new shared moment"}
        description={`Record an expense in ${group?.name || "your group"}.`}
      >
        {mutationError && (
          <div role="alert" className="form-error">
            {mutationError}
          </div>
        )}
        <ExpenseForm
          key={editing?.id || `new-${id}-${modal}`}
          members={members}
          currency={currency}
          expense={editing}
          pending={mutate.isPending}
          onSubmit={(data) =>
            act(() =>
              editing
                ? service.updateExpense(id, editing.id, data)
                : service.createExpense(id, data),
            )
          }
        />
      </Dialog>
      <Dialog
        open={modal === "settlement"}
        onOpenChange={(open) => !open && setModal(null)}
        title="A little closer to even"
        description="Record a payment you have already made. No money is transferred."
      >
        {mutationError && (
          <div role="alert" className="form-error">
            {mutationError}
          </div>
        )}
        <SettlementForm
          key={JSON.stringify(settlementDefaults) + modal}
          members={members}
          currency={currency}
          defaults={settlementDefaults}
          pending={mutate.isPending}
          onSubmit={(data) => act(() => service.createSettlement(id, data))}
        />
      </Dialog>
    </div>
  );
}
function CategoryChart({
  analytics,
  currency,
}: {
  analytics?: import("./services/types").Analytics;
  currency: string;
}) {
  return analytics?.by_category.length ? (
    <div className="category-chart">
      <div className="donut">
        <ResponsiveContainer width="100%" height={170}>
          <PieChart>
            <Pie
              data={analytics.by_category}
              dataKey="amount_minor"
              nameKey="category"
              innerRadius={54}
              outerRadius={73}
              paddingAngle={4}
              stroke="none"
            >
              {analytics.by_category.map((c, i) => (
                <Cell
                  key={c.category}
                  fill={categoryColors[i % categoryColors.length]}
                />
              ))}
            </Pie>
            <Tooltip formatter={(v) => money(Number(v), currency)} />
          </PieChart>
        </ResponsiveContainer>
        <div className="donut-center">
          <small>TOTAL SPENT</small>
          <strong>{money(analytics.total_minor, currency)}</strong>
        </div>
      </div>
      <div className="category-legend">
        {analytics.by_category.map((c, i) => (
          <div key={c.category}>
            <span
              style={{ background: categoryColors[i % categoryColors.length] }}
            />
            <span>{c.category}</span>
            <strong>
              {Math.round((c.amount_minor / analytics.total_minor) * 100)}%
            </strong>
          </div>
        ))}
      </div>
    </div>
  ) : (
    <Empty
      title="Make some memories"
      description="Your expense categories will appear here."
    />
  );
}
function GroupForm({
  group,
  pending,
  onSubmit,
}: {
  group?: Group;
  pending: boolean;
  onSubmit: (data: Pick<Group, "name" | "currency" | "description">) => void;
}) {
  const [name, setName] = useState(group?.name || ""),
    [description, setDescription] = useState(group?.description || ""),
    [currency, setCurrency] = useState(group?.currency || "USD");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({
          name: name.trim(),
          description: description.trim(),
          currency,
        });
      }}
    >
      <Field label="Group name">
        <input
          autoFocus
          required
          maxLength={100}
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="e.g. Summer in Lisbon"
        />
      </Field>
      <Field label="A little description">
        <input
          maxLength={500}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="What are you sharing?"
        />
      </Field>
      <Field
        label="Group currency"
        hint="Each group uses one currency, so the numbers always add up."
      >
        <select
          disabled={!!group}
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
        >
          <option value="USD">USD · US Dollar</option>
          <option value="KZT">KZT · Kazakhstan Tenge</option>
          <option value="EUR">EUR · Euro</option>
          <option value="GBP">GBP · British Pound</option>
        </select>
      </Field>
      <div className="form-footer">
        <Button disabled={pending || !name.trim()} type="submit">
          {pending ? (
            <LoaderCircle className="spin" size={16} />
          ) : (
            <Check size={16} />
          )}{" "}
          {group ? "Save changes" : "Create group"}
        </Button>
      </div>
    </form>
  );
}
function MemberForm({
  pending,
  onSubmit,
}: {
  pending: boolean;
  onSubmit: (name: string) => void;
}) {
  const [name, setName] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(name.trim());
      }}
    >
      <Field label="Member name">
        <input
          autoFocus
          required
          maxLength={100}
          placeholder="e.g. Aigerim"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </Field>
      <div className="form-footer">
        <Button type="submit" disabled={pending || !name.trim()}>
          <Plus size={16} />
          Add member
        </Button>
      </div>
    </form>
  );
}
function ExpenseForm({
  members,
  currency,
  expense,
  pending,
  onSubmit,
}: {
  members: Member[];
  currency: string;
  expense?: Expense;
  pending: boolean;
  onSubmit: (data: ExpenseInput) => void;
}) {
  const [description, setDescription] = useState(expense?.description || ""),
    [amount, setAmount] = useState(
      expense ? String(expense.amount_minor / 100) : "",
    ),
    [payer, setPayer] = useState(expense?.payer_id || members[0]?.id || ""),
    [category, setCategory] = useState(expense?.category || categories[0]),
    [date, setDate] = useState(expense?.date || today()),
    [split, setSplit] = useState<SplitType>(expense?.split_type || "equal"),
    [selected, setSelected] = useState<string[]>(
      expense ? Object.keys(expense.split_values) : members.map((m) => m.id),
    ),
    [values, setValues] = useState<Record<string, string>>(
      expense
        ? Object.fromEntries(
            Object.entries(expense.split_values).map(([k, v]) => [
              k,
              String(v / 100),
            ]),
          )
        : {},
    ),
    [error, setError] = useState("");
  const amountMinor = Math.round(Number(amount) * 100);
  const total = selected.reduce(
    (sum, id) => sum + Math.round(Number(values[id] || 0) * 100),
    0,
  );
  const target = split === "percentage" ? 10000 : amountMinor;
  const submit = (e: FormEvent) => {
    e.preventDefault();
    setError("");
    if (
      !Number.isFinite(Number(amount)) ||
      !/^\d+(\.\d{1,2})?$/.test(amount) ||
      amountMinor <= 0 ||
      !Number.isSafeInteger(amountMinor) ||
      amountMinor > 1e12
    ) {
      setError(
        "Enter a positive amount with at most two decimal places, up to 10 billion.",
      );
      return;
    }
    if (!selected.length) {
      setError("Select at least one participant.");
      return;
    }
    if (
      split !== "equal" &&
      selected.some((id) => !/^\d+(\.\d{1,2})?$/.test(values[id] || ""))
    ) {
      setError(
        "Enter a non-negative value with at most two decimal places for each participant.",
      );
      return;
    }
    if (split !== "equal" && total !== target) {
      setError(
        split === "exact"
          ? "Exact shares must equal the expense total."
          : "Percentages must add up to 100%.",
      );
      return;
    }
    onSubmit({
      description: description.trim(),
      amount_minor: amountMinor,
      payer_id: payer,
      category,
      date,
      split_type: split,
      split_values: Object.fromEntries(
        selected.map((id) => [
          id,
          split === "equal" ? 1 : Math.round(Number(values[id]) * 100),
        ]),
      ),
    });
  };
  return (
    <form onSubmit={submit}>
      {error && (
        <div role="alert" className="form-error">
          {error}
        </div>
      )}
      <Field label="What was it for?">
        <input
          autoFocus
          required
          maxLength={200}
          placeholder="e.g. Dinner with a view"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </Field>
      <div className="form-grid">
        <Field label={`Amount (${currency})`}>
          <input
            required
            inputMode="decimal"
            placeholder="0.00"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </Field>
        <Field label="Paid by">
          <select
            required
            value={payer}
            onChange={(e) => setPayer(e.target.value)}
          >
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Category">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {categories.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
        </Field>
        <Field label="Date">
          <input
            required
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </Field>
      </div>
      <div className="split-heading">
        <strong>How should we split it?</strong>
        <small>Fair, down to the last cent.</small>
      </div>
      <div className="segmented" role="group" aria-label="Split method">
        {(["equal", "exact", "percentage"] as SplitType[]).map((type) => (
          <button
            type="button"
            key={type}
            aria-pressed={split === type}
            className={split === type ? "selected" : ""}
            onClick={() => {
              setSplit(type);
              setError("");
            }}
          >
            {type === "equal"
              ? "Equally"
              : type === "exact"
                ? "Exact amounts"
                : "Percentages"}
          </button>
        ))}
      </div>
      <div className="split-members">
        {members.map((m, i) => (
          <div key={m.id} className="split-person">
            <label>
              <input
                type="checkbox"
                checked={selected.includes(m.id)}
                onChange={(e) =>
                  setSelected(
                    e.target.checked
                      ? [...selected, m.id]
                      : selected.filter((id) => id !== m.id),
                  )
                }
              />
              <Avatar name={m.name} index={i} size="small" />
              <span>{m.name}</span>
            </label>
            {selected.includes(m.id) &&
              (split === "equal" ? (
                <span className="muted">
                  {money(
                    Number.isFinite(amountMinor)
                      ? Math.floor(amountMinor / Math.max(selected.length, 1))
                      : 0,
                    currency,
                  )}
                  <small>approx.</small>
                </span>
              ) : (
                <div className="split-value">
                  <input
                    aria-label={`${m.name} ${split === "exact" ? "share" : "percentage"}`}
                    inputMode="decimal"
                    placeholder="0"
                    value={values[m.id] || ""}
                    onChange={(e) =>
                      setValues({ ...values, [m.id]: e.target.value })
                    }
                  />
                  <span>{split === "percentage" ? "%" : currency}</span>
                </div>
              ))}
          </div>
        ))}
      </div>
      {split !== "equal" && (
        <div
          className={`split-total ${total === target ? "positive" : "negative"}`}
        >
          <span>Allocated</span>
          <strong>
            {split === "percentage"
              ? `${total / 100}% / 100%`
              : `${money(total, currency)} / ${money(Number.isFinite(amountMinor) ? amountMinor : 0, currency)}`}
          </strong>
        </div>
      )}
      <p className="form-note">
        Any remaining cents go to the largest fractional shares, with ties
        settled by member ID.
      </p>
      <div className="form-footer">
        <Button
          type="submit"
          disabled={pending || !description.trim() || !members.length}
        >
          {pending ? (
            <LoaderCircle className="spin" size={16} />
          ) : (
            <Check size={16} />
          )}{" "}
          {expense ? "Save changes" : "Add expense"}
        </Button>
      </div>
    </form>
  );
}
function SettlementForm({
  members,
  currency,
  defaults,
  pending,
  onSubmit,
}: {
  members: Member[];
  currency: string;
  defaults: Partial<SettlementInput>;
  pending: boolean;
  onSubmit: (data: SettlementInput) => void;
}) {
  const [from, setFrom] = useState(
      defaults.from_member_id || members[0]?.id || "",
    ),
    [to, setTo] = useState(defaults.to_member_id || members[1]?.id || ""),
    [amount, setAmount] = useState(
      defaults.amount_minor ? String(defaults.amount_minor / 100) : "",
    ),
    [date, setDate] = useState(today()),
    [note, setNote] = useState(""),
    [error, setError] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (from === to) {
          setError("Choose two different members.");
          return;
        }
        if (
          !/^\d+(\.\d{1,2})?$/.test(amount) ||
          Number(amount) <= 0 ||
          !Number.isSafeInteger(Math.round(Number(amount) * 100)) ||
          Math.round(Number(amount) * 100) > 1e12
        ) {
          setError(
            "Enter a positive amount with at most two decimals, up to 10 billion.",
          );
          return;
        }
        onSubmit({
          from_member_id: from,
          to_member_id: to,
          amount_minor: Math.round(Number(amount) * 100),
          date,
          note: note.trim(),
        });
      }}
    >
      {error && (
        <div role="alert" className="form-error">
          {error}
        </div>
      )}
      <div className="form-grid">
        <Field label="Who paid?">
          <select value={from} onChange={(e) => setFrom(e.target.value)}>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Who received?">
          <select value={to} onChange={(e) => setTo(e.target.value)}>
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </Field>
        <Field label={`Payment amount (${currency})`}>
          <input
            required
            inputMode="decimal"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="0.00"
          />
        </Field>
        <Field label="Payment date">
          <input
            required
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </Field>
      </div>
      <Field label="Note (optional)">
        <input
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="e.g. Bank transfer"
          maxLength={500}
        />
      </Field>
      <p className="form-note">
        Partial payments are welcome. The amount must fit the payer’s debt and
        recipient’s credit.
      </p>
      <div className="form-footer">
        <Button type="submit" disabled={pending || members.length < 2}>
          <Check size={16} />
          Record payment
        </Button>
      </div>
    </form>
  );
}
function ExpensePage({
  expenses,
  render,
  currency,
}: {
  expenses: Expense[];
  render: () => ReactNode;
  currency: string;
}) {
  return (
    <section className="card">
      <div className="card-heading">
        <div>
          <h2>All the shared moments</h2>
          <p>
            {expenses.length} expenses <span>·</span>{" "}
            {money(
              expenses.reduce((s, e) => s + e.amount_minor, 0),
              currency,
            )}{" "}
            in total
          </p>
        </div>
        <span className="soft-pill">
          <SlidersHorizontal size={13} />
          Newest first
        </span>
      </div>
      {render()}
    </section>
  );
}
function SettingsPage({
  onNotice,
  onSaved,
}: {
  onNotice: (message: string) => void;
  onSaved: (name: string) => void;
}) {
  const [name, setName] = useState(
    () => localStorage.getItem("splitwise-display-name") || "Kairat Usmanov",
  );
  return (
    <section className="card settings-card">
      <div className="card-heading">
        <div>
          <h2>A workspace that feels like you</h2>
          <p>Preferences stay in this browser.</p>
        </div>
      </div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (!name.trim()) return;
          localStorage.setItem("splitwise-display-name", name.trim());
          setName(name.trim());
          onSaved(name.trim());
          onNotice("Your local preferences have been saved.");
        }}
      >
        <Field label="Display name">
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            maxLength={100}
          />
        </Field>
        <Button type="submit" disabled={!name.trim()}>
          Save preferences
        </Button>
      </form>
      <div className="settings-info">
        <Leaf size={22} />
        <div>
          <strong>Simple by design</strong>
          <p>
            A single shared workspace. No accounts, no bank connections, no
            money transfers. Currency is set for each group.
          </p>
        </div>
      </div>
    </section>
  );
}
export default App;
