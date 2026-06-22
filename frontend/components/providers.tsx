"use client";

import { ThemeProvider } from "next-themes";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <div className="min-h-screen">
        <Navbar />
        <div className="mx-auto flex max-w-7xl">
          <Sidebar />
          <main className="flex-1 px-4 py-8">{children}</main>
        </div>
      </div>
    </ThemeProvider>
  );
}
