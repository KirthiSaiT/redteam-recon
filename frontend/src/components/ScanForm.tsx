"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Loader2 } from "lucide-react";

export function ScanForm() {
    const [domain, setDomain] = useState("");
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleScan = async () => {
        if (!domain) return;
        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/api/scan", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ domain, scan_types: ["all"] }),
            });

            if (!res.ok) {
                throw new Error("Failed to start scan");
            }

            const data = await res.json();
            // Redirect to results page (or just show status, for now lets log it)
            console.log("Scan started:", data);

            // For MVP, we'll navigate to a details page (we need to build it)
            // Or just alert for now since the page doesn't exist yet
            router.push(`/scan/${data.id}`);

        } catch (error) {
            console.error(error);
            alert("Error starting scan. Make sure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex w-full max-w-lg items-center space-x-2 pt-6">
            <Input
                type="text"
                placeholder="Enter target domain (e.g. google.com)"
                className="h-12 text-lg shadow-sm"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleScan()}
            />
            <Button
                size="lg"
                className="h-12 px-8 font-semibold shadow-md transition-all hover:scale-105"
                onClick={handleScan}
                disabled={loading}
            >
                {loading ? <Loader2 className="mr-2 h-5 w-5 animate-spin" /> : <Search className="mr-2 h-5 w-5" />}
                {loading ? "Scanning..." : "Start Scan"}
            </Button>
        </div>
    );
}
