import { afterEach, describe, it, expect } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
afterEach(cleanup);
function mount(path = "/groups") {
  return render(
    <QueryClientProvider
      client={
        new QueryClient({ defaultOptions: { queries: { retry: false } } })
      }
    >
      <MemoryRouter initialEntries={[path]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}
describe("workspace forms", () => {
  it("renders groups and creates a named group through mock service", async () => {
    const user = userEvent.setup();
    mount();
    await screen.findByRole("heading", { name: "Lisbon getaway" });
    await user.click(screen.getByRole("button", { name: "New group" }));
    await user.type(screen.getByLabelText("Group name"), "Test explorers");
    await user.click(screen.getByRole("button", { name: "Create group" }));
    expect(
      await screen.findByRole("heading", { name: "Test explorers" }),
    ).toBeInTheDocument();
  });
  it("validates exact expense allocations before submitting", async () => {
    const user = userEvent.setup();
    mount("/expenses");
    await screen.findByText("Apartment in Alfama");
    await user.click(screen.getByRole("button", { name: "Add expense" }));
    await user.type(
      screen.getByLabelText("What was it for?"),
      "Unbalanced lunch",
    );
    await user.type(screen.getByLabelText("Amount (USD)"), "10");
    await user.click(screen.getByRole("button", { name: "Exact amounts" }));
    for (const person of ["Kairat", "Aigerim", "Timur", "Dana"])
      await user.type(screen.getByLabelText(`${person} share`), "1");
    await user.click(
      screen.getAllByRole("button", { name: "Add expense" }).at(-1)!,
    );
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Exact shares must equal the expense total.",
    );
    expect(screen.getByRole("dialog")).toBeInTheDocument();
  });
});
describe("regressions #35 and #36", () => {
  it("shows service rejection inside the active dialog and preserves the input", async () => {
    const user = userEvent.setup();
    mount("/groups/g1");
    await screen.findByText("The people behind the plans");
    await user.click(screen.getByRole("button", { name: "Add member" }));
    await user.type(screen.getByLabelText("Member name"), "Kairat");
    await user.click(
      screen.getByRole("dialog").querySelector("button[type=submit]")!,
    );
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "already exists",
    );
    expect(screen.getByLabelText("Member name")).toHaveValue("Kairat");
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    await user.clear(screen.getByLabelText("Member name"));
    await user.type(screen.getByLabelText("Member name"), "New friend");
    await user.click(
      screen.getByRole("dialog").querySelector("button[type=submit]")!,
    );
    expect(await screen.findByText("New friend")).toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
  it("updates the profile immediately and restores the saved display name", async () => {
    const user = userEvent.setup();
    const view = mount("/settings");
    const input = await screen.findByLabelText("Display name");
    await user.clear(input);
    await user.type(input, "  Jane Smith  ");
    await user.click(screen.getByRole("button", { name: "Save preferences" }));
    expect(screen.getByText("Jane Smith")).toBeInTheDocument();
    expect(localStorage.getItem("splitwise-display-name")).toBe("Jane Smith");
    await user.clear(input);
    await user.type(input, "   ");
    expect(
      screen.getByRole("button", { name: "Save preferences" }),
    ).toBeDisabled();
    expect(screen.getByText("Jane Smith")).toBeInTheDocument();
    view.unmount();
    mount("/settings");
    expect(await screen.findByLabelText("Display name")).toHaveValue("Jane Smith");
    expect(screen.getByText("Jane Smith")).toBeInTheDocument();
    localStorage.removeItem("splitwise-display-name");
  });
});
