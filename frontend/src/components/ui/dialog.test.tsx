import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Dialog } from "./dialog";

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function Example({ removeOpener = false }: { removeOpener?: boolean }) {
  const [open, setOpen] = useState(false);
  const [saved, setSaved] = useState(false);
  return (
    <main>
      {(!removeOpener || !saved) && (
        <button onClick={() => setOpen(true)}>Open details</button>
      )}
      <button>Continue working</button>
      <Dialog open={open} onOpenChange={setOpen} title="Details">
        <label>
          Name
          <input autoFocus />
        </label>
        <button
          onClick={() => {
            setSaved(true);
            setOpen(false);
          }}
        >
          Save
        </button>
      </Dialog>
    </main>
  );
}

describe("dialog keyboard focus regression #40", () => {
  it("returns focus to the surviving opener after Escape, close, and save", async () => {
    const user = userEvent.setup();
    render(<Example />);
    const opener = screen.getByRole("button", { name: "Open details" });
    // jsdom has no layout; provide a nonempty rectangle for the visible trigger.
    vi.spyOn(opener, "getClientRects").mockReturnValue([
      {},
    ] as unknown as DOMRectList);
    for (const close of ["Escape", "Close dialog", "Save"]) {
      await user.click(opener);
      expect(await screen.findByLabelText("Name")).toHaveFocus();
      if (close === "Escape") await user.keyboard("{Escape}");
      else await user.click(screen.getByRole("button", { name: close }));
      await waitFor(() => expect(opener).toHaveFocus());
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    }
  });

  it("focuses a surviving workspace action if the opener disappears on save", async () => {
    const user = userEvent.setup();
    render(<Example removeOpener />);
    vi.spyOn(
      screen.getByRole("button", { name: "Continue working" }),
      "getClientRects",
    ).mockReturnValue([{}] as unknown as DOMRectList);
    await user.click(screen.getByRole("button", { name: "Open details" }));
    await user.click(await screen.findByRole("button", { name: "Save" }));
    await waitFor(() =>
      expect(
        screen.getByRole("button", { name: "Continue working" }),
      ).toHaveFocus(),
    );
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});
