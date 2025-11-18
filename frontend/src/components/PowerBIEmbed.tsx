import { useEffect, useRef, useState } from "react";
import * as powerbi from "powerbi-client";
import { models } from "powerbi-client";
import type { IEmbedConfiguration } from "powerbi-client";

interface EmbedConfigResponse {
    reportId: string;
    embedUrl: string;
    embedToken: string;
}

const PowerBIEmbed: React.FC = () => {
    const reportRef = useRef<HTMLDivElement | null>(null);
    const [loaded, setLoaded] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function load(): Promise<void> {
            try {
                // 1. Fetch embed information from backend
                const res = await fetch("http://localhost:3001/api/get-embed-config");
                
                if (!res.ok) {
                    throw new Error(`Failed to fetch embed config: ${res.statusText}`);
                }

                const config: EmbedConfigResponse = await res.json();

                if (!config.reportId || !config.embedUrl || !config.embedToken) {
                    throw new Error("Invalid embed configuration received");
                }

                // 2. Prepare configuration for powerbi-client
                const embedConfig: IEmbedConfiguration = {
                    type: "report",
                    id: config.reportId,
                    embedUrl: config.embedUrl,
                    accessToken: config.embedToken,
                    tokenType: models.TokenType.Embed,
                    permissions: models.Permissions.All,
                    settings: {
                        panes: {
                            filters: { visible: true },
                            pageNavigation: { visible: true }
                        }
                    }
                };

                // 3. Embed the report
                if (!reportRef.current) {
                    throw new Error("Report container element not found");
                }

                const service = new powerbi.service.Service(
                    powerbi.factories.hpmFactory,
                    powerbi.factories.wpmpFactory,
                    powerbi.factories.routerFactory
                );

                service.embed(reportRef.current, embedConfig);

                setLoaded(true);
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : "An unknown error occurred";
                setError(errorMessage);
                console.error("Error loading Power BI report:", err);
            }
        }

        load();
    }, []);

    return (
        <div style={{ padding: 20 }}>
            <h2>Power BI Embedded Report</h2>

            {error && (
                <div style={{ color: "red", marginBottom: 10 }}>
                    <p>Error: {error}</p>
                </div>
            )}

            {!loaded && !error && <p>Loading report...</p>}

            <div
                ref={reportRef}
                style={{
                    width: "100%",
                    height: "85vh",
                    border: "1px solid #ccc"
                }}
            />
        </div>
    );
};

export default PowerBIEmbed;
