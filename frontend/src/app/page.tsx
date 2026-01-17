import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import { ScanForm } from "@/components/ScanForm";

export default function Home() {
  return (
    <div className="space-y-12 py-10">
      {/* Hero / Quick Scan Section */}
      <section className="flex flex-col items-center space-y-6 text-center pt-8">
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl md:text-7xl">
          <span className="bg-gradient-to-r from-primary to-blue-500 bg-clip-text text-transparent">
            Red Team
          </span>{" "}
          Recon
        </h1>
        <p className="max-w-[700px] text-muted-foreground md:text-xl">
          Automated intelligence gathering for security professionals. <br className="hidden sm:inline" />
          Discover subdomains, open ports, and tech stacks in seconds.
        </p>

        <ScanForm />
      </section>

      {/* Stats / Status Section */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card className="bg-card/50 backdrop-blur-sm border-muted transition-colors hover:border-primary/50 hover:bg-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Total Scans</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">+0% from last month</p>
          </CardContent>
        </Card>
        <Card className="bg-card/50 backdrop-blur-sm border-muted transition-colors hover:border-primary/50 hover:bg-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Targets Found</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">0</div>
            <p className="text-xs text-muted-foreground mt-1">Unique subdomains</p>
          </CardContent>
        </Card>
        <Card className="bg-card/50 backdrop-blur-sm border-muted transition-colors hover:border-primary/50 hover:bg-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">System Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
              </span>
              <span className="text-lg font-bold">Operational</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">Backend connected</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
