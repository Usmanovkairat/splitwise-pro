import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
export const money = (amount: number, currency = "USD") =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(amount / 100);
export const today = () => new Date().toISOString().slice(0, 10);
export const initials = (name: string) =>
  name
    .split(" ")
    .map((x) => x[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
export const categories = [
  "Food & drinks",
  "Travel",
  "Accommodation",
  "Shopping",
  "Entertainment",
  "Utilities",
  "Other",
];
export const categoryColors = [
  "#168769",
  "#e5ab60",
  "#718db0",
  "#b59cc7",
  "#d7846b",
  "#7aa9a2",
  "#a8afa2",
];
