"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const items = [
  { href: "/profile", label: "Student Profile" },
  { href: "/results", label: "Recommendations" },
  { href: "/universities", label: "Browse Universities" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 shrink-0 border-r bg-card/40 p-4 lg:block">
      <p className="mb-4 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        Dashboard
      </p>
      <div className="space-y-1">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "block rounded-md px-3 py-2 text-sm hover:bg-accent",
              pathname.startsWith(item.href) && "bg-accent font-medium",
            )}
          >
            {item.label}
          </Link>
        ))}
      </div>
    </aside>
  );
}
