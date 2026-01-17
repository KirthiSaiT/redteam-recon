"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Loader2, ArrowRight, Calendar, ExternalLink } from "lucide-react";

interface ScanResult {
    id: string;
    domain: string;
    status: string;
    timestamp: string;
    subdomains: any;
    ports: any;
    technologies: any;
}

export default function HistoryPage() {
    const [scans, setScans] = useState<ScanResult[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/scans");
                if (res.ok) {
                    const data = await res.json();
                    setScans(data);
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, []);

    if (loading) return (
        <div className="flex flex-col items-center justify-center h-[50vh]">
            <Loader2 className="w-10 h-10 animate-spin text-primary mb-4" />
            <h2 className="text-xl font-medium">Loading Scan History...</h2>
        </div>
    );

    return (
        <div className="space-y-8 py-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Scan History</h1>
                    <p className="text-muted-foreground mt-2">
                        View past reconnaissance reports and their status.
                    </p>
                </div>
                <Link href="/">
                    <Button>+ New Scan</Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Scans</CardTitle>
                    <CardDescription>A list of all requested domain scans.</CardDescription>
                </CardHeader>
                <CardContent>
                    {scans.length === 0 ? (
                        <div className="text-center py-10 text-muted-foreground">
                            No scans found. Start your first scan from the dashboard!
                        </div>
                    ) : (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Target Domain</TableHead>
                                    <TableHead>Date</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Result Overview</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {scans.map((scan) => (
                                    <TableRow key={scan.id}>
                                        <TableCell className="font-medium">{scan.domain}</TableCell>
                                        <TableCell className="text-muted-foreground">
                                            <div className="flex items-center text-xs">
                                                <Calendar className="mr-2 h-3 w-3" />
                                                {new Date(scan.timestamp).toLocaleString()}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={scan.status === "completed" ? "default" : (scan.status === "failed" ? "destructive" : "secondary")} className="capitalize">
                                                {scan.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex space-x-2 text-xs text-muted-foreground">
                                                {scan.subdomains?.count > 0 && <span>{scan.subdomains.count} Subs</span>}
                                                {scan.ports?.length > 0 && <span>• {scan.ports[0].ports.length} Ports</span>}
                                                {scan.technologies?.length > 0 && <span>• {scan.technologies.length} Techs</span>}
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Link href={`/scan/${scan.id}`}>
                                                <Button variant="ghost" size="sm">
                                                    View Report <ArrowRight className="ml-2 h-4 w-4" />
                                                </Button>
                                            </Link>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
